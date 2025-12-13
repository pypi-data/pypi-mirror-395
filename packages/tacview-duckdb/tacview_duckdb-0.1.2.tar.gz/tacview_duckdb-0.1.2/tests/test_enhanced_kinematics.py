"""Tests for enhanced kinematics computation."""

import math
import pytest
from src.tacview_duckdb.parser.types import TacviewObject, ObjectState, Transform


def test_velocity_and_speed_computation():
    """Test basic velocity and speed computation."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    # First state - no kinematics yet
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000)
    )
    obj.add_state(state1)
    
    # Verify first state defaults
    assert state1.transform.g_load == 1.0
    assert state1.transform.ax == 0.0
    assert state1.transform.ay == 0.0
    assert state1.transform.az == 0.0
    assert state1.transform.speed is None  # No velocity yet
    
    # Second state - compute velocity and speed
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=100, v=0, altitude=1000)
    )
    obj.add_state(state2)
    
    # Velocity: vx=100, vy=0, vz=0
    # Speed should be 100 m/s
    assert state2.transform.speed == pytest.approx(100.0, abs=0.001)
    
    # Verify velocity was cached
    assert hasattr(state2, '_velocity_cache')
    vx, vy, vz = state2._velocity_cache
    assert vx == pytest.approx(100.0, abs=0.001)
    assert vy == pytest.approx(0.0, abs=0.001)
    assert vz == pytest.approx(0.0, abs=0.001)


def test_acceleration_computation_state_n2():
    """Test acceleration computation at State N=2 (assumes v0=0)."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    # State 1
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000)
    )
    obj.add_state(state1)
    
    # State 2 - acceleration from v0=0 to v1
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=100, v=0, altitude=1000)
    )
    obj.add_state(state2)
    
    # Acceleration: a = (v1 - v0) / dt = (100 - 0) / 1.0 = 100 m/s²
    assert state2.transform.ax == pytest.approx(100.0, abs=0.001)
    assert state2.transform.ay == pytest.approx(0.0, abs=0.001)
    assert state2.transform.az == pytest.approx(0.0, abs=0.001)
    
    # G-loading: ||a - [0,0,-g]|| / g
    # a = [100, 0, 0], gravity = [0, 0, -9.81]
    # compensated = [100, 0, 9.81]
    # magnitude = sqrt(100^2 + 0^2 + 9.81^2) = sqrt(10000 + 96.24) ≈ 100.48
    # g_load = 100.48 / 9.81 ≈ 10.24
    expected_g = math.sqrt(100**2 + 0**2 + 9.81**2) / 9.81
    assert state2.transform.g_load == pytest.approx(expected_g, abs=0.01)


def test_acceleration_computation_state_n3():
    """Test acceleration computation at State N=3+ (using cached velocity)."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    # State 1
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000)
    )
    obj.add_state(state1)
    
    # State 2 - constant velocity 100 m/s
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=100, v=0, altitude=1000)
    )
    obj.add_state(state2)
    
    # State 3 - still constant velocity (no acceleration)
    state3 = ObjectState(
        timestamp=2.0,
        transform=Transform(u=200, v=0, altitude=1000)
    )
    obj.add_state(state3)
    
    # Velocity unchanged: v2 = 100, v3 = 100
    # Acceleration: a = (100 - 100) / 1.0 = 0
    assert state3.transform.ax == pytest.approx(0.0, abs=0.001)
    assert state3.transform.ay == pytest.approx(0.0, abs=0.001)
    assert state3.transform.az == pytest.approx(0.0, abs=0.001)
    
    # G-loading at rest (only gravity): ||[0,0,9.81]|| / 9.81 = 1.0
    assert state3.transform.g_load == pytest.approx(1.0, abs=0.01)


def test_g_loading_level_turn():
    """Test G-loading during a level turn (centripetal acceleration)."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    # State 1
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000)
    )
    obj.add_state(state1)
    
    # State 2 - moving in +X direction at 100 m/s
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=100, v=0, altitude=1000)
    )
    obj.add_state(state2)
    
    # State 3 - turning: now moving in +Y direction at 100 m/s
    # This represents a 90-degree turn with centripetal acceleration
    state3 = ObjectState(
        timestamp=2.0,
        transform=Transform(u=100, v=100, altitude=1000)
    )
    obj.add_state(state3)
    
    # Velocity changed from [100, 0, 0] to [0, 100, 0]
    # Acceleration: a = [(0-100)/1, (100-0)/1, 0] = [-100, 100, 0] m/s²
    assert state3.transform.ax == pytest.approx(-100.0, abs=0.001)  # (0-100)/1
    assert state3.transform.ay == pytest.approx(100.0, abs=0.001)  # (100-0)/1
    assert state3.transform.az == pytest.approx(0.0, abs=0.001)
    
    # G-loading with centripetal acceleration
    # Compensated: [-100, 100, 9.81]
    # magnitude = sqrt(100^2 + 100^2 + 9.81^2) ≈ 141.90
    expected_g = math.sqrt(100**2 + 100**2 + 9.81**2) / 9.81
    assert state3.transform.g_load == pytest.approx(expected_g, abs=0.01)


