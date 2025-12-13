"""Tests for enrichment pipeline."""

import tempfile
import pytest

from tacview_duckdb.parser.types import Transform, ObjectState, TacviewObject
from tacview_duckdb.storage.duckdb_store import DuckDBStore
from tacview_duckdb.enrichment.pipeline import EnrichmentPipeline
from tacview_duckdb.enrichment.coalitions import CoalitionPropagator
from tacview_duckdb.enrichment.ejection_events import EjectionEventEnricher


def test_coalition_propagator():
    """Test coalition propagation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {"Title": "Test", "RecordingTime": "2025-01-01T12:00:00Z"}
        store.initialize_from_metadata(metadata)

        # Create object with color but no coalition
        obj = TacviewObject(
            object_id="1",
            name="Test",
            color="Red",
        )

        objects = [obj]

        # Run enrichment
        enricher = CoalitionPropagator()
        enricher.enrich(objects, store)

        # Check coalition was inferred
        assert obj.coalition == "Enemies"  # Red -> Enemies


def test_enrichment_pipeline():
    """Test enrichment pipeline orchestration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {"Title": "Test", "RecordingTime": "2025-01-01T12:00:00Z"}
        store.initialize_from_metadata(metadata)

        obj = TacviewObject(object_id="1", name="Test", color="Blue")
        objects = [obj]

        # Create pipeline
        pipeline = EnrichmentPipeline(store)
        pipeline.add_enricher(CoalitionPropagator())

        # Run pipeline
        pipeline.run(objects)

        # Check enrichment applied
        assert obj.coalition == "Allies"  # Blue -> Allies


