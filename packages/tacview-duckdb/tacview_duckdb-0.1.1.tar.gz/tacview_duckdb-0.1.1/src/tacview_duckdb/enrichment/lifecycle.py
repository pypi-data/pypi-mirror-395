"""Object lifecycle enrichment logic.

Handles lifecycle events for all object types:
- Fixed-wing aircraft: takeoff, landing, touch-and-go, removal/destruction
- Rotorcraft: takeoff, landing, removal/destruction  
- Ground/Sea units: weapon-caused destruction
"""

from typing import Dict, List, Optional, Any
from collections import defaultdict
import duckdb

from .pipeline import Enricher


class FixedWingEnricher(Enricher):
    """
    Detects lifecycle events for fixed-wing aircraft.
    
    Detects:
    - Takeoff events (TakenOff)
    - Landing events (Landed)
    - Removal classification (Destroyed vs LeftArea based on speed)
    
    Uses SQL LAG/LEAD window functions to detect speed transitions and altitude trends.
    Injects native Tacview events into events table.
    """
    
    def __init__(
        self,
        airbase_database: Optional[Dict[str, Dict]] = None,
        use_airport_database: bool = False,
        airport_max_distance_km: float = 5.0,
        min_altitude_change: float = 15.0,
        max_ground_speed: float = 20.0,
        min_transition_speed: float = 30.0,
        detect_removals: bool = True,
        destruction_speed_threshold: float = 30.0,
        clean_removal_speed_threshold: float = 1.0,
        num_states_to_check: int = 3
    ):
        """
        Initialize fixed-wing enricher.
        
        Args:
            airbase_database: Optional airbase locations for identification (legacy)
            use_airport_database: Use OurAirports database (default: False)
            airport_max_distance_km: Maximum distance to search for airports (default: 5 km)
            min_altitude_change: Minimum altitude change to confirm event (default: 15m)
            max_ground_speed: Max speed considered "on ground" (default: 20 m/s)
            min_transition_speed: Min speed considered "in flight" (default: 30 m/s)
            detect_removals: Detect and classify aircraft removal events (default: True)
            destruction_speed_threshold: Speed (m/s) above which removal is considered destruction (default: 30.0)
            clean_removal_speed_threshold: Speed (m/s) below which removal is considered clean (default: 1.0)
            num_states_to_check: Number of last states to average for removal detection (default: 3)
        """
        self.airbase_database = airbase_database
        self.use_airport_database = use_airport_database
        self.airport_max_distance_km = airport_max_distance_km
        self.min_altitude_change = min_altitude_change
        self.max_ground_speed = max_ground_speed
        self.min_transition_speed = min_transition_speed
        self.detect_removals = detect_removals
        self.destruction_speed_threshold = destruction_speed_threshold
        self.clean_removal_speed_threshold = clean_removal_speed_threshold
        self.num_states_to_check = num_states_to_check
    
    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run fixed-wing flight phase enrichment.
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of aircraft enriched
        """
        # Check if we should use a pre-loaded table or load our own
        airports_table_loaded = False
        airports_table_name = None
        
        if self.use_airport_database:
            try:
                from . import airports
                airports.load_airports_to_duckdb(conn, table_name="temp_airports")
                airports_table_loaded = True
                airports_table_name = "temp_airports"
            except Exception as e:
                print(f"Warning: Failed to load airport database: {e}")
        
        try:
            # Get mission start time
            mission_start_result = conn.execute("""
                SELECT MIN(timestamp) FROM states
            """).fetchone()
            mission_start = mission_start_result[0] if mission_start_result else 0.0
            
            # Find all fixed-wing aircraft
            aircraft_list = conn.execute("""
                SELECT DISTINCT o.id, o.name, o.type_specific, o.pilot, o.first_seen
                FROM objects o
                JOIN states s ON o.id = s.object_id
                WHERE o.type_basic = 'FixedWing'
                  AND o.first_seen IS NOT NULL
                  AND o.last_seen IS NOT NULL
                  AND (o.last_seen - o.first_seen) > 60.0
                GROUP BY o.id, o.name, o.type_specific, o.pilot, o.first_seen
                HAVING COUNT(s.id) > 20
            """).fetchall()
            
            if not aircraft_list:
                return 0
            
            enriched_count = 0
            events_to_insert = []
            
            # PHASE 1: Detect air starts
            air_start_ids = self._detect_air_starts(
                conn, mission_start, airports_table_name, events_to_insert
            )
            
            # PHASE 2: Detect normal takeoff/landing
            for aircraft_id, aircraft_name, aircraft_type, pilot, first_seen in aircraft_list:
                if aircraft_id in air_start_ids:
                    continue
                
                detected_events = self._detect_ground_periods(
                    conn,
                    aircraft_id,
                    self.min_altitude_change,
                    self.max_ground_speed,
                    self.min_transition_speed
                )
                
                for event_timestamp, event_type, altitude, speed, longitude, latitude, heading in detected_events:
                    location_name = self._identify_location(
                        conn, latitude, longitude, airports_table_name
                    )
                    
                    runway = self._heading_to_runway(heading) if heading else None
                    location_str = f"{location_name}" + (f" (Runway {runway})" if runway else "")
                    
                    if event_type == 'takeoff':
                        event_name = 'TakenOff'
                        event_msg = f"{aircraft_name} has taken off from {location_str}"
                    else:
                        event_name = 'Landed'
                        event_msg = f"{aircraft_name} has landed at {location_str}"
                    
                    events_to_insert.append((
                        aircraft_id,
                        event_timestamp,
                        event_name,
                        event_msg
                    ))
                
                enriched_count += 1
            
            # Filter and deduplicate
            if events_to_insert:
                events_to_insert = _filter_bounce_events(events_to_insert)
                events_to_insert = _deduplicate_events(events_to_insert)
            
            # PHASE 3: Detect aircraft removals
            if self.detect_removals:
                removal_events = self._detect_aircraft_removals(conn)
                if removal_events:
                    events_to_insert.extend(removal_events)
            
            # Bulk insert
            if events_to_insert:
                conn.executemany(
                    """
                    INSERT OR REPLACE INTO events (
                        object_id, timestamp, event_name, event_params
                    ) VALUES (?, ?, ?, ?)
                    """,
                    events_to_insert
                )
            
            return enriched_count
        
        finally:
            if airports_table_loaded:
                from . import airports
                airports.cleanup_airports_table(conn, table_name=airports_table_name)
    
    def _detect_air_starts(
        self,
        conn: duckdb.DuckDBPyConnection,
        mission_start: float,
        airports_table_name: Optional[str],
        events_to_insert: list
    ) -> set:
        """Detect air starts for all Air category objects."""
        air_start_ids = set()
        
        all_air_objects = conn.execute("""
            SELECT DISTINCT o.id, o.name, o.type_basic, o.pilot, o.first_seen
            FROM objects o
            JOIN states s ON o.id = s.object_id
            WHERE o.type_class = 'Air'
              AND o.first_seen IS NOT NULL
              AND o.first_seen >= ?
            GROUP BY o.id, o.name, o.type_basic, o.pilot, o.first_seen
            HAVING COUNT(s.id) > 5
        """, [mission_start + 10.0]).fetchall()
        
        for obj_id, obj_name, obj_type, pilot, first_seen in all_air_objects:
            spawn_states = conn.execute("""
                SELECT timestamp, altitude, speed, longitude, latitude, heading
                FROM states
                WHERE object_id = ?
                ORDER BY timestamp
                OFFSET 1
                LIMIT 2
            """, [obj_id]).fetchall()
            
            if spawn_states:
                spawn_state = spawn_states[-1] if len(spawn_states) > 1 else spawn_states[0]
                spawn_time, spawn_alt, spawn_speed, spawn_lon, spawn_lat, spawn_hdg = spawn_state
                
                if (spawn_alt is not None and spawn_alt >= 100.0 and 
                    spawn_speed is not None and spawn_speed >= 30.0):
                    location_name = self._identify_location(
                        conn, spawn_lat, spawn_lon, airports_table_name, obj_type
                    )
                    
                    pilot_text = f"pilot '{pilot}'" if pilot else "pilot"
                    event_msg = f"{pilot_text} ({obj_name}) has spawned at {location_name}"
                    
                    events_to_insert.append((
                        obj_id,
                        spawn_time,
                        'TakenOff',
                        event_msg
                    ))
                    
                    air_start_ids.add(obj_id)
        
        return air_start_ids
    
    def _detect_ground_periods(
        self,
        conn: duckdb.DuckDBPyConnection,
        object_id: str,
        min_altitude_change: float,
        max_ground_speed: float,
        min_transition_speed: float
    ) -> List[tuple]:
        """Detect landing/takeoff events using SQL LAG/LEAD."""
        transition_query = """
        WITH windowed_data AS (
            SELECT 
                timestamp,
                altitude,
                speed,
                longitude,
                latitude,
                heading,
                MIN(speed) OVER (
                    ORDER BY timestamp 
                    ROWS BETWEEN 150 PRECEDING AND 150 FOLLOWING
                ) as window_min_speed,
                MAX(speed) OVER (
                    ORDER BY timestamp 
                    ROWS BETWEEN 150 PRECEDING AND 150 FOLLOWING
                ) as window_max_speed,
                LAG(altitude, 225) OVER (ORDER BY timestamp) as alt_45s_ago,
                LAG(altitude, 75) OVER (ORDER BY timestamp) as alt_15s_ago,
                LEAD(altitude, 150) OVER (ORDER BY timestamp) as alt_30s_ahead
            FROM states
            WHERE object_id = ?
              AND speed IS NOT NULL 
              AND altitude IS NOT NULL
        ),
        transitions AS (
            SELECT 
                timestamp,
                altitude,
                speed,
                longitude,
                latitude,
                heading,
                alt_45s_ago,
                alt_15s_ago,
                alt_30s_ahead,
                CASE 
                    WHEN alt_45s_ago IS NOT NULL 
                         AND alt_15s_ago IS NOT NULL
                         AND (alt_45s_ago - alt_15s_ago) > ? 
                    THEN 'landing'
                    WHEN alt_30s_ahead IS NOT NULL 
                         AND (alt_30s_ahead - altitude) > ? 
                    THEN 'takeoff'
                    ELSE NULL
                END as event_type
            FROM windowed_data
            WHERE window_min_speed < ? AND window_max_speed > ?
        )
        SELECT 
            timestamp,
            event_type,
            altitude,
            speed,
            longitude,
            latitude,
            heading
        FROM transitions
        WHERE event_type IS NOT NULL
        ORDER BY timestamp
        """
        
        transition_points = conn.execute(
            transition_query, 
            [object_id, min_altitude_change, min_altitude_change, max_ground_speed, min_transition_speed]
        ).fetchall()
        
        if not transition_points:
            return []
        
        # Deduplicate by type within 120s
        events_by_type = {'landing': [], 'takeoff': []}
        for event in transition_points:
            event_type = event[1]
            events_by_type[event_type].append(event)
        
        deduplicated = []
        for event_type, type_events in events_by_type.items():
            type_events.sort(key=lambda x: x[0])
            
            kept = []
            for event in type_events:
                timestamp = event[0]
                is_duplicate = any(abs(timestamp - kept_event[0]) < 120.0 for kept_event in kept)
                if not is_duplicate:
                    kept.append(event)
            
            deduplicated.extend(kept)
        
        deduplicated.sort(key=lambda x: x[0])
        return deduplicated
    
    def _identify_location(
        self,
        conn: duckdb.DuckDBPyConnection,
        latitude: float,
        longitude: float,
        airports_table_name: Optional[str],
        obj_type: Optional[str] = None
    ) -> str:
        """Identify location using airport database or coordinates."""
        location_name = None
        
        if airports_table_name:
            try:
                from . import airports
                airport_types = ['large_airport', 'medium_airport', 'small_airport', 'heliport', 'seaplane_base'] if obj_type == 'Rotorcraft' else None
                airport_info = airports.find_nearest_airport(
                    conn,
                    latitude,
                    longitude,
                    max_distance_km=self.airport_max_distance_km,
                    table_name=airports_table_name,
                    airport_types=airport_types
                )
                if airport_info:
                    location_name = airports.format_airport_description(airport_info)
            except Exception:
                pass
        
        if not location_name and self.airbase_database:
            location_name = _identify_airbase(longitude, latitude, self.airbase_database)
        
        if not location_name:
            location_name = f"({latitude:.3f}, {longitude:.3f})"
        
        return location_name
    
    def _heading_to_runway(self, heading: Optional[float]) -> Optional[str]:
        """Convert heading to runway designation."""
        if heading is None:
            return None
        
        heading = heading % 360
        runway_num = int((heading + 5) / 10) % 36
        if runway_num == 0:
            runway_num = 36
        
        return f"{runway_num:02d}"
    
    def _detect_aircraft_removals(self, conn: duckdb.DuckDBPyConnection) -> List[tuple]:
        """
        Detect and classify aircraft removal events based on speed.
        
        When an aircraft is removed from the battlefield (removed_at is set),
        examines the last N states to determine if the aircraft was:
        - Destroyed (average speed > destruction_speed_threshold)
        - Cleanly removed/despawned (average speed < clean_removal_speed_threshold)
        
        Returns:
            List of event tuples (object_id, timestamp, event_name, event_params)
        """
        # Find all Air objects with removed_at timestamp
        removed_aircraft = conn.execute("""
            SELECT id, name, removed_at
            FROM objects
            WHERE type_class = 'Air'
              AND removed_at IS NOT NULL
        """).fetchall()
        
        if not removed_aircraft:
            return []
        
        events_to_insert = []
        
        for aircraft_id, aircraft_name, removed_at in removed_aircraft:
            # Get the last N states before removal
            last_states = conn.execute("""
                SELECT speed
                FROM states
                WHERE object_id = ?
                  AND timestamp <= ?
                  AND speed IS NOT NULL
                ORDER BY timestamp DESC
                LIMIT ?
            """, [aircraft_id, removed_at, self.num_states_to_check]).fetchall()
            
            if not last_states:
                continue
            
            # Calculate average speed
            speeds = [state[0] for state in last_states]
            avg_speed = sum(speeds) / len(speeds)
            
            # Determine event type based on average speed
            if avg_speed > self.destruction_speed_threshold:
                # High speed removal = destroyed
                event_name = 'Destroyed'
                event_params = f"{aircraft_name or aircraft_id} was destroyed"
            elif avg_speed < self.clean_removal_speed_threshold:
                # Very low speed removal = clean exit
                event_name = 'LeftArea'
                event_params = f"{aircraft_name or aircraft_id} left the area"
            else:
                # Medium speed - ambiguous, skip
                continue
            
            events_to_insert.append((
                aircraft_id,
                removed_at,
                event_name,
                event_params
            ))
        
        return events_to_insert


class RotorcraftEnricher(Enricher):
    """
    Detects lifecycle events for rotorcraft (helicopters).
    
    Detects:
    - Takeoff events (TakenOff)
    - Landing events (Landed)
    - Removal classification (Destroyed vs LeftArea based on speed)
    
    Similar to FixedWingEnricher but adapted for rotorcraft flight characteristics.
    Uses the same SQL approach as fixed-wing but with helicopter-appropriate thresholds.
    """
    
    def __init__(
        self,
        airbase_database: Optional[Dict[str, Dict]] = None,
        use_airport_database: bool = False,
        airport_max_distance_km: float = 5.0,
        min_altitude_change: float = 10.0,
        max_ground_speed: float = 5.0,
        min_transition_speed: float = 10.0,
        detect_removals: bool = True,
        destruction_speed_threshold: float = 30.0,
        clean_removal_speed_threshold: float = 1.0,
        num_states_to_check: int = 3
    ):
        """
        Initialize rotorcraft enricher.
        
        Args:
            airbase_database: Optional airbase locations (legacy)
            use_airport_database: Use OurAirports database (default: False)
            airport_max_distance_km: Maximum distance to search (default: 5 km)
            min_altitude_change: Minimum altitude change (default: 10m)
            max_ground_speed: Max speed "on ground" (default: 5 m/s)
            min_transition_speed: Min speed "in flight" (default: 10 m/s)
            detect_removals: Detect and classify aircraft removal events (default: True)
            destruction_speed_threshold: Speed (m/s) above which removal is considered destruction (default: 30.0)
            clean_removal_speed_threshold: Speed (m/s) below which removal is considered clean (default: 1.0)
            num_states_to_check: Number of last states to average for removal detection (default: 3)
        """
        self.airbase_database = airbase_database
        self.use_airport_database = use_airport_database
        self.airport_max_distance_km = airport_max_distance_km
        self.min_altitude_change = min_altitude_change
        self.max_ground_speed = max_ground_speed
        self.min_transition_speed = min_transition_speed
        self.detect_removals = detect_removals
        self.destruction_speed_threshold = destruction_speed_threshold
        self.clean_removal_speed_threshold = clean_removal_speed_threshold
        self.num_states_to_check = num_states_to_check
    
    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run rotorcraft flight phase enrichment.
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of rotorcraft enriched
        """
        airports_table_loaded = False
        airports_table_name = None
        
        if self.use_airport_database:
            try:
                from . import airports
                airports.load_airports_to_duckdb(conn, table_name="temp_airports_helo")
                airports_table_loaded = True
                airports_table_name = "temp_airports_helo"
            except Exception as e:
                print(f"Warning: Failed to load airport database: {e}")
        
        try:
            rotorcraft_list = conn.execute("""
                SELECT DISTINCT o.id, o.name, o.type_specific
                FROM objects o
                JOIN states s ON o.id = s.object_id
                WHERE o.type_basic = 'Rotorcraft'
                  AND o.first_seen IS NOT NULL
                  AND o.last_seen IS NOT NULL
                  AND (o.last_seen - o.first_seen) > 60.0
                GROUP BY o.id, o.name, o.type_specific
                HAVING COUNT(s.id) > 20
            """).fetchall()
            
            if not rotorcraft_list:
                return 0
            
            enriched_count = 0
            events_to_insert = []
            
            for helo_id, helo_name, helo_type in rotorcraft_list:
                # Use same SQL-based detection with helicopter thresholds
                detected_events = self._detect_ground_periods(
                    conn,
                    helo_id,
                    self.min_altitude_change,
                    self.max_ground_speed,
                    self.min_transition_speed
                )
                
                for event_timestamp, event_type, altitude, speed, longitude, latitude, heading in detected_events:
                    lz_name = self._identify_location(
                        conn, latitude, longitude, airports_table_name
                    )
                    
                    if event_type == 'takeoff':
                        event_name = 'TakenOff'
                        event_msg = f"{helo_name} has taken off from {lz_name}"
                    else:
                        event_name = 'Landed'
                        event_msg = f"{helo_name} has landed at {lz_name}"
                    
                    events_to_insert.append((
                        helo_id,
                        event_timestamp,
                        event_name,
                        event_msg
                    ))
                
                enriched_count += 1
            
            # Filter and deduplicate
            if events_to_insert:
                events_to_insert = _filter_bounce_events(events_to_insert)
                events_to_insert = _deduplicate_events(events_to_insert)
            
            # PHASE 3: Detect aircraft removals (shared with fixed-wing)
            if self.detect_removals:
                removal_events = self._detect_aircraft_removals(conn)
                if removal_events:
                    events_to_insert.extend(removal_events)
            
            # Bulk insert
            if events_to_insert:
                conn.executemany(
                    """
                    INSERT OR REPLACE INTO events (
                        object_id, timestamp, event_name, event_params
                    ) VALUES (?, ?, ?, ?)
                    """,
                    events_to_insert
                )
            
            return enriched_count
        
        finally:
            if airports_table_loaded:
                from . import airports
                airports.cleanup_airports_table(conn, table_name=airports_table_name)
    
    def _detect_ground_periods(
        self,
        conn: duckdb.DuckDBPyConnection,
        object_id: str,
        min_altitude_change: float,
        max_ground_speed: float,
        min_transition_speed: float
    ) -> List[tuple]:
        """Detect landing/takeoff events using SQL LAG/LEAD."""
        # Same SQL query as fixed-wing
        transition_query = """
        WITH windowed_data AS (
            SELECT 
                timestamp,
                altitude,
                speed,
                longitude,
                latitude,
                heading,
                MIN(speed) OVER (
                    ORDER BY timestamp 
                    ROWS BETWEEN 150 PRECEDING AND 150 FOLLOWING
                ) as window_min_speed,
                MAX(speed) OVER (
                    ORDER BY timestamp 
                    ROWS BETWEEN 150 PRECEDING AND 150 FOLLOWING
                ) as window_max_speed,
                LAG(altitude, 225) OVER (ORDER BY timestamp) as alt_45s_ago,
                LAG(altitude, 75) OVER (ORDER BY timestamp) as alt_15s_ago,
                LEAD(altitude, 150) OVER (ORDER BY timestamp) as alt_30s_ahead
            FROM states
            WHERE object_id = ?
              AND speed IS NOT NULL 
              AND altitude IS NOT NULL
        ),
        transitions AS (
            SELECT 
                timestamp,
                altitude,
                speed,
                longitude,
                latitude,
                heading,
                alt_45s_ago,
                alt_15s_ago,
                alt_30s_ahead,
                CASE 
                    WHEN alt_45s_ago IS NOT NULL 
                         AND alt_15s_ago IS NOT NULL
                         AND (alt_45s_ago - alt_15s_ago) > ? 
                    THEN 'landing'
                    WHEN alt_30s_ahead IS NOT NULL 
                         AND (alt_30s_ahead - altitude) > ? 
                    THEN 'takeoff'
                    ELSE NULL
                END as event_type
            FROM windowed_data
            WHERE window_min_speed < ? AND window_max_speed > ?
        )
        SELECT 
            timestamp,
            event_type,
            altitude,
            speed,
            longitude,
            latitude,
            heading
        FROM transitions
        WHERE event_type IS NOT NULL
        ORDER BY timestamp
        """
        
        transition_points = conn.execute(
            transition_query, 
            [object_id, min_altitude_change, min_altitude_change, max_ground_speed, min_transition_speed]
        ).fetchall()
        
        if not transition_points:
            return []
        
        # Deduplicate
        events_by_type = {'landing': [], 'takeoff': []}
        for event in transition_points:
            event_type = event[1]
            events_by_type[event_type].append(event)
        
        deduplicated = []
        for event_type, type_events in events_by_type.items():
            type_events.sort(key=lambda x: x[0])
            
            kept = []
            for event in type_events:
                timestamp = event[0]
                is_duplicate = any(abs(timestamp - kept_event[0]) < 120.0 for kept_event in kept)
                if not is_duplicate:
                    kept.append(event)
            
            deduplicated.extend(kept)
        
        deduplicated.sort(key=lambda x: x[0])
        return deduplicated
    
    def _identify_location(
        self,
        conn: duckdb.DuckDBPyConnection,
        latitude: float,
        longitude: float,
        airports_table_name: Optional[str]
    ) -> str:
        """Identify location using airport database or coordinates."""
        lz_name = None
        
        if airports_table_name:
            try:
                from . import airports
                airport_info = airports.find_nearest_airport(
                    conn,
                    latitude,
                    longitude,
                    max_distance_km=self.airport_max_distance_km,
                    table_name=airports_table_name,
                    airport_types=['large_airport', 'medium_airport', 'small_airport', 
                                 'heliport', 'seaplane_base']
                )
                if airport_info:
                    lz_name = airports.format_airport_description(airport_info)
            except Exception:
                pass
        
        if not lz_name and self.airbase_database:
            lz_name = _identify_airbase(longitude, latitude, self.airbase_database)
        
        if not lz_name:
            lz_name = f"LZ ({latitude:.3f}, {longitude:.3f})"
        
        return lz_name
    
    def _detect_aircraft_removals(self, conn: duckdb.DuckDBPyConnection) -> List[tuple]:
        """
        Detect and classify aircraft removal events based on speed.
        
        When an aircraft is removed from the battlefield (removed_at is set),
        examines the last N states to determine if the aircraft was:
        - Destroyed (average speed > destruction_speed_threshold)
        - Cleanly removed/despawned (average speed < clean_removal_speed_threshold)
        
        Returns:
            List of event tuples (object_id, timestamp, event_name, event_params)
        """
        # Find all Air objects with removed_at timestamp
        removed_aircraft = conn.execute("""
            SELECT id, name, removed_at
            FROM objects
            WHERE type_class = 'Air'
              AND removed_at IS NOT NULL
        """).fetchall()
        
        if not removed_aircraft:
            return []
        
        events_to_insert = []
        
        for aircraft_id, aircraft_name, removed_at in removed_aircraft:
            # Get the last N states before removal
            last_states = conn.execute("""
                SELECT speed
                FROM states
                WHERE object_id = ?
                  AND timestamp <= ?
                  AND speed IS NOT NULL
                ORDER BY timestamp DESC
                LIMIT ?
            """, [aircraft_id, removed_at, self.num_states_to_check]).fetchall()
            
            if not last_states:
                continue
            
            # Calculate average speed
            speeds = [state[0] for state in last_states]
            avg_speed = sum(speeds) / len(speeds)
            
            # Determine event type based on average speed
            if avg_speed > self.destruction_speed_threshold:
                # High speed removal = destroyed
                event_name = 'Destroyed'
                event_params = f"{aircraft_name or aircraft_id} was destroyed"
            elif avg_speed < self.clean_removal_speed_threshold:
                # Very low speed removal = clean exit
                event_name = 'LeftArea'
                event_params = f"{aircraft_name or aircraft_id} left the area"
            else:
                # Medium speed - ambiguous, skip
                continue
            
            events_to_insert.append((
                aircraft_id,
                removed_at,
                event_name,
                event_params
            ))
        
        return events_to_insert