def test_vertical_climb_acceleration():
    """Test acceleration and G-loading during vertical climb."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    # State 1
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000)
    )
    obj.add_state(state1)
    
    # State 2 - climbing at 50 m/s
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=0, v=0, altitude=1050)
    )
    obj.add_state(state2)
    
    # Vertical acceleration
    assert state2.transform.az == pytest.approx(50.0, abs=0.001)
    assert state2.transform.vertical_speed == pytest.approx(50.0, abs=0.001)


def test_turn_radius_from_speed_and_turn_rate():
    """Test efficient turn radius computation from speed and turn rate."""
    obj = TacviewObject(object_id="1", type_class="Air", type_basic="FixedWing")
    
    # State 1
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000, yaw=0)
    )
    obj.add_state(state1)
    
    # State 2 - moving at 100 m/s, turning at 10 deg/sec
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=100, v=0, altitude=1000, yaw=10)
    )
    obj.add_state(state2)
    
    # Speed = 100 m/s, turn_rate = 10 deg/sec
    assert state2.transform.speed == pytest.approx(100.0, abs=0.001)
    assert state2.transform.turn_rate == pytest.approx(10.0, abs=0.001)
    
    # Turn radius: R = v / |ω|
    # ω = 10 * π / 180 ≈ 0.1745 rad/sec
    # R = 100 / 0.1745 ≈ 572.96 meters
    omega_rad = 10 * math.pi / 180.0
    expected_radius = 100.0 / omega_rad
    assert state2.transform.turn_radius == pytest.approx(expected_radius, abs=0.1)


def test_turn_radius_not_computed_for_small_turn_rate():
    """Test that turn radius is not computed for very small turn rates."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000, yaw=0)
    )
    obj.add_state(state1)
    
    # Moving but barely turning (< 0.01 deg/sec threshold)
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=100, v=0, altitude=1000, yaw=0.005)
    )
    obj.add_state(state2)
    
    # Turn radius should not be computed
    assert state2.transform.turn_radius is None


def test_ground_unit_speed_only():
    """Test that ground units only get speed computation."""
    obj = TacviewObject(object_id="1", type_class="Ground", type_basic="Vehicle")
    
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=0)
    )
    obj.add_state(state1)
    
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=10, v=0, altitude=0)
    )
    obj.add_state(state2)
    
    # Should have speed
    assert state2.transform.speed == pytest.approx(10.0, abs=0.001)
    
    # Should NOT have acceleration or G-loading (not 'full' kinematics)
    assert state2.transform.ax is None
    assert state2.transform.ay is None
    assert state2.transform.az is None
    assert state2.transform.g_load is None
    assert state2.transform.vertical_speed is None
    assert state2.transform.turn_rate is None


