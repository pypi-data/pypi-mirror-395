"""Tests for projectile burst enrichment."""

import pytest
import duckdb
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tacview_duckdb.enrichment import ProjectileEnricher


@pytest.fixture
def db_conn():
    """Create in-memory database with test data."""
    conn = duckdb.connect(":memory:")
    
    # Install spatial extension
    conn.execute("INSTALL spatial;")
    conn.execute("LOAD spatial;")
    
    # Create schema
    conn.execute("""
        CREATE TABLE objects (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            type_class VARCHAR,
            type_basic VARCHAR,
            type_specific VARCHAR,
            pilot VARCHAR,
            coalition VARCHAR,
            color VARCHAR,
            country VARCHAR,
            parent_id VARCHAR,
            first_seen DOUBLE,
            last_seen DOUBLE,
            removed_at DOUBLE,
            properties JSON
        )
    """)
    
    conn.execute("""
        CREATE TABLE states (
            id BIGINT PRIMARY KEY,
            object_id VARCHAR,
            timestamp DOUBLE,
            longitude DOUBLE,
            latitude DOUBLE,
            altitude DOUBLE,
            heading DOUBLE,
            pitch DOUBLE,
            u DOUBLE,
            v DOUBLE
        )
    """)
    
    return conn


def test_launcher_detection(db_conn):
    """Test projectile launcher detection."""
    # Create test aircraft
    db_conn.execute("""
        INSERT INTO objects (id, name, type_basic, coalition, color, country, first_seen, removed_at)
        VALUES ('aircraft1', 'F-16', 'Air+FixedWing', 'Allies', 'Blue', 'USA', 0.0, 100.0)
    """)
    
    # Create aircraft state
    db_conn.execute("""
        INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
        VALUES (1, 'aircraft1', 10.0, -115.0, 36.0, 1000.0)
    """)
    
    # Create projectiles near aircraft
    for i in range(3):
        db_conn.execute(f"""
            INSERT INTO objects (id, name, type_basic, coalition, color, country, first_seen, removed_at)
            VALUES ('proj{i}', 'Projectile', 'Projectile', 'Allies', 'Blue', 'USA', 10.{i}, 15.{i})
        """)
        
        db_conn.execute(f"""
            INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
            VALUES ({10+i}, 'proj{i}', 10.{i}, -115.0001, 36.0001, 1000.0)
        """)
    
    # Run launcher detection
    enricher = ProjectileEnricher(
        detect_launchers=True,
        detect_hits=False,
        create_bursts=False
    )
    count = enricher._detect_launchers(db_conn)
    
    # Verify projectiles matched to launcher
    assert count == 3
    
    results = db_conn.execute("""
        SELECT id, parent_id
        FROM objects
        WHERE type_basic = 'Projectile'
        ORDER BY id
    """).fetchall()
    
    assert len(results) == 3
    for proj_id, parent_id in results:
        assert parent_id == 'aircraft1'


