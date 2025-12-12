"""Tests for DuckDB storage."""

import tempfile
import shutil
from pathlib import Path
import pytest

from tacview_duckdb.parser.types import Transform, ObjectState, TacviewObject
from tacview_duckdb.storage.duckdb_store import DuckDBStore
from tacview_duckdb.storage.hash_utils import generate_db_hash


def test_generate_db_hash():
    """Test database hash generation."""
    metadata1 = {
        "Title": "Test Recording",
        "RecordingTime": "2025-01-01T12:00:00Z",
        "Author": "Test Author",
    }
    metadata2 = {
        "Title": "Test Recording",
        "RecordingTime": "2025-01-01T12:00:00Z",
        "Author": "Test Author",
    }
    metadata3 = {
        "Title": "Different Recording",
        "RecordingTime": "2025-01-01T12:00:00Z",
        "Author": "Test Author",
    }

    # Same metadata should produce same hash
    hash1 = generate_db_hash(metadata1)
    hash2 = generate_db_hash(metadata2)
    assert hash1 == hash2

    # Different metadata should produce different hash
    hash3 = generate_db_hash(metadata3)
    assert hash1 != hash3

    # Hash should be 16 characters
    assert len(hash1) == 16


def test_duckdb_store_init():
    """Test DuckDB store initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        assert store.output_dir == Path(tmpdir)
        assert store.db_path is None
        assert store.conn is None


def test_duckdb_store_from_metadata():
    """Test database creation from metadata."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {
            "Title": "Test Recording",
            "RecordingTime": "2025-01-01T12:00:00Z",
            "Author": "Test Author",
        }

        store.initialize_from_metadata(metadata)

        # Check database file exists
        assert store.db_path is not None
        assert store.db_path.exists()
        assert store.db_path.suffix == ".duckdb"

        # Check connection
        assert store.conn is not None

        # Check metadata stored
        result = store.conn.execute("SELECT * FROM metadata").fetchall()
        assert len(result) > 0


def test_duckdb_store_add_objects():
    """Test adding objects to database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {"Title": "Test", "RecordingTime": "2025-01-01T12:00:00Z"}
        store.initialize_from_metadata(metadata)

        # Create test object
        obj = TacviewObject(
            object_id="1",
            name="Test Aircraft",
            type="Air+FixedWing",
            coalition="Allies",
        )
        obj.add_state(
            ObjectState(
                timestamp=0.0,
                transform=Transform(u=0, v=0, altitude=1000),
            )
        )
        obj.add_state(
            ObjectState(
                timestamp=1.0,
                transform=Transform(u=100, v=0, altitude=1100),
            )
        )

        # Store object
        store.begin_bulk_load()
        store.add_objects_bulk([obj])
        store.end_bulk_load()

        # Verify object stored
        result = store.conn.execute("SELECT COUNT(*) FROM objects").fetchone()
        assert result[0] == 1

        # Verify states stored
        result = store.conn.execute("SELECT COUNT(*) FROM states").fetchone()
        assert result[0] == 2

        # Verify object data
        obj_result = store.get_object("1")
        assert obj_result is not None
        assert obj_result.name == "Test Aircraft"
        assert obj_result.type == "Air+FixedWing"


def test_duckdb_store_query():
    """Test database queries."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {"Title": "Test", "RecordingTime": "2025-01-01T12:00:00Z"}
        store.initialize_from_metadata(metadata)

        # Create test objects
        obj1 = TacviewObject(object_id="1", name="Aircraft 1", type="Air+FixedWing")
        obj1.add_state(ObjectState(timestamp=0.0, transform=Transform()))

        obj2 = TacviewObject(object_id="2", name="Aircraft 2", type="Air+FixedWing")
        obj2.add_state(ObjectState(timestamp=0.0, transform=Transform()))

        store.begin_bulk_load()
        store.add_objects_bulk([obj1, obj2])
        store.end_bulk_load()

        # Query all objects
        results = store.query_sql("SELECT * FROM objects ORDER BY id")
        assert len(results) == 2
        assert results[0]["id"] == "1"
        assert results[1]["id"] == "2"

        # Query specific type
        results = store.query_sql("SELECT * FROM objects WHERE type LIKE '%FixedWing%'")
        assert len(results) == 2


def test_duckdb_store_summary():
    """Test database summary."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {
            "Title": "Test Recording",
            "RecordingTime": "2025-01-01T12:00:00Z",
        }
        store.initialize_from_metadata(metadata)

        obj = TacviewObject(object_id="1", name="Test")
        obj.add_state(ObjectState(timestamp=10.0, transform=Transform()))
        obj.add_state(ObjectState(timestamp=20.0, transform=Transform()))

        store.begin_bulk_load()
        store.add_objects_bulk([obj])
        store.end_bulk_load()

        summary = store.get_summary()
        assert summary["object_count"] == 1
        assert summary["state_count"] == 2
        assert summary["start_time"] == 10.0
        assert summary["end_time"] == 20.0
        assert summary["duration"] == 10.0
        assert "Title" in summary["metadata"]


def test_duckdb_store_from_path():
    """Test opening existing database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create database
        store1 = DuckDBStore(tmpdir)
        metadata = {"Title": "Test", "RecordingTime": "2025-01-01T12:00:00Z"}
        store1.initialize_from_metadata(metadata)

        obj = TacviewObject(object_id="1", name="Test")
        obj.add_state(ObjectState(timestamp=0.0, transform=Transform()))

        store1.begin_bulk_load()
        store1.add_objects_bulk([obj])
        store1.end_bulk_load()

        db_path = store1.database_path
        store1.close()

        # Open existing database
        store2 = DuckDBStore.from_path(db_path)
        assert store2.database_path == db_path

        # Verify data
        summary = store2.get_summary()
        assert summary["object_count"] == 1

        store2.close()

