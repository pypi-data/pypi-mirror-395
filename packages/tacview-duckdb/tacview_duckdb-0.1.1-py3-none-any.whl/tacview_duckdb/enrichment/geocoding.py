"""Geocoding support using geopy with Photon and Nominatim.

This module provides forward and reverse geocoding functionality with automatic
fallback between providers.

Providers:
- Photon (primary): Fast, unlimited, no rate limits
  - No API key required
  - Based on OpenStreetMap data with Elasticsearch
  - Automatically falls back to Nominatim if unavailable
- Nominatim (fallback): Reliable, 1 req/sec
  - No API key required
  - Used when Photon is down or blocked (e.g., VPN)

Configuration:
- No configuration needed - both providers are free and require no API keys
- .env file support is automatic if python-dotenv is installed
"""

import os
from typing import Optional

# Optional .env file support
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # python-dotenv not installed, use shell environment variables only

# Optional geopy import
try:
    from geopy.geocoders import Photon, Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False


# Global state for geocoder instances
_photon_instance = None
_nominatim_instance = None

# Caching for geocoding results
_geocode_cache = {}  # Cache for reverse geocoding: (lat, lon, lang) -> location_string
_forward_cache = {}  # Cache for forward geocoding: location_name -> (lat, lon)
_cache_max_size = 1000  # Maximum cache entries


def get_geocoders(user_agent: str = "py-tacview-duckdb") -> tuple:
    """
    Get or create geocoder instances (Photon primary, Nominatim fallback).
    
    Returns both geocoders for automatic fallback:
    - Photon: Fast, unlimited, no rate limits (may be blocked by some VPNs)
    - Nominatim: Reliable, 1 req/sec (always works)
    
    Args:
        user_agent: User agent string for Nominatim
        
    Returns:
        Tuple of (photon, nominatim) geocoder instances, or (None, None) if geopy not available
    """
    global _photon_instance, _nominatim_instance
    
    if not GEOPY_AVAILABLE:
        return None, None
    
    # Create Photon instance if needed
    if _photon_instance is None:
        _photon_instance = Photon(timeout=5)
        print("Using Photon geocoder (primary, fast, unlimited)")
    
    # Create Nominatim instance if needed
    if _nominatim_instance is None:
        _nominatim_instance = Nominatim(user_agent=user_agent, timeout=10)
        print("Using Nominatim geocoder (fallback, reliable, 1 req/sec)")
    
    return _photon_instance, _nominatim_instance




def clear_geocoding_cache():
    """Clear the geocoding cache. Useful for freeing memory or forcing fresh lookups."""
    global _geocode_cache, _forward_cache
    _geocode_cache.clear()
    _forward_cache.clear()


def forward_geocode(location_name: str, timeout: int = 2) -> Optional[tuple]:
    """
    Get coordinates from a location name (forward geocoding) with caching.
    
    Uses Photon (primary, fast) with Nominatim fallback.
    Results are cached in memory (up to 1000 entries).
    
    Args:
        location_name: Location to search for (e.g., "Damascus, Syria", "Nellis AFB")
        timeout: Request timeout in seconds (default: 2)
        
    Returns:
        Tuple of (latitude, longitude) or None if lookup fails
    """
    global _forward_cache, _cache_max_size
    
    # Normalize location name for cache key (lowercase, strip whitespace)
    cache_key = location_name.lower().strip()
    
    # Check cache first
    if cache_key in _forward_cache:
        return _forward_cache[cache_key]
    
    photon, nominatim = get_geocoders()
    if not photon and not nominatim:
        return None
    
    result = None
    
    # Try Photon first (force English)
    if photon:
        try:
            location = photon.geocode(location_name, language='en', timeout=timeout)
            if location:
                result = (location.latitude, location.longitude)
        except Exception:
            pass  # Try fallback
    
    # Fallback to Nominatim if Photon failed
    if result is None and nominatim:
        try:
            location = nominatim.geocode(location_name, timeout=timeout)
            if location:
                result = (location.latitude, location.longitude)
        except Exception:
            pass  # Silently fail - geocoding is optional
    
    # Cache the result (LRU eviction when full)
    if len(_forward_cache) >= _cache_max_size:
        # Remove oldest entry (first key)
        _forward_cache.pop(next(iter(_forward_cache)))
    
    _forward_cache[cache_key] = result
    return result


def reverse_geocode(
    latitude: float,
    longitude: float,
    language: str = "en",
    timeout: int = 2
) -> Optional[str]:
    """
    Get human-readable location from coordinates using reverse geocoding.
    
    Uses Photon (primary, fast) with Nominatim fallback.
    Results are cached in memory (up to 1000 entries).
    
    Provider details:
    - Photon: Unlimited requests, no rate limits, forced English (may be blocked by VPNs)
    - Nominatim: Unlimited requests, 1 req/sec rate limit (always works, respects language param)
    
    Args:
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        language: Language code for results (default: "en")
        timeout: Request timeout in seconds (default: 2)
        
    Returns:
        Location string like "Damascus, Syria" or None if lookup fails
    """
    global _geocode_cache, _cache_max_size
    
    # Round coordinates to 3 decimal places (~100m precision) for cache key
    cache_key = (round(latitude, 3), round(longitude, 3), language)
    
    # Check cache first
    if cache_key in _geocode_cache:
        return _geocode_cache[cache_key]
    
    photon, nominatim = get_geocoders()
    if not photon and not nominatim:
        return None
    
    location = None
    
    # Try Photon first (force English with language='en')
    if photon:
        try:
            location = photon.reverse(
                f"{latitude}, {longitude}",
                exactly_one=True,
                language='en',
                timeout=timeout
            )
        except Exception:
            pass  # Try fallback
    
    # Fallback to Nominatim if Photon failed
    if not location and nominatim:
        try:
            location = nominatim.reverse(
                f"{latitude}, {longitude}",
                language=language,
                exactly_one=True,
                timeout=timeout
            )
        except Exception:
            pass  # Silently fail
    
    # Process result
    if not location:
        result = None
    else:
        # Extract useful parts from address
        # Photon uses 'properties' key, Nominatim uses 'address' key
        address = location.raw.get('properties', location.raw.get('address', {}))
        
        # Build location string from most specific to least
        parts = []
        
        # City/town/village
        city = (address.get('city') or 
                address.get('town') or 
                address.get('village') or
                address.get('municipality'))
        if city:
            parts.append(city)
        
        # Region/state (if different from city)
        region = (address.get('state') or 
                  address.get('region') or
                  address.get('province'))
        if region and region != city:
            parts.append(region)
        
        # Country
        country = address.get('country')
        if country:
            parts.append(country)
        
        # Fallback to display name if no parts
        if not parts:
            result = location.address.split(',')[0]  # First part of address
        else:
            # Format: "Damascus, Syria" or "Aleppo, Aleppo Governorate, Syria"
            result = ", ".join(parts)
    
    # Cache the result (LRU eviction when full)
    if len(_geocode_cache) >= _cache_max_size:
        # Remove oldest entry (first key)
        _geocode_cache.pop(next(iter(_geocode_cache)))
    
    _geocode_cache[cache_key] = result
    return result

