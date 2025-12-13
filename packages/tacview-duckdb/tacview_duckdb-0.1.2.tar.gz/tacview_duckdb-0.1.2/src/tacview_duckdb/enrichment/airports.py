"""Airport enrichment using OurAirports data.

This module provides functionality to enrich landing/takeoff events with
airport information from the OurAirports open data project.

For geocoding functionality (reverse/forward geocoding), see the geocoding module.

Data sources:
- OurAirports: https://github.com/davidmegginson/ourairports-data
"""

import os
import urllib.request
import csv
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta

# Import geocoding functionality from geocoding module
from . import geocoding


# OurAirports CSV URL
AIRPORTS_CSV_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"

# Cache location (in user's home directory)
CACHE_DIR = Path.home() / ".cache" / "py-tacview-duckdb"
AIRPORTS_CACHE_FILE = CACHE_DIR / "airports.csv"
CACHE_MAX_AGE_DAYS = 30  # Re-download after 30 days


def _ensure_cache_dir() -> None:
    """Ensure cache directory exists."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _is_cache_valid() -> bool:
    """Check if cached airport data is still valid."""
    if not AIRPORTS_CACHE_FILE.exists():
        return False
    
    # Check age
    file_age = datetime.now() - datetime.fromtimestamp(AIRPORTS_CACHE_FILE.stat().st_mtime)
    return file_age < timedelta(days=CACHE_MAX_AGE_DAYS)


def download_airports_data(force: bool = False) -> Path:
    """
    Download OurAirports data and cache it locally.
    
    Args:
        force: Force re-download even if cache is valid
        
    Returns:
        Path to cached CSV file
    """
    _ensure_cache_dir()
    
    if not force and _is_cache_valid():
        return AIRPORTS_CACHE_FILE
    
    print(f"Downloading airport data from {AIRPORTS_CSV_URL}...")
    try:
        urllib.request.urlretrieve(AIRPORTS_CSV_URL, AIRPORTS_CACHE_FILE)
        print(f"Airport data cached to {AIRPORTS_CACHE_FILE}")
    except Exception as e:
        # If download fails but we have old cache, use it
        if AIRPORTS_CACHE_FILE.exists():
            print(f"Download failed ({e}), using cached data from {AIRPORTS_CACHE_FILE}")
        else:
            raise RuntimeError(f"Failed to download airport data: {e}")
    
    return AIRPORTS_CACHE_FILE


def load_airports_to_duckdb(conn, table_name: str = "temp_airports") -> int:
    """
    Load airport data into a temporary DuckDB table.
    
    Args:
        conn: DuckDB connection
        table_name: Name for the temporary table
        
    Returns:
        Number of airports loaded
    """
    # Ensure we have the data
    csv_path = download_airports_data()
    
    # Create temporary table directly from CSV using read_csv
    # DuckDB automatically detects CSV configuration and column types
    conn.execute(f"""
        CREATE TEMPORARY TABLE IF NOT EXISTS {table_name} AS
        SELECT * FROM read_csv('{csv_path}', header=true)
    """)
    
    # Get count
    count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"Loaded {count:,} airports into temporary table '{table_name}'")
    
    return count


def find_nearest_airport(
    conn,
    latitude: float,
    longitude: float,
    max_distance_km: float = 10.0,
    table_name: str = "temp_airports",
    airport_types: Optional[List[str]] = None
) -> Optional[Dict]:
    """
    Find the nearest airport to given coordinates.
    
    Uses approximate distance calculation (faster than Haversine).
    
    Args:
        conn: DuckDB connection
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        max_distance_km: Maximum distance to search (default 10 km)
        table_name: Name of the airports table
        airport_types: Optional list of airport types to filter
                      (e.g., ['large_airport', 'medium_airport', 'small_airport'])
        
    Returns:
        Dictionary with airport info, or None if no airport found within range
    """
    if airport_types is None:
        airport_types = ['large_airport', 'medium_airport', 'small_airport', 'seaplane_base']
    
    # Build type filter
    type_filter = "AND type IN ({})".format(
        ','.join(f"'{t}'" for t in airport_types)
    ) if airport_types else ""
    
    # Use approximate distance calculation (returns meters, convert to km)
    query = f"""
        WITH distances AS (
            SELECT
                *,
                -- Approximate distance calculation (faster than Haversine)
                SQRT(calculate_approximate_distance_squared(
                    ? - latitude_deg,
                    ? - longitude_deg
                )) / 1000.0 as distance_km
            FROM {table_name}
            WHERE latitude_deg IS NOT NULL
              AND longitude_deg IS NOT NULL
              {type_filter}
        )
        SELECT
            id,
            ident,
            type,
            name,
            latitude_deg,
            longitude_deg,
            elevation_ft,
            continent,
            iso_country,
            iso_region,
            municipality,
            icao_code,
            iata_code,
            gps_code,
            local_code,
            distance_km
        FROM distances
        WHERE distance_km <= ?
        ORDER BY distance_km
        LIMIT 1
    """
    
    result = conn.execute(query, [latitude, longitude, max_distance_km]).fetchone()
    
    if not result:
        return None
    
    return {
        'id': result[0],
        'ident': result[1],
        'type': result[2],
        'name': result[3],
        'latitude': result[4],
        'longitude': result[5],
        'elevation_ft': result[6],
        'continent': result[7],
        'iso_country': result[8],
        'iso_region': result[9],
        'municipality': result[10],
        'icao_code': result[11],
        'iata_code': result[12],
        'gps_code': result[13],
        'local_code': result[14],
        'distance_km': result[15]
    }


def format_airport_description(airport: Dict, include_codes: bool = True) -> str:
    """
    Format airport information into a human-readable string.
    
    Args:
        airport: Airport dictionary from find_nearest_airport
        include_codes: Include ICAO/IATA codes in output
        
    Returns:
        Formatted string like "Nellis AFB (KLSV)" or "Creech AFB"
    """
    name = airport['name']
    
    if not include_codes:
        return name
    
    # Prefer ICAO code, fall back to IATA, GPS, or ident
    code = (
        airport.get('icao_code') or 
        airport.get('iata_code') or 
        airport.get('gps_code') or 
        airport.get('ident')
    )
    
    if code and code.strip():
        return f"{name} ({code})"
    
    return name


def cleanup_airports_table(conn, table_name: str = "temp_airports") -> None:
    """
    Drop the temporary airports table.
    
    Args:
        conn: DuckDB connection
        table_name: Name of the temporary table to drop
    """
    try:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    except Exception as e:
        # Ignore errors during cleanup
        pass


def format_location(
    latitude: float,
    longitude: float,
    max_distance_km: float = 5.0,
    use_airports: bool = True,
    use_geocoding: bool = False,
    conn = None,
    airport_table: str = "temp_airports"
) -> str:
    """
    Get best human-readable location string for coordinates.
    
    Tries multiple methods in priority order:
    1. Nearby airport (if use_airports and within max_distance_km)
    2. Reverse geocoding (if use_geocoding and geopy available)
    3. Raw coordinates (fallback)
    
    Args:
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        max_distance_km: Maximum distance for airport matching
        use_airports: Try airport database first
        use_geocoding: Try reverse geocoding if airport not found
        conn: DuckDB connection (required if use_airports=True)
        airport_table: Airport table name (if use_airports=True)
        
    Returns:
        Location string like "Beirut Airport (OLBA)" or "near Damascus, Syria"
    """
    # Try airport database first (most specific)
    if use_airports and conn:
        airport = find_nearest_airport(
            conn, latitude, longitude,
            max_distance_km=max_distance_km,
            table_name=airport_table
        )
        if airport:
            return format_airport_description(airport)
    
    # Try reverse geocoding (general location)
    if use_geocoding:
        location = geocoding.reverse_geocode(latitude, longitude)
        if location:
            return f"near {location}"
    
    # Fallback to coordinates
    return f"Location ({latitude:.3f}, {longitude:.3f})"