def test_ejection_event_enricher():
    """Test ejection event enrichment."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {"Title": "Test", "RecordingTime": "2025-01-01T12:00:00Z"}
        store.initialize_from_metadata(metadata)
        
        # Create aircraft
        aircraft = TacviewObject(
            object_id="100",
            name="F-16C",
            type="Air+FixedWing",
            pilot="Viper 1",
            coalition="Allies",
        )
        aircraft.type_class = "Air"
        aircraft.type_basic = "FixedWing"
        aircraft.first_seen = 0.0
        aircraft.last_seen = 10.0
        aircraft.add_state(
            ObjectState(
                timestamp=0.0,
                transform=Transform(u=1000, v=1000, altitude=5000),
            )
        )
        aircraft.add_state(
            ObjectState(
                timestamp=10.0,
                transform=Transform(u=1050, v=1050, altitude=4500),
            )
        )
        
        # Create parachutist
        parachutist = TacviewObject(
            object_id="200",
            name="Pilot",
            type="Ground+Light+Human+Air+Parachutist",
            coalition="Allies",
        )
        parachutist.type_class = "Air"
        parachutist.type_attributes = "Light"
        parachutist.type_basic = "Human"
        parachutist.type_specific = "Parachutist"
        parachutist.first_seen = 10.0
        parachutist.last_seen = 60.0
        parachutist.add_state(
            ObjectState(
                timestamp=10.0,
                transform=Transform(u=1050, v=1050, altitude=4500),  # Same position as aircraft
            )
        )
        parachutist.add_state(
            ObjectState(
                timestamp=60.0,
                transform=Transform(u=1060, v=1060, altitude=0),
            )
        )
        
        # Add objects to store
        store.add_objects_bulk([aircraft, parachutist])
        
        # Run ejected pilot enrichment first
        pilot_count = store.enrich_ejected_pilots(
            time_window=0.5,
            proximity_radius=500.0
        )
        assert pilot_count == 1
        
        # Now run ejection event enrichment
        enricher = EjectionEventEnricher()
        event_count = enricher.enrich([], store)
        
        # Should create 1 event per ejection (on the parachutist)
        assert event_count == 1
        
        # Query events from database
        events = store.conn.execute("""
            SELECT object_id, timestamp, event_name, event_params
            FROM events
            ORDER BY object_id
        """).fetchall()
        
        assert len(events) == 1
        
        # Check parachutist event
        pilot_event = events[0]
        assert pilot_event[0] == "200"  # parachutist object_id
        assert pilot_event[1] == 10.0   # ejection timestamp
        assert pilot_event[2] == "Message"
        assert "Viper 1" in pilot_event[3]  # Uses aircraft pilot name
        assert "ejected" in pilot_event[3]


def test_weapon_target_filtering():
    """Test that only missiles can target other weapons."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {"Title": "Test", "RecordingTime": "2025-01-01T12:00:00Z"}
        store.initialize_from_metadata(metadata)
        
        # Create aircraft target
        aircraft = TacviewObject(
            object_id="100",
            name="MiG-29",
            type="Air+FixedWing",
            coalition="Enemies",
        )
        aircraft.type_class = "Air"
        aircraft.type_basic = "FixedWing"
        aircraft.first_seen = 0.0
        aircraft.last_seen = 60.0
        aircraft.add_state(
            ObjectState(
                timestamp=50.0,
                transform=Transform(u=5000, v=5000, altitude=8000),
            )
        )
        
        # Create another missile that could be a target
        target_missile = TacviewObject(
            object_id="200",
            name="R-77",
            type="Weapon+Missile",
            coalition="Enemies",
        )
        target_missile.type_class = "Weapon"
        target_missile.type_basic = "Missile"
        target_missile.first_seen = 40.0
        target_missile.last_seen = 60.0
        target_missile.add_state(
            ObjectState(
                timestamp=50.0,
                transform=Transform(u=5100, v=5100, altitude=8000),  # 141m from aircraft
            )
        )
        
        # Create an interceptor missile (should be able to target the other missile)
        interceptor = TacviewObject(
            object_id="300",
            name="AIM-120",
            type="Weapon+Missile",
            coalition="Allies",
        )
        interceptor.type_class = "Weapon"
        interceptor.type_basic = "Missile"
        interceptor.first_seen = 30.0
        interceptor.last_seen = 50.0
        interceptor.add_state(
            ObjectState(
                timestamp=30.0,
                transform=Transform(u=3000, v=3000, altitude=7000),
            )
        )
        interceptor.add_state(
            ObjectState(
                timestamp=50.0,
                transform=Transform(u=5090, v=5090, altitude=8000),  # Very close to enemy missile
            )
        )
        
        # Create a bomb (should NOT be able to target the missile)
        bomb = TacviewObject(
            object_id="400",
            name="GBU-12",
            type="Weapon+Bomb",
            coalition="Allies",
        )
        bomb.type_class = "Weapon"
        bomb.type_basic = "Bomb"
        bomb.first_seen = 30.0
        bomb.last_seen = 55.0
        bomb.add_state(
            ObjectState(
                timestamp=30.0,
                transform=Transform(u=4000, v=4000, altitude=9000),
            )
        )
        bomb.add_state(
            ObjectState(
                timestamp=55.0,
                transform=Transform(u=5110, v=5110, altitude=8000),  # Very close to enemy missile
            )
        )
        
        # Add objects to store
        store.add_objects_bulk([aircraft, target_missile, interceptor, bomb])
        
        # Run target detection
        target_count = store.enrich_weapon_owners(
            time_window=1.0,
            proximity_radius=150.0,
            use_last_position=True  # Target detection
        )
        
        # Should detect targets for both weapons
        assert target_count >= 1
        
        # Check interceptor missile - should be able to target the enemy missile
        interceptor_data = store.conn.execute("""
            SELECT 
                id,
                json_extract_string(properties, '$.TargetID') as target_id,
                json_extract_string(properties, '$.TargetName') as target_name,
                json_extract_string(properties, '$.Fate') as fate
            FROM objects
            WHERE id = '300'
        """).fetchone()
        
        assert interceptor_data is not None
        # Missile should be able to target another missile
        if interceptor_data[1]:  # If a target was found
            # The target could be either the aircraft or the missile, both are valid for missiles
            assert interceptor_data[1] in ['100', '200']
        
        # Check bomb - should NOT target the missile, should target the aircraft instead
        bomb_data = store.conn.execute("""
            SELECT 
                id,
                json_extract_string(properties, '$.TargetID') as target_id,
                json_extract_string(properties, '$.TargetName') as target_name,
                json_extract_string(properties, '$.Fate') as fate
            FROM objects
            WHERE id = '400'
        """).fetchone()
        
        assert bomb_data is not None
        if bomb_data[1]:  # If a target was found
            # Bomb should ONLY target the aircraft (object_id='100'), NOT the missile
            assert bomb_data[1] == '100', f"Bomb should only target aircraft, not missile. Got target_id={bomb_data[1]}"
            assert bomb_data[2] == 'MiG-29'


