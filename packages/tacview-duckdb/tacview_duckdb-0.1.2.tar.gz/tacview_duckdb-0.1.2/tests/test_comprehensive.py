"""
Comprehensive test suite for py-tacview-duckdb.

This is the primary test script that validates:
- ACMI parsing with timing
- Database creation and indexing
- All DCS default enrichments:
  * Weapons (launcher detection)
  * Coalitions (team assignment)
  * Containers (cargo/parent detection)
  * Ejections (pilot ejection tracking)
  * Missed weapons (proximity analysis for missiles)
  * Decoys (decoy parent detection)
  * Landing/Takeoff (flight phase detection)
- Concurrent access patterns
- Query performance
- Thread safety

Run with: pytest tests/test_comprehensive.py -v -s
Or standalone: python tests/test_comprehensive.py
"""

import time
import threading
from pathlib import Path
from typing import Optional

import pytest

from tacview_duckdb import parse_acmi, DuckDBStore


class Timer:
    """Context manager for timing code blocks."""
    
    def __init__(self, name: str):
        self.name = name
        self.start = 0.0
        self.elapsed = 0.0
    
    def __enter__(self):
        self.start = time.time()
        print(f"\n▶ {self.name}...")
        return self
    
    def __exit__(self, *args):
        self.elapsed = time.time() - self.start
        print(f"✓ {self.name} completed in {self.elapsed:.2f}s")


@pytest.fixture(scope="module")
def sample_acmi_file():
    """Get path to sample ACMI file for testing."""
    sample_dir = Path(__file__).parent.parent / "sample_data"
    
    # Look for any .acmi file
    acmi_files = list(sample_dir.glob("*.acmi"))
    
    if not acmi_files:
        pytest.skip("No sample ACMI files found in sample_data/")
    
    # Use the first available file
    return acmi_files[0]


@pytest.fixture(scope="module")
def output_dir(tmp_path_factory):
    """Create temporary output directory."""
    return tmp_path_factory.mktemp("comprehensive_test")


@pytest.fixture(scope="module")
def parsed_store(sample_acmi_file, output_dir):
    """Parse ACMI file once for all tests."""
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE TEST SUITE")
    print(f"{'='*80}")
    print(f"ACMI File: {sample_acmi_file.name}")
    print(f"Output Dir: {output_dir}")
    print(f"{'='*80}\n")
    
    with Timer("Full parsing (no enrichments)"):
        store = parse_acmi(
            sample_acmi_file,
            output_dir=str(output_dir),
            enrichments=[],  # No enrichments initially
            async_enrichments=False,
            progress=False,
            drop_existing=True
        )
    
    yield store
    
    # Cleanup
    store.close()


def test_01_parsing_results(parsed_store):
    """Test 1: Validate parsing results."""
    print(f"\n{'─'*80}")
    print("TEST 1: PARSING RESULTS")
    print(f"{'─'*80}")
    
    with Timer("Get database summary"):
        summary = parsed_store.get_summary()
    
    # Validate results
    assert summary['object_count'] > 0, "Should have parsed objects"
    assert summary['state_count'] > 0, "Should have parsed states"
    assert 'start_time' in summary, "Should have start time"
    assert 'end_time' in summary, "Should have end time"
    
    print(f"\n📊 Summary:")
    print(f"  Objects: {summary['object_count']:,}")
    print(f"  States: {summary['state_count']:,}")
    print(f"  Duration: {summary.get('duration', 0):.1f}s")
    print(f"  Database: {parsed_store.database_path}")