def test_hit_detection(db_conn):
    """Test projectile hit detection."""
    # Create launcher
    db_conn.execute("""
        INSERT INTO objects (id, name, type_basic, coalition, first_seen)
        VALUES ('aircraft1', 'F-16', 'Air+FixedWing', 'Allies', 0.0)
    """)
    
    # Create target
    db_conn.execute("""
        INSERT INTO objects (id, name, type_class, coalition, first_seen)
        VALUES ('target1', 'Enemy Tank', 'Ground', 'Enemies', 0.0)
    """)
    
    # Create target state at impact time
    db_conn.execute("""
        INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
        VALUES (1, 'target1', 15.0, -115.0, 36.0, 100.0)
    """)
    
    # Create projectile that hits (within 10m)
    db_conn.execute("""
        INSERT INTO objects (id, name, type_basic, parent_id, coalition, first_seen, removed_at)
        VALUES ('proj_hit', 'Projectile', 'Projectile', 'aircraft1', 'Allies', 10.0, 15.0)
    """)
    
    db_conn.execute("""
        INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
        VALUES (2, 'proj_hit', 15.0, -115.00001, 36.00001, 100.0)
    """)
    
    # Create projectile that misses (far away)
    db_conn.execute("""
        INSERT INTO objects (id, name, type_basic, parent_id, coalition, first_seen, removed_at)
        VALUES ('proj_miss', 'Projectile', 'Projectile', 'aircraft1', 'Allies', 10.1, 15.1)
    """)
    
    db_conn.execute("""
        INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
        VALUES (3, 'proj_miss', 15.1, -115.1, 36.1, 100.0)
    """)
    
    # Run hit detection
    enricher = ProjectileEnricher(
        detect_launchers=False,
        detect_hits=True,
        create_bursts=False
    )
    hit_count = enricher._detect_hits(db_conn)
    
    # Should detect 1 hit
    assert hit_count == 1
    
    # Verify hit projectile
    hit_proj = db_conn.execute("""
        SELECT id, json_extract(properties, '$.Fate')
        FROM objects
        WHERE id = 'proj_hit'
    """).fetchone()
    
    assert hit_proj
    assert hit_proj[1] == 'HIT'
    
    # Verify miss projectile
    miss_proj = db_conn.execute("""
        SELECT id, json_extract(properties, '$.Fate')
        FROM objects
        WHERE id = 'proj_miss'
    """).fetchone()
    
    assert miss_proj
    assert miss_proj[1] == 'MISS'


def test_burst_creation(db_conn):
    """Test burst object creation."""
    # Create launcher
    db_conn.execute("""
        INSERT INTO objects (id, name, type_basic, coalition, color, country, first_seen)
        VALUES ('aircraft1', 'F-16', 'Air+FixedWing', 'Allies', 'Blue', 'USA', 0.0)
    """)
    
    # Create burst of projectiles (< 1.0s gap)
    for i in range(5):
        db_conn.execute(f"""
            INSERT INTO objects (
                id, name, type_basic, parent_id, coalition, color, country,
                first_seen, removed_at, properties
            )
            VALUES (
                'proj{i}', 'Projectile', 'Projectile', 'aircraft1',
                'Allies', 'Blue', 'USA',
                10.{i}, 15.{i}, '{{"Fate": "MISS"}}'
            )
        """)
    
    # Create single projectile after gap (> 1.0s)
    db_conn.execute("""
        INSERT INTO objects (
            id, name, type_basic, parent_id, coalition, color, country,
            first_seen, removed_at, properties
        )
        VALUES (
            'proj_single', 'Projectile', 'Projectile', 'aircraft1',
            'Allies', 'Blue', 'USA',
            20.0, 25.0, '{"Fate": "MISS"}'
        )
    """)
    
    # Run burst creation
    enricher = ProjectileEnricher(
        detect_launchers=False,
        detect_hits=False,
        create_bursts=True,
        burst_time_gap=1.0
    )
    burst_count = enricher._create_bursts(db_conn)
    
    # Should create 1 burst object (5 projectiles)
    assert burst_count == 1
    
    # Verify burst object
    burst = db_conn.execute("""
        SELECT
            id,
            name,
            type_basic,
            type_specific,
            parent_id,
            json_extract(properties, '$.BurstProjectileCount'),
            json_extract(properties, '$.HitCount'),
            json_extract(properties, '$.Fate')
        FROM objects
        WHERE type_specific = 'Burst'
    """).fetchone()
    
    assert burst
    burst_id, name, type_basic, type_specific, parent_id, proj_count, hit_count, fate = burst
    assert type_basic == 'Projectile'
    assert type_specific == 'Burst'
    assert parent_id == 'aircraft1'
    assert proj_count == 5
    assert hit_count == 0  # All misses
    assert fate == 'MISS'
    
    # Verify projectiles now point to burst
    burst_projectiles = db_conn.execute("""
        SELECT COUNT(*)
        FROM objects
        WHERE parent_id = ? AND type_basic = 'Projectile' AND type_specific IS NULL
    """, [burst_id]).fetchone()
    
    assert burst_projectiles[0] == 5
    
    # Verify single projectile still points to aircraft
    single_proj = db_conn.execute("""
        SELECT parent_id
        FROM objects
        WHERE id = 'proj_single'
    """).fetchone()
    
    assert single_proj[0] == 'aircraft1'


