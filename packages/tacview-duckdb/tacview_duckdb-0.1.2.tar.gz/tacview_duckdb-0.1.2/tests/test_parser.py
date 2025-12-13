"""Tests for ACMI parser."""

import io
import pytest

from tacview_duckdb.parser.acmi_parser import ACMIParser
from tacview_duckdb.parser.types import Transform, ObjectState, TacviewObject
from tacview_duckdb.parser.utils import (
    parse_property_value,
    unescape_property,
    parse_transform,
)


def test_parse_property_value():
    """Test property value parsing."""
    assert parse_property_value("123") == 123
    assert parse_property_value("123.45") == 123.45
    assert parse_property_value("hello") == "hello"
    assert parse_property_value("  test  ") == "test"


def test_unescape_property():
    """Test property unescaping."""
    assert unescape_property("hello\\,world") == "hello,world"
    assert unescape_property("line1\\nline2") == "line1\nline2"
    assert unescape_property("back\\\\slash") == "back\\slash"


def test_parse_transform():
    """Test transform parsing."""
    # Full transform
    result = parse_transform("5.2|4.8|1000|10|20|30|100|200|45")
    assert result["longitude"] == 5.2
    assert result["latitude"] == 4.8
    assert result["altitude"] == 1000
    assert result["roll"] == 10
    assert result["pitch"] == 20
    assert result["yaw"] == 30
    assert result["u"] == 100
    assert result["v"] == 200
    assert result["heading"] == 45

    # Partial transform (empty fields)
    result = parse_transform("5.2|4.8|1000|||30|||")
    assert result["longitude"] == 5.2
    assert result["latitude"] == 4.8
    assert result["altitude"] == 1000
    assert result["yaw"] == 30
    assert "roll" not in result
    assert "pitch" not in result


def test_transform_kinematic_computation():
    """Test enhanced kinematic field computation."""
    obj = TacviewObject(object_id="1", type_class="Air")

    # Add first state (defaults for Air types)
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000, yaw=0),
    )
    obj.add_state(state1)
    assert state1.transform.speed is None  # No velocity yet (need 2 states)
    assert state1.transform.g_load == 1.0  # Default at rest
    assert state1.transform.ax == 0.0

    # Add second state (compute speed, vertical speed, turn rate, acceleration)
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=100, v=0, altitude=1100, yaw=10),
    )
    obj.add_state(state2)

    # Check computed fields
    assert state2.transform.speed is not None
    assert abs(state2.transform.speed - 141.42) < 1  # sqrt(100^2 + 100^2) ≈ 141.42
    assert state2.transform.vertical_speed == 100.0
    assert state2.transform.turn_rate == 10.0
    # Turn radius from speed/turn_rate: R = v / ω
    assert state2.transform.turn_radius is not None
    # Acceleration (from v0=0 assumption)
    assert state2.transform.ax is not None
    assert state2.transform.g_load is not None

    # Add third state
    state3 = ObjectState(
        timestamp=2.0,
        transform=Transform(u=200, v=100, altitude=1200, yaw=20),
    )
    obj.add_state(state3)
    assert state3.transform.turn_radius is not None  # Still computed from speed + turn_rate


def test_acmi_parser_basic():
    """Test basic ACMI parsing."""
    import tempfile
    from src.tacview_duckdb.storage.duckdb_store import DuckDBStore
    
    acmi_content = """FileType=text/acmi/tacview
FileVersion=2.2
0,RecordingTime=2025-01-01T12:00:00Z
0,Title=Test Recording
#0
1,Name=Test Aircraft,Type=Air+FixedWing,Coalition=Allies
1,T=5.0|4.0|1000|||0|1000|2000|0
#1.0
1,T=5.0|4.0|1100|||0|1100|2100|0
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        store = DuckDBStore(tmpdir)
        metadata = {"Title": "Test", "RecordingTime": "2025-01-01T12:00:00Z"}
        store.initialize_from_metadata(metadata)
        
        parser = ACMIParser(store)
        with io.StringIO(acmi_content) as stream:
            parser._parse_stream(stream)

    # Check metadata
    assert parser.metadata["FileType"] == "text/acmi/tacview"
    assert parser.metadata["FileVersion"] == "2.2"
    assert parser.metadata["RecordingTime"] == "2025-01-01T12:00:00Z"
    assert parser.metadata["Title"] == "Test Recording"

    # Check objects
    assert "1" in parser.objects
    obj = parser.objects["1"]
    assert obj.name == "Test Aircraft"
    assert obj.type == "Air+FixedWing"
    assert obj.coalition == "Allies"
    assert len(obj.states) == 2

    # Check first state
    state1 = obj.states[0]
    assert state1.timestamp == 0.0
    assert state1.transform.altitude == 1000
    assert state1.transform.u == 1000
    assert state1.transform.v == 2000

    # Check second state
    state2 = obj.states[1]
    assert state2.timestamp == 1.0
    assert state2.transform.altitude == 1100
    assert state2.transform.vertical_speed == 100.0


def test_time_bounds():
    """Test first_seen and last_seen computation."""
    obj = TacviewObject(object_id="1")

    obj.add_state(ObjectState(timestamp=10.0, transform=Transform()))
    assert obj.first_seen == 10.0
    assert obj.last_seen == 10.0

    obj.add_state(ObjectState(timestamp=20.0, transform=Transform()))
    assert obj.first_seen == 10.0
    assert obj.last_seen == 20.0

    obj.add_state(ObjectState(timestamp=15.0, transform=Transform()))
    assert obj.first_seen == 10.0
    # last_seen tracks MAX timestamp seen, not insertion order
    assert obj.last_seen == 20.0

