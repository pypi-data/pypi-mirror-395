"""Weapon enrichment logic."""

import json
from typing import Optional
import duckdb

from .pipeline import Enricher


class WeaponEnricher(Enricher):
    """
    Enriches weapon objects with launcher/target information.
    
    Matches weapons to:
    - Launchers (parent_id): Platform that fired the weapon (first position)
    - Targets (properties.TargetIDs): Objects the weapon hit/approached (last position, array)
    """
    
    def __init__(
        self,
        time_window: float = 0.5,
        proximity_radius: float = 100.0,
        static_radius: float = 500.0,
        find_launchers: bool = True,
        find_targets: bool = True,
        batch_size: int = 200
    ):
        """
        Initialize weapon enricher.
        
        Args:
            time_window: Time window around weapon event (default: 0.5s, narrowed to ±0.2s for dynamic matching)
            proximity_radius: Distance for moving platforms (default: 100m)
            static_radius: Distance for static platforms (default: 500m)
            find_launchers: Enrich with launcher data (default: True)
            find_targets: Enrich with target data (default: True)
            batch_size: Objects per batch for chunked processing (default: 200)
        """
        self.time_window = time_window
        self.proximity_radius = proximity_radius
        self.static_radius = static_radius
        self.find_launchers = find_launchers
        self.find_targets = find_targets
        self.batch_size = batch_size
    
    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run weapon enrichment with object count-based batching.
        
        Two-stage approach:
        1. Stage 1 (Dynamic): Process ALL unmatched weapons with ±0.2s window
        2. Stage 2 (Static): Process remaining unmatched weapons with last-state matching
        
        Uses LIMIT without OFFSET - the filter automatically excludes already-enriched weapons,
        so each iteration naturally processes the next batch.
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of weapons enriched
        """
        total_enriched = 0
        
        # LAUNCHERS
        if self.find_launchers:
            # Stage 1: Dynamic matching (±0.2s window)
            while True:
                # print("Dynamic matching ", total_enriched)
                count = self._enrich_batched(
                    conn,
                    limit=self.batch_size,
                    use_last_position=False,
                    use_dynamic=True
                )
                if count == 0:
                    break
                total_enriched += count
            
            # Stage 2: Static matching (last state before weapon spawn)
            # Use smaller batch size to avoid OOM from large pair explosion
            static_batch_size = round(self.batch_size / 3)
            while True:
                # print("Static matching ", total_enriched)
                count = self._enrich_batched(
                    conn,
                    limit=static_batch_size,
                    use_last_position=False,
                    use_dynamic=False
                )
                if count == 0:
                    break
                total_enriched += count
        
        # TARGETS
        if self.find_targets:
            # Stage 1: Dynamic matching (±0.2s window)
            while True:
                count = self._enrich_batched(
                    conn,
                    limit=self.batch_size,
                    use_last_position=True,
                    use_dynamic=True
                )
                if count == 0:
                    break
                total_enriched += count
            
            # Stage 2: Static matching (last state before impact)
            # Use smaller batch size to avoid OOM from large pair explosion
            static_batch_size = round(self.batch_size / 4)
            while True:
                count = self._enrich_batched(
                    conn,
                    limit=static_batch_size,
                    use_last_position=True,
                    use_dynamic=False
                )
                if count == 0:
                    break
                total_enriched += count
        
        return total_enriched
    
    def _enrich_batched(
        self,
        conn: duckdb.DuckDBPyConnection,
        limit: int,
        use_last_position: bool = False,
        use_dynamic: bool = True
    ) -> int:
        """
        Batched enrichment using either dynamic or static matching.
        
        Args:
            conn: DuckDB connection
            limit: Batch size (LIMIT clause)
            use_last_position: If True, match at impact (target). If False, match at launch (launcher)
            use_dynamic: If True, use ±0.2s window matching. If False, use last-state matching.
            
        Returns:
            Number of weapons enriched in this batch
        """
        # Choose matching strategy
        if use_dynamic:
            matches = self._match_weapons_dynamic(
                conn, limit, use_last_position, self.proximity_radius
            )
        else:
            # Static matching uses different radius for launchers vs targets
            radius = self.static_radius if not use_last_position else self.proximity_radius * 1.5
            matches = self._match_weapons_static(
                conn, limit, use_last_position, radius
            )
        
        if not matches:
            return 0
        
        # Bulk update parent_id for launchers only
        if not use_last_position:
            weapon_launcher_pairs = [(platform_id, weapon_id) 
                                     for weapon_id, _, _, _, platform_id, *_ in matches]
            
            if weapon_launcher_pairs:
                conn.executemany(
                    "UPDATE objects SET parent_id = ? WHERE id = ?",
                    weapon_launcher_pairs
                )
                
                # Insert WEAPON_LAUNCH events into tactical_events
                self._insert_weapon_launch_events(conn, matches)
        
        # Insert WEAPON_HIT/WEAPON_MISS events into tactical_events
        if use_last_position:
            self._insert_weapon_impact_events(conn, matches)
        
        return len(matches)
    
    def _match_weapons_dynamic(
        self,
        conn: duckdb.DuckDBPyConnection,
        limit: int,
        use_last_position: bool,
        proximity_radius: float
    ) -> list:
        """
        Stage 1: Match weapons to platforms with recent states (±0.2s window).
        Uses LATERAL join to get only one state per platform candidate.
        Memory-efficient: doesn't load all states into CTEs.
        """
        order_direction = "DESC" if use_last_position else "ASC"
        event_name = "impact_time" if use_last_position else "launch_time"
        already_enriched_filter = "AND w.id NOT IN (SELECT initiator_id FROM tactical_events WHERE event_type IN ('WEAPON_HIT', 'WEAPON_MISS', 'WEAPON_DESTROYED'))" if use_last_position else "AND w.parent_id IS NULL"
        
        if use_last_position:
            platform_exclusion_filter = ""
            # For pairs CTE: use raw column names (p.type_class, w.type_basic)
            target_type_filter_pairs = "(w.weapon_type_basic = 'Missile') OR (p.type_class IN ('Air', 'Sea', 'Ground'))"
            # Allow matching targets removed up to 1 second BEFORE weapon impact
            # (ground targets often removed slightly before the weapon)
            target_time_tolerance = 1.0
        else:
            platform_exclusion_filter = "AND p.type_class IN ('Air', 'Sea', 'Ground')"
            target_type_filter_pairs = "TRUE"
            target_time_tolerance = 1.0
        
        proximity_radius_sq = proximity_radius * proximity_radius
        
        query = f"""
        WITH weapon_batch AS (
            SELECT id
            FROM objects w
            WHERE (w.type_class = 'Weapon' 
                   OR w.type_basic IN ('Missile', 'Rocket', 'Bomb', 'Torpedo', 'Beam'))
              AND w.coalition IS NOT NULL
              {already_enriched_filter}
            ORDER BY w.first_seen
            LIMIT ?
        ),
        weapon_state AS (
            SELECT 
                w.id as weapon_id,
                w.type_basic as weapon_type_basic,
                s.timestamp as {event_name},
                s.u as weapon_u,
                s.v as weapon_v,
                s.altitude as weapon_alt,
                s.id as weapon_state_id,
                ROW_NUMBER() OVER (PARTITION BY w.id ORDER BY s.timestamp {order_direction}) as rn
            FROM weapon_batch wb
            JOIN objects w ON w.id = wb.id
            JOIN states s ON w.id = s.object_id
            WHERE s.u IS NOT NULL AND s.v IS NOT NULL
        ),
        weapon_first AS (
            SELECT * FROM weapon_state WHERE rn = 1
        ),
        weapon_platform_pairs AS (
            SELECT
                w.weapon_id,
                w.weapon_type_basic,
                w.{event_name},
                w.weapon_u,
                w.weapon_v,
                w.weapon_alt,
                w.weapon_state_id,
                p.id as platform_id,
                p.name as platform_name,
                p.type_class as platform_type_class,
                p.type_class || '+' || COALESCE(p.type_basic, '') as platform_type,
                p.type_basic as platform_type_basic,
                p.pilot as platform_pilot,
                p.coalition as platform_coalition,
                w.weapon_alt - 100 as min_alt,
                w.weapon_alt + 100 as max_alt
            FROM weapon_first w
            JOIN objects p ON p.id != w.weapon_id
                AND p.coalition IS NOT NULL
                AND p.first_seen <= w.{event_name}
                AND (p.removed_at IS NULL OR p.removed_at >= w.{event_name} - {target_time_tolerance})
                AND ({target_type_filter_pairs})
                {platform_exclusion_filter}
        ),
        platform_closest_state AS (
            SELECT
                wpp.weapon_id,
                wpp.weapon_type_basic,
                wpp.{event_name},
                wpp.weapon_u,
                wpp.weapon_v,
                wpp.weapon_alt,
                wpp.weapon_state_id,
                wpp.platform_id,
                wpp.platform_name,
                wpp.platform_type,
                wpp.platform_type_class,
                wpp.platform_type_basic,
                wpp.platform_pilot,
                wpp.platform_coalition,
                ps.u as platform_u,
                ps.v as platform_v,
                ps.altitude as platform_alt,
                ps.id as platform_state_id
            FROM weapon_platform_pairs wpp
            JOIN LATERAL (
                SELECT u, v, altitude, id
                FROM states
                WHERE object_id = wpp.platform_id
                  AND u IS NOT NULL
                  AND altitude BETWEEN wpp.min_alt AND wpp.max_alt
                  AND timestamp BETWEEN wpp.{event_name} - 0.2 AND wpp.{event_name} + 0.2
                ORDER BY ABS(timestamp - wpp.{event_name})
                LIMIT 1
            ) ps ON true
        ),
        closest_match AS (
            SELECT
                weapon_id,
                weapon_state_id,
                weapon_type_basic,
                {event_name},
                platform_id,
                platform_name,
                platform_type,
                platform_type_class,
                platform_type_basic,
                platform_pilot,
                platform_coalition,
                platform_state_id,
                POWER(weapon_u - platform_u, 2) + 
                POWER(weapon_v - platform_v, 2) + 
                POWER(weapon_alt - platform_alt, 2) as distance_sq,
                ROW_NUMBER() OVER (
                    PARTITION BY weapon_id
                    ORDER BY 
                        POWER(weapon_u - platform_u, 2) + 
                        POWER(weapon_v - platform_v, 2) + 
                        POWER(weapon_alt - platform_alt, 2)
                ) as rn
            FROM platform_closest_state
            WHERE POWER(weapon_u - platform_u, 2) + 
                  POWER(weapon_v - platform_v, 2) + 
                  POWER(weapon_alt - platform_alt, 2) <= ?
        )
        SELECT 
            weapon_id, weapon_state_id, weapon_type_basic, {event_name},
            platform_id, platform_name, platform_type, platform_type_basic,
            platform_pilot, platform_coalition, platform_state_id, 
            SQRT(distance_sq) as distance_meters
        FROM closest_match
        WHERE rn = 1
        """
        
        return conn.execute(query, [limit, proximity_radius_sq]).fetchall()

    def _match_weapons_static(
        self,
        conn: duckdb.DuckDBPyConnection,
        limit: int,
        use_last_position: bool,
        static_radius: float
    ) -> list:
        """
        Stage 2: Match weapons to platforms using last state before weapon spawn.
        Uses LATERAL join to get only one state per platform candidate.
        Memory-efficient: doesn't load all states into CTEs.
        """
        order_direction = "DESC" if use_last_position else "ASC"
        event_name = "impact_time" if use_last_position else "launch_time"
        # Only process weapons not already matched
        already_enriched_filter = "AND w.id NOT IN (SELECT initiator_id FROM tactical_events WHERE event_type IN ('WEAPON_HIT', 'WEAPON_MISS', 'WEAPON_DESTROYED'))" if use_last_position else "AND w.parent_id IS NULL"
        
        if use_last_position:
            platform_exclusion_filter = ""
            # For pairs CTE: use raw column names (p.type_class, w.type_basic)
            target_type_filter_pairs = "(w.weapon_type_basic = 'Missile') OR (p.type_class IN ('Air', 'Sea', 'Ground'))"
            # Allow targets removed up to 1 second BEFORE weapon impact
            # (ground targets often removed slightly before the weapon)
            # No upper limit: targets can be removed any time after (or still alive)
            target_time_tolerance = 1.0
        else:
            platform_exclusion_filter = "AND p.type_class IN ('Air', 'Sea', 'Ground')"
            target_type_filter_pairs = "TRUE"
            target_time_tolerance = 0.0
        
        static_radius_sq = static_radius * static_radius
        
        query = f"""
        WITH weapon_batch AS (
            SELECT id
            FROM objects w
            WHERE (w.type_class = 'Weapon' 
                   OR w.type_basic IN ('Missile', 'Rocket', 'Bomb', 'Torpedo', 'Beam'))
              AND w.coalition IS NOT NULL
              {already_enriched_filter}
            ORDER BY w.first_seen
            LIMIT ?
        ),
        weapon_state AS (
            SELECT 
                w.id as weapon_id,
                w.type_basic as weapon_type_basic,
                s.timestamp as {event_name},
                s.u as weapon_u,
                s.v as weapon_v,
                s.altitude as weapon_alt,
                s.id as weapon_state_id,
                ROW_NUMBER() OVER (PARTITION BY w.id ORDER BY s.timestamp {order_direction}) as rn
            FROM weapon_batch wb
            JOIN objects w ON w.id = wb.id
            JOIN states s ON w.id = s.object_id
            WHERE s.u IS NOT NULL AND s.v IS NOT NULL
        ),
        weapon_first AS (
            SELECT * FROM weapon_state WHERE rn = 1
        ),
        weapon_platform_pairs AS (
            SELECT
                w.weapon_id,
                w.weapon_type_basic,
                w.{event_name},
                w.weapon_u,
                w.weapon_v,
                w.weapon_alt,
                w.weapon_state_id,
                p.id as platform_id,
                p.name as platform_name,
                p.type_class as platform_type_class,
                p.type_class || '+' || COALESCE(p.type_basic, '') as platform_type,
                p.type_basic as platform_type_basic,
                p.pilot as platform_pilot,
                p.coalition as platform_coalition,
                w.weapon_alt - 100 as min_alt,
                w.weapon_alt + 100 as max_alt
            FROM weapon_first w
            JOIN objects p ON p.id != w.weapon_id
                AND p.coalition IS NOT NULL
                AND p.first_seen <= w.{event_name}
                AND (p.removed_at IS NULL OR p.removed_at >= w.{event_name} - {target_time_tolerance})
                AND ({target_type_filter_pairs})
                {platform_exclusion_filter}
        ),
        platform_last_state AS (
            SELECT
                wpp.weapon_id,
                wpp.weapon_type_basic,
                wpp.{event_name},
                wpp.weapon_u,
                wpp.weapon_v,
                wpp.weapon_alt,
                wpp.weapon_state_id,
                wpp.platform_id,
                wpp.platform_name,
                wpp.platform_type,
                wpp.platform_type_class,
                wpp.platform_type_basic,
                wpp.platform_pilot,
                wpp.platform_coalition,
                ps.u as platform_u,
                ps.v as platform_v,
                ps.altitude as platform_alt,
                ps.id as platform_state_id
            FROM weapon_platform_pairs wpp
            JOIN LATERAL (
                SELECT u, v, altitude, id
                FROM states
                WHERE object_id = wpp.platform_id
                  AND u IS NOT NULL
                  AND altitude BETWEEN wpp.min_alt AND wpp.max_alt
                  AND timestamp <= wpp.{event_name} + 0.1
                ORDER BY timestamp DESC
                LIMIT 1
            ) ps ON true
        ),
        closest_match AS (
            SELECT
                weapon_id,
                weapon_state_id,
                weapon_type_basic,
                {event_name},
                platform_id,
                platform_name,
                platform_type,
                platform_type_class,
                platform_type_basic,
                platform_pilot,
                platform_coalition,
                platform_state_id,
                POWER(weapon_u - platform_u, 2) + 
                POWER(weapon_v - platform_v, 2) + 
                POWER(weapon_alt - platform_alt, 2) as distance_sq,
                ROW_NUMBER() OVER (
                    PARTITION BY weapon_id
                    ORDER BY 
                        POWER(weapon_u - platform_u, 2) + 
                        POWER(weapon_v - platform_v, 2) + 
                        POWER(weapon_alt - platform_alt, 2)
                ) as rn
            FROM platform_last_state
            WHERE POWER(weapon_u - platform_u, 2) + 
                  POWER(weapon_v - platform_v, 2) + 
                  POWER(weapon_alt - platform_alt, 2) <= ?
        )
        SELECT 
            weapon_id, weapon_state_id, weapon_type_basic, {event_name},
            platform_id, platform_name, platform_type, platform_type_basic,
            platform_pilot, platform_coalition, platform_state_id, 
            SQRT(distance_sq) as distance_meters
        FROM closest_match
        WHERE rn = 1
        """
        
        return conn.execute(query, [limit, static_radius_sq]).fetchall()
    
    def _insert_weapon_launch_events(self, conn: duckdb.DuckDBPyConnection, matches: list):
        """
        Insert WEAPON_LAUNCH events into tactical_events table.
        
        Args:
            conn: DuckDB connection
            matches: List of launcher matches from bulk query
                Format: (weapon_id, wpn_state_id, weapon_type_basic, event_time,
                        platform_id, platform_name, platform_type, platform_type_basic,
                        platform_pilot, platform_coalition, platform_state_id, distance_meters)
        """
        if not matches:
            return
        
        # Use SQL INSERT...SELECT for efficiency
        insert_query = """
        INSERT INTO tactical_events 
        (event_type, timestamp, initiator_id, target_id,
         initiator_type, target_type, initiator_coalition, target_coalition,
         longitude, latitude, altitude,
         initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
        SELECT 
            'WEAPON_LAUNCH',
            w.first_seen,
            l.id,                    -- initiator = launcher
            w.id,                    -- target = weapon
            l.type_class,            -- initiator_type
            w.type_basic,            -- target_type
            l.coalition,
            w.coalition,
            ws.longitude, ws.latitude, ws.altitude,
            ls.id,                   -- initiator_state_id = launcher state
            ws.id,                   -- target_state_id = weapon state
            NULL,                    -- initiator_parent_state_id
            '{}'::JSON
        FROM objects w
        JOIN objects l ON w.parent_id = l.id
        JOIN states ws ON ws.object_id = w.id AND ws.timestamp = w.first_seen
        JOIN LATERAL (
            SELECT id, longitude, latitude, altitude
            FROM states
            WHERE object_id = l.id AND timestamp <= w.first_seen
            ORDER BY timestamp DESC LIMIT 1
        ) ls ON true
        WHERE w.id IN (SELECT UNNEST(?))
          AND w.first_seen IS NOT NULL
        """
        
        # Extract weapon IDs from matches
        weapon_ids = [match[0] for match in matches]
        
        conn.execute(insert_query, [weapon_ids])
    
    def _insert_weapon_impact_events(self, conn: duckdb.DuckDBPyConnection, matches: list):
        """
        Insert WEAPON_HIT/WEAPON_MISS events into tactical_events table.
        
        NOTE: WEAPON_DECOYED events are handled by the missed_weapons enricher,
        which does sophisticated trajectory analysis to identify decoys and intended targets.
        
        Args:
            conn: DuckDB connection
            matches: List of target matches from bulk query
                Format: (weapon_id, wpn_state_id, weapon_type_basic, event_time,
                        platform_id, platform_name, platform_type, platform_type_basic,
                        platform_pilot, platform_coalition, platform_state_id, distance_meters)
        """
        # Filter out decoy hits - they'll be handled by missed_weapons enricher
        hit_events = []
        
        if matches:
            for match in matches:
                (weapon_id, wpn_state_id, weapon_type_basic, event_time,
                 platform_id, platform_name, platform_type, platform_type_basic,
                 platform_pilot, platform_coalition, platform_state_id, distance_meters) = match
                
                is_decoy = platform_type_basic == 'Decoy'
                
                if not is_decoy:
                    # WEAPON_HIT event (skip decoys)
                    hit_events.append((weapon_id, platform_id, wpn_state_id, platform_state_id, distance_meters))
        
        # Insert WEAPON_HIT events
        if hit_events:
            self._insert_hit_events(conn, hit_events)
        
        # Insert WEAPON_MISS events
        # The MISS query filters out weapons that already have HIT events
        # DECOYED weapons will be handled later by missed_weapons enricher
        self._insert_weapon_miss_events(conn)
    
    def _insert_hit_events(self, conn: duckdb.DuckDBPyConnection, hit_events: list):
        """Insert WEAPON_HIT events using SQL INSERT...SELECT."""
        # hit_events format: (weapon_id, target_id, weapon_state_id, target_state_id, distance)
        
        insert_query = """
        WITH hit_data AS (
            SELECT 
                UNNEST(?) as weapon_id,
                UNNEST(?) as target_id,
                UNNEST(?) as weapon_state_id,
                UNNEST(?) as target_state_id,
                UNNEST(?) as distance
        )
        INSERT INTO tactical_events 
        (event_type, timestamp, initiator_id, target_id,
         initiator_type, target_type, initiator_coalition, target_coalition,
         longitude, latitude, altitude,
         initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
        SELECT 
            CASE 
                WHEN t.type_class = 'Weapon' AND w.coalition != t.coalition THEN 'WEAPON_DESTROYED'
                ELSE 'WEAPON_HIT'
            END,
            w.last_seen,
            w.id,                    -- initiator = weapon
            h.target_id,            -- target = hit object
            w.type_basic,
            t.type_class,
            w.coalition,
            t.coalition,
            ws.longitude, ws.latitude, ws.altitude,
            h.weapon_state_id,       -- weapon state at impact
            h.target_state_id,       -- target state at impact
            ls.id,                   -- launcher state at impact
            ('{"hit_distance": ' || h.distance || ', "hit_type": "' || 
             CASE 
                WHEN w.coalition = t.coalition THEN 'FRIENDLY_FIRE'
                WHEN w.coalition != t.coalition THEN 'ENEMY'
                ELSE 'NEUTRAL'
             END || '"}')::JSON
        FROM hit_data h
        JOIN objects w ON w.id = h.weapon_id
        JOIN objects t ON t.id = h.target_id
        JOIN states ws ON ws.id = h.weapon_state_id
        JOIN LATERAL (
            SELECT id
            FROM states
            WHERE object_id = w.parent_id AND timestamp <= w.last_seen
            ORDER BY timestamp DESC LIMIT 1
        ) ls ON w.parent_id IS NOT NULL
        """
        
        # Unpack hit_events into separate lists
        weapon_ids = [h[0] for h in hit_events]
        target_ids = [h[1] for h in hit_events]
        weapon_state_ids = [h[2] for h in hit_events]
        target_state_ids = [h[3] for h in hit_events]
        distances = [h[4] for h in hit_events]
        
        conn.execute(insert_query, [weapon_ids, target_ids, weapon_state_ids, target_state_ids, distances])
    
    def _insert_weapon_miss_events(self, conn: duckdb.DuckDBPyConnection):
        """Insert WEAPON_MISS events for weapons that didn't hit anything."""
        insert_query = """
        INSERT INTO tactical_events 
        (event_type, timestamp, initiator_id, target_id,
         initiator_type, target_type, initiator_coalition, target_coalition,
         longitude, latitude, altitude,
         initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
        SELECT 
            'WEAPON_MISS',
            w.last_seen,
            w.id,                    -- initiator = weapon
            NULL,                    -- target = none (for now, intended target analysis is separate)
            w.type_basic,
            NULL,
            w.coalition,
            NULL,
            ws.longitude, ws.latitude, ws.altitude,
            ws.id,                   -- weapon state at end of flight
            NULL,                    -- no target state
            (SELECT id FROM states 
             WHERE object_id = w.parent_id AND timestamp <= w.last_seen
             ORDER BY timestamp DESC LIMIT 1),  -- launcher state at end of flight
            '{}'::JSON
        FROM objects w
        JOIN LATERAL (
            SELECT id, longitude, latitude, altitude
            FROM states
            WHERE object_id = w.id
            ORDER BY timestamp DESC LIMIT 1
        ) ws ON true
        WHERE (w.type_class = 'Weapon' 
               OR w.type_basic IN ('Missile', 'Rocket', 'Bomb', 'Torpedo', 'Beam'))
          AND w.coalition IS NOT NULL
          AND w.last_seen IS NOT NULL
          AND w.id NOT IN (
              SELECT initiator_id FROM tactical_events 
              WHERE event_type IN ('WEAPON_HIT')
          )
        """
        
        conn.execute(insert_query)