class GroundSeaEnricher(Enricher):
    """
    Creates destruction events for Ground and Sea units hit by weapons.
    
    When ground/sea units are hit and subsequently removed within a time window,
    creates 'Destroyed' events with hit information. Handles:
    - Ground targets that burn before being destroyed
    - Ships that sink after taking damage
    - Multiple hits (uses latest hit time)
    
    Note: Aircraft destruction is handled by FixedWingEnricher and RotorcraftEnricher
    based on speed analysis at removal time.
    
    Args:
        time_window: Maximum seconds between last hit and removal to attribute
                     destruction to weapons (default: 120 seconds / 2 minutes)
    """
    
    def __init__(self, time_window: float = 120.0):
        self.time_window = time_window
    
    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> dict:
        """
        Create Destroyed events for ground/sea units that were hit and removed.
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Dictionary with enrichment statistics
        """
        # Find ground/sea units that were hit and subsequently removed
        query = """
        WITH weapon_hits AS (
            SELECT 
                te.target_id,
                te.timestamp as hit_time,
                te.initiator_id as weapon_id
            FROM tactical_events te
            JOIN objects o ON o.id = te.target_id
            WHERE te.event_type = 'WEAPON_HIT'
              AND te.target_id IS NOT NULL
              AND o.type_class IN ('Ground', 'Sea')
        ),
        removals AS (
            SELECT 
                o.id,
                o.name,
                o.type_class,
                o.removed_at
            FROM objects o
            WHERE o.type_class IN ('Ground', 'Sea')
              AND o.removed_at IS NOT NULL
        )
        SELECT 
            r.id,
            r.name,
            r.type_class,
            r.removed_at,
            MAX(h.hit_time) as latest_hit_time,
            COUNT(DISTINCT h.weapon_id) as hit_count
        FROM removals r
        JOIN weapon_hits h ON h.target_id = r.id
        WHERE r.removed_at >= h.hit_time
          AND r.removed_at <= h.hit_time + ?
        GROUP BY r.id, r.name, r.type_class, r.removed_at
        """
        
        destructions = conn.execute(query, [self.time_window]).fetchall()
        
        if not destructions:
            return {
                "ground_sea_destroyed_created": 0,
                "time_window_seconds": self.time_window
            }
        
        # Check which ones don't already have Destroyed events
        events_to_insert = []
        
        for unit_id, unit_name, type_class, removed_at, latest_hit, hit_count in destructions:
            # Check if Destroyed event already exists
            existing = conn.execute("""
                SELECT 1 FROM events
                WHERE object_id = ?
                  AND timestamp = ?
                  AND event_name = 'Destroyed'
            """, [unit_id, removed_at]).fetchone()
            
            if existing:
                continue  # Already has Destroyed event
            
            name = unit_name or unit_id
            time_to_destruction = removed_at - latest_hit
            
            # Build message with hit count
            if hit_count == 1:
                hit_info = f"{int(time_to_destruction)}s after being hit"
            else:
                hit_info = f"{int(time_to_destruction)}s after being hit {hit_count} times"
            
            event_params = f"{name} was destroyed ({hit_info})"
            
            events_to_insert.append((
                unit_id,
                removed_at,
                'Destroyed',
                event_params
            ))
        
        if events_to_insert:
            conn.executemany("""
                INSERT OR REPLACE INTO events (object_id, timestamp, event_name, event_params)
                VALUES (?, ?, ?, ?)
            """, events_to_insert)
        
        return {
            "ground_sea_destroyed_created": len(events_to_insert),
            "time_window_seconds": self.time_window
        }


