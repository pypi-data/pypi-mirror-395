"""ACMI v2.2 parser implementation."""

from pathlib import Path
from typing import Dict, List, Optional, Union
import re

from .types import Transform, ObjectState, TacviewObject
from .utils import open_acmi_file, parse_property_value, unescape_property, parse_transform


class ACMIParser:
    """Parser for Tacview ACMI v2.2 files."""

    def __init__(self, store):
        """
        Initialize ACMI parser.
        
        Args:
            store: DuckDBStore instance to write parsed data to
        """
        self.store = store
        self.objects: Dict[str, TacviewObject] = {}
        self.metadata: Dict[str, any] = {}
        self.events: List[tuple] = []  # List of (object_id, timestamp, event_name, event_params)
        self.current_timestamp: float = 0.0
        
        # Reference point for coordinate offset conversion
        self.reference_latitude: float = 0.0
        self.reference_longitude: float = 0.0
        
        # Batch writing
        self.batch_size: int = 1000
        self.states_batch: List = []
        
        # Progress tracking
        self.lines_parsed: int = 0
        self.states_written: int = 0
        self.progress_interval: int = 10000  # Report every N lines
        self.total_lines: Optional[int] = None  # Total lines in file (for progress bar)
        
        # Decoy interpolation support
        # Decoys update at ~2Hz (0.5s gaps) - interpolate to 4Hz (0.25s gaps)
        # to improve proximity detection for fast missiles (Mach 2 = 343m in 0.5s)
        self.interpolate_decoys: bool = True
        self.decoy_target_interval: float = 0.25  # Target 4Hz update rate
        self.last_decoy_states: Dict[str, ObjectState] = {}  # Track last state per decoy

    
    def _count_lines_if_text_file(self, filepath: Union[str, Path]) -> Optional[int]:
        """
        Count total lines in file if it's a plain text file.
        Returns None for ZIP files (to avoid extraction overhead).
        
        Args:
            filepath: Path to ACMI file
            
        Returns:
            Total line count for plain text files, None for ZIP files
        """
        filepath = Path(filepath)
        
        # Check if it's a ZIP file
        try:
            with open(filepath, "rb") as f:
                magic = f.read(4)
            
            if magic.startswith(b"PK"):
                # ZIP file - skip line counting (would need extraction)
                return None
            
            # Plain text file - count lines efficiently
            with open(filepath, "rb") as f:
                line_count = sum(1 for _ in f)
            
            return line_count
        except Exception:
            # If we can't count lines, just return None (fallback to no progress bar)
            return None
    
    def parse(self, filepath: Union[str, Path]) -> tuple[Dict[str, TacviewObject], Dict[str, any]]:
        """
        Parse ACMI file and return objects and metadata.

        Args:
            filepath: Path to ACMI file (.txt.acmi, .zip.acmi, or .acmi)

        Returns:
            Tuple of (objects dict, metadata dict)
        """
        self.objects = {}
        self.current_timestamp = 0.0
        
        # Count total lines for progress bar (only for plain text files)
        self.total_lines = self._count_lines_if_text_file(filepath)
        
        # Show initial progress if no line count available (ZIP files, etc.)
        if not self.total_lines:
            print(f"  Progress: 50% (ingesting...)")

        with open_acmi_file(filepath) as f:
            self._parse_stream(f)
        
        # Final progress report at 100%
        if self.total_lines:
            print(f"  Progress: {self.lines_parsed:,} / {self.total_lines:,} lines (100.0%), {len(self.objects):,} objects, {self.states_written:,} states written")
        else:
            print(f"  Progress: 100% (complete) - {self.lines_parsed:,} lines, {len(self.objects):,} objects, {self.states_written:,} states written")
        
        # Flush any remaining states
        if self.states_batch:
            self._flush_states_batch()
        
        # Store events if any
        if self.events:
            self.store.add_events(self.events)

        return self.objects, self.metadata

    def _parse_stream(self, stream):
        """Parse ACMI stream line by line."""
        accumulated_line = ""
        
        for raw_line in stream:
            line = raw_line.rstrip("\n\r")
            self.lines_parsed += 1
            
            # Progress reporting
            if self.lines_parsed % self.progress_interval == 0:
                # Build progress message with optional progress bar
                if self.total_lines:
                    progress_pct = (self.lines_parsed / self.total_lines) * 100
                    progress_msg = f"  Progress: {self.lines_parsed:,} / {self.total_lines:,} lines ({progress_pct:.1f}%), {len(self.objects):,} objects, {self.states_written:,} states written"
                else:
                    progress_msg = f"  Progress: {self.lines_parsed:,} lines, {len(self.objects):,} objects, {self.states_written:,} states written"
                
                try:
                    import psutil
                    import os
                    process = psutil.Process(os.getpid())
                    memory_mb = process.memory_info().rss / 1024 / 1024
                    
                    # Count states still in memory
                    total_states_in_memory = sum(len(obj.states) for obj in self.objects.values())
                    batch_size = len(self.states_batch)
                    
                    print(progress_msg)
                    print(f"    Memory: {memory_mb:.0f} MB | In-memory states: {total_states_in_memory:,} obj.states + {batch_size:,} batch = {total_states_in_memory + batch_size:,} total")
                except ImportError:
                    print(progress_msg)

            # Handle line continuation (backslash at end)
            if line.endswith("\\"):
                # Remove trailing backslash and add content
                line_content = line[:-1]
                accumulated_line += line_content
                
                # Always add newline after content (backslash means "line continues, preserve newline")
                accumulated_line += "\n"
                continue
            
            # Complete line (either single line or end of multi-line)
            if accumulated_line:
                line = accumulated_line + line
                accumulated_line = ""
            
            # Skip empty lines
            if not line:
                continue

            # Header lines
            if line.startswith("FileType="):
                self.metadata["FileType"] = line.split("=", 1)[1]
            elif line.startswith("FileVersion="):
                self.metadata["FileVersion"] = line.split("=", 1)[1]
            # Time frame
            elif line.startswith("#"):
                self._parse_timestamp(line)
            # Object lines (including bare object IDs with no properties)
            elif "," in line or "=" in line or (len(line) > 0 and not line[0].isspace()):
                self._parse_object_line(line)

    def _parse_timestamp(self, line: str):
        """Parse timestamp line (#12.34)."""
        try:
            self.current_timestamp = float(line[1:])
        except ValueError:
            pass  # Skip invalid timestamps

    def _parse_object_line(self, line: str):
        """
        Parse object property line or removal line.

        Format: object_id,Property=Value,Property=Value,...
        or: -object_id (removal/destruction)
        or: object_id=Property=Value (for global properties when object_id=0)
        """
        # Check for object removal (lines starting with -)
        if line.startswith("-"):
            object_id = line[1:]  # Remove the - prefix
            if object_id in self.objects:
                self.objects[object_id].removed_at = self.current_timestamp
            return
        
        # Parse object_id and properties
        if "," not in line:
            # Could be:
            # 1. object_id=Property=Value format (rare)
            # 2. Bare object_id with no properties (valid but rare)
            if "=" in line:
                parts = line.split("=", 1)
                if len(parts) != 2:
                    return
                object_id = parts[0]
                properties_str = parts[1]
            else:
                # Bare object ID - valid but no properties to update
                object_id = line.strip()
                properties_str = ""
        else:
            first_comma = line.index(",")
            object_id = line[:first_comma]
            properties_str = line[first_comma + 1 :]

        # Parse properties (empty string returns empty dict)
        properties = self._parse_properties(properties_str) if properties_str else {}

        # Handle global properties (object 0)
        if object_id == "0":
            self.metadata.update(properties)
            # Extract reference point for coordinate offset conversion
            if "ReferenceLatitude" in properties:
                self.reference_latitude = float(properties["ReferenceLatitude"])
            if "ReferenceLongitude" in properties:
                self.reference_longitude = float(properties["ReferenceLongitude"])
            return

        # Get or create object
        if object_id not in self.objects:
            self.objects[object_id] = TacviewObject(
                object_id=object_id
            )

        obj = self.objects[object_id]

        # Extract transform if present
        transform_data = {}
        if "T" in properties:
            transform_data = parse_transform(properties["T"])
            del properties["T"]

        # Update object attributes
        self._update_object_attributes(obj, properties)

        # Create state if transform present or if it's a state update
        if transform_data or self.current_timestamp > 0:
            kinematic_mode = obj.should_compute_kinematics()
            
            # For objects with 'none' kinematics: only create states for containers and decoys
            # (needed for enrichment parent/target detection)
            if kinematic_mode == 'none':
                # Only create states for containers and decoys (they need position data for enrichment)
                if transform_data and (obj.type_specific == 'Container' or obj.type_basic == 'Decoy' or obj.type_basic == 'Projectile'):
                    # Convert coordinate offsets to absolute coordinates
                    if 'latitude' in transform_data and transform_data['latitude'] is not None:
                        transform_data['latitude'] += self.reference_latitude
                    if 'longitude' in transform_data and transform_data['longitude'] is not None:
                        transform_data['longitude'] += self.reference_longitude
                    
                    # For FIRST state: default NULL altitude to 0 (sea level)
                    # This propagates through missing value completion logic
                    if not obj.states and ('altitude' not in transform_data or transform_data.get('altitude') is None):
                        transform_data['altitude'] = 0.0
                    
                    # Create state with position data but no kinematics
                    transform = Transform(**transform_data)
                    state = ObjectState(
                        timestamp=self.current_timestamp, 
                        transform=transform, 
                        properties={}
                    )
                    obj.states.append(state)
                    obj.update_time_bounds_from_timestamp(self.current_timestamp)
                    
                    # Add to batch for DB insert
                    self.states_batch.append((obj.object_id, state))
                    
                    # Interpolate intermediate states for decoys (improves proximity detection)
                    if obj.type_basic == 'Decoy':
                        self._interpolate_decoy_states(obj.object_id, obj, state)
                    
                    if len(self.states_batch) >= self.batch_size:
                        self._flush_states_batch()
                else:
                    # No position data or not a container/decoy, just update time bounds
                    obj.update_time_bounds_from_timestamp(self.current_timestamp)
                return
            
            # Check if we already have a state at this exact timestamp
            if obj.states and obj.states[-1].timestamp == self.current_timestamp:
                # MERGE: Update existing state in place (multiple updates at same timestamp)
                existing_transform = obj.states[-1].transform
                for key, value in transform_data.items():
                    setattr(existing_transform, key, value)
                
                # Also update the corresponding entry in states_batch if present
                for i in range(len(self.states_batch) - 1, -1, -1):
                    if self.states_batch[i][0] == obj.object_id and self.states_batch[i][1].timestamp == self.current_timestamp:
                        self.states_batch[i] = (obj.object_id, obj.states[-1])
                        break
                return
            
            # Merge delta with previous full state (Tacview sends partial updates!)
            full_transform_data = {}
            if obj.states:
                # Copy last state's full transform (coordinates are already absolute)
                last = obj.states[-1].transform
                full_transform_data = {
                    'longitude': last.longitude,
                    'latitude': last.latitude,
                    'altitude': last.altitude,
                    'roll': last.roll,
                    'pitch': last.pitch,
                    'yaw': last.yaw,
                    'u': last.u,
                    'v': last.v,
                    'heading': last.heading,
                }
            
            # Apply delta update (only fields present in transform_data)
            # NOTE: Only apply reference offset to NEW coordinate values from the delta
            # Copied coordinates from previous state are already absolute
            for key, value in transform_data.items():
                if value is not None:
                    # Add reference offset only to NEW lat/lon values in the delta
                    if key == 'latitude':
                        full_transform_data[key] = value + self.reference_latitude
                    elif key == 'longitude':
                        full_transform_data[key] = value + self.reference_longitude
                    else:
                        full_transform_data[key] = value
            
            # For FIRST state: default NULL altitude to 0 (sea level)
            # This propagates through missing value completion logic
            if not obj.states and ('altitude' not in full_transform_data or full_transform_data.get('altitude') is None):
                full_transform_data['altitude'] = 0.0
            
            # Create FULL state for database
            transform = Transform(**full_transform_data)
            state = ObjectState(
                timestamp=self.current_timestamp, 
                transform=transform, 
                properties={}  # Don't store properties in states - saves massive memory
            )
            
            # Update object time bounds and compute kinematics from last state
            obj.add_state(state)
            
            # Add to batch for DB insert
            self.states_batch.append((obj.object_id, state))
            
            # Flush batch if full
            if len(self.states_batch) >= self.batch_size:
                self._flush_states_batch()
    
    def _interpolate_decoy_states(self, object_id: str, obj: TacviewObject, current_state: ObjectState):
        """
        Interpolate intermediate states for decoys to improve proximity detection.
        
        Decoys update at ~2Hz (0.5s gaps), but fast missiles (Mach 2) travel 343m in that time.
        This interpolates to 4Hz (0.25s gaps), reducing the gap to 172m.
        
        Args:
            object_id: The object ID
            obj: The TacviewObject (must be a decoy)
            current_state: The newly created state
        """
        if not self.interpolate_decoys or obj.type_basic != 'Decoy':
            return
        
        # Check if we have a previous state for this decoy
        last_state = self.last_decoy_states.get(object_id)
        if not last_state:
            # First state for this decoy, just store it
            self.last_decoy_states[object_id] = current_state
            return
        
        # Calculate time gap
        time_gap = current_state.timestamp - last_state.timestamp
        
        # Only interpolate if gap is larger than target interval and we have valid positions
        if time_gap <= self.decoy_target_interval:
            self.last_decoy_states[object_id] = current_state
            return
        
        # Check if both states have valid coordinates
        if (last_state.transform.longitude is None or last_state.transform.latitude is None or
            current_state.transform.longitude is None or current_state.transform.latitude is None):
            self.last_decoy_states[object_id] = current_state
            return
        
        # Calculate number of interpolation points needed
        num_intervals = int(time_gap / self.decoy_target_interval)
        if num_intervals < 2:
            # Not enough gap, skip interpolation
            self.last_decoy_states[object_id] = current_state
            return
        
        # Interpolate states
        for i in range(1, num_intervals):
            # Linear interpolation factor (0 < t < 1)
            t = i / num_intervals
            
            # Interpolate timestamp
            interp_time = last_state.timestamp + t * time_gap
            
            # Interpolate position (linear interpolation)
            interp_lon = last_state.transform.longitude + t * (current_state.transform.longitude - last_state.transform.longitude)
            interp_lat = last_state.transform.latitude + t * (current_state.transform.latitude - last_state.transform.latitude)
            
            # Interpolate altitude if available
            interp_alt = None
            if last_state.transform.altitude is not None and current_state.transform.altitude is not None:
                interp_alt = last_state.transform.altitude + t * (current_state.transform.altitude - last_state.transform.altitude)
            
            # Create interpolated transform (only position data for decoys)
            interp_transform = Transform(
                longitude=interp_lon,
                latitude=interp_lat,
                altitude=interp_alt,
                u=None, v=None,  # Decoys don't have U/V
                roll=None, pitch=None, yaw=None, heading=None
            )
            
            # Create interpolated state
            interp_state = ObjectState(
                timestamp=interp_time,
                transform=interp_transform,
                properties={}
            )
            
            # Add to batch for DB insert
            self.states_batch.append((object_id, interp_state))
        
        # Update last known state
        self.last_decoy_states[object_id] = current_state
    
    def _flush_states_batch(self):
        """Flush states batch to storage (DB or Parquet staging)."""
        if not self.states_batch:
            return
        
        # Prefer Parquet staging (auto-initializes on first call) over direct DB insert
        if hasattr(self.store, 'stage_states_batch'):
            try:
                self.store.stage_states_batch(self.states_batch)
            except Exception as e:
                # If staging fails, fall back to direct DB insert
                import warnings
                warnings.warn(f"Parquet staging failed, using slower fallback: {e}")
                self.store.add_states_batch(self.states_batch)
        else:
            self.store.add_states_batch(self.states_batch)
        self.states_written += len(self.states_batch)
        self.states_batch = []

    def _parse_properties(self, properties_str: str) -> Dict[str, any]:
        """
        Parse property string into dictionary.

        Handles: Property=Value,Property=Value,...
        Supports escaped commas in values.
        """
        properties = {}
        current_key = None
        current_value = []
        in_escape = False

        i = 0
        while i < len(properties_str):
            char = properties_str[i]

            if char == "\\" and not in_escape:
                in_escape = True
                current_value.append(char)
            elif char == "=" and not in_escape and current_key is None:
                # Found key=value separator
                current_key = "".join(current_value).strip()
                current_value = []
            elif char == "," and not in_escape:
                # End of property
                if current_key:
                    value = unescape_property("".join(current_value))
                    # Don't parse "T" (Transform) as it must remain a string
                    if current_key == "T":
                        properties[current_key] = value
                    else:
                        properties[current_key] = parse_property_value(value)
                current_key = None
                current_value = []
            else:
                current_value.append(char)
                in_escape = False

            i += 1

        # Handle last property
        if current_key:
            value = unescape_property("".join(current_value))
            # Don't parse "T" (Transform) as it must remain a string
            if current_key == "T":
                properties[current_key] = value
            else:
                properties[current_key] = parse_property_value(value)

        return properties

    def _update_object_attributes(self, obj: TacviewObject, properties: Dict[str, any]):
        """Update object attributes from properties."""
        if "Name" in properties:
            obj.name = str(properties["Name"])
        if "Type" in properties:
            obj.type = str(properties["Type"])
            # Parse type into structured components
            from .type_parser import parse_type, format_attributes
            parsed = parse_type(obj.type)
            obj.type_class = parsed.type_class
            obj.type_attributes = format_attributes(parsed.type_attributes)
            obj.type_basic = parsed.type_basic
            obj.type_specific = parsed.type_specific
        if "Pilot" in properties:
            obj.pilot = str(properties["Pilot"])
        if "Group" in properties:
            obj.group = str(properties["Group"])
        if "Coalition" in properties:
            obj.coalition = str(properties["Coalition"])
        if "Color" in properties:
            obj.color = str(properties["Color"])
        if "Country" in properties:
            obj.country = str(properties["Country"])
        if "Parent" in properties:
            obj.parent_id = str(properties["Parent"])
        
        # Handle events
        if "Event" in properties:
            event_str = str(properties["Event"])
            # Event format: EventName|Param1|Param2|...
            parts = event_str.split("|", 1)
            event_name = parts[0]
            event_params = parts[1] if len(parts) > 1 else ""
            self.events.append((obj.object_id, self.current_timestamp, event_name, event_params))

        # Store other properties (excluding standard ones and Event)
        for key, value in properties.items():
            if key not in ["Name", "Type", "Pilot", "Group", "Coalition", "Color", "Country", "Parent", "T", "Event"]:
                obj.properties[key] = value

