"""Event geodata enrichment."""

import time
import re
from typing import Optional, List
import duckdb

from .pipeline import Enricher


class EventGeodataEnricher(Enricher):
    """
    Retroactively enriches events containing coordinates with location names.
    
    Scans events table for "Location (lat, lon)" patterns and replaces them
    with human-readable location names using:
    1. Nearby airport names (if within max_distance_km)
    2. Reverse geocoding via geopy (if use_geocoding=True and geopy available)
    3. Coordinates (fallback if both above fail)
    """
    
    def __init__(
        self,
        max_distance_km: float = 5.0,
        airport_types: Optional[List[str]] = None,
        use_geocoding: bool = True
    ):
        """
        Initialize event geodata enricher.
        
        Args:
            max_distance_km: Maximum distance to search for airports (default: 5 km)
            airport_types: Optional list of airport types to include
            use_geocoding: Use geopy reverse geocoding (default: True)
        """
        self.max_distance_km = max_distance_km
        self.airport_types = airport_types
        self.use_geocoding = use_geocoding
    
    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run event geodata enrichment.
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of events updated with location data
        """
        # Load airport database
        try:
            from . import airports, geocoding
            airports.load_airports_to_duckdb(conn, table_name="temp_airports_geodata")
        except Exception as e:
            print(f"Warning: Failed to load airport database: {e}")
            return 0
        
        try:
            # Find all events with coordinate patterns for takeoff, landing, destruction, and ejection events
            # Matches format from lifecycle.py:
            # "has taken off from (lat, lon)" or "has landed at (lat, lon)" - lifecycle events
            # Coordinates appear after "from " or "at " and have decimal points (e.g., 33.826, 35.503)
            # Valid event types: TakenOff, Landed, Destroyed (includes crashes), Message (ejections)
            events_with_coords = conn.execute("""
                SELECT 
                    object_id,
                    timestamp,
                    event_name,
                    event_params,
                    CAST(REGEXP_EXTRACT(event_params, '(?:from|at)\\s+\\(([-0-9]+\\.[0-9]+),\\s*([-0-9]+\\.[0-9]+)\\)', 1) AS DOUBLE) as latitude,
                    CAST(REGEXP_EXTRACT(event_params, '(?:from|at)\\s+\\(([-0-9]+\\.[0-9]+),\\s*([-0-9]+\\.[0-9]+)\\)', 2) AS DOUBLE) as longitude
                FROM events
                WHERE event_name IN ('TakenOff', 'Landed', 'Destroyed', 'Message')
                  AND (event_params LIKE '%from (%' OR event_params LIKE '%at (%')
                  AND REGEXP_EXTRACT(event_params, '(?:from|at)\\s+\\(([-0-9]+\\.[0-9]+),\\s*([-0-9]+\\.[0-9]+)\\)', 1) IS NOT NULL
            """).fetchall()
            
            if not events_with_coords:
                return 0
            
            print(f"Found {len(events_with_coords)} events with coordinates to enrich...")
            
            # Rate limiting
            last_geocode_time = 0
            
            updates = []
            airport_matches = 0
            geocode_matches = 0
            
            for obj_id, ts, event_name, old_params, lat, lon in events_with_coords:
                if lat is None or lon is None:
                    continue
                
                location_name = None
                
                # Try airport database first
                airport = airports.find_nearest_airport(
                    conn,
                    lat,
                    lon,
                    max_distance_km=self.max_distance_km,
                    table_name="temp_airports_geodata",
                    airport_types=self.airport_types
                )
                
                if airport:
                    # Found airport match - use it and skip geocoding API
                    location_name = airports.format_airport_description(airport)
                    airport_matches += 1
                elif self.use_geocoding:
                    # Only try geocoding API if no airport match was found
                    # Rate limit: wait at least 1 second between requests
                    current_time = time.time()
                    if current_time - last_geocode_time < 1.0:
                        time.sleep(1.0 - (current_time - last_geocode_time))
                    
                    geocoded = geocoding.reverse_geocode(lat, lon)
                    last_geocode_time = time.time()
                    
                    if geocoded:
                        location_name = f"near {geocoded}"
                        geocode_matches += 1
                
                # Update if we found a better name
                if location_name:
                    # Use regex to replace coordinate patterns, preserving coordinates
                    # Matches lifecycle.py format:
                    # "has taken off from (lat, lon)" -> "has taken off from {location_name} (lat, lon)"
                    # "has landed at (lat, lon)" -> "has landed at {location_name} (lat, lon)"
                    # Use the actual coordinates we extracted to ensure exact match
                    coord_str = f'({lat:.3f}, {lon:.3f})'
                    pattern = r'(from|at)\s+' + re.escape(coord_str)
                    new_params = re.sub(pattern, f'\\1 {location_name} {coord_str}', old_params)
                    updates.append((new_params, obj_id, ts, event_name))
            
            # Bulk update events
            if updates:
                conn.executemany("""
                    UPDATE events
                    SET event_params = ?
                    WHERE object_id = ?
                      AND timestamp = ?
                      AND event_name = ?
                """, updates)
                
                print(f"✓ Enriched {len(updates)} events:")
                print(f"  - {airport_matches} with airport names")
                if self.use_geocoding:
                    print(f"  - {geocode_matches} with reverse geocoding")
            
            return len(updates)
        
        finally:
            # Cleanup
            from . import airports
            airports.cleanup_airports_table(conn, table_name="temp_airports_geodata")