# Helper functions (module-level)

def _filter_bounce_events(
    events: List[tuple],
    bounce_window: float = 5.0
) -> List[tuple]:
    """Filter out touch-and-go bounce events."""
    if not events:
        return events
    
    aircraft_events = defaultdict(list)
    for event in events:
        object_id, timestamp, event_name, event_params = event
        aircraft_events[object_id].append((timestamp, event_name, event))
    
    filtered_events = []
    
    for object_id, aircraft_event_list in aircraft_events.items():
        aircraft_event_list.sort(key=lambda x: x[0])
        events_to_keep = set(range(len(aircraft_event_list)))
        
        for i, (timestamp, event_name, event) in enumerate(aircraft_event_list):
            obj_id, ts, evt_name, evt_params = event
            is_touch_and_go = evt_name == 'Message' and 'touch-and-go' in evt_params.lower()
            
            if is_touch_and_go:
                for j in range(i + 1, len(aircraft_event_list)):
                    next_time, next_name, next_event = aircraft_event_list[j]
                    
                    if next_time - timestamp > bounce_window:
                        break
                    
                    if next_name in ('TakenOff', 'Landed'):
                        events_to_keep.discard(i)
                        break
                    
                    next_obj_id, next_ts, next_evt_name, next_evt_params = next_event
                    is_next_touch_and_go = next_evt_name == 'Message' and 'touch-and-go' in next_evt_params.lower()
                    if is_next_touch_and_go and next_time - timestamp < 3.0:
                        events_to_keep.discard(i)
                        break
        
        for idx in sorted(events_to_keep):
            filtered_events.append(aircraft_event_list[idx][2])
    
    removed_count = len(events) - len(filtered_events)
    if removed_count > 0:
        print(f"    Filtered out {removed_count} bounce events")
    
    return filtered_events