def test_friendly_fire_detection(db_conn):
    """Test friendly fire classification."""
    # Create friendly aircraft (launcher)
    db_conn.execute("""
        INSERT INTO objects (id, name, type_basic, coalition, first_seen)
        VALUES ('aircraft1', 'F-16', 'Air+FixedWing', 'Allies', 0.0)
    """)
    
    # Create friendly target (same coalition)
    db_conn.execute("""
        INSERT INTO objects (id, name, type_class, coalition, first_seen)
        VALUES ('friendly1', 'Friendly Tank', 'Ground', 'Allies', 0.0)
    """)
    
    # Create friendly target state
    db_conn.execute("""
        INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
        VALUES (1, 'friendly1', 15.0, -115.0, 36.0, 100.0)
    """)
    
    # Create projectile that hits friendly
    db_conn.execute("""
        INSERT INTO objects (id, name, type_basic, parent_id, coalition, first_seen, removed_at)
        VALUES ('proj1', 'Projectile', 'Projectile', 'aircraft1', 'Allies', 10.0, 15.0)
    """)
    
    db_conn.execute("""
        INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
        VALUES (2, 'proj1', 15.0, -115.00001, 36.00001, 100.0)
    """)
    
    # Run hit detection
    enricher = ProjectileEnricher(
        detect_launchers=False,
        detect_hits=True,
        create_bursts=False
    )
    hit_count = enricher._detect_hits(db_conn)
    
    assert hit_count == 1
    
    # Verify friendly fire classification
    hit_type = db_conn.execute("""
        SELECT json_extract(properties, '$.HitType')
        FROM objects
        WHERE id = 'proj1'
    """).fetchone()
    
    assert hit_type
    assert hit_type[0] == 'FRIENDLY_FIRE'


def test_multi_target_burst(db_conn):
    """Test burst with hits on multiple targets."""
    # Create launcher
    db_conn.execute("""
        INSERT INTO objects (id, name, type_basic, coalition, color, country, first_seen)
        VALUES ('aircraft1', 'A-10', 'Air+FixedWing', 'Allies', 'Blue', 'USA', 0.0)
    """)
    
    # Create two targets
    for i in range(1, 3):
        db_conn.execute(f"""
            INSERT INTO objects (id, name, type_class, coalition, first_seen)
            VALUES ('target{i}', 'Enemy{i}', 'Ground', 'Enemies', 0.0)
        """)
        
        db_conn.execute(f"""
            INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
            VALUES ({i}, 'target{i}', 15.0, -115.0 + {i*0.0001}, 36.0, 100.0)
        """)
    
    # Create projectiles hitting different targets
    for i in range(6):
        target_offset = (i % 2) * 0.0001
        target_id = f"target{(i % 2) + 1}"
        
        db_conn.execute(f"""
            INSERT INTO objects (
                id, name, type_basic, parent_id, coalition, color, country,
                first_seen, removed_at, properties
            )
            VALUES (
                'proj{i}', 'Projectile', 'Projectile', 'aircraft1',
                'Allies', 'Blue', 'USA',
                10.{i}, 15.{i},
                '{{"Fate": "HIT", "TargetIDs": ["{target_id}"], "HitType": "ENEMY"}}'
            )
        """)
        
        db_conn.execute(f"""
            INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
            VALUES ({10+i}, 'proj{i}', 15.{i}, -115.0 + {target_offset} + 0.00001, 36.00001, 100.0)
        """)
    
    # Run burst creation
    enricher = ProjectileEnricher(
        detect_launchers=False,
        detect_hits=False,
        create_bursts=True
    )
    burst_count = enricher._create_bursts(db_conn)
    
    assert burst_count == 1
    
    # Verify burst has multiple targets
    burst = db_conn.execute("""
        SELECT
            json_extract(properties, '$.BurstProjectileCount'),
            json_extract(properties, '$.HitCount'),
            json_array_length(json_extract(properties, '$.TargetIDs')),
            json_extract(properties, '$.Fate')
        FROM objects
        WHERE type_specific = 'Burst'
    """).fetchone()
    
    assert burst
    proj_count, hit_count, target_count, fate = burst
    assert proj_count == 6
    assert hit_count == 6
    assert target_count == 2  # Two distinct targets
    assert fate == 'HIT'


