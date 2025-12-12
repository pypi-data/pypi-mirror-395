"""Spatial cluster analysis for simultaneous destruction events."""

import json
from typing import Optional
import duckdb

from .pipeline import Enricher


class SpatialClusterEnricher(Enricher):
    """
    Analyzes objects destroyed simultaneously to detect:
    - Splash damage (multiple targets from one weapon)
    - Weapon intercepts (weapon-on-weapon)
    - Mid-air collisions (multiple aircraft)
    - Cluster munition debris
    
    Runs AFTER weapon enrichment to leverage parent_id tracking.
    """
    
    def __init__(
        self,
        proximity_radius: float = 50.0,
        collision_speed_threshold: float = 50.0,
        exclude_projectiles: bool = True,
        time_window: float = 0.5
    ):
        """
        Initialize spatial cluster enricher.
        
        Args:
            proximity_radius: 3D distance threshold for clustering (default: 50m)
            collision_speed_threshold: Speed threshold to classify as collision (default: 50 m/s)
            exclude_projectiles: Skip untracked projectiles (default: True)
            time_window: Time window for matching removals (default: 0.5s, allows ±0.5s)
        """
        self.proximity_radius = proximity_radius
        self.collision_speed_threshold = collision_speed_threshold
        self.exclude_projectiles = exclude_projectiles
        self.time_window = time_window
    
    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run spatial cluster analysis on simultaneous destructions.
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of cluster events detected
        """
        # Ensure spatial extension is loaded
        conn.execute("INSTALL spatial")
        conn.execute("LOAD spatial")
        
        return self._analyze_clusters(conn)
    
    def _analyze_clusters(self, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Detect and classify spatial clusters of simultaneous destructions.
        
        Returns:
            Number of cluster events detected
        """
        projectile_filter = "AND o.type_basic != 'Projectile'" if self.exclude_projectiles else ""
        projectile_filter2 = "AND o2.type_basic != 'Projectile'" if self.exclude_projectiles else ""
        
        cluster_query = f"""
        -- Step 1: Find cluster candidates by time window
        WITH cluster_candidates AS (
            SELECT 
                o.id,
                o.name,
                o.type_class,
                o.type_basic,
                o.pilot,
                o.coalition,
                o.removed_at,
                o.parent_id
            FROM objects o
            WHERE o.removed_at IS NOT NULL
              AND o.type_class IN ('Air', 'Sea', 'Ground', 'Weapon')
              {projectile_filter}
              -- Skip objects already clustered (for re-run efficiency)
              AND json_extract_string(o.properties, '$.ClusterEvent') IS NULL
              -- Only consider objects destroyed near-simultaneously with others (within time window)
              AND EXISTS (
                SELECT 1
                FROM objects o2
                WHERE ABS(o2.removed_at - o.removed_at) <= ?
                  AND o2.id != o.id
                  AND o2.type_class IN ('Air', 'Sea', 'Ground', 'Weapon')
                  {projectile_filter2}
              )
        ),
        
        -- Step 2: Get last state positions for all candidates
        candidates_with_positions AS (
            SELECT 
                c.id,
                c.name,
                c.type_class,
                c.type_basic,
                c.pilot,
                c.coalition,
                c.removed_at,
                c.parent_id,
                s.longitude,
                s.latitude,
                s.altitude,
                s.speed as last_speed
            FROM cluster_candidates c
            LEFT JOIN LATERAL (
                SELECT longitude, latitude, altitude, speed
                FROM states
                WHERE object_id = c.id
                  AND timestamp <= c.removed_at
                  AND longitude IS NOT NULL
                  AND latitude IS NOT NULL
                ORDER BY timestamp DESC
                LIMIT 1
            ) s ON true
            WHERE s.longitude IS NOT NULL
              AND s.latitude IS NOT NULL
        ),
        
        -- Step 3: Spatial clustering within {self.proximity_radius}m
        spatial_pairs AS (
            SELECT 
                d1.removed_at,
                d1.id as obj1_id,
                d1.name as obj1_name,
                d1.type_class as obj1_type_class,
                d1.type_basic as obj1_type_basic,
                d1.pilot as obj1_pilot,
                d1.coalition as obj1_coalition,
                d1.parent_id as obj1_parent_id,
                d1.longitude as obj1_lon,
                d1.latitude as obj1_lat,
                d1.altitude as obj1_alt,
                d1.last_speed as obj1_speed,
                d2.id as obj2_id,
                d2.name as obj2_name,
                d2.type_class as obj2_type_class,
                d2.type_basic as obj2_type_basic,
                d2.pilot as obj2_pilot,
                d2.coalition as obj2_coalition,
                d2.parent_id as obj2_parent_id,
                d2.longitude as obj2_lon,
                d2.latitude as obj2_lat,
                d2.altitude as obj2_alt,
                d2.last_speed as obj2_speed,
                SQRT(
                    POWER(ST_Distance_Sphere(
                        ST_Point(d1.longitude, d1.latitude),
                        ST_Point(d2.longitude, d2.latitude)
                    ), 2) +
                    POWER(d1.altitude - d2.altitude, 2)
                ) as distance_3d
            FROM candidates_with_positions d1
            JOIN candidates_with_positions d2 
                ON ABS(d1.removed_at - d2.removed_at) <= ?
                AND d1.id < d2.id
            WHERE SQRT(
                POWER(ST_Distance_Sphere(
                    ST_Point(d1.longitude, d1.latitude),
                    ST_Point(d2.longitude, d2.latitude)
                ), 2) +
                POWER(d1.altitude - d2.altitude, 2)
            ) <= ?
        ),
        
        -- Step 4: Flatten pairs into all cluster members
        cluster_members AS (
            SELECT removed_at, obj1_id as object_id, obj1_name as name, 
                   obj1_type_class as type_class, obj1_type_basic as type_basic,
                   obj1_pilot as pilot, obj1_coalition as coalition,
                   obj1_parent_id as parent_id, obj1_lon as lon, obj1_lat as lat, 
                   obj1_alt as alt, obj1_speed as speed
            FROM spatial_pairs
            UNION ALL
            SELECT removed_at, obj2_id, obj2_name, obj2_type_class, obj2_type_basic,
                   obj2_pilot, obj2_coalition, obj2_parent_id, obj2_lon, obj2_lat, 
                   obj2_alt, obj2_speed
            FROM spatial_pairs
        ),
        
        -- Step 5: Analyze each cluster
        cluster_analysis AS (
            SELECT 
                removed_at,
                STRING_AGG(object_id::VARCHAR, '_' ORDER BY object_id) as group_token,
                COUNT(*) as cluster_size,
                
                -- Weapon analysis
                COUNT(*) FILTER (WHERE type_class = 'Weapon') as weapon_count,
                COUNT(*) FILTER (WHERE type_class = 'Weapon' AND parent_id IS NOT NULL) as tracked_weapon_count,
                COUNT(DISTINCT parent_id) FILTER (WHERE type_class = 'Weapon' AND parent_id IS NOT NULL) as unique_launcher_count,
                
                -- Target analysis
                COUNT(*) FILTER (WHERE type_class IN ('Air', 'Sea', 'Ground')) as target_count,
                
                -- Speed analysis for collision detection
                AVG(COALESCE(speed, 0)) FILTER (WHERE type_class IN ('Air', 'Sea', 'Ground')) as avg_target_speed,
                
                -- Coalition analysis
                COUNT(DISTINCT coalition) as coalition_count,
                
                -- Get primary weapon info if present (prefer tracked weapons)
                MAX(object_id) FILTER (WHERE type_class = 'Weapon' AND parent_id IS NOT NULL) as primary_weapon_id,
                MAX(parent_id) FILTER (WHERE type_class = 'Weapon' AND parent_id IS NOT NULL) as launcher_id,
                
                -- Collect IDs by type (DISTINCT prevents duplication from pairing logic)
                ARRAY_AGG(DISTINCT object_id) FILTER (WHERE type_class = 'Weapon') as weapon_ids,
                ARRAY_AGG(DISTINCT object_id) FILTER (WHERE type_class IN ('Air', 'Sea', 'Ground')) as target_ids,
                ARRAY_AGG(DISTINCT parent_id) FILTER (WHERE type_class = 'Weapon' AND parent_id IS NOT NULL) as launcher_ids
                
            FROM cluster_members
            GROUP BY removed_at, 
                (SELECT object_id FROM cluster_members cm2 
                 WHERE cm2.removed_at = cluster_members.removed_at 
                 ORDER BY object_id LIMIT 1)
        ),
        
        -- Step 6: Classify scenarios
        classified_clusters AS (
            SELECT 
                *,
                CASE
                    -- EDGE CASE: Multiple weapons from same launcher, no targets = coordinated MISS
                    WHEN weapon_count >= 2 AND unique_launcher_count = 1 AND target_count = 0 THEN 'COORDINATED_MISS'
                    
                    -- CASE 1: Weapon + Target(s) = Impact/Splash Damage
                    WHEN tracked_weapon_count >= 1 AND target_count >= 1 THEN 
                        CASE 
                            WHEN target_count = 1 AND tracked_weapon_count = 1 THEN 'WEAPON_IMPACT'
                            WHEN target_count > 1 THEN 'WEAPON_SPLASH_DAMAGE'
                            WHEN tracked_weapon_count > 1 THEN 'COORDINATED_STRIKE'
                        END
                    
                    -- CASE 2: Weapon + Weapon = Intercept
                    WHEN weapon_count >= 2 AND target_count = 0 AND unique_launcher_count > 1 THEN 'WEAPON_INTERCEPT'
                    
                    -- CASE 3: Multiple objects, no tracked weapon
                    WHEN tracked_weapon_count = 0 THEN
                        CASE
                            WHEN avg_target_speed > ? THEN 'MID_AIR_COLLISION'
                            ELSE 'DEBRIS_CLUSTER'
                        END
                    
                    -- Edge case: untracked weapon present
                    WHEN weapon_count > 0 AND tracked_weapon_count = 0 THEN 'UNTRACKED_WEAPON_IMPACT'
                    
                    ELSE 'UNKNOWN'
                END as event_type,
                
                -- Confidence scoring
                CASE
                    WHEN tracked_weapon_count >= 1 AND target_count >= 1 THEN 1.0
                    WHEN weapon_count >= 2 AND unique_launcher_count > 1 THEN 0.9
                    WHEN avg_target_speed > ? * 2 THEN 0.95
                    WHEN avg_target_speed > ? THEN 0.8
                    ELSE 0.5
                END as confidence
            FROM cluster_analysis
        )
        
        -- Step 7: Return clusters (excluding COORDINATED_MISS as they're just normal misses)
        SELECT 
            cc.removed_at,
            cc.group_token,
            cc.cluster_size,
            cc.event_type,
            cc.confidence,
            cc.weapon_count,
            cc.target_count,
            cc.primary_weapon_id,
            cc.launcher_id,
            cc.unique_launcher_count,
            cc.weapon_ids,
            cc.target_ids
        FROM classified_clusters cc
        WHERE cc.event_type != 'COORDINATED_MISS'  -- Skip multi-weapon misses
        ORDER BY cc.removed_at, cc.group_token
        """
        
        # Execute cluster detection
        #print("DEBUG: Query:", cluster_query[:500])  # First 500 chars
        clusters = conn.execute(
            cluster_query,
            [
                self.time_window,  # EXISTS check for near-simultaneous removals
                self.time_window,  # JOIN condition for spatial pairs
                self.proximity_radius,
                self.collision_speed_threshold,
                self.collision_speed_threshold,
                self.collision_speed_threshold
            ]
        ).fetchall()
        
        if not clusters:
            return 0
        
        # Update weapons with cluster information AND create tactical events
        weapon_updates = []
        target_updates = []
        tactical_events_to_insert = []
        
        for (removed_at, group_token, cluster_size, event_type, confidence,
             weapon_count, target_count, primary_weapon_id, launcher_id,
             unique_launcher_count, weapon_ids, target_ids) in clusters:
            
            # Update all weapons in the cluster
            if weapon_ids:
                for weapon_id in weapon_ids:
                    cluster_props = {
                        "ClusterEvent": group_token,
                        "EventType": event_type,
                        "ClusterSize": int(cluster_size),
                        "Confidence": float(confidence)
                    }
                    
                    # Add target information for impact events
                    if event_type in ('WEAPON_IMPACT', 'WEAPON_SPLASH_DAMAGE', 'COORDINATED_STRIKE', 'WEAPON_INTERCEPT'):
                        cluster_props["MultiKillCount"] = int(target_count)
                        if target_ids and len(target_ids) > 0:
                            # Store target IDs as array (TargetIDs, not ClusterTargets)
                            cluster_props["TargetIDs"] = list(target_ids)
                            cluster_props["Fate"] = "HIT"  # Mark as successful hit/intercept
                    
                    # Mark if this is the primary weapon
                    if weapon_id == primary_weapon_id:
                        cluster_props["IsPrimaryWeapon"] = True
                    
                    weapon_updates.append((json.dumps(cluster_props), weapon_id))
            
            # Create WEAPON_HIT tactical events for weapon-target pairs
            if event_type in ('WEAPON_IMPACT', 'WEAPON_SPLASH_DAMAGE', 'COORDINATED_STRIKE'):
                if weapon_ids and target_ids:
                    for weapon_id in weapon_ids:
                        for target_id in target_ids:
                            # Collect event data for bulk insert
                            tactical_events_to_insert.append((
                                weapon_id,
                                target_id,
                                removed_at,
                                event_type,
                                group_token,
                                int(cluster_size),
                                float(confidence)
                            ))
            
            # Create WEAPON_DESTROYED events for weapon intercepts
            elif event_type == 'WEAPON_INTERCEPT':
                if weapon_ids and len(weapon_ids) >= 2:
                    # All weapons in cluster destroyed each other
                    for weapon_id in weapon_ids:
                        for other_weapon_id in weapon_ids:
                            if weapon_id != other_weapon_id:
                                tactical_events_to_insert.append((
                                    weapon_id,
                                    other_weapon_id,
                                    removed_at,
                                    'WEAPON_INTERCEPT',
                                    group_token,
                                    int(cluster_size),
                                    float(confidence)
                                ))
            
            # Update all targets in the cluster
            if target_ids:
                for target_id in target_ids:
                    target_props = {
                        "ClusterEvent": group_token,
                        "EventType": event_type,
                        "ClusterSize": int(cluster_size)
                    }
                    
                    # Add weapon information for impact events
                    if event_type in ('WEAPON_IMPACT', 'WEAPON_SPLASH_DAMAGE', 'COORDINATED_STRIKE'):
                        if primary_weapon_id:
                            target_props["DestroyedByWeapon"] = str(primary_weapon_id)
                        if launcher_id:
                            target_props["DestroyedByLauncher"] = str(launcher_id)
                        if weapon_count > 1:
                            target_props["MultiWeaponStrike"] = int(weapon_count)
                    
                    target_updates.append((json.dumps(target_props), target_id))
        
        # Bulk update weapons
        if weapon_updates:
            conn.executemany(
                """
                UPDATE objects
                SET properties = json_merge_patch(COALESCE(properties, '{}'), ?)
                WHERE id = ?
                """,
                weapon_updates
            )
        
        # Bulk update targets
        if target_updates:
            conn.executemany(
                """
                UPDATE objects
                SET properties = json_merge_patch(COALESCE(properties, '{}'), ?)
                WHERE id = ?
                """,
                target_updates
            )
        
        # Bulk insert tactical events (WEAPON_HIT / WEAPON_DESTROYED)
        if tactical_events_to_insert:
            insert_query = """
            WITH event_data AS (
                SELECT 
                    UNNEST(?) as weapon_id,
                    UNNEST(?) as target_id,
                    UNNEST(?) as timestamp,
                    UNNEST(?) as event_type,
                    UNNEST(?) as cluster_token,
                    UNNEST(?) as cluster_size,
                    UNNEST(?) as confidence
            )
            INSERT INTO tactical_events 
            (event_type, timestamp, initiator_id, target_id,
             initiator_type, target_type, initiator_coalition, target_coalition,
             longitude, latitude, altitude,
             initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
            SELECT 
                CASE 
                    WHEN ed.event_type = 'WEAPON_INTERCEPT' THEN 'WEAPON_DESTROYED'
                    ELSE 'WEAPON_HIT'
                END,
                ed.timestamp,
                w.id,                    -- initiator = weapon
                ed.target_id,            -- target = hit object
                w.type_basic,
                t.type_class,
                w.coalition,
                t.coalition,
                ws.longitude, ws.latitude, ws.altitude,
                ws.id,                   -- weapon state at impact
                ts.id,                   -- target state at impact
                ls.id,                   -- launcher state at impact
                json_object(
                    'cluster_event', ed.cluster_token,
                    'event_type', ed.event_type,
                    'cluster_size', ed.cluster_size,
                    'confidence', ed.confidence,
                    'detection_method', 'spatial_cluster'
                )
            FROM event_data ed
            JOIN objects w ON w.id = ed.weapon_id
            JOIN objects t ON t.id = ed.target_id
            -- Get weapon state at impact
            JOIN LATERAL (
                SELECT id, longitude, latitude, altitude
                FROM states
                WHERE object_id = w.id AND timestamp <= ed.timestamp
                ORDER BY timestamp DESC LIMIT 1
            ) ws ON true
            -- Get target state at impact
            JOIN LATERAL (
                SELECT id
                FROM states
                WHERE object_id = t.id AND timestamp <= ed.timestamp
                ORDER BY timestamp DESC LIMIT 1
            ) ts ON true
            -- Get launcher state at impact (if weapon has launcher)
            LEFT JOIN states ls ON (
                ls.object_id = w.parent_id 
                AND ls.id = (
                    SELECT id FROM states
                    WHERE object_id = w.parent_id AND timestamp <= ed.timestamp
                    ORDER BY timestamp DESC LIMIT 1
                )
            )
            """
            
            # Unpack events into separate lists
            weapon_ids = [e[0] for e in tactical_events_to_insert]
            target_ids = [e[1] for e in tactical_events_to_insert]
            timestamps = [e[2] for e in tactical_events_to_insert]
            event_types = [e[3] for e in tactical_events_to_insert]
            cluster_tokens = [e[4] for e in tactical_events_to_insert]
            cluster_sizes = [e[5] for e in tactical_events_to_insert]
            confidences = [e[6] for e in tactical_events_to_insert]
            
            conn.execute(insert_query, [
                weapon_ids, target_ids, timestamps, event_types,
                cluster_tokens, cluster_sizes, confidences
            ])
        
        return len(clusters)