def test_weapon_gets_full_kinematics():
    """Test that weapons get full kinematic computation."""
    obj = TacviewObject(object_id="1", type_class="Weapon")
    
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000)
    )
    obj.add_state(state1)
    
    # First state defaults
    assert state1.transform.g_load == 1.0
    assert state1.transform.ax == 0.0
    
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=100, v=0, altitude=1000)
    )
    obj.add_state(state2)
    
    # Should have full kinematics
    assert state2.transform.speed == pytest.approx(100.0, abs=0.001)
    assert state2.transform.ax == pytest.approx(100.0, abs=0.001)
    assert state2.transform.g_load is not None


def test_single_state_object():
    """Test single-state objects (normal behavior for static units)."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    # Only one state (static or instantly destroyed)
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=0)
    )
    obj.add_state(state1)
    
    # Should have defaults
    assert state1.transform.g_load == 1.0
    assert state1.transform.ax == 0.0
    assert state1.transform.ay == 0.0
    assert state1.transform.az == 0.0
    assert state1.transform.speed is None  # No second state to compute velocity


def test_missing_position_data():
    """Test handling of missing position data."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000)
    )
    obj.add_state(state1)
    
    # State with missing U coordinate
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=None, v=0, altitude=1000)
    )
    obj.add_state(state2)
    
    # Should not crash, kinematics should be None
    assert state2.transform.speed is None
    assert state2.transform.ax is None


def test_zero_time_delta():
    """Test handling of zero time delta (skip computation)."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000)
    )
    obj.add_state(state1)
    
    # Same timestamp (zero delta)
    state2 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=100, v=0, altitude=1000)
    )
    obj.add_state(state2)
    
    # Should skip computation, no divide by zero
    assert state2.transform.speed is None


def test_state_buffer_management():
    """Test that only last 3 states are kept in memory."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    # Add 5 states
    for i in range(5):
        state = ObjectState(
            timestamp=float(i),
            transform=Transform(u=float(i*10), v=0, altitude=1000)
        )
        obj.add_state(state)
    
    # Should only keep last 3 states
    assert len(obj.states) == 3
    assert obj.states[0].timestamp == 2.0
    assert obj.states[1].timestamp == 3.0
    assert obj.states[2].timestamp == 4.0
    
    # But first and last state should be preserved
    assert obj.first_state.timestamp == 0.0
    assert obj.last_state.timestamp == 4.0


def test_vertical_speed_computation():
    """Test vertical speed computation."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000)
    )
    obj.add_state(state1)
    
    # Climbing 50 meters in 1 second
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=0, v=0, altitude=1050)
    )
    obj.add_state(state2)
    
    assert state2.transform.vertical_speed == pytest.approx(50.0, abs=0.001)
    
    # Descending 30 meters in 1 second
    state3 = ObjectState(
        timestamp=2.0,
        transform=Transform(u=0, v=0, altitude=1020)
    )
    obj.add_state(state3)
    
    assert state3.transform.vertical_speed == pytest.approx(-30.0, abs=0.001)


def test_turn_rate_wraparound():
    """Test yaw angle wraparound handling."""
    obj = TacviewObject(object_id="1", type_class="Air")
    
    state1 = ObjectState(
        timestamp=0.0,
        transform=Transform(u=0, v=0, altitude=1000, yaw=350)
    )
    obj.add_state(state1)
    
    # Crossing 360/0 boundary: 350 -> 10 should be +20 degrees, not -340
    state2 = ObjectState(
        timestamp=1.0,
        transform=Transform(u=10, v=0, altitude=1000, yaw=10)
    )
    obj.add_state(state2)
    
    # Should handle wraparound correctly
    assert state2.transform.turn_rate == pytest.approx(20.0, abs=0.001)
    
    # Reverse: 10 -> 350 should be -20 degrees, not +340
    state3 = ObjectState(
        timestamp=2.0,
        transform=Transform(u=20, v=0, altitude=1000, yaw=350)
    )
    obj.add_state(state3)
    
    assert state3.transform.turn_rate == pytest.approx(-20.0, abs=0.001)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