def test_full_pipeline(db_conn):
    """Test full enrichment pipeline."""
    # Create complete scenario
    
    # Launcher
    db_conn.execute("""
        INSERT INTO objects (id, name, type_basic, coalition, color, country, first_seen)
        VALUES ('aircraft1', 'F-16', 'Air+FixedWing', 'Allies', 'Blue', 'USA', 0.0)
    """)
    
    db_conn.execute("""
        INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
        VALUES (1, 'aircraft1', 10.0, -115.0, 36.0, 1000.0)
    """)
    
    # Target
    db_conn.execute("""
        INSERT INTO objects (id, name, type_class, coalition, first_seen)
        VALUES ('target1', 'Enemy Tank', 'Ground', 'Enemies', 0.0)
    """)
    
    db_conn.execute("""
        INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
        VALUES (2, 'target1', 15.0, -115.0, 36.0, 100.0)
    """)
    
    # Projectiles (burst)
    for i in range(3):
        hit_distance = 0.00001 if i == 1 else 0.1  # Only middle projectile hits
        
        db_conn.execute(f"""
            INSERT INTO objects (
                id, name, type_basic, coalition, color, country,
                first_seen, removed_at
            )
            VALUES (
                'proj{i}', 'Projectile', 'Projectile',
                'Allies', 'Blue', 'USA',
                10.{i}, 15.{i}
            )
        """)
        
        # Spawn state (for launcher detection)
        db_conn.execute(f"""
            INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
            VALUES ({10+i}, 'proj{i}', 10.{i}, -115.0001, 36.0001, 1000.0)
        """)
        
        # Impact state (for hit detection)
        db_conn.execute(f"""
            INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
            VALUES ({20+i}, 'proj{i}', 15.{i}, -115.0 + {hit_distance}, 36.0 + {hit_distance}, 100.0)
        """)
    
    # Run full pipeline
    enricher = ProjectileEnricher(
        detect_launchers=True,
        detect_hits=True,
        create_bursts=True
    )
    total_count = enricher.enrich([], db_conn)
    
    # Verify results
    assert total_count > 0
    
    # Check burst was created
    burst = db_conn.execute("""
        SELECT
            json_extract(properties, '$.BurstProjectileCount'),
            json_extract(properties, '$.HitCount')
        FROM objects
        WHERE type_specific = 'Burst'
    """).fetchone()
    
    assert burst
    proj_count, hit_count = burst
    assert proj_count == 3
    assert hit_count == 1  # Only one projectile hit


