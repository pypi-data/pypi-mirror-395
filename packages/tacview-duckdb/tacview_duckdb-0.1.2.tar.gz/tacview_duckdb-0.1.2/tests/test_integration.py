"""Integration tests with sample data."""

import tempfile
from pathlib import Path
import pytest

from tacview_duckdb import parse_acmi, DuckDBStore


# Skip if sample data not available
SAMPLE_DATA_DIR = Path(__file__).parent.parent / "sample_data"
SAMPLE_FILES = list(SAMPLE_DATA_DIR.glob("*.acmi")) if SAMPLE_DATA_DIR.exists() else []


@pytest.mark.skipif(not SAMPLE_FILES, reason="No sample data available")
@pytest.mark.parametrize("sample_file", SAMPLE_FILES, ids=lambda f: f.name)
def test_parse_sample_files(sample_file):
    """Test parsing real sample ACMI files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Parse file (use sync mode for tests to avoid threading issues)
        store = parse_acmi(sample_file, output_dir=tmpdir, async_enrichments=False, progress=False)

        # Basic validation
        assert store.database_path is not None
        assert Path(store.database_path).exists()

        # Check summary
        summary = store.get_summary()
        assert summary["object_count"] > 0
        assert summary["state_count"] > 0

        # Verify database structure
        results = store.query_sql("SELECT COUNT(*) as count FROM objects")
        assert results[0]["count"] > 0

        results = store.query_sql("SELECT COUNT(*) as count FROM states")
        assert results[0]["count"] > 0

        store.close()


def test_parse_and_reopen():
    """Test parsing and reopening database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        if not SAMPLE_FILES:
            pytest.skip("No sample data available")

        sample_file = SAMPLE_FILES[0]

        # Parse file (use sync mode for tests)
        store1 = parse_acmi(sample_file, output_dir=tmpdir, async_enrichments=False, progress=False)
        db_path = store1.database_path
        summary1 = store1.get_summary()
        store1.close()

        # Reopen database
        store2 = DuckDBStore.from_path(db_path)
        summary2 = store2.get_summary()

        # Verify data matches
        assert summary1["object_count"] == summary2["object_count"]
        assert summary1["state_count"] == summary2["state_count"]

        store2.close()


def test_parse_with_enrichments():
    """Test parsing with enrichments."""
    with tempfile.TemporaryDirectory() as tmpdir:
        if not SAMPLE_FILES:
            pytest.skip("No sample data available")

        sample_file = SAMPLE_FILES[0]

        # Parse with enrichments (use sync mode for tests)
        store = parse_acmi(
            sample_file,
            output_dir=tmpdir,
            enrichments=["weapons", "coalitions"],
            async_enrichments=False,
            progress=False,
        )

        # Verify database created
        assert store.database_path is not None
        summary = store.get_summary()
        assert summary["object_count"] > 0

        store.close()


def test_mission_name_fallback():
    """Test that filename is used as mission name when Title is missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a minimal ACMI file without Title field
        test_file = Path(tmpdir) / "my_mission_name.txt.acmi"
        acmi_content = """FileType=text/acmi/tacview
FileVersion=2.2
0,ReferenceTime=2024-01-15T12:00:00Z
0,ReferenceLongitude=45.0
0,ReferenceLatitude=35.0
#0.0
1,T=0|0|1000,Type=Air+FixedWing,Name=TestAircraft
#1.0
-1
"""
        test_file.write_text(acmi_content)
        
        # Parse the file
        store = parse_acmi(test_file, output_dir=tmpdir, enrichments=[], progress=False)
        
        # Verify mission name is the filename without extension
        result = store.query_sql("SELECT value FROM metadata WHERE key = 'Title'")
        assert len(result) == 1
        assert result[0]['value'] == "my_mission_name"
        
        store.close()


def test_mission_name_fallback_different_extensions():
    """Test mission name fallback with different file extensions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        acmi_content = """FileType=text/acmi/tacview
FileVersion=2.2
0,ReferenceTime=2024-01-15T12:00:00Z
#0.0
1,T=0|0|1000,Type=Air+FixedWing,Name=TestAircraft
#1.0
-1
"""
        
        test_cases = [
            ("test_mission.txt.acmi", "test_mission"),
            ("test_mission.zip.acmi", "test_mission"),
            ("test_mission.acmi", "test_mission"),
        ]
        
        for filename, expected_name in test_cases:
            test_file = Path(tmpdir) / filename
            test_file.write_text(acmi_content)
            
            # Parse the file
            store = parse_acmi(test_file, output_dir=tmpdir, enrichments=[], progress=False, drop_existing=True)
            
            # Verify mission name
            result = store.query_sql("SELECT value FROM metadata WHERE key = 'Title'")
            assert len(result) == 1
            assert result[0]['value'] == expected_name, f"Failed for {filename}"
            
            store.close()
            test_file.unlink()