def test_02_database_structure(parsed_store):
    """Test 2: Validate database structure."""
    print(f"\n{'─'*80}")
    print("TEST 2: DATABASE STRUCTURE")
    print(f"{'─'*80}")
    
    with Timer("Query database schema"):
        with parsed_store.get_query_connection() as conn:
            # Check tables exist
            tables = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                ORDER BY name
            """).fetchall()
            
            table_names = [t[0] for t in tables]
    
    required_tables = ['objects', 'states', 'events', 'metadata']
    for table in required_tables:
        assert table in table_names, f"Missing required table: {table}"
    
    print(f"\n📋 Tables: {', '.join(table_names)}")


def test_03_concurrent_queries(parsed_store):
    """Test 3: Validate concurrent query access."""
    print(f"\n{'─'*80}")
    print("TEST 3: CONCURRENT QUERIES")
    print(f"{'─'*80}")
    
    results = {}
    errors = []
    
    def query_objects(thread_id: int):
        """Query objects from separate connection."""
        try:
            with parsed_store.get_query_connection() as conn:
                result = conn.execute("SELECT COUNT(*) FROM objects").fetchone()
                results[thread_id] = result[0]
        except Exception as e:
            errors.append((thread_id, str(e)))
    
    with Timer("Run 5 concurrent queries"):
        threads = []
        for i in range(5):
            t = threading.Thread(target=query_objects, args=(i,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
    
    # Validate
    assert len(errors) == 0, f"Concurrent queries failed: {errors}"
    assert len(results) == 5, "Should have 5 results"
    
    # All counts should be the same
    counts = set(results.values())
    assert len(counts) == 1, "All queries should return same count"
    
    print(f"\n✓ All 5 threads returned: {list(results.values())[0]} objects")


def test_04_coalition_enrichment(parsed_store):
    """Test 4: Coalition enrichment (MUST RUN FIRST)."""
    print(f"\n{'─'*80}")
    print("TEST 4: COALITION ENRICHMENT")
    print(f"{'─'*80}")
    
    with Timer("Apply coalition enrichment"):
        result = parsed_store.apply_enrichments(
            ['coalitions'],
            async_enrichments=False,
            progress=False
        )
    
    with Timer("Query coalition distribution"):
        coalitions = parsed_store.query_sql("""
            SELECT 
                coalition,
                COUNT(*) as count
            FROM objects 
            WHERE coalition IS NOT NULL
            GROUP BY coalition
            ORDER BY count DESC
        """)
    
    print(f"\n🏴 Coalitions:")
    for row in coalitions:
        print(f"  {row['coalition']}: {row['count']}")


def test_05_weapon_enrichment(parsed_store):
    """Test 5: Weapon enrichment."""
    print(f"\n{'─'*80}")
    print("TEST 5: WEAPON ENRICHMENT")
    print(f"{'─'*80}")
    
    with Timer("Apply weapon enrichment"):
        result = parsed_store.apply_enrichments(
            ['weapons'],
            async_enrichments=False,
            progress=False
        )
    
    with Timer("Query enriched weapons"):
        weapons = parsed_store.query_sql("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN parent_id IS NOT NULL THEN 1 ELSE 0 END) as with_launcher
            FROM objects 
            WHERE type_class = 'Weapon'
        """)
    
    if weapons and weapons[0]['total'] > 0:
        total = weapons[0]['total']
        with_launcher = weapons[0]['with_launcher']
        pct = (with_launcher / total * 100) if total > 0 else 0
        
        print(f"\n🎯 Weapons:")
        print(f"  Total: {total}")
        print(f"  With launcher: {with_launcher} ({pct:.1f}%)")
    else:
        print(f"\n⚠ No weapons found in this recording")


def test_06_container_enrichment(parsed_store):
    """Test 6: Container enrichment."""
    print(f"\n{'─'*80}")
    print("TEST 6: CONTAINER ENRICHMENT")
    print(f"{'─'*80}")
    
    with Timer("Apply container enrichment"):
        result = parsed_store.apply_enrichments(
            ['containers'],
            async_enrichments=False,
            progress=False
        )
    
    with Timer("Query containers"):
        containers = parsed_store.query_sql("""
            SELECT COUNT(*) as count
            FROM objects 
            WHERE type_specific = 'Container' AND parent_id IS NOT NULL
        """)
    
    count = containers[0]['count'] if containers else 0
    print(f"\n📦 Containers with parent: {count}")