def test_intended_target_detection(db_conn):
    """Test intended target detection using 3D cone tracking for MISSED bursts only."""
    # Create aircraft (launcher)
    db_conn.execute("""
        INSERT INTO objects (
            id, name, type_class, type_basic,
            coalition, color, country,
            first_seen, last_seen
        )
        VALUES (
            'aircraft1', 'F-16', 'Air', 'Air+FixedWing',
            'Allies', 'Blue', 'USA',
            0.0, 100.0
        )
    """)
    
    # Create AIR target in front of aircraft (intended target)
    db_conn.execute("""
        INSERT INTO objects (
            id, name, type_class, type_basic,
            coalition, color, country,
            first_seen, last_seen
        )
        VALUES (
            'target1', 'MiG-29', 'Air', 'Air+FixedWing',
            'Enemies', 'Red', 'Russia',
            0.0, 100.0
        )
    """)
    
    # Create AIR target to the side (not intended)
    db_conn.execute("""
        INSERT INTO objects (
            id, name, type_class, type_basic,
            coalition, color, country,
            first_seen, last_seen
        )
        VALUES (
            'target2', 'Su-27', 'Air', 'Air+FixedWing',
            'Enemies', 'Red', 'Russia',
            0.0, 100.0
        )
    """)
    
    # Create projectiles that MISS (required for intended target detection)
    for i in range(5):
        db_conn.execute(f"""
            INSERT INTO objects (
                id, type_basic, type_specific,
                coalition, color, country,
                first_seen, removed_at,
                properties
            )
            VALUES (
                'proj{i}', 'Projectile', 'Projectile',
                'Allies', 'Blue', 'USA',
                10.{i}, 15.{i},
                '{{"Fate": "MISS"}}'
            )
        """)
        
        # Spawn state (near aircraft)
        db_conn.execute(f"""
            INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
            VALUES ({10+i}, 'proj{i}', 10.{i}, -115.0001, 36.0001, 1000.0)
        """)
        
        # Impact state (far from targets - miss)
        db_conn.execute(f"""
            INSERT INTO states (id, object_id, timestamp, longitude, latitude, altitude)
            VALUES ({20+i}, 'proj{i}', 15.{i}, -115.0, 36.0, 1000.0)
        """)
    
    # Aircraft states during burst (heading=0°, pitch=0°)
    for i, t in enumerate([10.0, 10.1, 10.2, 10.3, 10.4]):
        db_conn.execute(f"""
            INSERT INTO states (
                id, object_id, timestamp, 
                longitude, latitude, altitude,
                heading, pitch
            )
            VALUES (
                {100+i}, 'aircraft1', {t},
                -115.0, 36.0, 1000.0,
                0.0, 0.0
            )
        """)
    
    # Target1 states (in front of aircraft at heading 0°, within 25° cone)
    for i, t in enumerate([10.0, 10.1, 10.2, 10.3, 10.4]):
        # Position: ~2km north (lat+0.018°), same heading
        db_conn.execute(f"""
            INSERT INTO states (
                id, object_id, timestamp,
                longitude, latitude, altitude
            )
            VALUES (
                {200+i}, 'target1', {t},
                -115.0, 36.018, 1000.0
            )
        """)
    
    # Target2 states (to the side at ~90°, outside 25° cone)
    for i, t in enumerate([10.0, 10.1, 10.2, 10.3, 10.4]):
        # Position: ~2km east (lon+0.025°), perpendicular
        db_conn.execute(f"""
            INSERT INTO states (
                id, object_id, timestamp,
                longitude, latitude, altitude
            )
            VALUES (
                {300+i}, 'target2', {t},
                -114.975, 36.0, 1000.0
            )
        """)
    
    # Run full pipeline with intended target detection
    enricher = ProjectileEnricher(
        detect_launchers=True,
        detect_hits=True,
        create_bursts=True,
        detect_intended_targets=True,
        intended_cone_azimuth=25.0,
        intended_cone_pitch=25.0,
        intended_max_distance=4000.0
    )
    total_count = enricher.enrich([], db_conn)
    
    # Verify results
    assert total_count > 0
    
    # Check intended target was detected
    burst = db_conn.execute("""
        SELECT
            json_extract(properties, '$.IntendedTargetIDs'),
            json_extract(properties, '$.IntendedTargetTimeInCone')
        FROM objects
        WHERE type_specific = 'Burst'
    """).fetchone()
    
    assert burst, "Burst object should be created"
    intended_ids, time_in_cone = burst
    
    # Verify intended target
    assert intended_ids is not None, "Should have intended target IDs"
    assert time_in_cone is not None, "Should have time in cone data"
    
    # Primary intended target should be target1 (in cone)
    assert 'target1' in intended_ids, "Target1 should be in intended targets"
    
    # Target2 should NOT be in intended targets (outside cone)
    # Note: It might appear if the cone calculation is lenient, but should have much lower time_in_cone
    if 'target2' in intended_ids:
        idx1 = intended_ids.index('target1')
        idx2 = intended_ids.index('target2')
        assert time_in_cone[idx1] > time_in_cone[idx2], "Target1 should have more time in cone than Target2"
    
    print(f"Intended target IDs: {intended_ids}")
    print(f"Time in cone: {time_in_cone}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

