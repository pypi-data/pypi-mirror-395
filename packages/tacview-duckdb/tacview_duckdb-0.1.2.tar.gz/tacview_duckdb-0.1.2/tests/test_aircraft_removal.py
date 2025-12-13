#!/usr/bin/env python3
"""Tests for aircraft removal detection in lifecycle enrichers."""

import pytest
import duckdb
from tacview_duckdb.enrichment.lifecycle import FixedWingEnricher, RotorcraftEnricher


def test_fixedwing_removal_detector_basic():
    """Test basic aircraft removal detection for fixed-wing."""
    # Create in-memory database with test data
    conn = duckdb.connect(":memory:")
    
    # Create tables
    conn.execute("""
        CREATE TABLE objects (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            type_class VARCHAR,
            type_basic VARCHAR,
            type_specific VARCHAR,
            pilot VARCHAR,
            first_seen DOUBLE,
            last_seen DOUBLE,
            removed_at DOUBLE
        )
    """)
    
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS states_id_seq START 1
    """)
    
    conn.execute("""
        CREATE TABLE states (
            id BIGINT PRIMARY KEY DEFAULT nextval('states_id_seq'),
            object_id VARCHAR,
            timestamp DOUBLE,
            speed DOUBLE,
            altitude DOUBLE,
            longitude DOUBLE,
            latitude DOUBLE,
            heading DOUBLE
        )
    """)
    
    conn.execute("""
        CREATE TABLE events (
            object_id VARCHAR,
            timestamp DOUBLE,
            event_name VARCHAR,
            event_params VARCHAR,
            PRIMARY KEY (object_id, timestamp, event_name)
        )
    """)
    
    # Insert test aircraft
    conn.execute("""
        INSERT INTO objects VALUES
        ('1', 'HighSpeedAircraft', 'Air', 'FixedWing', 'F-16C', 'Pilot1', 10.0, 100.0, 100.0),
        ('2', 'LowSpeedAircraft', 'Air', 'FixedWing', 'F-16C', 'Pilot2', 10.0, 200.0, 200.0),
        ('3', 'MediumSpeedAircraft', 'Air', 'FixedWing', 'F-16C', 'Pilot3', 10.0, 300.0, 300.0),
        ('4', 'GroundUnit', 'Ground', 'Tank', 'T-72', NULL, 10.0, 400.0, 400.0)
    """)
    
    # Insert states for high-speed aircraft (should be marked as Destroyed)
    conn.execute("""
        INSERT INTO states (object_id, timestamp, speed, altitude, longitude, latitude) VALUES
        ('1', 98.0, 100.0, 1000.0, 0.0, 0.0),
        ('1', 99.0, 120.0, 900.0, 0.0, 0.0),
        ('1', 100.0, 110.0, 800.0, 0.0, 0.0)
    """)
    
    # Insert states for low-speed aircraft (should be marked as LeftArea)
    conn.execute("""
        INSERT INTO states (object_id, timestamp, speed, altitude, longitude, latitude) VALUES
        ('2', 198.0, 0.5, 100.0, 0.0, 0.0),
        ('2', 199.0, 0.3, 100.0, 0.0, 0.0),
        ('2', 200.0, 0.2, 100.0, 0.0, 0.0)
    """)
    
    # Insert states for medium-speed aircraft (should be skipped - ambiguous)
    conn.execute("""
        INSERT INTO states (object_id, timestamp, speed, altitude, longitude, latitude) VALUES
        ('3', 298.0, 15.0, 500.0, 0.0, 0.0),
        ('3', 299.0, 20.0, 500.0, 0.0, 0.0),
        ('3', 300.0, 18.0, 500.0, 0.0, 0.0)
    """)
    
    # Insert states for ground unit (should be ignored - not Air type)
    conn.execute("""
        INSERT INTO states (object_id, timestamp, speed, altitude, longitude, latitude) VALUES
        ('4', 398.0, 50.0, 0.0, 0.0, 0.0),
        ('4', 399.0, 60.0, 0.0, 0.0, 0.0),
        ('4', 400.0, 55.0, 0.0, 0.0, 0.0)
    """)
    
    # Run enricher
    enricher = FixedWingEnricher(
        destruction_speed_threshold=30.0,
        clean_removal_speed_threshold=1.0,
        num_states_to_check=3,
        detect_removals=True
    )
    
    enricher.enrich([], conn)
    
    # Check events
    events = conn.execute("""
        SELECT object_id, event_name 
        FROM events
        WHERE event_name IN ('Destroyed', 'LeftArea')
        ORDER BY object_id
    """).fetchall()
    
    assert len(events) == 2
    assert events[0] == ('1', 'Destroyed')  # High speed
    assert events[1] == ('2', 'LeftArea')   # Low speed
    
    conn.close()


def test_rotorcraft_removal_detector():
    """Test removal detection for rotorcraft."""
    conn = duckdb.connect(":memory:")
    
    # Create tables
    conn.execute("""
        CREATE TABLE objects (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            type_class VARCHAR,
            type_basic VARCHAR,
            type_specific VARCHAR,
            pilot VARCHAR,
            first_seen DOUBLE,
            last_seen DOUBLE,
            removed_at DOUBLE
        )
    """)
    
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS states_id_seq START 1
    """)
    
    conn.execute("""
        CREATE TABLE states (
            id BIGINT PRIMARY KEY DEFAULT nextval('states_id_seq'),
            object_id VARCHAR,
            timestamp DOUBLE,
            speed DOUBLE,
            altitude DOUBLE,
            longitude DOUBLE,
            latitude DOUBLE,
            heading DOUBLE
        )
    """)
    
    conn.execute("""
        CREATE TABLE events (
            object_id VARCHAR,
            timestamp DOUBLE,
            event_name VARCHAR,
            event_params VARCHAR,
            PRIMARY KEY (object_id, timestamp, event_name)
        )
    """)
    
    # Insert test helicopter
    conn.execute("""
        INSERT INTO objects VALUES
        ('1', 'Apache', 'Air', 'Rotorcraft', 'AH-64D', 'Pilot1', 10.0, 100.0, 100.0)
    """)
    
    # High speed crash
    conn.execute("""
        INSERT INTO states (object_id, timestamp, speed, altitude, longitude, latitude) VALUES
        ('1', 98.0, 40.0, 50.0, 0.0, 0.0),
        ('1', 99.0, 45.0, 30.0, 0.0, 0.0),
        ('1', 100.0, 50.0, 10.0, 0.0, 0.0)
    """)
    
    # Run enricher
    enricher = RotorcraftEnricher(
        destruction_speed_threshold=30.0,
        clean_removal_speed_threshold=1.0,
        num_states_to_check=3,
        detect_removals=True
    )
    
    enricher.enrich([], conn)
    
    # Check event
    event = conn.execute("""
        SELECT event_name 
        FROM events
        WHERE event_name IN ('Destroyed', 'LeftArea')
    """).fetchone()
    
    assert event is not None
    assert event[0] == 'Destroyed'
    
    conn.close()


