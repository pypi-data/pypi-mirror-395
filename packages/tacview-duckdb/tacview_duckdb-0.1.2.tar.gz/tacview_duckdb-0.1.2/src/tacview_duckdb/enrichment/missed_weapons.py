"""Missed weapon proximity analysis."""

import json
from typing import Optional
import duckdb

from .pipeline import Enricher


def _insert_single_decoyed_or_miss_event(conn, event_type, weapon_id, weapon_time, weapon_state_id, 
                                         target_state_id, final_target_id, proximity_target_id, distance_meters):
    """Helper to insert a single WEAPON_DECOYED or WEAPON_MISS event."""
    # Get weapon info
    weapon_info = conn.execute("""
        SELECT w.type_basic, w.coalition, w.parent_id,
               ws.longitude, ws.latitude, ws.altitude
        FROM objects w
        JOIN states ws ON ws.id = ?
        WHERE w.id = ?
    """, [weapon_state_id, weapon_id]).fetchone()
    
    if not weapon_info:
        return
    
    weapon_type, weapon_coalition, parent_id, lon, lat, alt = weapon_info
    
    # Get target info
    target_type, target_coalition = None, None
    if final_target_id:
        target_info = conn.execute(
            "SELECT type_class, coalition FROM objects WHERE id = ?",
            [final_target_id]
        ).fetchone()
        if target_info:
            target_type, target_coalition = target_info
    
    # Get launcher state
    launcher_state_id = None
    if parent_id:
        launcher_result = conn.execute("""
            SELECT id FROM states
            WHERE object_id = ? AND timestamp <= ?
            ORDER BY timestamp DESC LIMIT 1
        """, [parent_id, weapon_time]).fetchone()
        if launcher_result:
            launcher_state_id = launcher_result[0]
    
    # Build metadata
    metadata = {"proximity_distance": distance_meters}
    if event_type == 'WEAPON_DECOYED':
        metadata["decoy_id"] = proximity_target_id
        # Get decoy type_specific (e.g., "Flare", "Chaff")
        decoy_info = conn.execute(
            "SELECT type_specific FROM objects WHERE id = ?",
            [proximity_target_id]
        ).fetchone()
        if decoy_info and decoy_info[0]:
            metadata["decoy_type"] = decoy_info[0]
    
    conn.execute("""
        INSERT INTO tactical_events 
        (event_type, timestamp, initiator_id, target_id,
         initiator_type, target_type, initiator_coalition, target_coalition,
         longitude, latitude, altitude,
         initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?::JSON)
    """, [
        event_type, weapon_time, weapon_id, final_target_id,
        weapon_type, target_type, weapon_coalition, target_coalition,
        lon, lat, alt,
        weapon_state_id, target_state_id, launcher_state_id,
        json.dumps(metadata)
    ])


