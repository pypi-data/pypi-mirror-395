"""
ACMI Type Tag Parser

Parses Tacview type strings like "Air+FixedWing" or "Ground+Static+Vehicle+Light"
into structured components based on the ACMI 2.2 specification.
"""

from typing import Optional, List
from dataclasses import dataclass

# Type categories from ACMI 2.2 spec
CLASSES = {
    'Air', 'Ground', 'Sea', 'Weapon', 'Sensor', 'Navaid', 'Misc'
}

ATTRIBUTES = {
    'Static', 'Heavy', 'Medium', 'Light', 'Minor'
}

BASIC_TYPES = {
    'FixedWing', 'Rotorcraft', 'Armor', 'AntiAircraft', 'Vehicle',
    'Watercraft', 'Human', 'Biologic', 'Missile', 'Rocket', 'Bomb',
    'Torpedo', 'Projectile', 'Beam', 'Decoy', 'Building', 'Bullseye', 'Waypoint'
}

SPECIFIC_TYPES = {
    'Tank', 'Warship', 'AircraftCarrier', 'Submarine', 'Infantry',
    'Parachutist', 'Shell', 'Bullet', 'Grenade', 'Flare', 'Chaff',
    'SmokeGrenade', 'Aerodrome', 'Container', 'Shrapnel', 'Explosion'
}


@dataclass
class ParsedType:
    """Parsed type components."""
    type_class: Optional[str] = None
    type_attributes: List[str] = None
    type_basic: Optional[str] = None
    type_specific: Optional[str] = None
    
    def __post_init__(self):
        if self.type_attributes is None:
            self.type_attributes = []


def parse_type(type_string: str) -> ParsedType:
    """
    Parse ACMI type string into structured components.
    
    Args:
        type_string: Type string like "Air+FixedWing" or "Ground+Static+Vehicle+Light"
    
    Returns:
        ParsedType object with categorized components
    
    Examples:
        >>> parse_type("Air+FixedWing")
        ParsedType(type_class='Air', type_basic='FixedWing', ...)
        
        >>> parse_type("Ground+Static+Vehicle+Light")
        ParsedType(type_class='Ground', type_attributes=['Static', 'Light'], 
                   type_basic='Vehicle', ...)
    """
    if not type_string:
        return ParsedType()
    
    tags = type_string.split('+')
    result = ParsedType()
    
    for tag in tags:
        tag = tag.strip()
        if not tag:
            continue
            
        if tag in CLASSES:
            result.type_class = tag
        elif tag in ATTRIBUTES:
            result.type_attributes.append(tag)
        elif tag in BASIC_TYPES:
            result.type_basic = tag
        elif tag in SPECIFIC_TYPES:
            result.type_specific = tag
    
    return result


def format_attributes(attributes: List[str]) -> Optional[str]:
    """
    Format attributes list as comma-separated string.
    
    Args:
        attributes: List of attribute tags
    
    Returns:
        Comma-separated string or None if empty
    """
    if not attributes:
        return None
    return ','.join(sorted(attributes))