def test_weapons_cannot_be_launchers():
    """Test that weapons cannot be detected as launchers for other weapons."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {"Title": "Test", "RecordingTime": "2025-01-01T12:00:00Z"}
        store.initialize_from_metadata(metadata)
        
        # Create an aircraft that is the real launcher
        aircraft = TacviewObject(
            object_id="100",
            name="F-16C",
            type="Air+FixedWing",
            coalition="Allies",
            pilot="Viper 1",
        )
        aircraft.type_class = "Air"
        aircraft.type_basic = "FixedWing"
        aircraft.first_seen = 0.0
        aircraft.last_seen = 60.0
        aircraft.add_state(
            ObjectState(
                timestamp=30.0,
                transform=Transform(u=5000, v=5000, altitude=8000),
            )
        )
        
        # Create a missile that spawns near the aircraft
        missile1 = TacviewObject(
            object_id="200",
            name="AIM-120",
            type="Weapon+Missile",
            coalition="Allies",
        )
        missile1.type_class = "Weapon"
        missile1.type_basic = "Missile"
        missile1.first_seen = 30.0
        missile1.last_seen = 40.0
        missile1.add_state(
            ObjectState(
                timestamp=30.0,
                transform=Transform(u=5010, v=5010, altitude=8000),  # Very close to aircraft
            )
        )
        
        # Create another missile that spawns very close to the first missile
        # (to test if it incorrectly detects the first missile as its launcher)
        missile2 = TacviewObject(
            object_id="300",
            name="AIM-120 #2",
            type="Weapon+Missile",
            coalition="Allies",
        )
        missile2.type_class = "Weapon"
        missile2.type_basic = "Missile"
        missile2.first_seen = 31.0  # Spawns 1 second after first missile
        missile2.last_seen = 41.0
        missile2.add_state(
            ObjectState(
                timestamp=31.0,
                transform=Transform(u=5015, v=5015, altitude=8000),  # Closer to missile1 than aircraft
            )
        )
        
        # Add objects to store
        store.add_objects_bulk([aircraft, missile1, missile2])
        
        # Run launcher detection
        launcher_count = store.enrich_weapon_owners(
            time_window=1.0,
            proximity_radius=150.0,
            use_last_position=False  # Launcher detection
        )
        
        # Should detect launchers for both missiles
        assert launcher_count >= 1
        
        # Check missile1 - should have aircraft as launcher
        missile1_data = store.conn.execute("""
            SELECT 
                id,
                parent_id,
                json_extract_string(properties, '$.LauncherName') as launcher_name
            FROM objects
            WHERE id = '200'
        """).fetchone()
        
        assert missile1_data is not None
        # Missile1 should have aircraft as parent, NOT another weapon
        if missile1_data[1]:  # If a launcher was found
            assert missile1_data[1] == '100', f"Missile1 should have aircraft as launcher, got parent_id={missile1_data[1]}"
            assert missile1_data[2] == 'F-16C'
        
        # Check missile2 - should have aircraft as launcher, NOT the first missile
        missile2_data = store.conn.execute("""
            SELECT 
                id,
                parent_id,
                json_extract_string(properties, '$.LauncherName') as launcher_name
            FROM objects
            WHERE id = '300'
        """).fetchone()
        
        assert missile2_data is not None
        if missile2_data[1]:  # If a launcher was found
            # Missile2 should have aircraft as parent, NOT missile1
            assert missile2_data[1] == '100', f"Missile2 should have aircraft as launcher, NOT another missile. Got parent_id={missile2_data[1]}, launcher_name={missile2_data[2]}"
            assert missile2_data[2] == 'F-16C'


def test_decoy_parent_enrichment():
    """Test decoy parent detection using haversine distance."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {"Title": "Test", "RecordingTime": "2025-01-01T12:00:00Z"}
        store.initialize_from_metadata(metadata)
        
        # Create aircraft that will deploy decoy
        aircraft = TacviewObject(
            object_id="100",
            name="F-16C",
            type_class="Air",
            type_basic="FixedWing",
            coalition="Allies",
            pilot="Viper 1"
        )
        aircraft.first_seen = 10.0
        aircraft.last_seen = 50.0
        
        # Add aircraft state at time of decoy deployment
        aircraft.add_state(
            ObjectState(
                timestamp=20.0,
                # Decoys don't have U/V, so we use lat/lon
                transform=Transform(
                    longitude=45.0,
                    latitude=35.0,
                    altitude=8000.0
                )
            )
        )
        
        # Create decoy deployed by aircraft
        decoy = TacviewObject(
            object_id="200",
            name="Chaff",
            type_basic="Decoy",
            coalition="Allies"
        )
        decoy.first_seen = 20.0
        decoy.last_seen = 25.0
        
        # Decoy position near aircraft (using lat/lon, not U/V)
        # ~100m away from aircraft
        decoy.add_state(
            ObjectState(
                timestamp=20.0,
                transform=Transform(
                    longitude=45.001,  # ~100m east
                    latitude=35.0,
                    altitude=7950.0  # 50m below
                )
            )
        )
        
        # Add objects to store
        store.add_objects_bulk([aircraft, decoy])
        
        # Run decoy enrichment
        decoy_count = store.enrich_decoy_parents(
            time_window=1.0,
            proximity_radius=500.0
        )
        
        # Should enrich the decoy
        assert decoy_count == 1
        
        # Check decoy has correct parent
        decoy_data = store.conn.execute("""
            SELECT 
                id,
                parent_id,
                json_extract_string(properties, '$.ParentName') as parent_name,
                json_extract_string(properties, '$.ParentType') as parent_type,
                json_extract_string(properties, '$.DeploymentRange') as deployment_range
            FROM objects
            WHERE id = '200'
        """).fetchone()
        
        assert decoy_data is not None
        assert decoy_data[1] == '100', f"Decoy should have aircraft as parent, got parent_id={decoy_data[1]}"
        assert decoy_data[2] == 'F-16C'
        assert 'FixedWing' in decoy_data[3]
        
        # Check deployment range is reasonable (~100m horizontal + 50m vertical = ~112m)
        if decoy_data[4]:
            deployment_range = float(decoy_data[4])
            assert 100 < deployment_range < 150, f"Deployment range {deployment_range}m seems incorrect"