def test_removal_detector_custom_thresholds():
    """Test detector with custom thresholds."""
    conn = duckdb.connect(":memory:")
    
    # Create tables
    conn.execute("""
        CREATE TABLE objects (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            type_class VARCHAR,
            type_basic VARCHAR,
            type_specific VARCHAR,
            pilot VARCHAR,
            first_seen DOUBLE,
            last_seen DOUBLE,
            removed_at DOUBLE
        )
    """)
    
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS states_id_seq START 1
    """)
    
    conn.execute("""
        CREATE TABLE states (
            id BIGINT PRIMARY KEY DEFAULT nextval('states_id_seq'),
            object_id VARCHAR,
            timestamp DOUBLE,
            speed DOUBLE,
            altitude DOUBLE,
            longitude DOUBLE,
            latitude DOUBLE,
            heading DOUBLE
        )
    """)
    
    conn.execute("""
        CREATE TABLE events (
            object_id VARCHAR,
            timestamp DOUBLE,
            event_name VARCHAR,
            event_params VARCHAR,
            PRIMARY KEY (object_id, timestamp, event_name)
        )
    """)
    
    # Insert test aircraft with moderate speed
    conn.execute("""
        INSERT INTO objects VALUES
        ('1', 'ModerateSpeedAircraft', 'Air', 'FixedWing', 'F-16C', 'Pilot1', 10.0, 100.0, 100.0)
    """)
    
    conn.execute("""
        INSERT INTO states (object_id, timestamp, speed, altitude, longitude, latitude) VALUES
        ('1', 98.0, 25.0, 500.0, 0.0, 0.0),
        ('1', 99.0, 20.0, 500.0, 0.0, 0.0),
        ('1', 100.0, 30.0, 500.0, 0.0, 0.0)
    """)
    
    # With default thresholds (30 m/s), this should be skipped
    enricher_default = FixedWingEnricher(detect_removals=True)
    enricher_default.enrich([], conn)
    
    events_default = conn.execute("""
        SELECT COUNT(*) FROM events WHERE event_name IN ('Destroyed', 'LeftArea')
    """).fetchone()
    assert events_default[0] == 0  # Ambiguous speed
    
    # With custom lower threshold (20 m/s), should be marked as destroyed
    enricher_custom = FixedWingEnricher(
        destruction_speed_threshold=20.0,
        clean_removal_speed_threshold=1.0,
        num_states_to_check=3,
        detect_removals=True
    )
    
    # Clear previous events
    conn.execute("DELETE FROM events")
    
    enricher_custom.enrich([], conn)
    
    event = conn.execute("""
        SELECT event_name FROM events WHERE event_name IN ('Destroyed', 'LeftArea')
    """).fetchone()
    assert event is not None
    assert event[0] == 'Destroyed'
    
    conn.close()


def test_removal_detector_only_air_objects():
    """Test that detector only processes Air type objects."""
    conn = duckdb.connect(":memory:")
    
    # Create tables
    conn.execute("""
        CREATE TABLE objects (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            type_class VARCHAR,
            type_basic VARCHAR,
            type_specific VARCHAR,
            pilot VARCHAR,
            first_seen DOUBLE,
            last_seen DOUBLE,
            removed_at DOUBLE
        )
    """)
    
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS states_id_seq START 1
    """)
    
    conn.execute("""
        CREATE TABLE states (
            id BIGINT PRIMARY KEY DEFAULT nextval('states_id_seq'),
            object_id VARCHAR,
            timestamp DOUBLE,
            speed DOUBLE,
            altitude DOUBLE,
            longitude DOUBLE,
            latitude DOUBLE,
            heading DOUBLE
        )
    """)
    
    conn.execute("""
        CREATE TABLE events (
            object_id VARCHAR,
            timestamp DOUBLE,
            event_name VARCHAR,
            event_params VARCHAR,
            PRIMARY KEY (object_id, timestamp, event_name)
        )
    """)
    
    # Insert various object types, all with high speed
    conn.execute("""
        INSERT INTO objects VALUES
        ('1', 'Aircraft', 'Air', 'FixedWing', 'F-16C', 'Pilot1', 10.0, 100.0, 100.0),
        ('2', 'Tank', 'Ground', 'Tank', 'T-72', NULL, 10.0, 200.0, 200.0),
        ('3', 'Ship', 'Sea', 'Ship', 'Destroyer', NULL, 10.0, 300.0, 300.0),
        ('4', 'Missile', 'Weapon', 'Missile', 'AIM-120', NULL, 10.0, 400.0, 400.0)
    """)
    
    # All have high-speed states
    for obj_id in ['1', '2', '3', '4']:
        removal_time = float(obj_id) * 100.0
        conn.execute(f"""
            INSERT INTO states (object_id, timestamp, speed, altitude, longitude, latitude) VALUES
            ('{obj_id}', {removal_time - 2.0}, 100.0, 1000.0, 0.0, 0.0),
            ('{obj_id}', {removal_time - 1.0}, 120.0, 900.0, 0.0, 0.0),
            ('{obj_id}', {removal_time}, 110.0, 800.0, 0.0, 0.0)
        """)
    
    # Run detector
    enricher = FixedWingEnricher(detect_removals=True)
    enricher.enrich([], conn)
    
    # Should only detect the Air type object
    events = conn.execute("""
        SELECT object_id FROM events WHERE event_name IN ('Destroyed', 'LeftArea')
    """).fetchall()
    
    assert len(events) == 1
    assert events[0][0] == '1'  # Only the Air type
    
    conn.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