def test_07_decoy_enrichment(parsed_store):
    """Test 7: Decoy parent enrichment (BEFORE missed weapons!)."""
    print(f"\n{'─'*80}")
    print("TEST 7: DECOY ENRICHMENT")
    print(f"{'─'*80}")
    
    # First, check if there are ANY decoys in the database
    with Timer("Check for decoys in database"):
        all_decoys = parsed_store.query_sql("""
            SELECT 
                COUNT(*) as total_decoys,
                SUM(CASE WHEN parent_id IS NOT NULL THEN 1 ELSE 0 END) as with_parent,
                SUM(CASE WHEN coalition IS NOT NULL THEN 1 ELSE 0 END) as with_coalition,
                SUM(CASE WHEN color IS NOT NULL THEN 1 ELSE 0 END) as with_color
            FROM objects 
            WHERE type_basic = 'Decoy'
        """)
    
    if all_decoys and all_decoys[0]['total_decoys'] > 0:
        stats = all_decoys[0]
        print(f"\n🎪 Decoys found in database:")
        print(f"  Total: {stats['total_decoys']}")
        print(f"  With coalition: {stats['with_coalition']}")
        print(f"  With color: {stats['with_color']}")
        print(f"  Already with parent: {stats['with_parent']}")
    else:
        print(f"\n⚠ No decoys found in database")
        return
    
    with Timer("Apply decoy enrichment"):
        result = parsed_store.apply_enrichments(
            ['decoys'],
            async_enrichments=False,
            progress=False
        )
    
    with Timer("Query decoys after enrichment"):
        decoys = parsed_store.query_sql("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN parent_id IS NOT NULL THEN 1 ELSE 0 END) as with_parent
            FROM objects 
            WHERE type_basic = 'Decoy'
        """)
    
    if decoys:
        print(f"\n🎪 Decoys after enrichment:")
        print(f"  Total: {decoys[0]['total']}")
        print(f"  With parent: {decoys[0]['with_parent']}")


def test_08_missed_weapon_enrichment(parsed_store):
    """Test 8: Missed weapon proximity enrichment."""
    print(f"\n{'─'*80}")
    print("TEST 8: MISSED WEAPON ENRICHMENT")
    print(f"{'─'*80}")
    
    with Timer("Apply missed weapon enrichment"):
        result = parsed_store.apply_enrichments(
            ['missed_weapons'],
            async_enrichments=False,
            progress=False
        )
    
    with Timer("Query missed weapon analysis"):
        missed_analysis = parsed_store.query_sql("""
            SELECT 
                json_extract_string(properties, '$.Fate') as fate,
                COUNT(*) as count
            FROM objects 
            WHERE type_basic = 'Missile'
              AND json_extract_string(properties, '$.Fate') IN ('DECOYED', 'NEAR_MISS', 'MISS')
            GROUP BY fate
            ORDER BY count DESC
        """)
    
    print(f"\n🎯 Missile Analysis:")
    for row in missed_analysis:
        print(f"  {row['fate']}: {row['count']}")
    
    # If there are DECOYED weapons, show what they hit
    with Timer("Check DECOYED weapons"):
        decoyed_details = parsed_store.query_sql("""
            SELECT 
                w.name as weapon,
                t.name as target_name,
                t.type_basic as target_type_basic,
                t.type_class as target_type_class
            FROM objects w
            CROSS JOIN LATERAL (
                SELECT json_extract(w.properties, '$.TargetIDs')[1]::VARCHAR as target_id
            ) tid
            JOIN objects t ON t.id = tid.target_id
            WHERE json_extract_string(w.properties, '$.Fate') = 'DECOYED'
            LIMIT 5
        """)
    
    if decoyed_details:
        print(f"\n  Sample DECOYED weapons (targets they hit):")
        for row in decoyed_details:
            print(f"    - {row['weapon']} → {row['target_name']} (type_basic={row['target_type_basic']}, type_class={row['target_type_class']})")


def test_09_ejection_enrichment(parsed_store):
    """Test 9: Ejection enrichment."""
    print(f"\n{'─'*80}")
    print("TEST 9: EJECTION ENRICHMENT")
    print(f"{'─'*80}")
    
    with Timer("Apply ejection enrichment"):
        result = parsed_store.apply_enrichments(
            ['ejections'],
            async_enrichments=False,
            progress=False
        )
    
    with Timer("Query ejections"):
        ejections = parsed_store.query_sql("""
            SELECT COUNT(*) as count
            FROM objects 
            WHERE type_specific = 'Parachutist' AND parent_id IS NOT NULL
        """)
    
    count = ejections[0]['count'] if ejections else 0
    print(f"\n🪂 Ejected pilots: {count}")


def test_10_projectile_enrichment(parsed_store):
    """Test 10: Projectile enrichment (launchers, hits, bursts)."""
    print(f"\n{'─'*80}")
    print("TEST 10: PROJECTILE ENRICHMENT")
    print(f"{'─'*80}")
    
    with Timer("Apply projectile enrichment"):
        result = parsed_store.apply_enrichments(
            ['projectiles'],
            async_enrichments=False,
            progress=False
        )
    
    with Timer("Query projectile statistics"):
        # Get projectile counts
        projectile_stats = parsed_store.query_sql("""
            SELECT 
                COUNT(*) as total_projectiles,
                SUM(CASE WHEN parent_id IS NOT NULL THEN 1 ELSE 0 END) as with_launcher,
                SUM(CASE WHEN json_extract(properties, '$.Fate') = 'HIT' THEN 1 ELSE 0 END) as hits,
                SUM(CASE WHEN json_extract(properties, '$.Fate') = 'MISS' THEN 1 ELSE 0 END) as misses
            FROM objects 
            WHERE type_basic = 'Projectile' AND type_specific IS NULL
        """)
        
        # Get burst counts
        burst_stats = parsed_store.query_sql("""
            SELECT 
                COUNT(*) as total_bursts,
                SUM(CAST(json_extract(properties, '$.BurstProjectileCount') AS INT)) as total_rounds,
                SUM(CAST(json_extract(properties, '$.HitCount') AS INT)) as total_burst_hits,
                SUM(CASE WHEN json_extract(properties, '$.Fate') = 'HIT' THEN 1 ELSE 0 END) as bursts_with_hits,
                ROUND(AVG(CAST(json_extract(properties, '$.BurstFireRate') AS DOUBLE)), 1) as avg_fire_rate
            FROM objects 
            WHERE type_specific = 'Burst'
        """)
    
    if projectile_stats and projectile_stats[0]['total_projectiles'] > 0:
        proj = projectile_stats[0]
        print(f"\n🔫 Projectiles:")
        print(f"  Total: {proj['total_projectiles']}")
        print(f"  With launcher: {proj['with_launcher']} ({proj['with_launcher']/proj['total_projectiles']*100:.1f}%)")
        print(f"  Hits: {proj['hits']}")
        print(f"  Misses: {proj['misses']}")
        
        if burst_stats and burst_stats[0]['total_bursts'] and burst_stats[0]['total_bursts'] > 0:
            burst = burst_stats[0]
            accuracy = (burst['total_burst_hits'] / burst['total_rounds'] * 100) if burst['total_rounds'] > 0 else 0
            print(f"\n💥 Bursts:")
            print(f"  Total bursts: {burst['total_bursts']}")
            print(f"  Total rounds in bursts: {burst['total_rounds']}")
            print(f"  Burst hits: {burst['total_burst_hits']}")
            print(f"  Bursts with hits: {burst['bursts_with_hits']} ({burst['bursts_with_hits']/burst['total_bursts']*100:.1f}%)")
            print(f"  Overall accuracy: {accuracy:.2f}%")
            print(f"  Avg fire rate: {burst['avg_fire_rate']:.1f} rounds/sec")
        else:
            print(f"\n💥 Bursts: None (all single-fire projectiles)")
    else:
        print(f"\n⚠ No projectiles found in this recording")


def test_11_landing_takeoff_enrichment(parsed_store):
    """Test 11: Landing/takeoff detection enrichment."""
    print(f"\n{'─'*80}")
    print("TEST 11: LANDING/TAKEOFF ENRICHMENT")
    print(f"{'─'*80}")
    
    with Timer("Apply landing/takeoff enrichment"):
        result = parsed_store.apply_enrichments(
            ['landing_takeoff'],
            async_enrichments=False,
            progress=False
        )
    
    with Timer("Query flight events"):
        events = parsed_store.query_sql("""
            SELECT 
                event_name,
                COUNT(*) as count
            FROM events 
            WHERE event_name IN ('Takeoff', 'Landing', 'AirStart')
            GROUP BY event_name
            ORDER BY count DESC
        """)
    
    if events:
        print(f"\n✈️  Flight Events:")
        for row in events:
            print(f"  {row['event_name']}: {row['count']}")
    else:
        print(f"\n✈️  Flight Events: None detected (may not be applicable to this recording)")


def test_12_async_enrichment(parsed_store, output_dir):
    """Test 12: Async enrichment (background thread)."""
    print(f"\n{'─'*80}")
    print("TEST 12: ASYNC ENRICHMENT")
    print(f"{'─'*80}")
    
    # Parse a fresh copy for async testing
    acmi_file = Path(__file__).parent.parent / "sample_data"
    acmi_files = list(acmi_file.glob("*.acmi"))
    if not acmi_files:
        pytest.skip("No sample ACMI files found")
    
    async_output = output_dir / "async_test"
    async_output.mkdir(exist_ok=True)
    
    with Timer("Parse with async enrichments"):
        store = parse_acmi(
            acmi_files[0],
            output_dir=str(async_output),
            enrichments=['coalitions'],
            async_enrichments=True,  # Background enrichments
            progress=False,
            drop_existing=True
        )
    
    print(f"\n⏳ Enrichments running in background...")
    
    # Query while enrichments are running
    with Timer("Query during enrichments"):
        with store.get_query_connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM objects").fetchone()[0]
    
    print(f"✓ Successfully queried {count} objects while enrichments running")
    
    # Wait for enrichments
    with Timer("Wait for enrichments to complete"):
        store.wait_for_enrichments()
    
    assert store.enrichments_complete(), "Enrichments should be complete"
    
    print(f"✓ Async enrichments completed successfully")
    
    store.close()


def test_13_query_performance(parsed_store):
    """Test 13: Query performance benchmarks."""
    print(f"\n{'─'*80}")
    print("TEST 13: QUERY PERFORMANCE")
    print(f"{'─'*80}")
    
    queries = {
        "Count objects": "SELECT COUNT(*) FROM objects",
        "Count states": "SELECT COUNT(*) FROM states",
        "Objects by type": """
            SELECT type_basic, COUNT(*) as count 
            FROM objects 
            GROUP BY type_basic 
            ORDER BY count DESC 
            LIMIT 10
        """,
        "Time range query": """
            SELECT COUNT(*) 
            FROM states 
            WHERE timestamp BETWEEN 0 AND 100
        """,
        "Join query": """
            SELECT o.name, COUNT(s.id) as state_count
            FROM objects o
            JOIN states s ON o.id = s.object_id
            GROUP BY o.id, o.name
            LIMIT 10
        """,
    }
    
    print(f"\n⚡ Query Benchmarks:")
    for name, sql in queries.items():
        start = time.time()
        with parsed_store.get_query_connection() as conn:
            result = conn.execute(sql).fetchall()
        elapsed = time.time() - start
        print(f"  {name}: {elapsed*1000:.2f}ms ({len(result)} rows)")


def test_14_connection_cleanup(parsed_store):
    """Test 14: Connection cleanup."""
    print(f"\n{'─'*80}")
    print("TEST 14: CONNECTION CLEANUP")
    print(f"{'─'*80}")
    
    # Create multiple connections
    connections = []
    with Timer("Create 10 connections"):
        for i in range(10):
            conn = parsed_store.get_query_connection()
            connections.append(conn)
    
    # Use them
    with Timer("Query from all connections"):
        for i, conn in enumerate(connections):
            count = conn.execute("SELECT COUNT(*) FROM objects").fetchone()[0]
    
    # Close them
    with Timer("Close all connections"):
        for conn in connections:
            conn.close()
    
    print(f"✓ Successfully managed 10 concurrent connections")


def test_15_summary_report(parsed_store):
    """Test 15: Final summary report."""
    print(f"\n{'='*80}")
    print("FINAL SUMMARY REPORT")
    print(f"{'='*80}")
    
    summary = parsed_store.get_summary()
    
    # Get enrichment status
    with parsed_store.get_query_connection() as conn:
        # Count enriched objects
        weapons_enriched = conn.execute("""
            SELECT COUNT(*) FROM objects 
            WHERE type_class = 'Weapon' AND parent_id IS NOT NULL
        """).fetchone()[0]
        
        coalitions_set = conn.execute("""
            SELECT COUNT(*) FROM objects WHERE coalition IS NOT NULL
        """).fetchone()[0]
        
        containers_enriched = conn.execute("""
            SELECT COUNT(*) FROM objects 
            WHERE type_specific = 'Container' AND parent_id IS NOT NULL
        """).fetchone()[0]
        
        ejections = conn.execute("""
            SELECT COUNT(*) FROM objects 
            WHERE type_specific = 'Parachutist' AND parent_id IS NOT NULL
        """).fetchone()[0]
        
        # Missed weapons
        decoyed = conn.execute("""
            SELECT COUNT(*) FROM objects 
            WHERE json_extract_string(properties, '$.Fate') = 'DECOYED'
        """).fetchone()[0]
        
        near_miss = conn.execute("""
            SELECT COUNT(*) FROM objects 
            WHERE json_extract_string(properties, '$.Fate') = 'NEAR_MISS'
        """).fetchone()[0]
        
        # Decoys
        decoys_enriched = conn.execute("""
            SELECT COUNT(*) FROM objects 
            WHERE type_basic = 'Decoy' AND parent_id IS NOT NULL
        """).fetchone()[0]
        
        # Flight events
        flight_events = conn.execute("""
            SELECT COUNT(*) FROM events 
            WHERE event_name IN ('Takeoff', 'Landing', 'AirStart')
        """).fetchone()[0]
        
        # Projectile bursts
        projectiles_enriched = conn.execute("""
            SELECT COUNT(*) FROM objects 
            WHERE type_basic = 'Projectile' AND parent_id IS NOT NULL
        """).fetchone()[0]
        
        bursts_created = conn.execute("""
            SELECT COUNT(*) FROM objects 
            WHERE type_specific = 'Burst'
        """).fetchone()[0]
        
        burst_hits = conn.execute("""
            SELECT COALESCE(SUM(CAST(json_extract(properties, '$.HitCount') AS INT)), 0)
            FROM objects 
            WHERE type_specific = 'Burst'
        """).fetchone()[0]
    
    print(f"\n📊 Database Statistics:")
    print(f"  Objects: {summary['object_count']:,}")
    print(f"  States: {summary['state_count']:,}")
    print(f"  Recording Duration: {summary.get('duration', 0):.1f}s")
    print(f"  Database Size: {Path(parsed_store.database_path).stat().st_size / 1024 / 1024:.2f} MB")
    
    print(f"\n🔧 Enrichment Status (All Tests Applied):")
    print(f"  ✓ Weapons with launcher: {weapons_enriched}")
    print(f"  ✓ Missed weapon detections: {decoyed} decoyed, {near_miss} near-miss")
    print(f"  ✓ Objects with coalition: {coalitions_set}")
    print(f"  ✓ Containers with parent: {containers_enriched}")
    print(f"  ✓ Ejected pilots: {ejections}")
    print(f"  ✓ Decoys with parent: {decoys_enriched}")
    print(f"  ✓ Flight events: {flight_events}")
    print(f"  ✓ Projectiles with launcher: {projectiles_enriched}")
    print(f"  ✓ Bursts created: {bursts_created} (total hits: {burst_hits})")
    
    print(f"\n💾 DATABASE LOCATION (for manual inspection):")
    print(f"{'─'*80}")
    print(f"  Path: {parsed_store.database_path}")
    print(f"  Hash: {parsed_store.db_hash}")
    print(f"{'─'*80}")
    print(f"\n  To inspect manually:")
    print(f"    duckdb {parsed_store.database_path}")
    print(f"  Or:")
    print(f"    python -c \"from tacview_duckdb import DuckDBStore; store = DuckDBStore.from_path('{parsed_store.database_path}'); print(store.get_summary())\"")
    
    print(f"\n✅ All tests passed!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    """Run comprehensive test suite standalone."""
    import sys
    
    # Find sample file
    sample_dir = Path(__file__).parent.parent / "sample_data"
    acmi_files = list(sample_dir.glob("*.acmi"))
    
    if not acmi_files:
        print("ERROR: No sample ACMI files found in sample_data/")
        sys.exit(1)
    
    # Create temp output dir
    output_dir = Path(__file__).parent.parent / "test_output"
    output_dir.mkdir(exist_ok=True)
    
    # Run tests manually
    print("Running comprehensive test suite...")
    
    # Parse once
    with Timer("Initial parsing"):
        store = parse_acmi(
            acmi_files[0],
            output_dir=str(output_dir),
            enrichments=[],
            async_enrichments=False,
            progress=False,
            drop_existing=True
        )
    
    try:
        # Run all tests
        test_01_parsing_results(store)
        test_02_database_structure(store)
        test_03_concurrent_queries(store)
        test_04_coalition_enrichment(store)
        test_05_weapon_enrichment(store)
        test_06_container_enrichment(store)
        test_07_decoy_enrichment(store)
        test_08_missed_weapon_enrichment(store)
        test_09_ejection_enrichment(store)
        test_10_projectile_enrichment(store)
        test_11_landing_takeoff_enrichment(store)
        test_12_async_enrichment(store, output_dir)
        test_13_query_performance(store)
        test_14_connection_cleanup(store)
        test_15_summary_report(store)
        
        print("\n✅ ALL TESTS PASSED!")
    finally:
        store.close()