class MissedWeaponAnalyzer(Enricher):
    """
    Analyzes missed weapons to detect if they were decoyed or passed near targets.
    
    For weapons marked as MISS, this searches the ENTIRE trajectory from launch to impact
    to find the closest object the weapon passed near, classifying as:
    - DECOYED: Weapon was lured away by a decoy
    - NEAR_MISS: Weapon passed close to a potential target
    
    The analyzer uses a two-pass approach:
    1. Coarse pass: Samples trajectory points (excluding launch position), uses 2D distance
       for fast filtering with adaptive search radius = distance_to_next_sample / 2
    2. Refinement pass: Uses full 3D distance for accurate closest approach calculation
    
    For each sample at time T, searches for target states within T±time_window.
    """

    def __init__(
        self,
        lookback_duration: float = 5.0,
        proximity_radius: float = 200.0,
        sample_count: int = None,
        refine_matches: bool = True,
        time_window: float = 0.75,
        max_proximity_radius: float = 2000.0,
        target_interval: float = 2.5,
        # Kinematic defeat detection parameters
        detect_kinematic_defeats: bool = True,
        defeat_analysis_window: float = 2.0,
        min_opening_closure: float = -30.0,
        peak_opening_closure: float = -50.0,
        max_pointing_error: float = 20.0,
        min_high_g_states: int = 3,
        min_high_g_threshold: float = 10.0,
        max_g_variance: float = 2.5,
        min_effective_speed: float = 150.0,
        min_speed_loss: float = 100.0,
        batch_size: int = 100,  # Spatial-temporal scan allows larger batches
        # Proximity kill detection parameters
        detect_proximity_kills: bool = True,
        proximity_kill_threshold: float = 25.0,
        proximity_kill_time_window: float = 1.0
    ):
        """
        Initialize missed weapon analyzer.
        
        Args:
            lookback_duration: DEPRECATED - No longer used. Kept for backward compatibility.
            proximity_radius: Detection radius in meters (default: 200.0m)
            sample_count: Number of trajectory samples (default: None = use target_interval)
                         If specified, overrides target_interval calculation.
                         Fixed count mode is useful for testing/benchmarking.
            refine_matches: Enable dense refinement pass (default: True)
            time_window: ±seconds to search for nearby target states (default: 0.75s)
            max_proximity_radius: Maximum search radius in meters (default: 2000.0m)
                                 Caps the adaptive radius calculation. Higher values allow
                                 fewer samples for long-range missiles. For 300s flight at 500m/s:
                                 - 1000m: Needs 75 samples for full coverage
                                 - 2000m: Needs 37 samples for full coverage
                                 - 3000m: Needs 25 samples for full coverage
            target_interval: Target time between samples in seconds (default: 2.5s)
                            Automatically scales sample count with flight duration:
                            - 10s flight: 4 samples
                            - 80s flight: 32 samples
                            - 300s flight: 120 samples
                            Only used if sample_count is None.
            
            # Kinematic defeat detection parameters:
            detect_kinematic_defeats: Enable kinematic defeat detection (default: True)
            defeat_analysis_window: Time window around closest approach in seconds (default: 2.0s = ±2s)
            min_opening_closure: Avg closure rate threshold for maneuver defeat (default: -30 m/s)
            peak_opening_closure: Peak closure rate threshold for maneuver defeat (default: -50 m/s)
            max_pointing_error: Max off-boresight angle for maneuver defeat (default: 20°)
            min_high_g_states: Min consecutive high-G states for G-limit defeat (default: 3)
            min_high_g_threshold: G threshold for high-G detection (default: 10.0g)
            max_g_variance: Max stddev for sustained G (default: 2.5g)
            min_effective_speed: Min speed for effective intercept (default: 150 m/s)
            min_speed_loss: Min speed loss for energy defeat (default: 100 m/s)
            batch_size: Objects per batch for chunked processing (default: 100). Spatial-temporal scan allows larger batches with controlled memory usage.
            
            # Proximity kill detection parameters:
            detect_proximity_kills: Enable proximity kill detection (default: True)
            proximity_kill_threshold: Maximum miss distance for proximity kill (default: 25.0m)
            proximity_kill_time_window: Time window for removal matching (default: 1.0s)
        """
        self.lookback_duration = lookback_duration  # Kept for backward compatibility
        self.proximity_radius = proximity_radius
        self.sample_count = sample_count
        self.refine_matches = refine_matches
        self.time_window = time_window
        self.max_proximity_radius = max_proximity_radius
        self.target_interval = target_interval
        self.batch_size = batch_size

        # Kinematic defeat detection parameters
        self.detect_kinematic_defeats = detect_kinematic_defeats
        self.defeat_analysis_window = defeat_analysis_window
        self.min_opening_closure = min_opening_closure
        self.peak_opening_closure = peak_opening_closure
        self.max_pointing_error = max_pointing_error
        self.min_high_g_states = min_high_g_states
        self.min_high_g_threshold = min_high_g_threshold
        self.max_g_variance = max_g_variance
        self.min_effective_speed = min_effective_speed
        self.min_speed_loss = min_speed_loss

        # Proximity kill detection parameters
        self.detect_proximity_kills = detect_proximity_kills
        self.proximity_kill_threshold = proximity_kill_threshold
        self.proximity_kill_time_window = proximity_kill_time_window

    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run missed weapon proximity analysis and kinematic defeat detection with batching.
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of weapons enriched with proximity data
        """
        # Ensure spatial extension is loaded
        conn.execute("INSTALL spatial")
        conn.execute("LOAD spatial")

        total_enriched = 0

        # Stage 1: Missiles (batched, small batches due to trajectory sampling)
        loop_count = 0
        while True:
            # print(f"Loop {loop_count} - Analyzing missiles - {total_enriched} enriched")
            enriched = self._analyze_missiles(conn, self.batch_size)
            if enriched == 0:
                break
            total_enriched += enriched
            loop_count += 1

        # Stage 2: Bombs/Rockets (batched, larger batches - simpler queries)
        loop_count = 0
        while True:
            # print(f"Loop {loop_count} - Analyzing bombs/rockets - {total_enriched} enriched")
            enriched = self._analyze_bombs_rockets(conn, batch_size=100)
            if enriched == 0:
                break
            total_enriched += enriched
            loop_count += 1

        # Stage 3: Proximity kill detection (reclassify WEAPON_MISS as WEAPON_HIT when missile and target destroyed together)
        if self.detect_proximity_kills:
            self._detect_proximity_kills(conn)

        # Clean up any duplicate events (e.g., MISS at end-of-life + DECOYED from trajectory analysis)
        # Keep the earliest event (trajectory analysis is more accurate than end-of-life MISS)
        if total_enriched > 0:
            self._remove_duplicate_weapon_events(conn)

        # Stage 4: Kinematic defeats (processes NEAR_MISS events - no batching needed, very few events)
        if self.detect_kinematic_defeats and total_enriched > 0:
            # print(f"Detecting kinematic defeats (near miss)")
            self._detect_kinematic_defeats(conn)

        # Stage 5: Energy depletion defeats (missiles tracking but ran out of energy)
        if self.detect_kinematic_defeats and total_enriched > 0:
            while True:
                # print(f"Detecting energy depletion defeats")
                defeated = self._detect_energy_depletion_defeats(conn, batch_size=100)
                if defeated == 0:
                    break

        return total_enriched

    def _remove_duplicate_weapon_events(self, conn: duckdb.DuckDBPyConnection):
        """
        Remove duplicate weapon outcome events, keeping the earliest one.
        
        If a weapon has multiple outcome events (e.g., DECOYED from trajectory + MISS from end-of-life),
        keep the earliest event since that's the actual outcome.
        """
        conn.execute("""
            DELETE FROM tactical_events
            WHERE id IN (
                SELECT id
                FROM (
                    SELECT 
                        id,
                        ROW_NUMBER() OVER (
                            PARTITION BY initiator_id 
                            ORDER BY timestamp ASC
                        ) as rn
                    FROM tactical_events
                    WHERE event_type IN ('WEAPON_MISS', 'WEAPON_DECOYED')
                ) ranked
                WHERE rn > 1
            )
        """)

    def _analyze_missiles(self, conn: duckdb.DuckDBPyConnection, limit: int) -> int:
        """
        Batched missile analysis with spatial-temporal state scan.
        
        Uses spatial-temporal filtering instead of CROSS JOIN for memory efficiency:
        - Each missile gets 4-120 samples depending on flight duration
        - Each sample scans states in ±0.25s window with U/V/altitude cube filter
        - 100 missiles × 50 avg samples × ~30 nearby states = ~150K state checks per batch
        - No CROSS JOIN explosion, direct state lookup with spatial filtering
        
        Args:
            conn: DuckDB connection
            limit: Batch size (LIMIT clause, default: 100)
            
        Returns:
            Number of missiles enriched in this batch
        """
        max_proximity_radius = self.max_proximity_radius
        use_dynamic_sampling = self.sample_count is None

        # PASS 1: Coarse sampling with batching
        bulk_proximity_query_batched = """
        WITH weapon_batch AS (
            SELECT id
            FROM objects
            WHERE type_basic = 'Missile'
              AND first_seen IS NOT NULL
              AND last_seen IS NOT NULL
              AND EXISTS (
                  SELECT 1 FROM tactical_events 
                  WHERE event_type = 'WEAPON_MISS' 
                    AND initiator_id = objects.id
              )
              -- Skip if already analyzed (has proximity data or decoyed event)
              AND NOT EXISTS (
                  SELECT 1 FROM tactical_events 
                  WHERE initiator_id = objects.id
                    AND (event_type = 'WEAPON_DECOYED' 
                         OR (event_type = 'WEAPON_MISS' AND (metadata->>'proximity_distance') IS NOT NULL))
              )
              AND (last_seen - first_seen) >= 1.0
              AND (last_seen - first_seen) < 300.0
            ORDER BY first_seen
            LIMIT ?
        ),
        missed_weapons AS (
            SELECT 
                o.id as weapon_id,
                o.name as weapon_name,
                o.type_basic as weapon_type_basic,
                o.coalition as weapon_coalition,
                o.first_seen,
                o.last_seen,
                o.first_seen as search_start_time,
                CASE 
                    WHEN ? THEN GREATEST(4, CAST((o.last_seen - o.first_seen) / ? AS INTEGER))
                    ELSE ?
                END as weapon_sample_count
            FROM weapon_batch wb
            JOIN objects o ON o.id = wb.id
        ),
        weapon_all_states AS (
            SELECT 
                mw.weapon_id,
                mw.weapon_name,
                mw.weapon_type_basic,
                mw.weapon_coalition,
                mw.weapon_sample_count,
                s.timestamp,
                s.u,
                s.v,
                s.longitude,
                s.latitude,
                s.altitude,
                s.id as state_id,
                ROW_NUMBER() OVER (PARTITION BY mw.weapon_id ORDER BY s.timestamp ASC) as state_rank,
                COUNT(*) OVER (PARTITION BY mw.weapon_id) as total_states
            FROM missed_weapons mw
            JOIN states s ON s.object_id = mw.weapon_id
            WHERE s.timestamp BETWEEN mw.search_start_time AND mw.last_seen
              AND s.longitude IS NOT NULL
              AND s.latitude IS NOT NULL
              AND s.u IS NOT NULL
              AND s.v IS NOT NULL
        ),
        weapon_sampled_states AS (
            SELECT 
                weapon_id,
                weapon_name,
                weapon_type_basic,
                weapon_coalition,
                timestamp,
                u, v,
                longitude, latitude, altitude,
                state_id,
                state_rank,
                total_states,
                weapon_sample_count,
                LEAD(longitude) OVER (PARTITION BY weapon_id ORDER BY state_rank) as next_lon,
                LEAD(latitude) OVER (PARTITION BY weapon_id ORDER BY state_rank) as next_lat,
                LEAD(altitude) OVER (PARTITION BY weapon_id ORDER BY state_rank) as next_alt
            FROM weapon_all_states
            WHERE state_rank % GREATEST(1, CAST(total_states / weapon_sample_count AS INTEGER)) = 1
               OR state_rank = total_states
        ),
        samples_with_radius AS (
            SELECT 
                weapon_id,
                weapon_name,
                weapon_type_basic,
                weapon_coalition,
                timestamp,
                u, v,
                longitude, latitude, altitude,
                state_id,
                LEAST(
                    ?,
                    GREATEST(
                        ?,
                        COALESCE(
                            SQRT(calculate_approximate_distance_squared(
                                latitude - next_lat,
                                longitude - next_lon
                            )) / 2,
                            ?
                        )
                    )
                ) as search_radius,
                CASE WHEN LEAST(
                    ?,
                    GREATEST(
                        ?,
                        COALESCE(
                            SQRT(calculate_approximate_distance_squared(
                                latitude - next_lat,
                                longitude - next_lon
                            )) / 2,
                            ?
                        )
                    )
                ) <= ? THEN 1 ELSE 0 END as is_precise
            FROM weapon_sampled_states
        ),
        weapon_parents AS (
            SELECT 
                o.id as weapon_id,
                o.parent_id
            FROM weapon_batch wb
            JOIN objects o ON o.id = wb.id
            WHERE o.parent_id IS NOT NULL
        ),
        weapon_sample_target_states AS (
            -- PARTITION 0: Force parallel execution by splitting sample points across 2 threads
            (SELECT
                ws.weapon_id,
                ws.weapon_name,
                ws.weapon_type_basic,
                ws.weapon_coalition,
                ws.state_id as weapon_state_id,
                ws.timestamp as weapon_time,
                ws.u as weapon_u,
                ws.v as weapon_v,
                ws.longitude as weapon_lon,
                ws.latitude as weapon_lat,
                ws.altitude as weapon_alt,
                ws.search_radius,
                ws.is_precise,
                s.object_id as target_id,
                s.id as target_state_id,
                s.u as target_u,
                s.v as target_v,
                s.longitude as target_lon,
                s.latitude as target_lat,
                s.altitude as target_alt,
                -- Calculate squared distance (defer SQRT for performance)
                POWER(ws.u - s.u, 2) +
                POWER(ws.v - s.v, 2) +
                POWER(ws.altitude - s.altitude, 2) as distance_sq
            FROM samples_with_radius ws
            LEFT JOIN weapon_parents wp ON wp.weapon_id = ws.weapon_id
            JOIN states s ON 
                -- Temporal filter: ±0.25s window (REQUIRES INDEX on timestamp)
                s.timestamp BETWEEN ws.timestamp - 0.25 AND ws.timestamp + 0.25
                -- Spatial cube filter: U/V/altitude within search radius
                AND s.u BETWEEN ws.u - ws.search_radius AND ws.u + ws.search_radius
                AND s.v BETWEEN ws.v - ws.search_radius AND ws.v + ws.search_radius
                AND s.altitude BETWEEN ws.altitude - ws.search_radius AND ws.altitude + ws.search_radius
                -- Exclude own missile states
                AND s.object_id != ws.weapon_id
                -- Parent exclusion
                AND (wp.parent_id IS NULL OR s.object_id != wp.parent_id)
                -- Ensure U/V coordinates exist (missiles always have them)
                AND s.u IS NOT NULL
                AND s.v IS NOT NULL
            WHERE (ASCII(RIGHT(ws.weapon_id, 1)) % 2) = 0
              AND distance_sq <= POWER(ws.search_radius, 2))
            
            UNION ALL
            
            -- PARTITION 1
            (SELECT
                ws.weapon_id,
                ws.weapon_name,
                ws.weapon_type_basic,
                ws.weapon_coalition,
                ws.state_id as weapon_state_id,
                ws.timestamp as weapon_time,
                ws.u as weapon_u,
                ws.v as weapon_v,
                ws.longitude as weapon_lon,
                ws.latitude as weapon_lat,
                ws.altitude as weapon_alt,
                ws.search_radius,
                ws.is_precise,
                s.object_id as target_id,
                s.id as target_state_id,
                s.u as target_u,
                s.v as target_v,
                s.longitude as target_lon,
                s.latitude as target_lat,
                s.altitude as target_alt,
                POWER(ws.u - s.u, 2) +
                POWER(ws.v - s.v, 2) +
                POWER(ws.altitude - s.altitude, 2) as distance_sq
            FROM samples_with_radius ws
            LEFT JOIN weapon_parents wp ON wp.weapon_id = ws.weapon_id
            JOIN states s ON 
                s.timestamp BETWEEN ws.timestamp - 0.25 AND ws.timestamp + 0.25
                AND s.u BETWEEN ws.u - ws.search_radius AND ws.u + ws.search_radius
                AND s.v BETWEEN ws.v - ws.search_radius AND ws.v + ws.search_radius
                AND s.altitude BETWEEN ws.altitude - ws.search_radius AND ws.altitude + ws.search_radius
                AND s.object_id != ws.weapon_id
                AND (wp.parent_id IS NULL OR s.object_id != wp.parent_id)
                AND s.u IS NOT NULL
                AND s.v IS NOT NULL
            WHERE (ASCII(RIGHT(ws.weapon_id, 1)) % 2) = 1
              AND distance_sq <= POWER(ws.search_radius, 2))
        ),
        target_state_per_pair AS (
            SELECT
                wsts.weapon_id,
                wsts.weapon_name,
                wsts.weapon_type_basic,
                wsts.weapon_coalition,
                wsts.weapon_state_id,
                wsts.weapon_time,
                wsts.weapon_lon,
                wsts.weapon_lat,
                wsts.weapon_alt,
                wsts.search_radius,
                wsts.is_precise,
                wsts.target_id,
                o.name as target_name,
                o.type_class || '+' || COALESCE(o.type_basic, '') as target_type,
                o.type_basic as target_type_basic,
                o.coalition as target_coalition,
                wsts.target_state_id,
                wsts.target_lon,
                wsts.target_lat,
                wsts.target_alt,
                SQRT(wsts.distance_sq) as distance_meters
            FROM weapon_sample_target_states wsts
            JOIN objects o ON o.id = wsts.target_id
                -- Filter to valid target types
                AND o.coalition IS NOT NULL
                AND (o.type_class IN ('Air', 'Ground', 'Sea') OR o.type_basic = 'Decoy')
                AND NOT (o.type_class = 'Weapon'
                         OR o.type_basic IN ('Chaff', 'Flare', 'Missile', 'Rocket', 'Bomb', 'Torpedo', 'Projectile', 'Beam'))
        ),
        proximity_matches AS (
            SELECT 
                weapon_id,
                weapon_name,
                weapon_type_basic,
                weapon_coalition,
                weapon_state_id,
                weapon_time,
                target_id,
                target_name,
                target_type,
                target_type_basic,
                target_coalition,
                target_state_id,
                distance_meters,
                is_precise,
                ROW_NUMBER() OVER (
                    PARTITION BY weapon_id 
                    ORDER BY weapon_time DESC
                ) AS rank
            FROM target_state_per_pair
        )
        SELECT 
            weapon_id,
            weapon_name,
            weapon_type_basic,
            weapon_state_id,
            weapon_time,
            target_id,
            target_name,
            target_type,
            target_type_basic,
            target_coalition,
            target_state_id,
            distance_meters,
            is_precise
        FROM proximity_matches
        WHERE rank = 1
        ORDER BY weapon_id
        """

        # Execute PASS 1
        coarse_matches = conn.execute(
            bulk_proximity_query_batched,
            [
                limit,  # Batch size
                use_dynamic_sampling,
                self.target_interval,
                self.sample_count if self.sample_count is not None else 50,
                max_proximity_radius,
                self.proximity_radius,
                max_proximity_radius,
                max_proximity_radius,
                self.proximity_radius,
                max_proximity_radius,
                self.proximity_radius
            ]
        ).fetchall()

        if not coarse_matches:
            return 0

        # PASS 2: Refinement (same as original)
        refined_matches = []

        if self.refine_matches and coarse_matches:
            precise_matches = []
            weapons_to_refine = {}

            for match in coarse_matches:
                weapon_id = match[0]
                encounter_time = match[4]
                is_precise = match[12]

                if is_precise == 1:
                    precise_matches.append(match)
                else:
                    if weapon_id not in weapons_to_refine:
                        weapons_to_refine[weapon_id] = {
                            'weapon_name': match[1],
                            'weapon_type_basic': match[2],
                            'encounter_time': encounter_time,
                            'coarse_match': match
                        }
                    elif encounter_time < weapons_to_refine[weapon_id]['encounter_time']:
                        weapons_to_refine[weapon_id]['encounter_time'] = encounter_time

            # Refine each weapon
            refine_query = """
            WITH weapon_info AS (
                SELECT first_seen, last_seen, coalition, parent_id
                FROM objects
                WHERE id = ?
            ),
            weapon_dense_states AS (
                SELECT 
                    ? as weapon_id,
                    s.timestamp,
                    s.longitude, s.latitude, s.altitude,
                    s.id as state_id
                FROM states s, weapon_info wi
                WHERE s.object_id = ?
                  AND s.timestamp BETWEEN wi.first_seen AND wi.last_seen
                  AND s.longitude IS NOT NULL
                  AND s.latitude IS NOT NULL
            ),
            potential_targets AS (
                SELECT 
                    o.id as target_id,
                    o.name as target_name,
                    o.type_class || '+' || COALESCE(o.type_basic, '') as target_type,
                    o.type_basic as target_type_basic,
                    o.coalition as target_coalition,
                    o.first_seen,
                    o.removed_at
                FROM objects o, weapon_info wi
                WHERE o.coalition IS NOT NULL
                  AND NOT (o.type_class = 'Weapon' 
                           OR o.type_basic IN ('Missile', 'Rocket', 'Bomb', 'Torpedo', 'Projectile', 'Beam'))
                  AND (wi.parent_id IS NULL OR o.id != wi.parent_id)
            ),
            proximity_matches AS (
                SELECT 
                    ws.weapon_id,
                    ? as weapon_name,
                    ? as weapon_type_basic,
                    ws.state_id as weapon_state_id,
                    ws.timestamp as weapon_time,
                    pt.target_id,
                    pt.target_name,
                    pt.target_type,
                    pt.target_type_basic,
                    pt.target_coalition,
                    ts.id as target_state_id,
                    SQRT(
                        calculate_approximate_distance_squared(
                            ws.latitude - ts.latitude,
                            ws.longitude - ts.longitude
                        ) + 
                        POWER(ws.altitude - ts.altitude, 2)
                    ) AS distance_meters
                FROM weapon_dense_states ws
                CROSS JOIN potential_targets pt
                JOIN states ts ON ts.object_id = pt.target_id
                WHERE ts.timestamp BETWEEN ws.timestamp - ? AND ws.timestamp + ?
                  AND ts.longitude IS NOT NULL
                  AND ts.latitude IS NOT NULL
                  AND (
                      calculate_approximate_distance_squared(
                          ws.latitude - ts.latitude,
                          ws.longitude - ts.longitude
                      ) + 
                      POWER(ws.altitude - ts.altitude, 2)
                  ) <= (? * ?)
                  AND ws.timestamp >= pt.first_seen
                  AND (pt.removed_at IS NULL OR ws.timestamp <= pt.removed_at)
            )
            SELECT *
            FROM proximity_matches
            ORDER BY distance_meters
            LIMIT 1
            """

            for weapon_id, info in weapons_to_refine.items():
                refined_result = conn.execute(
                    refine_query,
                    [
                        weapon_id,
                        weapon_id,
                        weapon_id,
                        info['weapon_name'], info['weapon_type_basic'],
                        self.time_window,
                        self.time_window,
                        self.proximity_radius, self.proximity_radius
                    ]
                ).fetchone()

                if refined_result:
                    refined_matches.append(refined_result)

            refined_matches.extend(precise_matches)
        else:
            refined_matches = coarse_matches

        matches = refined_matches

        # Insert events
        if matches:
            for (weapon_id, weapon_name, weapon_type_basic, weapon_state_id, weapon_time,
                 target_id, target_name, target_type, target_type_basic, target_coalition,
                 target_state_id, distance_meters, *_) in matches:

                is_decoy = target_type_basic == 'Decoy'

                # Get intended target for decoys
                intended_target_id = None
                if is_decoy:
                    decoy_parent = conn.execute(
                        """SELECT parent_id FROM objects WHERE id = ?""",
                        [target_id]
                    ).fetchone()

                    if decoy_parent and decoy_parent[0]:
                        intended_target_id = decoy_parent[0]

                # Insert tactical event
                event_type = 'WEAPON_DECOYED' if is_decoy else 'WEAPON_MISS'
                _insert_single_decoyed_or_miss_event(
                    conn, event_type, weapon_id, weapon_time, weapon_state_id, target_state_id,
                    intended_target_id if is_decoy else target_id, target_id, distance_meters
                )

            return len(matches)

        return 0

    def _analyze_bombs_rockets(self, conn: duckdb.DuckDBPyConnection, batch_size: int) -> int:
        """
        Batched impact point analysis for ballistic weapons and unmatched missiles.
        
        Handles:
        - Bombs, Rockets, Torpedoes (ballistic weapons - check impact point)
        - Missiles with no proximity match yet (stationary targets, AGMs, long-duration missiles)
        
        Uses LATERAL JOIN to fetch last target state at/before impact time.
        
        Args:
            conn: DuckDB connection
            batch_size: Batch size (LIMIT clause, default: 100)
            
        Returns:
            Number of weapons enriched in this batch
        """
        # Batched query with last-state lookup
        impact_query_batched = """
        WITH weapon_batch AS (
            SELECT id
            FROM objects
            WHERE (
                type_basic IN ('Bomb', 'Rocket', 'Torpedo')
                OR (type_basic = 'Missile' 
                    AND EXISTS (
                        SELECT 1 FROM tactical_events 
                        WHERE event_type = 'WEAPON_MISS' AND initiator_id = objects.id
                    )
                    AND NOT EXISTS (
                        SELECT 1 FROM tactical_events 
                        WHERE initiator_id = objects.id
                          AND (event_type = 'WEAPON_DECOYED' 
                               OR (event_type = 'WEAPON_MISS' AND (metadata->>'proximity_distance') IS NOT NULL))
                    )
                )
            )
              AND first_seen IS NOT NULL
              AND last_seen IS NOT NULL
              AND EXISTS (
                  SELECT 1 FROM tactical_events 
                  WHERE event_type = 'WEAPON_MISS' AND initiator_id = objects.id
              )
              -- Skip if already analyzed
              AND NOT EXISTS (
                  SELECT 1 FROM tactical_events 
                  WHERE initiator_id = objects.id
                    AND (event_type = 'WEAPON_DECOYED' 
                         OR (event_type = 'WEAPON_MISS' AND (metadata->>'proximity_distance') IS NOT NULL))
              )
            ORDER BY last_seen
            LIMIT ?
        ),
        missed_ballistic AS (
            SELECT 
                o.id as weapon_id,
                o.name as weapon_name,
                o.type_basic as weapon_type_basic,
                o.coalition as weapon_coalition,
                o.last_seen as impact_time
            FROM weapon_batch wb
            JOIN objects o ON o.id = wb.id
        ),
        impact_states AS (
            SELECT 
                mb.weapon_id,
                mb.weapon_name,
                mb.weapon_type_basic,
                mb.weapon_coalition,
                mb.impact_time,
                s.id as state_id,
                s.u,
                s.v,
                s.longitude,
                s.latitude,
                s.altitude as weapon_alt
            FROM missed_ballistic mb
            JOIN states s ON s.object_id = mb.weapon_id
            WHERE s.timestamp = mb.impact_time
              AND s.longitude IS NOT NULL
              AND s.latitude IS NOT NULL
              AND s.u IS NOT NULL
              AND s.v IS NOT NULL
        ),
        weapon_impact_pairs AS (
            SELECT
                ws.weapon_id,
                ws.weapon_name,
                ws.weapon_type_basic,
                ws.impact_time,
                ws.state_id as weapon_state_id,
                ws.u as weapon_u,
                ws.v as weapon_v,
                ws.longitude as weapon_lon,
                ws.latitude as weapon_lat,
                ws.weapon_alt,
                pt.target_id
            FROM impact_states ws
            CROSS JOIN (
                SELECT id as target_id, first_seen, removed_at
                FROM objects
                WHERE coalition IS NOT NULL
                  AND type_class IN ('Air', 'Ground', 'Sea')
            ) pt
            WHERE ws.impact_time >= pt.first_seen
              AND (pt.removed_at IS NULL OR ws.impact_time <= pt.removed_at)
        ),
        weapon_impact_target_states AS (
            SELECT
                wip.weapon_id,
                wip.weapon_name,
                wip.weapon_type_basic,
                wip.impact_time,
                wip.weapon_state_id,
                wip.weapon_u,
                wip.weapon_v,
                wip.weapon_lon,
                wip.weapon_lat,
                wip.weapon_alt,
                wip.target_id,
                ts.target_state_id,
                ts.target_lon,
                ts.target_lat,
                ts.target_alt,
                -- Calculate squared distance (defer SQRT for performance)
                POWER(wip.weapon_u - ts.u, 2) +
                POWER(wip.weapon_v - ts.v, 2) +
                POWER(wip.weapon_alt - ts.target_alt, 2) as distance_sq
            FROM weapon_impact_pairs wip
            JOIN LATERAL (
                SELECT 
                    s.id as target_state_id,
                    s.u,
                    s.v,
                    s.longitude as target_lon,
                    s.latitude as target_lat,
                    s.altitude as target_alt
                FROM states s
                WHERE s.object_id = wip.target_id
                  AND s.timestamp <= wip.impact_time + 0.1
                ORDER BY s.timestamp DESC
                LIMIT 1
            ) ts ON ts.u IS NOT NULL
                AND ts.v IS NOT NULL
                AND ABS(ts.target_alt - wip.weapon_alt) <= 300
            WHERE distance_sq <= POWER(?, 2)  -- Search radius squared
        ),
        target_state_per_pair AS (
            SELECT
                wits.weapon_id,
                wits.weapon_name,
                wits.weapon_type_basic,
                wits.impact_time,
                wits.weapon_state_id,
                wits.weapon_lon,
                wits.weapon_lat,
                wits.weapon_alt,
                wits.target_id,
                o.name as target_name,
                o.type_class || '+' || COALESCE(o.type_basic, '') as target_type,
                o.type_basic as target_type_basic,
                wits.target_state_id,
                wits.target_lon,
                wits.target_lat,
                wits.target_alt,
                SQRT(wits.distance_sq) as distance_meters
            FROM weapon_impact_target_states wits
            JOIN objects o ON o.id = wits.target_id
                -- Filter to valid target types
                AND o.coalition IS NOT NULL
                AND o.type_class IN ('Air', 'Ground', 'Sea')
        ),
        proximity_matches AS (
            SELECT 
                weapon_id,
                weapon_name,
                weapon_type_basic,
                weapon_state_id,
                impact_time as weapon_time,
                target_id,
                target_name,
                target_type,
                target_type_basic,
                target_state_id,
                distance_meters,
                ROW_NUMBER() OVER (
                    PARTITION BY weapon_id 
                    ORDER BY distance_meters
                ) AS rank
            FROM target_state_per_pair
        )
        SELECT 
            weapon_id,
            weapon_name,
            weapon_type_basic,
            weapon_state_id,
            weapon_time,
            target_id,
            target_name,
            target_type,
            target_type_basic,
            target_state_id,
            distance_meters
        FROM proximity_matches
        WHERE rank = 1
        """

        # Execute batched query
        matches = conn.execute(
            impact_query_batched,
            [
                batch_size,  # weapon_batch LIMIT
                self.proximity_radius  # weapon_impact_target_states search radius
            ]
        ).fetchall()

        if not matches:
            return 0

        # Insert tactical events (for consistency with missiles and infinite loop protection)
        for (weapon_id, weapon_name, weapon_type_basic, weapon_state_id, weapon_time,
             target_id, target_name, target_type, target_type_basic,
             target_state_id, distance_meters) in matches:

            # Bombs/rockets/AGMs: insert WEAPON_MISS event with proximity data
            _insert_single_decoyed_or_miss_event(
                conn, 'WEAPON_MISS', weapon_id, weapon_time, weapon_state_id, target_state_id,
                target_id, target_id, distance_meters
            )

            # Also update object properties for backward compatibility
            existing_props = conn.execute(
                "SELECT properties FROM objects WHERE id = ?",
                [weapon_id]
            ).fetchone()

            if existing_props and existing_props[0]:
                props_dict = json.loads(existing_props[0])
            else:
                props_dict = {}

            proximity_data = {
                "Fate": "NEAR_MISS",
                "TargetIDs": [target_id],
                "ProximityDistance": distance_meters,
                "ProximityTime": weapon_time,
                "WeaponStateAtProximity": weapon_state_id,
                "TargetStateAtProximity": target_state_id
            }

            props_dict.update(proximity_data)

            conn.execute(
                "UPDATE objects SET properties = ? WHERE id = ?",
                [json.dumps(props_dict), weapon_id]
            )

        return len(matches)

    def _detect_kinematic_defeats(self, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Kinematic defeat detection - analyzes ALL NEAR_MISS events in one pass.
        Analyzes missile trajectory in a focused window: 5 seconds before and 2 seconds after near miss.
        
        Args:
            conn: DuckDB connection
            
        Returns:
            Number of WEAPON_MISS events upgraded to WEAPON_DEFEATED
        """
        defeat_query = """
        WITH defeat_candidates AS (
            SELECT 
                te.id as event_id,
                te.initiator_id as missile_id,
                te.target_id as target_id,
                te.timestamp as closest_approach_time,
                te.initiator_state_id as missile_state_id,
                te.target_state_id as target_state_id,
                (te.metadata->>'proximity_distance')::DOUBLE as miss_distance
            FROM tactical_events te
            WHERE te.event_type = 'WEAPON_MISS'
              AND te.initiator_type = 'Missile'
              AND (te.metadata->>'proximity_distance') IS NOT NULL  -- Has proximity data (NEAR_MISS)
              AND (te.metadata->>'miss_distance_meters') IS NULL     -- But not yet analyzed for defeat
        ),
        missile_trajectory AS (
            -- Fetch missile states in focused window: 5s before, 2s after near miss
            SELECT
                dc.event_id,
                dc.missile_id,
                dc.target_id,
                dc.closest_approach_time,
                s.id as state_id,
                s.timestamp,
                s.timestamp - dc.closest_approach_time as time_to_miss,
                s.speed,
                s.g_load,
                s.pitch,
                s.yaw,
                s.u, s.v, s.altitude,
                LAG(s.u) OVER w as prev_u,
                LAG(s.v) OVER w as prev_v,
                LAG(s.altitude) OVER w as prev_alt,
                LAG(s.timestamp) OVER w as prev_time,
                LAG(s.speed) OVER w as prev_speed
            FROM defeat_candidates dc
            JOIN states s ON s.object_id = dc.missile_id
            WHERE s.timestamp BETWEEN dc.closest_approach_time - ? AND dc.closest_approach_time + ?
            WINDOW w AS (PARTITION BY dc.missile_id ORDER BY s.timestamp)
        ),
        target_trajectory AS (
            -- Fetch target states in same window for relative motion analysis
            SELECT
                dc.event_id,
                dc.target_id,
                ts.timestamp,
                ts.u as target_u,
                ts.v as target_v,
                ts.altitude as target_alt
            FROM defeat_candidates dc
            JOIN states ts ON ts.object_id = dc.target_id
            WHERE ts.timestamp BETWEEN dc.closest_approach_time - ? AND dc.closest_approach_time + ?
        ),
        kinematic_analysis AS (
            SELECT
                mt.event_id,
                mt.missile_id,
                mt.target_id,
                mt.timestamp,
                mt.time_to_miss,
                SQRT(POWER(mt.u - tt.target_u, 2) + 
                     POWER(mt.v - tt.target_v, 2) + 
                     POWER(mt.altitude - tt.target_alt, 2)) as range_to_target,
                CASE WHEN mt.prev_time IS NOT NULL THEN
                    (SQRT(POWER(mt.prev_u - tt.target_u, 2) + 
                          POWER(mt.prev_v - tt.target_v, 2) + 
                          POWER(mt.prev_alt - tt.target_alt, 2)) - 
                     SQRT(POWER(mt.u - tt.target_u, 2) + 
                          POWER(mt.v - tt.target_v, 2) + 
                          POWER(mt.altitude - tt.target_alt, 2))) / 
                    (mt.timestamp - mt.prev_time)
                END as closure_rate,
                ABS(mt.yaw - ATAN2(tt.target_v - mt.v, tt.target_u - mt.u) * 180/PI()) as azimuth_error,
                ABS(mt.pitch - ATAN2(tt.target_alt - mt.altitude,
                                     SQRT(POWER(tt.target_u - mt.u, 2) + 
                                          POWER(tt.target_v - mt.v, 2))) * 180/PI()) as pitch_error,
                mt.speed,
                mt.g_load
            FROM missile_trajectory mt
            JOIN target_trajectory tt ON tt.event_id = mt.event_id
                AND ABS(tt.timestamp - mt.timestamp) < 0.1
        ),
        defeat_indicators AS (
            SELECT
                event_id,
                missile_id,
                target_id,
                AVG(CASE WHEN time_to_miss > 0 AND time_to_miss <= 1.5 THEN closure_rate END) as avg_closure_post_miss,
                AVG(CASE WHEN time_to_miss > 0 AND time_to_miss <= 1.5 THEN azimuth_error END) as avg_azimuth_post_miss,
                AVG(CASE WHEN time_to_miss > 0 AND time_to_miss <= 1.5 THEN pitch_error END) as avg_pitch_post_miss,
                MIN(CASE WHEN time_to_miss > 0 AND time_to_miss <= 1.5 THEN closure_rate END) as min_closure_post_miss,
                COUNT(CASE WHEN g_load > ? THEN 1 END) as high_g_state_count,
                AVG(CASE WHEN g_load > ? THEN g_load END) as avg_high_g,
                STDDEV(CASE WHEN g_load > ? THEN g_load END) as stddev_high_g,
                MAX(g_load) as max_g,
                MIN(speed) as min_speed,
                MAX(speed) - MIN(speed) as speed_loss,
                AVG(CASE WHEN time_to_miss BETWEEN -0.5 AND 0.5 THEN speed END) as speed_at_miss,
                MIN(range_to_target) as actual_miss_distance
            FROM kinematic_analysis
            GROUP BY event_id, missile_id, target_id
        ),
        defeat_classification AS (
            SELECT
                event_id,
                missile_id,
                target_id,
                CASE
                    WHEN avg_closure_post_miss < ?
                         AND min_closure_post_miss < ?
                         AND avg_azimuth_post_miss < ?
                         AND avg_pitch_post_miss < ?
                    THEN 'MANEUVER_DEFEAT'
                    
                    WHEN high_g_state_count >= ?
                         AND avg_high_g > ?
                         AND COALESCE(stddev_high_g, 0) < ?
                         AND actual_miss_distance > 100
                    THEN 'G_LIMIT_DEFEAT'
                    
                    WHEN min_speed < ?
                         AND speed_loss > ?
                         AND speed_at_miss < 200
                    THEN 'ENERGY_DEFEAT'
                    
                    ELSE NULL
                END as defeat_type,
                avg_closure_post_miss,
                min_closure_post_miss,
                avg_azimuth_post_miss,
                avg_pitch_post_miss,
                max_g,
                avg_high_g,
                min_speed,
                speed_loss,
                actual_miss_distance
            FROM defeat_indicators
        )
        UPDATE tactical_events
        SET 
            event_type = CASE WHEN dc.defeat_type IS NOT NULL THEN 'WEAPON_DEFEATED' ELSE event_type END,
            metadata = json_merge_patch(
                COALESCE(metadata, '{}'::JSON),
                json_object(
                    'defeat_type', dc.defeat_type,
                    'closure_rate_post_miss_avg', ROUND(dc.avg_closure_post_miss, 2),
                    'closure_rate_post_miss_min', ROUND(dc.min_closure_post_miss, 2),
                    'azimuth_error_post_miss', ROUND(dc.avg_azimuth_post_miss, 2),
                    'pitch_error_post_miss', ROUND(dc.avg_pitch_post_miss, 2),
                    'off_boresight_post_miss', ROUND((dc.avg_azimuth_post_miss + dc.avg_pitch_post_miss) / 2, 2),
                    'max_g_load', ROUND(dc.max_g, 2),
                    'avg_sustained_g', ROUND(dc.avg_high_g, 2),
                    'min_speed_mps', ROUND(dc.min_speed, 2),
                    'speed_loss_mps', ROUND(dc.speed_loss, 2),
                    'miss_distance_meters', ROUND(dc.actual_miss_distance, 2)
                )
            )
        FROM defeat_classification dc
        WHERE tactical_events.id = dc.event_id;
        """

        # Execute the UPDATE - processes all NEAR_MISS events at once (<50 events)
        conn.execute(
            defeat_query,
            [
                5.0,  # Missile trajectory: 5s before near miss
                2.0,  # Missile trajectory: 2s after near miss
                5.0,  # Target trajectory: 5s before near miss
                2.0,  # Target trajectory: 2s after near miss
                self.min_high_g_threshold,
                self.min_high_g_threshold,
                self.min_high_g_threshold,
                self.min_opening_closure,
                self.peak_opening_closure,
                self.max_pointing_error,
                self.max_pointing_error,
                self.min_high_g_states,
                self.min_high_g_threshold,
                self.max_g_variance,
                self.min_effective_speed,
                self.min_speed_loss
            ]
        )

        # Return count of analyzed events
        analyzed = conn.execute("""
            SELECT COUNT(*) FROM tactical_events
            WHERE event_type IN ('WEAPON_MISS', 'WEAPON_DEFEATED')
              AND initiator_type = 'Missile'
              AND (metadata->>'miss_distance_meters') IS NOT NULL
        """).fetchone()[0]

        return analyzed

    def _detect_energy_depletion_defeats(self, conn: duckdb.DuckDBPyConnection, batch_size: int) -> int:
        """
        Detect missiles that ran out of energy while tracking an Air target.
        
        Detection: Missile in last state points at Air target within ±5° in BOTH heading and pitch (3D alignment).
        Confirms tracking by checking same target is also aligned 1s earlier.
        Then finds closest approach point and creates WEAPON_DEFEATED event.
        
        Args:
            conn: DuckDB connection
            batch_size: Batch size (LIMIT clause)
            
        Returns:
            Number of energy depletion defeats detected
        """

        # Step 1: Find missiles without NEAR_MISS that might have energy defeats
        energy_defeat_query = """
        WITH missile_batch AS (
            SELECT id
            FROM objects
            WHERE type_basic = 'Missile'
              AND first_seen IS NOT NULL
              AND last_seen IS NOT NULL
              AND EXISTS (
                  SELECT 1 FROM tactical_events 
                  WHERE event_type = 'WEAPON_MISS' 
                    AND initiator_id = objects.id
                    AND (metadata->>'proximity_distance') IS NULL  -- No NEAR_MISS
                    AND (metadata->>'energy_defeat_analyzed') IS NULL  -- Not yet analyzed
              )
            ORDER BY first_seen
            LIMIT ?
        ),
        missile_last_state AS (
            SELECT 
                mb.id as missile_id,
                o.last_seen,
                s.u as missile_u,
                s.v as missile_v,
                s.altitude as missile_alt,
                s.heading as missile_heading,
                s.pitch as missile_pitch,
                s.timestamp as last_timestamp
            FROM missile_batch mb
            JOIN objects o ON o.id = mb.id
            JOIN states s ON s.object_id = mb.id AND s.timestamp = o.last_seen
            WHERE s.heading IS NOT NULL
              AND s.pitch IS NOT NULL
              AND s.u IS NOT NULL
              AND s.v IS NOT NULL
        ),
        targets_in_cone_last AS (
            -- Find targets within ±5° of missile body axis (3D: heading + pitch) at last state
            SELECT
                mls.missile_id,
                mls.last_timestamp,
                mls.missile_u,
                mls.missile_v,
                mls.missile_alt,
                mls.missile_heading,
                mls.missile_pitch,
                ts.object_id as target_id,
                ts.u as target_u,
                ts.v as target_v,
                ts.altitude as target_alt,
                -- Horizontal distance for elevation calculation
                SQRT(POWER(ts.u - mls.missile_u, 2) + POWER(ts.v - mls.missile_v, 2)) as horizontal_distance,
                -- Azimuth to target (heading plane)
                DEGREES(ATAN2(ts.v - mls.missile_v, ts.u - mls.missile_u)) as azimuth_to_target,
                -- Elevation to target (pitch plane) = atan2(altitude_delta, horizontal_distance)
                DEGREES(ATAN2(ts.altitude - mls.missile_alt, SQRT(POWER(ts.u - mls.missile_u, 2) + POWER(ts.v - mls.missile_v, 2)))) as elevation_to_target,
                -- Heading deviation (normalize to ±180°)
                ABS(((DEGREES(ATAN2(ts.v - mls.missile_v, ts.u - mls.missile_u)) - mls.missile_heading + 540) % 360) - 180) as heading_deviation,
                -- Pitch deviation (simple difference since pitch is already ±90°)
                ABS(DEGREES(ATAN2(ts.altitude - mls.missile_alt, SQRT(POWER(ts.u - mls.missile_u, 2) + POWER(ts.v - mls.missile_v, 2)))) - mls.missile_pitch) as pitch_deviation
            FROM missile_last_state mls
            JOIN states ts ON ts.timestamp BETWEEN mls.last_timestamp - 0.2 AND mls.last_timestamp + 0.2
                AND ts.u IS NOT NULL
                AND ts.v IS NOT NULL
                AND ts.object_id != mls.missile_id
            JOIN objects o ON o.id = ts.object_id
                AND o.type_class = 'Air'  -- Air targets only
                AND o.type_basic NOT IN ('Missile', 'Rocket', 'Bomb', 'Torpedo', 'Projectile', 'Decoy', 'Chaff', 'Flare')
            WHERE ABS(((DEGREES(ATAN2(ts.v - mls.missile_v, ts.u - mls.missile_u)) - mls.missile_heading + 540) % 360) - 180) <= 5
              AND ABS(DEGREES(ATAN2(ts.altitude - mls.missile_alt, SQRT(POWER(ts.u - mls.missile_u, 2) + POWER(ts.v - mls.missile_v, 2)))) - mls.missile_pitch) <= 5
              AND SQRT(POWER(ts.u - mls.missile_u, 2) + POWER(ts.v - mls.missile_v, 2)) <= 10000  -- Within 10km
        ),
        targets_in_cone_minus_1s AS (
            -- Confirm target was also in cone 1 second earlier (tracking confirmation with 3D alignment)
            SELECT
                tic.missile_id,
                tic.target_id,
                tic.last_timestamp
            FROM targets_in_cone_last tic
            JOIN states ms ON ms.object_id = tic.missile_id 
                AND ms.timestamp BETWEEN tic.last_timestamp - 1.2 AND tic.last_timestamp - 0.8
                AND ms.heading IS NOT NULL
                AND ms.pitch IS NOT NULL
                AND ms.u IS NOT NULL
                AND ms.v IS NOT NULL
            JOIN states ts ON ts.object_id = tic.target_id
                AND ts.timestamp BETWEEN ms.timestamp - 0.2 AND ms.timestamp + 0.2
                AND ts.u IS NOT NULL
                AND ts.v IS NOT NULL
            WHERE ABS(((DEGREES(ATAN2(ts.v - ms.v, ts.u - ms.u)) - ms.heading + 540) % 360) - 180) <= 5
              AND ABS(DEGREES(ATAN2(ts.altitude - ms.altitude, SQRT(POWER(ts.u - ms.u, 2) + POWER(ts.v - ms.v, 2)))) - ms.pitch) <= 5
        ),
        closest_approach AS (
            -- Find closest approach between missile and confirmed target
            SELECT
                tcm.missile_id,
                tcm.target_id,
                ms.timestamp as approach_timestamp,
                ms.id as missile_state_id,
                ts.id as target_state_id,
                SQRT(
                    POWER(ms.u - ts.u, 2) +
                    POWER(ms.v - ts.v, 2) +
                    POWER(ms.altitude - ts.altitude, 2)
                ) as distance_meters,
                ROW_NUMBER() OVER (PARTITION BY tcm.missile_id, tcm.target_id ORDER BY 
                    SQRT(POWER(ms.u - ts.u, 2) + POWER(ms.v - ts.v, 2) + POWER(ms.altitude - ts.altitude, 2))
                ) as rn
            FROM targets_in_cone_minus_1s tcm
            JOIN objects o ON o.id = tcm.missile_id
            JOIN states ms ON ms.object_id = tcm.missile_id
                AND ms.timestamp BETWEEN o.first_seen AND tcm.last_timestamp
                AND ms.u IS NOT NULL
                AND ms.v IS NOT NULL
            JOIN states ts ON ts.object_id = tcm.target_id
                AND ts.timestamp BETWEEN ms.timestamp - 0.2 AND ms.timestamp + 0.2
                AND ts.u IS NOT NULL
                AND ts.v IS NOT NULL
        )
        SELECT
            missile_id,
            target_id,
            approach_timestamp,
            missile_state_id,
            target_state_id,
            distance_meters
        FROM closest_approach
        WHERE rn = 1
          AND distance_meters > 50  -- Must have actually missed (not a hit)
        """

        results = conn.execute(energy_defeat_query, [batch_size]).fetchall()

        if not results:
            return 0

        # Step 2: Create WEAPON_DEFEATED events for each energy depletion defeat
        for missile_id, target_id, approach_time, missile_state_id, target_state_id, distance in results:
            # Get coalition info
            missile_info = conn.execute(
                "SELECT coalition FROM objects WHERE id = ?",
                [missile_id]
            ).fetchone()

            target_info = conn.execute(
                "SELECT coalition, name, type_class, type_basic FROM objects WHERE id = ?",
                [target_id]
            ).fetchone()

            if not missile_info or not target_info:
                continue

            missile_coalition = missile_info[0]
            target_coalition, target_name, target_type_class, target_type_basic = target_info

            # Insert WEAPON_DEFEATED event
            self._insert_single_decoyed_or_miss_event(
                conn,
                event_type='WEAPON_DEFEATED',
                timestamp=approach_time,
                initiator_id=missile_id,
                initiator_coalition=missile_coalition,
                initiator_type='Missile',
                initiator_state_id=missile_state_id,
                target_id=target_id,
                target_coalition=target_coalition,
                target_type=f"{target_type_class}+{target_type_basic}",
                target_name=target_name,
                target_state_id=target_state_id,
                metadata={
                    'defeat_type': 'ENERGY_DEPLETION',
                    'miss_distance_meters': round(distance, 2),
                    'tracking_confirmed': True
                }
            )

        # Step 3: Mark missiles as analyzed
        missile_ids = [r[0] for r in results]
        if missile_ids:
            placeholders = ','.join(['?'] * len(missile_ids))
            conn.execute(f"""
                UPDATE tactical_events
                SET metadata = json_merge_patch(
                    COALESCE(metadata, '{{}}'::JSON),
                    json_object('energy_defeat_analyzed', true)
                )
                WHERE event_type = 'WEAPON_MISS'
                  AND initiator_id IN ({placeholders})
            """, missile_ids)

        return len(results)

    def _detect_proximity_kills(self, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Detect proximity kills - reclassify WEAPON_MISS events as WEAPON_HIT when missile and target are destroyed together.
        
        This handles the case where high-speed targets separate quickly after proximity detonation,
        making spatial clustering (which uses removal-time positions) fail.
        
        Reclassifies WEAPON_MISS events where:
        - Miss distance < proximity_kill_threshold (default: 25m)
        - Both missile and target removed within time_window (default: 1.0s) of miss event
        - Missile and target removed within time_window of each other
        
        Returns:
            Number of proximity kills detected
        """
        # Find WEAPON_MISS events that are actually proximity kills
        # Note: Using json_extract_path_text instead of ->' to avoid DuckDB casting issues
        proximity_kills_query = """
        WITH proximity_candidates AS (
            SELECT 
                e.id as event_id,
                e.timestamp as miss_time,
                e.initiator_id as weapon_id,
                e.target_id,
                json_extract_path_text(e.metadata, 'proximity_distance') as miss_distance_str,
                w.removed_at as weapon_removed,
                t.removed_at as target_removed
            FROM tactical_events e
            JOIN objects w ON e.initiator_id = w.id
            LEFT JOIN objects t ON e.target_id = t.id
            WHERE e.event_type = 'WEAPON_MISS'
                AND json_extract_path_text(e.metadata, 'proximity_distance') IS NOT NULL
                AND w.removed_at IS NOT NULL
                AND (t.removed_at IS NOT NULL OR e.target_id IS NULL)
        ),
        
        proximity_kills AS (
            SELECT 
                event_id,
                weapon_id,
                target_id,
                miss_time,
                weapon_removed,
                target_removed,
                CAST(miss_distance_str AS DOUBLE) as miss_distance
            FROM proximity_candidates
            WHERE miss_distance_str IS NOT NULL
                AND CAST(miss_distance_str AS DOUBLE) < ?
                AND (weapon_removed - miss_time) <= ?
                AND (target_removed IS NULL OR (target_removed - miss_time) <= ?)
                AND (target_removed IS NULL OR ABS(weapon_removed - target_removed) <= ?)
                -- Require target_id to be present for proximity kills (need to know what was killed)
                AND target_id IS NOT NULL
        )
        
        SELECT 
            pk.event_id,
            pk.weapon_id,
            pk.target_id,
            pk.miss_time,
            pk.miss_distance,
            w.type_basic as weapon_type,
            w.coalition as weapon_coalition,
            t.type_class as target_type,
            t.coalition as target_coalition,
            w.parent_id as launcher_id
        FROM proximity_kills pk
        JOIN objects w ON pk.weapon_id = w.id
        LEFT JOIN objects t ON pk.target_id = t.id
        """

        # Execute query to find proximity kills
        kills = conn.execute(
            proximity_kills_query,
            [
                self.proximity_kill_threshold,
                self.proximity_kill_time_window,
                self.proximity_kill_time_window,
                self.proximity_kill_time_window
            ]
        ).fetchall()

        if not kills:
            return 0

        # Reclassify events and create WEAPON_HIT events
        for (event_id, weapon_id, target_id, miss_time, miss_distance,
             weapon_type, weapon_coalition, target_type, target_coalition,
             launcher_id) in kills:

            # Get weapon state at miss time
            weapon_state = conn.execute("""
                SELECT id, longitude, latitude, altitude
                FROM states
                WHERE object_id = ? AND timestamp <= ?
                ORDER BY timestamp DESC LIMIT 1
            """, [weapon_id, miss_time]).fetchone()

            if not weapon_state:
                continue

            weapon_state_id, lon, lat, alt = weapon_state

            # Get target state at miss time (if target exists)
            target_state_id = None
            if target_id:
                target_state_result = conn.execute("""
                    SELECT id FROM states
                    WHERE object_id = ? AND timestamp <= ?
                    ORDER BY timestamp DESC LIMIT 1
                """, [target_id, miss_time]).fetchone()
                if target_state_result:
                    target_state_id = target_state_result[0]

            # Get launcher state at miss time
            launcher_state_id = None
            if launcher_id:
                launcher_state_result = conn.execute("""
                    SELECT id FROM states
                    WHERE object_id = ? AND timestamp <= ?
                    ORDER BY timestamp DESC LIMIT 1
                """, [launcher_id, miss_time]).fetchone()
                if launcher_state_result:
                    launcher_state_id = launcher_state_result[0]

            # Delete the WEAPON_MISS event
            conn.execute("DELETE FROM tactical_events WHERE id = ?", [event_id])

            # Insert WEAPON_HIT event with proximity kill metadata
            metadata = {
                "proximity_kill": True,
                "miss_distance": float(miss_distance),
                "detection_method": "proximity_fuze"
            }

            conn.execute("""
                INSERT INTO tactical_events 
                (event_type, timestamp, initiator_id, target_id,
                 initiator_type, target_type, initiator_coalition, target_coalition,
                 longitude, latitude, altitude,
                 initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?::JSON)
            """, [
                'WEAPON_HIT',
                miss_time,
                weapon_id,
                target_id,
                weapon_type,
                target_type,
                weapon_coalition,
                target_coalition,
                lon, lat, alt,
                weapon_state_id,
                target_state_id,
                launcher_state_id,
                json.dumps(metadata)
            ])

        return len(kills)