def _deduplicate_events(
    events: List[tuple],
    time_window: float = 120.0
) -> List[tuple]:
    """Remove duplicate events within time window."""
    if not events:
        return events
    
    event_groups = {}
    for event in events:
        obj_id, timestamp, event_name, event_params = event
        key = (obj_id, event_name)
        if key not in event_groups:
            event_groups[key] = []
        event_groups[key].append(event)
    
    deduplicated = []
    for key, group_events in event_groups.items():
        group_events.sort(key=lambda x: x[1])
        
        kept_events = []
        for event in group_events:
            obj_id, timestamp, event_name, event_params = event
            
            is_duplicate = False
            for kept_event in kept_events:
                if abs(timestamp - kept_event[1]) < time_window:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                kept_events.append(event)
        
        deduplicated.extend(kept_events)
    
    removed_count = len(events) - len(deduplicated)
    if removed_count > 0:
        print(f"    Deduplicated {removed_count} events")
    
    return deduplicated


def _identify_airbase(
    longitude: float,
    latitude: float,
    airbase_db: Dict[str, Dict],
    threshold: float = 0.05
) -> Optional[str]:
    """Identify airbase from coordinates."""
    for name, coords in airbase_db.items():
        if (abs(longitude - coords.get("lon", 0)) < threshold and
            abs(latitude - coords.get("lat", 0)) < threshold):
            return name
    return None

