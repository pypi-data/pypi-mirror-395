"""Projectile tracking and enrichment."""

import json
from typing import Optional
import duckdb

from .pipeline import Enricher


class ProjectileEnricher(Enricher):
    """
    Enriches projectile objects with launcher detection, hit detection, and burst grouping.
    
    Creates a clean hierarchy: Aircraft → Burst → Individual Projectiles
    
    Processing order:
    1. Launcher Detection - Match projectiles to launchers using spatial proximity
    2. Hit Detection - Classify projectiles as HIT/MISS before burst grouping
    3. Burst Detection - Group projectiles into burst objects with aggregated statistics
    4. Intended Target Detection - Identify likely intended targets for missed air-to-air bursts (enabled by default)
    
    Burst objects are synthetic (not part of ACMI spec) and group related projectiles
    fired in quick succession. Single-fire projectiles maintain direct parent_id to launcher.
    
    Intended target detection uses 3D cone tracking (azimuth + pitch) to identify which
    air targets stayed in the shooter's line of sight longest during missed bursts.
    """

    def __init__(
        self,
        launcher_radius: float = 150.0,
        hit_radius: float = 15.0,
        hit_altitude_tolerance: float = 50.0,
        burst_time_gap: float = 1.0,
        detect_launchers: bool = True,
        detect_hits: bool = True,
        create_bursts: bool = True,
        analyze_misses: bool = False,
        missed_cone_angle: float = 30.0,
        missed_max_distance: float = 3704.0,  # 2 nautical miles
        detect_intended_targets: bool = True,
        intended_cone_azimuth: float = 22.5,  # half-angle in degrees (±22.5° = 45° total cone)
        intended_cone_pitch: float = 22.5,     # half-angle in degrees (±22.5° = 45° total cone)
        intended_max_distance: float = 4000.0, # meters
        batch_size: int = 500,  # objects per batch (fixed count for consistent performance)
    ):
        """
        Initialize projectile enricher.
        
        Args:
            launcher_radius: Detection radius for launcher matching (default: 100m)
            hit_radius: Detection radius for hit matching (default: 10m, no splash damage)
            hit_altitude_tolerance: Altitude tolerance for hit detection (default: 25m)
            burst_time_gap: Time gap to trigger new burst (default: 1.0s)
            detect_launchers: Run launcher detection (default: True)
            detect_hits: Run hit detection (default: True)
            create_bursts: Create burst objects from grouped projectiles (default: True)
            analyze_misses: Analyze missed bursts for likely targets (default: False, DEPRECATED - use detect_intended_targets)
            missed_cone_angle: Cone angle for missed burst analysis (default: 30°)
            missed_max_distance: Max distance for missed burst targets (default: 3704m = 2nm)
            detect_intended_targets: Detect intended targets for MISSED air-to-air bursts using 3D cone tracking (default: True)
            intended_cone_azimuth: Azimuth cone HALF-ANGLE in degrees (default: 22.5° = ±22.5° = 45° total cone)
            intended_cone_pitch: Pitch cone HALF-ANGLE in degrees (default: 22.5° = ±22.5° = 45° total cone)
            intended_max_distance: Max distance for intended target detection (default: 4000m)
            batch_size: Objects per batch for chunked processing (default: 500). Fixed count ensures consistent performance regardless of mission action density.
            
        Note:
            Cone angles are HALF-ANGLES (the ± value):
            - intended_cone_azimuth=25.0 means ±25° (50° total azimuth cone)
            - intended_cone_azimuth=12.5 means ±12.5° (25° total azimuth cone)
        """
        self.launcher_radius = launcher_radius
        self.hit_radius = hit_radius
        self.hit_altitude_tolerance = hit_altitude_tolerance
        self.burst_time_gap = burst_time_gap
        self.detect_launchers = detect_launchers
        self.detect_hits = detect_hits
        self.create_bursts = create_bursts
        self.analyze_misses = analyze_misses
        self.missed_cone_angle = missed_cone_angle
        self.missed_max_distance = missed_max_distance
        self.detect_intended_targets = detect_intended_targets
        self.intended_cone_azimuth = intended_cone_azimuth
        self.intended_cone_pitch = intended_cone_pitch
        self.intended_max_distance = intended_max_distance
        self.batch_size = batch_size

    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run projectile enrichment pipeline with object count-based batching.
        
        Two-stage matching for launchers and hits:
        1. Stage 1 (Dynamic): Process ALL unmatched with ±0.2s window (fast, catches most)
        2. Stage 2 (Static): Process remaining unmatched with last-state matching (slower, edge cases)
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of projectiles enriched (total across all steps)
        """
        total_enriched = 0
        total_launchers = 0
        total_hits_found = 0  # Actual hits detected
        total_processed = 0   # Projectiles processed (for progress tracking)

        # Ensure spatial extension is loaded
        try:
            conn.execute("INSTALL spatial;")
            conn.execute("LOAD spatial;")
        except Exception:
            pass  # Already installed/loaded

        # Step 1: Launcher Detection
        if self.detect_launchers:
            # Stage 1: Dynamic window (±0.2s) - catches most aircraft/moving launchers
            while True:
                # print(f"Associating launchers with projectiles (dynamic) - {total_launchers}/{total_enriched}")
                launcher_count = self._detect_launchers(conn, self.batch_size, use_dynamic=True)
                if launcher_count == 0:
                    break
                total_enriched += launcher_count
                total_launchers += launcher_count

            # Stage 2: Static last-state - catches remaining (SAM sites, static launchers)
            while True:
                # print(f"Associating launchers with projectiles (static) - {total_launchers}/{total_enriched}")
                launcher_count = self._detect_launchers(conn, self.batch_size, use_dynamic=False)
                if launcher_count == 0:
                    break
                total_enriched += launcher_count
                total_launchers += launcher_count

        # Step 2: Hit Detection (must happen BEFORE burst grouping)
        # Two-pass approach:
        #   Pass 1: Dynamic mode for air-to-air (moving Air targets)
        #   Pass 2: Static mode for ground targets (Ground/Sea targets)
        if self.detect_hits:
            # Create temp table for projectile events (same structure as tactical_events)
            # This table persists across batches to track which projectiles have been processed
            conn.execute("""
                CREATE TEMP TABLE IF NOT EXISTS projectile_events (
                    id BIGINT,
                    event_type VARCHAR NOT NULL,
                    timestamp DOUBLE NOT NULL,
                    initiator_id VARCHAR NOT NULL,
                    target_id VARCHAR,
                    initiator_type VARCHAR,
                    target_type VARCHAR,
                    initiator_coalition VARCHAR,
                    target_coalition VARCHAR,
                    longitude DOUBLE,
                    latitude DOUBLE,
                    altitude DOUBLE,
                    initiator_state_id BIGINT,
                    target_state_id BIGINT,
                    initiator_parent_state_id BIGINT,
                    metadata JSON
                )
            """)
            conn.execute("DELETE FROM projectile_events")
            
            # Pass 1: Dynamic window (±0.2s) - air-to-air engagements
            while True:
                # print(
                #     f"Detecting hits with projectiles (dynamic, air-to-air) - {total_enriched} hits, {total_processed} processed"
                # )
                # Returns tuple: (projectiles_processed, hits_found)
                # processed_count == 0 means no more projectiles to process (termination condition)
                processed_count, hits_found = self._detect_hits_dynamic(conn, self.batch_size)
                if processed_count == 0:
                    break
                total_enriched += hits_found
                total_processed += processed_count

            # Pass 2: Static last-state - ground targets (Ground/Sea only)
            while True:
                # print(
                #     f"Detecting hits with projectiles (static, ground targets) - {total_enriched} enriched, {total_processed} processed"
                # )
                # Returns tuple: (projectiles_processed, hits_found)
                # processed_count == 0 means no more projectiles to process (termination condition)
                # Note: A batch with all misses still returns processed_count > 0 (projectiles were processed)
                processed_count, hits_found = self._detect_hits_static(conn, self.batch_size)
                if processed_count == 0:
                    break
                total_enriched += hits_found
                total_processed += processed_count

        # Step 3: Burst Detection and Aggregation
        if self.create_bursts:
            burst_count = self._create_bursts(conn)
            total_enriched += burst_count
            
            # Step 3b: Insert tactical events for bursts
            self._insert_burst_events(conn)

        # Step 4: Missed Burst Analysis (Optional, legacy)
        if self.analyze_misses:
            missed_count = self._analyze_missed_bursts(conn)
            total_enriched += missed_count

        # Step 5: Intended Target Detection (Optional, enhanced 3D cone tracking)
        if self.detect_intended_targets:
            intended_count = self._detect_intended_targets(conn)
            total_enriched += intended_count

        return total_enriched

    def _detect_launchers(self, conn: duckdb.DuckDBPyConnection, limit: int, use_dynamic: bool = True) -> int:
        """
        Match projectiles to launchers using coalition/color/country matching and spatial proximity.
        Uses LIMIT without OFFSET - filter automatically excludes already-enriched projectiles.
        
        Args:
            conn: DuckDB connection
            limit: Batch size (LIMIT clause)
            use_dynamic: If True, use ±0.2s window. If False, use last-state before spawn.
            
        Returns:
            Number of projectiles matched to launchers in this batch
        """
        launcher_radius_sq = self.launcher_radius * self.launcher_radius

        # Choose query based on dynamic vs static matching
        if use_dynamic:
            # DYNAMIC: Use ±0.2s time window (fast, catches most moving platforms)
            launcher_query = f"""
            WITH projectile_batch AS (
              SELECT id
              FROM objects
              WHERE type_basic = 'Projectile'
                AND parent_id IS NULL
              ORDER BY first_seen
              LIMIT ?
            ),
            projectile_first AS (
              SELECT
                p.id as projectile_id,
                p.country,
                p.first_seen,
                s.longitude as proj_lon,
                s.latitude as proj_lat,
                s.altitude as proj_alt
              FROM projectile_batch pb
              JOIN objects p ON p.id = pb.id
              JOIN states s ON p.id = s.object_id
                AND s.timestamp = p.first_seen
              WHERE s.longitude IS NOT NULL
            ),
            projectile_launcher_pairs AS (
              SELECT
                p.projectile_id,
                p.first_seen,
                p.proj_lon,
                p.proj_lat,
                p.proj_alt,
                l.id as launcher_id,
                p.proj_alt - {self.launcher_radius} as min_alt,
                p.proj_alt + {self.launcher_radius} as max_alt
              FROM projectile_first p
              JOIN objects l ON (l.country = p.country OR l.country IS NULL OR p.country IS NULL)
                AND l.type_class IN ('Air', 'Ground', 'Sea')
                AND l.first_seen <= p.first_seen
                AND (l.removed_at IS NULL OR l.removed_at >= p.first_seen)
            ),
            launcher_state_per_pair AS (
              SELECT
                plp.projectile_id,
                plp.launcher_id,
                plp.proj_lon,
                plp.proj_lat,
                plp.proj_alt,
                ls.longitude as launcher_lon,
                ls.latitude as launcher_lat,
                ls.altitude as launcher_alt
              FROM projectile_launcher_pairs plp
              JOIN LATERAL (
                SELECT longitude, latitude, altitude
                FROM states
                WHERE object_id = plp.launcher_id
                  AND longitude IS NOT NULL
                  AND altitude BETWEEN plp.min_alt AND plp.max_alt
                  AND timestamp BETWEEN plp.first_seen - 0.2 AND plp.first_seen + 0.2
                ORDER BY ABS(timestamp - plp.first_seen)
                LIMIT 1
              ) ls ON true
            ),
            closest_launcher AS (
              SELECT
                projectile_id,
                launcher_id,
                calculate_approximate_distance_squared(
                  launcher_lat - proj_lat,
                  launcher_lon - proj_lon
                ) + POW(launcher_alt - proj_alt, 2) as distance_sq,
                ROW_NUMBER() OVER (
                  PARTITION BY projectile_id
                  ORDER BY 
                    calculate_approximate_distance_squared(
                      launcher_lat - proj_lat,
                      launcher_lon - proj_lon
                    ) +
                    POW(launcher_alt - proj_alt, 2) ASC
                ) as rn
              FROM launcher_state_per_pair
              WHERE calculate_approximate_distance_squared(
                  launcher_lat - proj_lat,
                  launcher_lon - proj_lon
                ) + POW(launcher_alt - proj_alt, 2) <= ?
            )
            UPDATE objects
            SET parent_id = (
              SELECT launcher_id
              FROM closest_launcher cl
              WHERE cl.projectile_id = objects.id
                AND cl.rn = 1
            )
            WHERE id IN (SELECT projectile_id FROM closest_launcher WHERE rn = 1)
            """
        else:
            # STATIC: Use last state before spawn (slower, for static platforms)
            launcher_query = f"""
            WITH projectile_batch AS (
              SELECT id
              FROM objects
              WHERE type_basic = 'Projectile'
                AND parent_id IS NULL
              ORDER BY first_seen
              LIMIT ?
            ),
            projectile_first AS (
              SELECT
                p.id as projectile_id,
                p.country,
                p.first_seen,
                s.longitude as proj_lon,
                s.latitude as proj_lat,
                s.altitude as proj_alt
              FROM projectile_batch pb
              JOIN objects p ON p.id = pb.id
              JOIN states s ON p.id = s.object_id
                AND s.timestamp = p.first_seen
              WHERE s.longitude IS NOT NULL
            ),
            projectile_launcher_pairs AS (
              SELECT
                p.projectile_id,
                p.first_seen,
                p.proj_lon,
                p.proj_lat,
                p.proj_alt,
                l.id as launcher_id,
                p.proj_alt - {self.launcher_radius} as min_alt,
                p.proj_alt + {self.launcher_radius} as max_alt
              FROM projectile_first p
              JOIN objects l ON (l.country = p.country OR l.country IS NULL OR p.country IS NULL)
                AND l.type_class IN ('Air', 'Ground', 'Sea')
                AND l.first_seen <= p.first_seen
                AND (l.removed_at IS NULL OR l.removed_at >= p.first_seen)
            ),
            launcher_state_per_pair AS (
              SELECT
                plp.projectile_id,
                plp.launcher_id,
                plp.proj_lon,
                plp.proj_lat,
                plp.proj_alt,
                ls.longitude as launcher_lon,
                ls.latitude as launcher_lat,
                ls.altitude as launcher_alt
              FROM projectile_launcher_pairs plp
              JOIN LATERAL (
                SELECT longitude, latitude, altitude
                FROM states
                WHERE object_id = plp.launcher_id
                  AND longitude IS NOT NULL
                  AND altitude BETWEEN plp.min_alt AND plp.max_alt
                  AND timestamp <= plp.first_seen
                ORDER BY timestamp DESC
                LIMIT 1
              ) ls ON true
            ),
            closest_launcher AS (
              SELECT
                projectile_id,
                launcher_id,
                calculate_approximate_distance_squared(
                  launcher_lat - proj_lat,
                  launcher_lon - proj_lon
                ) + POW(launcher_alt - proj_alt, 2) as distance_sq,
                ROW_NUMBER() OVER (
                  PARTITION BY projectile_id
                  ORDER BY 
                    calculate_approximate_distance_squared(
                      launcher_lat - proj_lat,
                      launcher_lon - proj_lon
                    ) +
                    POW(launcher_alt - proj_alt, 2) ASC
                ) as rn
              FROM launcher_state_per_pair
              WHERE calculate_approximate_distance_squared(
                  launcher_lat - proj_lat,
                  launcher_lon - proj_lon
                ) + POW(launcher_alt - proj_alt, 2) <= ?
            )
            UPDATE objects
            SET parent_id = (
              SELECT launcher_id
              FROM closest_launcher cl
              WHERE cl.projectile_id = objects.id
                AND cl.rn = 1
            )
            WHERE id IN (SELECT projectile_id FROM closest_launcher WHERE rn = 1)
            """

        # Execute the update
        result = conn.execute(launcher_query, [limit, launcher_radius_sq])
        rows_updated = result.fetchone()[0] if result else 0

        # Return number of projectiles matched
        return rows_updated

    def _detect_hits_dynamic(self, conn: duckdb.DuckDBPyConnection, limit: int) -> tuple[int, int]:
        """
        Detect projectile hits against Air targets using dynamic time window matching.
        
        Uses asymmetric time window (-1s to +0.5s) to catch moving Air targets.
        Processes projectiles NOT yet in projectile_events table.
        Inserts PROJECTILE_HIT or PROJECTILE_PENDING events, then updates objects table.
        """
        hit_radius_sq = self.hit_radius * self.hit_radius

        # Dynamic mode: Process projectiles NOT in projectile_events (haven't been checked yet)
        already_processed_filter = "AND p.id NOT IN (SELECT initiator_id FROM projectile_events)"

        # Get batch count first
        batch_count_query = f"""
        SELECT COUNT(*) FROM (
          SELECT p.id
          FROM objects p
          WHERE p.type_basic = 'Projectile'
            AND p.removed_at IS NOT NULL
            {already_processed_filter}
          ORDER BY p.first_seen
          LIMIT ?
        )
        """
        batch_count = conn.execute(batch_count_query, [limit]).fetchone()[0]
        if batch_count == 0:
            return (0, 0)

        # DYNAMIC: Use -1s to +0.5s time window for air-to-air engagements (moving Air targets)
        # Asymmetric window: look back 1s, forward 0.5s (catches targets that were hit before projectile removal)
        hit_query = f"""
        WITH projectile_batch AS (
          SELECT p.id as projectile_id
          FROM objects p
          WHERE p.type_basic = 'Projectile'
            AND p.removed_at IS NOT NULL
            {already_processed_filter}
          ORDER BY p.first_seen
          LIMIT ?
        ),
        projectile_final AS (
          SELECT
            pb.projectile_id,
            p.last_seen,
            p.parent_id as launcher_id,
            p.coalition as projectile_coalition,
            s.id as projectile_state_id,
            s.longitude as proj_lon,
            s.latitude as proj_lat,
            s.altitude as proj_alt
          FROM projectile_batch pb
          JOIN objects p ON p.id = pb.projectile_id
          JOIN LATERAL (
            SELECT id, longitude, latitude, altitude
            FROM states
            WHERE object_id = p.id AND longitude IS NOT NULL
            ORDER BY timestamp DESC
            LIMIT 1
          ) s ON true
        ),
        projectile_target_pairs AS (
          SELECT
            pf.projectile_id,
            pf.projectile_state_id,
            pf.last_seen,
            pf.launcher_id,
            pf.projectile_coalition,
            pf.proj_lon,
            pf.proj_lat,
            pf.proj_alt,
            t.id as target_id,
            t.coalition as target_coalition
          FROM projectile_final pf
          JOIN objects t ON t.type_class = 'Air'
            AND t.first_seen <= pf.last_seen
            -- Allow targets that were alive at impact time OR destroyed within 1s before impact
            -- (targets destroyed by the projectile will have removed_at slightly before last_seen)
            AND (t.removed_at IS NULL OR t.removed_at >= pf.last_seen - 1.0)
            AND (pf.launcher_id IS NULL OR t.id != pf.launcher_id)
        ),
        target_state_per_pair AS (
          SELECT
            ptp.projectile_id,
            ptp.projectile_state_id,
            ptp.projectile_coalition,
            ptp.target_coalition,
            ptp.target_id,
            ts.id as target_state_id,
            calculate_approximate_distance_squared(
              ts.latitude - ptp.proj_lat,
              ts.longitude - ptp.proj_lon
            ) + POW(ts.altitude - ptp.proj_alt, 2) as distance_sq
          FROM projectile_target_pairs ptp
          JOIN LATERAL (
            SELECT id, longitude, latitude, altitude
            FROM states
            WHERE object_id = ptp.target_id
              AND longitude IS NOT NULL
              AND altitude BETWEEN ptp.proj_alt - ? AND ptp.proj_alt + ?
              AND timestamp BETWEEN ptp.last_seen - 1.0 AND ptp.last_seen + 0.5
            ORDER BY ABS(timestamp - ptp.last_seen)
            LIMIT 1
          ) ts ON true
        ),
        closest_target AS (
          SELECT
            projectile_id,
            projectile_state_id,
            target_id,
            target_state_id,
            projectile_coalition,
            target_coalition,
            distance_sq,
            ROW_NUMBER() OVER (
              PARTITION BY projectile_id
              ORDER BY distance_sq ASC
            ) as rn
          FROM target_state_per_pair
          WHERE distance_sq <= ?
        ),
        hits_found AS (
          SELECT
            projectile_id,
            projectile_state_id,
            target_id,
            target_state_id,
            SQRT(distance_sq) as distance,
            CASE
              WHEN projectile_coalition = target_coalition THEN 'FRIENDLY_FIRE'
              WHEN projectile_coalition != target_coalition THEN 'ENEMY'
              ELSE 'NEUTRAL'
            END as hit_type
          FROM closest_target
          WHERE rn = 1
        )
        SELECT
          pb.projectile_id,
          hf.target_id,
          hf.projectile_state_id,
          hf.target_state_id,
          hf.distance,
          hf.hit_type
        FROM projectile_batch pb
        LEFT JOIN hits_found hf ON pb.projectile_id = hf.projectile_id
        """

        # Query hits with state IDs
        hits = conn.execute(
            hit_query,
            [limit, self.hit_altitude_tolerance, self.hit_altitude_tolerance, hit_radius_sq]
        ).fetchall()

        # Collect hit events and missed projectile IDs
        hit_events = []
        hit_projectile_ids = set()
        missed_projectile_ids = []
        
        for row in hits:
            projectile_id, target_id, projectile_state_id, target_state_id, distance, hit_type = row
            if target_id is not None:
                # Hit found
                hit_events.append((projectile_id, target_id, projectile_state_id, target_state_id, distance, hit_type))
                hit_projectile_ids.add(projectile_id)
            else:
                # No hit
                missed_projectile_ids.append(projectile_id)
        
        # Dynamic mode: Insert HIT or PENDING events
        if hit_events:
            self._insert_projectile_hit_events(conn, hit_events)
        if missed_projectile_ids:
            self._insert_projectile_pending_events(conn, missed_projectile_ids)
        
        # Update objects table based on events
        if hit_events:
            # Update hits
            conn.execute("""
                UPDATE objects
                SET properties = json_merge_patch(
                  COALESCE(properties, json('{}')),
                  json_object(
                    'Fate', 'HIT',
                    'TargetIDs', json_array(pe.target_id),
                    'HitDistance', (pe.metadata->>'hit_distance')::DOUBLE,
                    'HitType', pe.metadata->>'hit_type'
                  )
                )
                FROM projectile_events pe
                WHERE objects.id = pe.initiator_id
                  AND pe.event_type = 'PROJECTILE_HIT'
            """)
        
        # Update misses - dynamic mode marks as PENDING
        if missed_projectile_ids:
            conn.execute("""
                UPDATE objects
                SET properties = json_merge_patch(COALESCE(properties, json('{}')), json_object('Fate', 'PENDING'))
                WHERE id IN (SELECT UNNEST(?))
            """, [missed_projectile_ids])
        
        # Count hits from events
        hits_found = len(hit_events)
        
        return (batch_count, hits_found)

    def _detect_hits_static(self, conn: duckdb.DuckDBPyConnection, limit: int) -> tuple[int, int]:
        """
        Detect projectile hits against Ground/Sea targets using static last-state matching.
        
        Uses last state before impact for stationary/slow-moving targets.
        Processes projectiles with PENDING events from dynamic mode.
        Updates PROJECTILE_PENDING events to PROJECTILE_HIT or PROJECTILE_MISS, then updates objects table.
        """
        hit_radius_sq = self.hit_radius * self.hit_radius

        # Static mode: Process projectiles with PENDING events (from dynamic mode, need Ground/Sea check)
        already_processed_filter = "AND p.id IN (SELECT initiator_id FROM projectile_events WHERE event_type = 'PROJECTILE_PENDING')"

        # Get batch count first
        batch_count_query = f"""
        SELECT COUNT(*) FROM (
          SELECT p.id
          FROM objects p
          WHERE p.type_basic = 'Projectile'
            AND p.removed_at IS NOT NULL
            {already_processed_filter}
          ORDER BY p.first_seen
          LIMIT ?
        )
        """
        batch_count = conn.execute(batch_count_query, [limit]).fetchone()[0]
        if batch_count == 0:
            return (0, 0)

        # STATIC: Use last state before impact for ground targets (Ground/Sea only)
        # Process projectiles with PENDING events from dynamic mode
        hit_query = f"""
        WITH projectile_batch AS (
          SELECT p.id as projectile_id
          FROM objects p
          WHERE p.type_basic = 'Projectile'
            AND p.removed_at IS NOT NULL
            {already_processed_filter}
          ORDER BY p.first_seen
          LIMIT ?
        ),
        projectile_final AS (
          SELECT
            pb.projectile_id,
            p.last_seen,
            p.parent_id as launcher_id,
            p.coalition as projectile_coalition,
            s.id as projectile_state_id,
            s.longitude as proj_lon,
            s.latitude as proj_lat,
            s.altitude as proj_alt
          FROM projectile_batch pb
          JOIN objects p ON p.id = pb.projectile_id
          JOIN LATERAL (
            SELECT id, longitude, latitude, altitude
            FROM states
            WHERE object_id = p.id AND longitude IS NOT NULL
            ORDER BY timestamp DESC
            LIMIT 1
          ) s ON true
        ),
        projectile_target_pairs AS (
          SELECT
            pf.projectile_id,
            pf.projectile_state_id,
            pf.last_seen,
            pf.launcher_id,
            pf.projectile_coalition,
            pf.proj_lon,
            pf.proj_lat,
            pf.proj_alt,
            t.id as target_id,
            t.coalition as target_coalition,
            t.first_seen as target_first_seen,
            t.removed_at as target_removed_at
          FROM projectile_final pf
          JOIN objects t ON t.type_class IN ('Sea', 'Ground')
            AND t.first_seen <= pf.last_seen
            -- Target must be alive at impact time OR was alive within 1 second before impact
            AND (t.removed_at IS NULL OR t.removed_at >= pf.last_seen - 1.0)
            AND (pf.launcher_id IS NULL OR t.id != pf.launcher_id)
        ),
        -- Pre-filter targets by altitude using approximate bounds (fast approximation)
        -- This reduces the expensive LATERAL join to only targets within altitude tolerance
        targets_with_altitude_bounds AS (
          SELECT
            ptp.projectile_id,
            ptp.projectile_state_id,
            ptp.last_seen,
            ptp.launcher_id,
            ptp.projectile_coalition,
            ptp.proj_lon,
            ptp.proj_lat,
            ptp.proj_alt,
            ptp.target_id,
            ptp.target_coalition,
            ptp.target_first_seen,
            ptp.target_removed_at,
            -- Get target's approximate altitude from last state (for pre-filtering)
            ts_approx.altitude as target_alt_approx
          FROM projectile_target_pairs ptp
          JOIN LATERAL (
            SELECT altitude
            FROM states
            WHERE object_id = ptp.target_id
              AND longitude IS NOT NULL
              AND timestamp <= ptp.last_seen + 0.1
            ORDER BY timestamp DESC
            LIMIT 1
          ) ts_approx ON true
          WHERE ts_approx.altitude BETWEEN ptp.proj_alt - ? AND ptp.proj_alt + ?
        ),
        target_state_per_pair AS (
          SELECT
            twab.projectile_id,
            twab.projectile_state_id,
            twab.projectile_coalition,
            twab.target_coalition,
            twab.target_id,
            ts.id as target_state_id,
            calculate_approximate_distance_squared(
              ts.latitude - twab.proj_lat,
              ts.longitude - twab.proj_lon
            ) + POW(ts.altitude - twab.proj_alt, 2) as distance_sq
          FROM targets_with_altitude_bounds twab
          JOIN LATERAL (
            SELECT id, longitude, latitude, altitude
            FROM states
            WHERE object_id = twab.target_id
              AND longitude IS NOT NULL
              AND timestamp <= twab.last_seen + 0.1
            ORDER BY timestamp DESC
            LIMIT 1
          ) ts ON true
        ),
        closest_target AS (
          SELECT
            projectile_id,
            projectile_state_id,
            target_id,
            target_state_id,
            projectile_coalition,
            target_coalition,
            distance_sq,
            ROW_NUMBER() OVER (
              PARTITION BY projectile_id
              ORDER BY distance_sq ASC
            ) as rn
          FROM target_state_per_pair
          WHERE distance_sq <= ?
        ),
        hits_found AS (
          SELECT
            projectile_id,
            projectile_state_id,
            target_id,
            target_state_id,
            SQRT(distance_sq) as distance,
            CASE
              WHEN projectile_coalition = target_coalition THEN 'FRIENDLY_FIRE'
              WHEN projectile_coalition != target_coalition THEN 'ENEMY'
              ELSE 'NEUTRAL'
            END as hit_type
          FROM closest_target
          WHERE rn = 1
        )
        SELECT
          pb.projectile_id,
          hf.target_id,
          hf.projectile_state_id,
          hf.target_state_id,
          hf.distance,
          hf.hit_type
        FROM projectile_batch pb
        LEFT JOIN hits_found hf ON pb.projectile_id = hf.projectile_id
        """

        # Query hits with state IDs
        hits = conn.execute(
            hit_query,
            [limit, self.hit_altitude_tolerance, self.hit_altitude_tolerance, hit_radius_sq]
        ).fetchall()

        # Collect hit events and missed projectile IDs
        hit_events = []
        hit_projectile_ids = set()
        missed_projectile_ids = []
        
        for row in hits:
            projectile_id, target_id, projectile_state_id, target_state_id, distance, hit_type = row
            if target_id is not None:
                # Hit found
                hit_events.append((projectile_id, target_id, projectile_state_id, target_state_id, distance, hit_type))
                hit_projectile_ids.add(projectile_id)
            else:
                # No hit
                missed_projectile_ids.append(projectile_id)
        
        # Static mode: Update PENDING events to HIT or MISS
        if hit_events:
            self._update_projectile_hit_events(conn, hit_events)
        if missed_projectile_ids:
            self._update_projectile_miss_events(conn, missed_projectile_ids)
        
        # Update objects table based on events
        if hit_events:
            # Update hits
            conn.execute("""
                UPDATE objects
                SET properties = json_merge_patch(
                  COALESCE(properties, json('{}')),
                  json_object(
                    'Fate', 'HIT',
                    'TargetIDs', json_array(pe.target_id),
                    'HitDistance', (pe.metadata->>'hit_distance')::DOUBLE,
                    'HitType', pe.metadata->>'hit_type'
                  )
                )
                FROM projectile_events pe
                WHERE objects.id = pe.initiator_id
                  AND pe.event_type = 'PROJECTILE_HIT'
            """)
        
        # Update misses - static mode marks as MISS
        if missed_projectile_ids:
            conn.execute("""
                UPDATE objects
                SET properties = json_merge_patch(COALESCE(properties, json('{}')), json_object('Fate', 'MISS'))
                WHERE id IN (SELECT UNNEST(?))
            """, [missed_projectile_ids])
        
        # Count hits from events
        hits_found = len(hit_events)
        
        return (batch_count, hits_found)
    
    def _insert_projectile_hit_events(self, conn: duckdb.DuckDBPyConnection, hit_events: list):
        """
        Insert PROJECTILE_HIT events into temp projectile_events table.
        
        Args:
            conn: DuckDB connection
            hit_events: List of hit tuples (projectile_id, target_id, projectile_state_id, target_state_id, distance, hit_type)
        """
        if not hit_events:
            return
        
        # Unpack hit_events into separate lists
        projectile_ids = [h[0] for h in hit_events]
        target_ids = [h[1] for h in hit_events]
        projectile_state_ids = [h[2] for h in hit_events]
        target_state_ids = [h[3] for h in hit_events]
        distances = [h[4] for h in hit_events]
        hit_types = [h[5] for h in hit_events]
        
        insert_query = """
        WITH hit_data AS (
            SELECT 
                UNNEST(?) as projectile_id,
                UNNEST(?) as target_id,
                UNNEST(?) as projectile_state_id,
                UNNEST(?) as target_state_id,
                UNNEST(?) as distance,
                UNNEST(?) as hit_type
        )
        INSERT INTO projectile_events 
        (event_type, timestamp, initiator_id, target_id,
         initiator_type, target_type, initiator_coalition, target_coalition,
         longitude, latitude, altitude,
         initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
        SELECT 
            'PROJECTILE_HIT',
            p.last_seen,
            p.id,                    -- initiator = projectile
            h.target_id,            -- target = hit object
            p.type_basic,
            t.type_class,
            p.coalition,
            t.coalition,
            ps.longitude, ps.latitude, ps.altitude,
            h.projectile_state_id,   -- projectile state at impact
            h.target_state_id,       -- target state at impact
            ls.id,                   -- launcher state at impact
            json_object('hit_distance', h.distance, 'hit_type', h.hit_type)
        FROM hit_data h
        JOIN objects p ON p.id = h.projectile_id
        JOIN objects t ON t.id = h.target_id
        JOIN states ps ON ps.id = h.projectile_state_id
        JOIN LATERAL (
            SELECT id
            FROM states
            WHERE object_id = p.parent_id AND timestamp <= p.last_seen
            ORDER BY timestamp DESC LIMIT 1
        ) ls ON p.parent_id IS NOT NULL
        """
        
        conn.execute(insert_query, [projectile_ids, target_ids, projectile_state_ids, target_state_ids, distances, hit_types])
    
    def _insert_projectile_pending_events(self, conn: duckdb.DuckDBPyConnection, projectile_ids: list):
        """
        Insert PROJECTILE_PENDING events into temp projectile_events table.
        Used by dynamic mode for projectiles that didn't hit Air targets (will be checked against Ground/Sea in static mode).
        
        Args:
            conn: DuckDB connection
            projectile_ids: List of projectile IDs that didn't hit (pending Ground/Sea check)
        """
        if not projectile_ids:
            return
        
        insert_query = """
        INSERT INTO projectile_events 
        (event_type, timestamp, initiator_id, target_id,
         initiator_type, target_type, initiator_coalition, target_coalition,
         longitude, latitude, altitude,
         initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
        SELECT 
            'PROJECTILE_PENDING',
            p.last_seen,
            p.id,                    -- initiator = projectile
            NULL,                    -- target = none
            p.type_basic,
            NULL,
            p.coalition,
            NULL,
            ps.longitude, ps.latitude, ps.altitude,
            ps.id,                   -- projectile state at end of flight
            NULL,                    -- no target state
            (SELECT id FROM states 
             WHERE object_id = p.parent_id AND timestamp <= p.last_seen
             ORDER BY timestamp DESC LIMIT 1),  -- launcher state at end of flight
            json('{}')
        FROM objects p
        JOIN LATERAL (
            SELECT id, longitude, latitude, altitude
            FROM states
            WHERE object_id = p.id
            ORDER BY timestamp DESC LIMIT 1
        ) ps ON true
        WHERE p.id IN (SELECT UNNEST(?))
          AND p.last_seen IS NOT NULL
        """
        
        conn.execute(insert_query, [projectile_ids])
    
    def _insert_projectile_miss_events(self, conn: duckdb.DuckDBPyConnection, projectile_ids: list):
        """
        Insert PROJECTILE_MISS events into temp projectile_events table.
        Used by static mode for projectiles that didn't hit Ground/Sea targets.
        
        Args:
            conn: DuckDB connection
            projectile_ids: List of projectile IDs that missed
        """
        if not projectile_ids:
            return
        
        insert_query = """
        INSERT INTO projectile_events 
        (event_type, timestamp, initiator_id, target_id,
         initiator_type, target_type, initiator_coalition, target_coalition,
         longitude, latitude, altitude,
         initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
        SELECT 
            'PROJECTILE_MISS',
            p.last_seen,
            p.id,                    -- initiator = projectile
            NULL,                    -- target = none
            p.type_basic,
            NULL,
            p.coalition,
            NULL,
            ps.longitude, ps.latitude, ps.altitude,
            ps.id,                   -- projectile state at end of flight
            NULL,                    -- no target state
            (SELECT id FROM states 
             WHERE object_id = p.parent_id AND timestamp <= p.last_seen
             ORDER BY timestamp DESC LIMIT 1),  -- launcher state at end of flight
            json('{}')
        FROM objects p
        JOIN LATERAL (
            SELECT id, longitude, latitude, altitude
            FROM states
            WHERE object_id = p.id
            ORDER BY timestamp DESC LIMIT 1
        ) ps ON true
        WHERE p.id IN (SELECT UNNEST(?))
          AND p.last_seen IS NOT NULL
        """
        
        conn.execute(insert_query, [projectile_ids])
    
    def _update_projectile_hit_events(self, conn: duckdb.DuckDBPyConnection, hit_events: list):
        """
        Update PROJECTILE_PENDING events to PROJECTILE_HIT in temp projectile_events table.
        Used by static mode to update PENDING events from dynamic mode.
        
        Args:
            conn: DuckDB connection
            hit_events: List of hit tuples (projectile_id, target_id, projectile_state_id, target_state_id, distance, hit_type)
        """
        if not hit_events:
            return
        
        # Unpack hit_events into separate lists
        projectile_ids = [h[0] for h in hit_events]
        target_ids = [h[1] for h in hit_events]
        projectile_state_ids = [h[2] for h in hit_events]
        target_state_ids = [h[3] for h in hit_events]
        distances = [h[4] for h in hit_events]
        hit_types = [h[5] for h in hit_events]
        
        update_query = """
        WITH hit_data AS (
            SELECT 
                UNNEST(?) as projectile_id,
                UNNEST(?) as target_id,
                UNNEST(?) as projectile_state_id,
                UNNEST(?) as target_state_id,
                UNNEST(?) as distance,
                UNNEST(?) as hit_type
        )
        UPDATE projectile_events pe
        SET 
            event_type = 'PROJECTILE_HIT',
            target_id = h.target_id,
            target_type = t.type_class,
            target_coalition = t.coalition,
            initiator_state_id = h.projectile_state_id,
            target_state_id = h.target_state_id,
            metadata = json_object('hit_distance', h.distance, 'hit_type', h.hit_type)
        FROM hit_data h
        JOIN objects t ON t.id = h.target_id
        WHERE pe.initiator_id = h.projectile_id
          AND pe.event_type = 'PROJECTILE_PENDING'
        """
        
        conn.execute(update_query, [projectile_ids, target_ids, projectile_state_ids, target_state_ids, distances, hit_types])
    
    def _update_projectile_miss_events(self, conn: duckdb.DuckDBPyConnection, projectile_ids: list):
        """
        Update PROJECTILE_PENDING events to PROJECTILE_MISS in temp projectile_events table.
        Used by static mode to update PENDING events from dynamic mode.
        
        Args:
            conn: DuckDB connection
            projectile_ids: List of projectile IDs that missed
        """
        if not projectile_ids:
            return
        
        update_query = """
        UPDATE projectile_events
        SET event_type = 'PROJECTILE_MISS'
        WHERE initiator_id IN (SELECT UNNEST(?))
          AND event_type = 'PROJECTILE_PENDING'
        """
        
        conn.execute(update_query, [projectile_ids])

    def _create_bursts(self, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Group projectiles into burst objects using time-based analysis.
        
        Creates burst objects for multi-projectile groups (2+ projectiles within burst_time_gap).
        Single-fire projectiles keep direct parent_id to launcher. Burst objects aggregate
        statistics from already-classified projectiles.
        
        Args:
            conn: DuckDB connection
            
        Returns:
            Number of burst objects created
        """
        # Step 3a: Assign burst IDs and aggregate statistics
        burst_query = f"""
        WITH projectile_gaps AS (
          SELECT
            p.id as projectile_id,
            p.parent_id as launcher_id,
            p.first_seen,
            LAG(p.first_seen) OVER (
              PARTITION BY p.parent_id
              ORDER BY p.first_seen
            ) as prev_timestamp,
            p.first_seen - LAG(p.first_seen) OVER (
              PARTITION BY p.parent_id
              ORDER BY p.first_seen
            ) as time_gap
          FROM objects p
          WHERE p.type_basic = 'Projectile'
            AND p.parent_id IS NOT NULL
        ),
        burst_flags AS (
          SELECT *,
            CASE
              WHEN time_gap IS NULL THEN 1
              WHEN time_gap >= ? THEN 1
              ELSE 0
            END as new_burst_flag
          FROM projectile_gaps
        ),
        burst_assignments AS (
          SELECT *,
            launcher_id || '_burst_' ||
            SUM(new_burst_flag) OVER (
              PARTITION BY launcher_id
              ORDER BY first_seen
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) as burst_id
          FROM burst_flags
        ),
        burst_groups AS (
          SELECT
            ba.burst_id,
            ba.launcher_id,
            MIN(ba.first_seen) as burst_first_seen,
            MAX(ba.first_seen) as burst_last_seen,
            MAX(p.removed_at) as burst_removed_at,
            COUNT(*) as projectile_count,
            COUNT(*) FILTER (WHERE p.properties->>'Fate' = 'HIT') as hit_count,
            ARRAY_AGG(DISTINCT json_extract(p.properties, '$.TargetIDs')[1])
              FILTER (WHERE json_extract(p.properties, '$.TargetIDs') IS NOT NULL) as target_ids,
            ARRAY_AGG(ba.projectile_id ORDER BY ba.first_seen) as projectile_ids,
            (ARRAY_AGG(p.name ORDER BY ba.first_seen))[1] as projectile_name
          FROM burst_assignments ba
          JOIN objects p ON p.id = ba.projectile_id
          GROUP BY ba.burst_id, ba.launcher_id
          HAVING COUNT(*) > 1
        )
        SELECT * FROM burst_groups
        """

        burst_groups = conn.execute(burst_query, [self.burst_time_gap]).fetchall()

        if not burst_groups:
            return 0

        # Step 3b: Insert burst objects with statistics
        insert_bursts = []
        burst_projectiles = {}  # Map burst_id -> [projectile_ids]

        for row in burst_groups:
            (burst_id, launcher_id, burst_first_seen, burst_last_seen,
             burst_removed_at, projectile_count, hit_count, target_ids, projectile_ids, projectile_name) = row

            # Get launcher info for naming and pilot
            launcher = conn.execute(
                "SELECT name, coalition, color, country, pilot FROM objects WHERE id = ?",
                [launcher_id]
            ).fetchone()

            if not launcher:
                continue

            launcher_name, coalition, color, country, pilot = launcher

            # Calculate burst sequence number for this launcher
            burst_num = int(burst_id.split('_burst_')[-1])

            burst_duration = burst_last_seen - burst_first_seen
            fire_rate = projectile_count / burst_duration if burst_duration > 0 else 0

            # Use parent.pilot format for pilot name
            pilot_name = f"{launcher_name}.{pilot}" if pilot else launcher_name

            properties = {
                "BurstProjectileCount": projectile_count,
                "BurstDuration": burst_duration,
                "BurstFireRate": fire_rate,
                "ProjectileIDs": projectile_ids,
                "HitCount": hit_count,
                "TargetIDs": target_ids if target_ids else [],
                "Fate": "HIT" if hit_count > 0 else "MISS",
                "Pilot": pilot_name
            }

            insert_bursts.append((
                burst_id,
                projectile_name,  # Use the projectile type name (e.g., "30x165mm")
                'Projectile',
                'Burst',
                launcher_id,
                burst_first_seen,
                burst_last_seen,
                burst_removed_at,
                coalition,
                color,
                country,
                json.dumps(properties)
            ))

            burst_projectiles[burst_id] = projectile_ids

        if insert_bursts:
            conn.executemany(
                """
                INSERT INTO objects 
                (id, name, type_basic, type_specific, parent_id, first_seen, last_seen, 
                 removed_at, coalition, color, country, properties)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                insert_bursts
            )

        # Step 3c: Rewrite parent_id for projectiles in bursts
        parent_updates = []
        for burst_id, projectile_ids in burst_projectiles.items():
            for proj_id in projectile_ids:
                parent_updates.append((burst_id, proj_id))

        if parent_updates:
            conn.executemany(
                "UPDATE objects SET parent_id = ? WHERE id = ?",
                parent_updates
            )

        return len(insert_bursts)
    
    def _insert_burst_events(self, conn: duckdb.DuckDBPyConnection):
        """
        Insert WEAPON_HIT and WEAPON_MISS events into tactical_events table for bursts.
        Uses the gun round name (e.g., "M61_20_PGU28") as the weapon name.
        
        Creates one WEAPON_HIT event per target hit (handles A/G strafe with multiple targets).
        Creates a single WEAPON_MISS event for bursts with no hits.
        
        Args:
            conn: DuckDB connection
        """
        insert_query = """
        WITH burst_hits AS (
          -- For bursts with hits: use projectile_events to get all targets hit
          -- Group by burst_id and target_id to create one WEAPON_HIT event per target
          SELECT DISTINCT
            b.id as burst_id,
            b.last_seen,
            b.coalition,
            b.properties,
            b.parent_id as launcher_id,
            REGEXP_EXTRACT(b.name, '([^.]+)$') as weapon_name,
            pe.target_id,
            pe.target_state_id,
            pe.target_type,
            pe.target_coalition
          FROM objects b
          JOIN objects p ON p.parent_id = b.id AND p.type_basic = 'Projectile'
          JOIN projectile_events pe ON pe.initiator_id = p.id AND pe.event_type = 'PROJECTILE_HIT'
          WHERE b.type_specific = 'Burst'
            AND b.last_seen IS NOT NULL
            AND CAST(b.properties->>'HitCount' AS INTEGER) > 0
        ),
        burst_misses AS (
          -- For bursts with no hits: single MISS event
          SELECT 
            b.id as burst_id,
            b.last_seen,
            b.coalition,
            b.properties,
            b.parent_id as launcher_id,
            REGEXP_EXTRACT(b.name, '([^.]+)$') as weapon_name,
            NULL::VARCHAR as target_id,
            NULL::BIGINT as target_state_id,
            NULL::VARCHAR as target_type,
            NULL::VARCHAR as target_coalition
          FROM objects b
          WHERE b.type_specific = 'Burst'
            AND b.last_seen IS NOT NULL
            AND CAST(b.properties->>'HitCount' AS INTEGER) = 0
        ),
        all_burst_events AS (
          SELECT * FROM burst_hits
          UNION ALL
          SELECT * FROM burst_misses
        )
        INSERT INTO tactical_events 
        (event_type, timestamp, initiator_id, target_id,
         initiator_type, target_type, initiator_coalition, target_coalition,
         longitude, latitude, altitude,
         initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
        SELECT 
            CASE 
                WHEN abe.target_id IS NOT NULL THEN 'WEAPON_HIT'
                ELSE 'WEAPON_MISS'
            END,
            abe.last_seen,
            abe.burst_id,                    -- initiator = burst (weapon)
            abe.target_id,                    -- target = hit target (one per event)
            abe.weapon_name,                  -- initiator_type = gun round name (e.g., "M61_20_PGU28")
            abe.target_type,                  -- target_type from projectile_events (if hit)
            abe.coalition,
            abe.target_coalition,             -- target_coalition from projectile_events (if hit)
            ls.longitude, ls.latitude, ls.altitude,
            ls.id,                            -- launcher state at burst end (used as initiator state)
            abe.target_state_id,              -- target state at hit from projectile_events (if hit)
            ls.id,                            -- launcher state at burst end
            json_object(
                'burst_projectile_count', CAST(abe.properties->>'BurstProjectileCount' AS INTEGER),
                'burst_duration', CAST(abe.properties->>'BurstDuration' AS DOUBLE),
                'burst_fire_rate', CAST(abe.properties->>'BurstFireRate' AS DOUBLE),
                'hit_count', CAST(abe.properties->>'HitCount' AS INTEGER),
                'pilot', abe.properties->>'Pilot'
            )
        FROM all_burst_events abe
        LEFT JOIN objects launcher ON launcher.id = abe.launcher_id
        JOIN LATERAL (
            SELECT id, longitude, latitude, altitude
            FROM states
            WHERE object_id = launcher.id 
              AND timestamp <= abe.last_seen
            ORDER BY timestamp DESC LIMIT 1
        ) ls ON launcher.id IS NOT NULL
        WHERE launcher.id IS NOT NULL
        """
        
        conn.execute(insert_query)

    def _analyze_missed_bursts(self, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Analyze missed bursts to identify likely intended targets.
        
        For bursts marked as MISS, looks forward from launcher heading to find potential
        targets within cone angle and max distance.
        
        Args:
            conn: DuckDB connection
            
        Returns:
            Number of missed bursts enriched with proximity data
        """
        # Get missed bursts and their launcher states at fire time
        missed_query = f"""
        WITH launcher_state_at_fire AS (
          SELECT
            b.id as burst_id,
            b.parent_id as launcher_id,
            b.first_seen as fire_time,
            s.u, s.v, s.heading,
            s.longitude, s.latitude
          FROM objects b
          JOIN objects l ON b.parent_id = l.id
          JOIN LATERAL (
            SELECT u, v, heading, longitude, latitude
            FROM states
            WHERE object_id = l.id
              AND timestamp <= b.first_seen
            ORDER BY ABS(timestamp - b.first_seen)
            LIMIT 1
          ) s ON true
          WHERE b.type_specific = 'Burst'
            AND b.properties->>'Fate' = 'MISS'
        ),
        targets_in_cone AS (
          SELECT
            ls.burst_id,
            t.id as target_id,
            t.name as target_name,
            t.type_basic as target_type,
            SQRT(POW(ls.u - ts.u, 2) + POW(ls.v - ts.v, 2)) as distance_2d,
            ATAN2(ts.v - ls.v, ts.u - ls.u) * 180 / PI() as bearing,
            ABS(ATAN2(ts.v - ls.v, ts.u - ls.u) * 180 / PI() - ls.heading) as angle_off,
            ROW_NUMBER() OVER (
              PARTITION BY ls.burst_id
              ORDER BY SQRT(POW(ls.u - ts.u, 2) + POW(ls.v - ts.v, 2))
            ) as rn
          FROM launcher_state_at_fire ls
          CROSS JOIN objects t
          JOIN LATERAL (
            SELECT u, v
            FROM states
            WHERE object_id = t.id
              AND timestamp BETWEEN ls.fire_time - 0.5 AND ls.fire_time + 0.5
            ORDER BY ABS(timestamp - ls.fire_time)
            LIMIT 1
          ) ts ON true
          WHERE t.type_class IN ('Air', 'Sea', 'Ground')
            AND t.id != ls.launcher_id
            AND SQRT(POW(ls.u - ts.u, 2) + POW(ls.v - ts.v, 2)) <= ?
            AND ABS(ATAN2(ts.v - ls.v, ts.u - ls.u) * 180 / PI() - ls.heading) <= ?
        )
        SELECT
          burst_id,
          ARRAY_AGG(target_id ORDER BY distance_2d) as likely_targets,
          ARRAY_AGG(target_name ORDER BY distance_2d) as target_names,
          ARRAY_AGG(distance_2d ORDER BY distance_2d) as distances
        FROM targets_in_cone
        WHERE rn <= 5
        GROUP BY burst_id
        """

        missed_bursts = conn.execute(
            missed_query,
            [self.missed_max_distance, self.missed_cone_angle]
        ).fetchall()

        if not missed_bursts:
            return 0

        # Update missed bursts with likely targets
        updates = []
        for burst_id, likely_targets, target_names, distances in missed_bursts:
            properties_update = {
                "LikelyTargets": likely_targets,
                "LikelyTargetNames": target_names,
                "LikelyTargetDistances": distances
            }
            updates.append((json.dumps(properties_update), burst_id))

        if updates:
            conn.executemany(
                """
                UPDATE objects
                SET properties = json_merge_patch(COALESCE(properties, '{}'), ?)
                WHERE id = ?
                """,
                updates
            )

        return len(updates)

    def _detect_intended_targets(self, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Detect intended targets for all bursts using 3D cone tracking.
        
        Analyzes the entire burst firing period, tracking which targets stayed in the
        launcher's 3D cone (azimuth + pitch) the longest. This identifies the most
        likely intended target based on time-weighted visibility.
        
        Args:
            conn: DuckDB connection
            
        Returns:
            Number of bursts enriched with intended target data
        """
        # Build the comprehensive SQL query
        intended_query = f"""
        WITH burst_firing_periods AS (
          -- Get MISSED bursts from AIR launchers targeting AIR targets
          -- If you hit something, that's the target - no need to guess intent
          SELECT
            b.id as burst_id,
            b.parent_id as launcher_id,
            b.first_seen,
            b.last_seen,
            l.coalition as launcher_coalition,
            l.name as launcher_name
          FROM objects b
          JOIN objects l ON b.parent_id = l.id
          WHERE b.type_specific = 'Burst'
            AND l.type_class = 'Air'  -- Only aircraft gun bursts (aggressors are aircraft)
            AND COALESCE(CAST(b.properties->>'HitCount' AS INT), 0) = 0  -- Missed bursts only
        ),
        launcher_states_during_burst AS (
          -- Get launcher states during each burst firing period
          SELECT
            bfp.burst_id,
            bfp.launcher_id,
            bfp.launcher_name,
            s.timestamp,
            s.longitude as launcher_lon,
            s.latitude as launcher_lat,
            s.altitude as launcher_alt,
            COALESCE(s.heading, 0) as launcher_heading,
            COALESCE(s.pitch, 0) as launcher_pitch
          FROM burst_firing_periods bfp
          JOIN states s ON s.object_id = bfp.launcher_id
          WHERE s.timestamp BETWEEN bfp.first_seen AND bfp.last_seen
            AND s.longitude IS NOT NULL
        ),
        potential_targets AS (
          -- Pre-filter AIR targets that were alive during each burst
          SELECT
            bfp.burst_id,
            bfp.launcher_id,
            t.id as target_id,
            t.name as target_name,
            t.type_basic as target_type,
            t.coalition as target_coalition,
            bfp.first_seen,
            bfp.last_seen
          FROM burst_firing_periods bfp
          CROSS JOIN objects t
          WHERE t.type_class = 'Air'  -- Only air targets for gun engagements
            AND t.id != bfp.launcher_id
            AND t.first_seen <= bfp.last_seen
            AND (t.removed_at IS NULL OR t.removed_at >= bfp.first_seen)
        ),
        -- Use LATERAL to get closest target state for each launcher state
        launcher_target_observations AS (
          SELECT
            ls.burst_id,
            ls.launcher_id,
            ls.launcher_name,
            ls.timestamp,
            ls.launcher_lon,
            ls.launcher_lat,
            ls.launcher_alt,
            ls.launcher_heading,
            ls.launcher_pitch,
            pt.target_id,
            pt.target_name,
            pt.target_type,
            pt.target_coalition,
            ts.longitude as target_lon,
            ts.latitude as target_lat,
            ts.altitude as target_alt
          FROM launcher_states_during_burst ls
          JOIN potential_targets pt ON pt.burst_id = ls.burst_id
          JOIN LATERAL (
            SELECT longitude, latitude, altitude
            FROM states
            WHERE object_id = pt.target_id
              AND longitude IS NOT NULL
              AND timestamp BETWEEN ls.timestamp - 0.15 AND ls.timestamp + 0.15
            ORDER BY ABS(timestamp - ls.timestamp)
            LIMIT 1
          ) ts ON true
        ),
        cone_analysis AS (
          -- Calculate distances and angles
          SELECT
            burst_id,
            target_id,
            target_name,
            target_type,
            target_coalition,
            -- 3D distance
            SQRT(
              calculate_approximate_distance_squared(
                launcher_lat - target_lat,
                launcher_lon - target_lon
              ) +
              POW(target_alt - launcher_alt, 2)
            ) as distance_3d,
            -- Bearing from launcher to target
            DEGREES(ATAN2(
              target_lon - launcher_lon,
              target_lat - launcher_lat
            )) as bearing_to_target,
            launcher_heading,
            -- Elevation angle from launcher to target
            DEGREES(ATAN2(
              target_alt - launcher_alt,
              GREATEST(SQRT(calculate_approximate_distance_squared(
                launcher_lat - target_lat,
                launcher_lon - target_lon
              )), 0.1)  -- Avoid division by zero
            )) as elevation_to_target,
            launcher_pitch
          FROM launcher_target_observations
        ),
        cone_filtered AS (
          -- Filter by 3D cone constraints BEFORE aggregation
          SELECT
            burst_id,
            target_id,
            target_name,
            target_type,
            target_coalition,
            distance_3d
          FROM cone_analysis
          WHERE
            distance_3d <= ?  -- intended_max_distance
            AND 
            -- Azimuth cone check (handle 360° wraparound)
            CASE
              WHEN ABS(bearing_to_target - launcher_heading) <= 180
                THEN ABS(bearing_to_target - launcher_heading)
              ELSE 360 - ABS(bearing_to_target - launcher_heading)
            END <= ?  -- intended_cone_azimuth
            AND ABS(elevation_to_target - launcher_pitch) <= ?  -- intended_cone_pitch
        ),
        targets_in_cone AS (
          -- Aggregate: count states and calculate average distance
          SELECT
            burst_id,
            target_id,
            target_name,
            target_type,
            target_coalition,
            COUNT(*) as states_in_cone,
            AVG(distance_3d) as avg_distance,
            MIN(distance_3d) as min_distance
          FROM cone_filtered
          GROUP BY burst_id, target_id, target_name, target_type, target_coalition
        ),
        ranked_targets AS (
          -- Rank targets by time in cone (most states = most likely intended)
          SELECT
            burst_id,
            target_id,
            target_name,
            target_type,
            target_coalition,
            states_in_cone,
            avg_distance,
            min_distance,
            ROW_NUMBER() OVER (
              PARTITION BY burst_id
              ORDER BY states_in_cone DESC, avg_distance ASC
            ) as rank
          FROM targets_in_cone
        )
        SELECT
          burst_id,
          ARRAY_AGG(target_id ORDER BY rank) as intended_target_ids,
          ARRAY_AGG(states_in_cone ORDER BY rank) as time_in_cone,
          ARRAY_AGG(avg_distance ORDER BY rank) as avg_distances,
          ARRAY_AGG(min_distance ORDER BY rank) as min_distances
        FROM ranked_targets
        WHERE rank <= 3  -- Top 3 most likely intended targets
        GROUP BY burst_id
        """

        # Execute query with parameters
        results = conn.execute(
            intended_query,
            [
                self.intended_max_distance,
                self.intended_cone_azimuth,
                self.intended_cone_pitch
            ]
        ).fetchall()

        if not results:
            return 0

        # Update bursts with intended target data
        updates = []
        tactical_event_updates = []
        for row in results:
            (burst_id, target_ids, time_in_cone, avg_distances, min_distances) = row

            properties_update = {
                "IntendedTargetIDs": target_ids,
                "IntendedTargetTimeInCone": time_in_cone,
                "IntendedTargetAvgDistance": [round(d, 1) for d in avg_distances],
                "IntendedTargetMinDistance": [round(d, 1) for d in min_distances]
            }
            updates.append((json.dumps(properties_update), burst_id))
            
            # Prepare tactical event update data
            # Use first intended target as the primary target_id
            if target_ids and len(target_ids) > 0:
                primary_target_id = target_ids[0]
                intended_metadata = {
                    "intended_target_ids": target_ids,
                    "intended_target_time_in_cone": time_in_cone,
                    "intended_target_avg_distance": [round(d, 1) for d in avg_distances],
                    "intended_target_min_distance": [round(d, 1) for d in min_distances]
                }
                tactical_event_updates.append((
                    primary_target_id,
                    json.dumps(intended_metadata),
                    burst_id
                ))

        if updates:
            conn.executemany(
                """
                UPDATE objects
                SET properties = json_merge_patch(COALESCE(properties, '{}'), ?)
                WHERE id = ?
                """,
                updates
            )
        
        # Update WEAPON_MISS tactical_events with intended target information
        if tactical_event_updates:
            # Prepare data for bulk update
            burst_ids = [te[2] for te in tactical_event_updates]
            target_ids_list = [te[0] for te in tactical_event_updates]
            metadata_list = [te[1] for te in tactical_event_updates]
            
            # Bulk update WEAPON_MISS events with intended target information
            conn.execute(
                """
                WITH update_data AS (
                    SELECT 
                        UNNEST(?) as burst_id,
                        UNNEST(?) as primary_target_id,
                        UNNEST(?) as intended_metadata_json
                )
                UPDATE tactical_events te
                SET 
                    target_id = ud.primary_target_id,
                    target_type = t.type_class,
                    target_coalition = t.coalition,
                    metadata = json_merge_patch(
                        COALESCE(te.metadata, '{}'::JSON),
                        ud.intended_metadata_json::JSON
                    )
                FROM update_data ud
                JOIN objects t ON t.id = ud.primary_target_id
                WHERE te.event_type = 'WEAPON_MISS'
                  AND te.initiator_id = ud.burst_id
                """,
                [burst_ids, target_ids_list, metadata_list]
            )

        return len(updates)
