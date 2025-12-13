"""Data types for ACMI parsing."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import math


@dataclass
class Transform:
    """Transform data from ACMI file with computed kinematic fields."""

    # Raw data from ACMI
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    altitude: Optional[float] = None  # meters
    roll: Optional[float] = None  # degrees
    pitch: Optional[float] = None  # degrees
    yaw: Optional[float] = None  # degrees
    u: Optional[float] = None  # Flat world X coordinate (meters)
    v: Optional[float] = None  # Flat world Y coordinate (meters)
    heading: Optional[float] = None  # degrees

    # Computed kinematic fields
    speed: Optional[float] = None  # m/s - 3D speed (TAS)
    vertical_speed: Optional[float] = None  # m/s
    turn_rate: Optional[float] = None  # deg/sec
    turn_radius: Optional[float] = None  # meters
    
    # Acceleration (m/s²) - world frame
    ax: Optional[float] = None
    ay: Optional[float] = None
    az: Optional[float] = None
    
    # G-loading (1.0 = 1g)
    g_load: Optional[float] = None
    
    # Energy state (for fixed-wing aircraft)
    potential_energy: Optional[float] = None  # Joules (PE = mgh)
    kinetic_energy: Optional[float] = None    # Joules (KE = 0.5mv²)
    specific_energy: Optional[float] = None   # meters (Es = h + v²/2g)


@dataclass
class ObjectState:
    """Object state at a specific timestamp."""

    timestamp: float
    transform: Transform
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TacviewObject:
    """Tacview object with all attributes and states."""

    object_id: str
    name: Optional[str] = None
    type: Optional[str] = None
    type_class: Optional[str] = None
    type_attributes: Optional[str] = None  # Comma-separated attributes
    type_basic: Optional[str] = None
    type_specific: Optional[str] = None
    pilot: Optional[str] = None
    group: Optional[str] = None
    coalition: Optional[str] = None
    color: Optional[str] = None
    country: Optional[str] = None
    parent_id: Optional[str] = None  # For weapons - launching platform object_id
    properties: Dict[str, Any] = field(default_factory=dict)
    states: List[ObjectState] = field(default_factory=list)

    # Computed fields
    first_seen: Optional[float] = None
    last_seen: Optional[float] = None
    removed_at: Optional[float] = None  # Timestamp when object was explicitly removed
    
    # Keep first and last states for efficient enrichment (spawn/impact detection)
    first_state: Optional[ObjectState] = None
    last_state: Optional[ObjectState] = None

    def should_compute_kinematics(self) -> str:
        """
        Determine what kinematics to compute based on parsed object type.
        
        Returns:
            'full' - All kinematics (aircraft, weapons)
            'speed' - Speed only (ground vehicles, ships)
            'none' - No kinematics (static, decoys, buildings)
        """
        # Check if static
        if self.type_attributes and 'Static' in self.type_attributes:
            return 'none'
        
        # Aircraft - full kinematics
        if self.type_class == 'Air':
            return 'full'
        
        # Weapons - full kinematics
        if self.type_class == 'Weapon':
            return 'full'
        
        # Ground vehicles - speed only (not static)
        if self.type_class == 'Ground' and self.type_basic in ['Vehicle', 'Armor', 'AntiAircraft']:
            return 'speed'
        
        # Ships - speed only
        if self.type_class == 'Sea':
            return 'speed'
        
        # Everything else (buildings, decoys, waypoints, etc.) - nothing
        return 'none'

    def add_state(self, new_state: ObjectState):
        """
        Add state with enhanced kinematics computation.
        Memory-efficient: keeps only last 3 states for computation.
        
        Computes for Air/Weapon types:
        - Velocity, speed, vertical speed, turn rate
        - Acceleration (ax, ay, az) starting at State N=2
        - G-loading starting at State N=2
        - Turn radius from speed and turn rate
        """
        kinematic_mode = self.should_compute_kinematics()
        
        if len(self.states) >= 1:
            prev_state = self.states[-1]
            time_delta = new_state.timestamp - prev_state.timestamp
            
            if time_delta > 0:
                # 1. Compute velocity components (world frame using U/V coordinates)
                if all(x is not None for x in [
                    new_state.transform.u, new_state.transform.v, new_state.transform.altitude,
                    prev_state.transform.u, prev_state.transform.v, prev_state.transform.altitude
                ]):
                    vx = (new_state.transform.u - prev_state.transform.u) / time_delta
                    vy = (new_state.transform.v - prev_state.transform.v) / time_delta
                    vz = (new_state.transform.altitude - prev_state.transform.altitude) / time_delta
                    
                    # 2. Speed (3D TAS) - reusing velocity computation
                    speed = math.sqrt(vx**2 + vy**2 + vz**2)
                    new_state.transform.speed = speed
                    
                    # Cache velocity for next iteration (acceleration computation)
                    new_state._velocity_cache = (vx, vy, vz)
                    
                    # 3. Acceleration (starting at State N=2, assuming v₀=0 for N=1)
                    if kinematic_mode == 'full':
                        # Get previous velocity (or assume zero for first velocity state)
                        if hasattr(prev_state, '_velocity_cache'):
                            prev_vx, prev_vy, prev_vz = prev_state._velocity_cache
                        else:
                            # State N=2: assume initial velocity was zero
                            prev_vx, prev_vy, prev_vz = 0.0, 0.0, 0.0
                        
                        # Acceleration components
                        ax = (vx - prev_vx) / time_delta
                        ay = (vy - prev_vy) / time_delta
                        az = (vz - prev_vz) / time_delta
                        
                        new_state.transform.ax = ax
                        new_state.transform.ay = ay
                        new_state.transform.az = az
                        
                        # 4. G-loading (compensate for gravity in Z-axis)
                        g = 9.81
                        g_load = math.sqrt(ax**2 + ay**2 + (az + g)**2) / g
                        new_state.transform.g_load = g_load
                
                # 5. Vertical speed (existing, keep current - for all kinematic modes)
                if kinematic_mode == 'full':
                    if new_state.transform.altitude is not None and prev_state.transform.altitude is not None:
                        new_state.transform.vertical_speed = (
                            new_state.transform.altitude - prev_state.transform.altitude
                        ) / time_delta
                    
                    # 6. Energy state (for all full-kinematic objects)
                    if new_state.transform.altitude is not None and new_state.transform.speed is not None:
                        mass = 17000.0  # kg (36,000 lbs rounded to nearest metric ton)
                        g = 9.81
                        
                        # Potential energy: PE = mgh
                        new_state.transform.potential_energy = mass * g * new_state.transform.altitude
                        
                        # Kinetic energy: KE = 0.5mv²
                        new_state.transform.kinetic_energy = 0.5 * mass * (new_state.transform.speed ** 2)
                        
                        # Specific energy (mass-independent): Es = h + v²/(2g)
                        new_state.transform.specific_energy = new_state.transform.altitude + ((new_state.transform.speed ** 2) / (2 * g))
                    
                    # 7. Turn rate (existing, keep current)
                    if new_state.transform.yaw is not None and prev_state.transform.yaw is not None:
                        yaw_delta = new_state.transform.yaw - prev_state.transform.yaw
                        # Handle 360-degree wraparound
                        if yaw_delta > 180:
                            yaw_delta -= 360
                        elif yaw_delta < -180:
                            yaw_delta += 360
                        new_state.transform.turn_rate = yaw_delta / time_delta
                        
                        # 8. Turn radius (efficient formula)
                        if new_state.transform.speed and abs(new_state.transform.turn_rate) > 0.01:
                            omega_rad = abs(new_state.transform.turn_rate) * math.pi / 180.0
                            new_state.transform.turn_radius = new_state.transform.speed / omega_rad
        
        # Update state buffer (existing logic)
        if self.first_state is None:
            self.first_state = new_state
            # First state defaults for full kinematics
            if self.should_compute_kinematics() == 'full':
                new_state.transform.g_load = 1.0
                new_state.transform.ax = 0.0
                new_state.transform.ay = 0.0
                new_state.transform.az = 0.0
        
        self.last_state = new_state
        
        # Keep only last 3 states (memory-efficient)
        self.states.append(new_state)
        if len(self.states) > 3:
            self.states.pop(0)
        
        self.update_time_bounds_from_timestamp(new_state.timestamp)
    
    def update_time_bounds_from_timestamp(self, timestamp: float):
        """Update time bounds from timestamp without iterating states."""
        if self.first_seen is None or timestamp < self.first_seen:
            self.first_seen = timestamp
        if self.last_seen is None or timestamp > self.last_seen:
            self.last_seen = timestamp

    def update_time_bounds(self):
        """Update first_seen and last_seen from states (legacy - prefer update_time_bounds_from_timestamp)."""
        if self.states:
            # Use running update for each state instead of iteration
            for state in self.states:
                self.update_time_bounds_from_timestamp(state.timestamp)

