"""Parsing utilities."""

import zipfile
import io
from pathlib import Path
from typing import TextIO, Union


def open_acmi_file(filepath: Union[str, Path]):
    """
    Open ACMI file, automatically handling compressed formats.
    
    Returns a context manager that provides line-by-line streaming
    without loading the entire file into memory.

    Supports:
    - .txt.acmi - uncompressed text files
    - .zip.acmi - ZIP compressed files (may contain .txt.acmi, .acmi, or acmi.txt)
    - .acmi - auto-detect format (check ZIP magic bytes)

    Args:
        filepath: Path to ACMI file

    Returns:
        Context manager providing text stream (use with 'with' statement)

    Raises:
        ValueError: If no valid ACMI file found in ZIP archive
        
    Example:
        with open_acmi_file('recording.zip.acmi') as f:
            for line in f:
                process(line)
    """
    filepath = Path(filepath)

    # Check if it's a ZIP file
    with open(filepath, "rb") as f:
        magic = f.read(4)
    
    if magic.startswith(b"PK"):
        # It's a ZIP file - return streaming wrapper
        return _ZipACMIReader(filepath)
    else:
        # Plain text ACMI file
        return open(filepath, "r", encoding="utf-8-sig")


class _ZipACMIReader:
    """Context manager for streaming ACMI content from ZIP archives."""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.zipfile = None
        self.acmi_file = None
        
    def __enter__(self):
        # Open ZIP file
        self.zipfile = zipfile.ZipFile(self.filepath, 'r')
        
        # Find ACMI file in archive
        acmi_files = [
            name for name in self.zipfile.namelist()
            if (name.endswith(".txt.acmi") or name.endswith(".acmi") 
                or name.endswith("acmi.txt") or name == "acmi.txt")
        ]
        if not acmi_files:
            self.zipfile.close()
            raise ValueError(
                f"No .txt.acmi, .acmi, or acmi.txt file found in ZIP archive: {self.filepath}"
            )
        
        # Prefer .txt.acmi over .acmi, then acmi.txt
        acmi_filename = next(
            (f for f in acmi_files if f.endswith(".txt.acmi")),
            next(
                (f for f in acmi_files if f.endswith("acmi.txt")),
                acmi_files[0],
            ),
        )
        
        # Open file in ZIP for streaming (returns binary stream)
        binary_stream = self.zipfile.open(acmi_filename, 'r')
        
        # Wrap in text decoder for line-by-line reading
        import codecs
        self.acmi_file = codecs.getreader('utf-8-sig')(binary_stream)
        
        return self.acmi_file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.acmi_file:
            self.acmi_file.close()
        if self.zipfile:
            self.zipfile.close()


def parse_property_value(value: str) -> Union[str, float, int]:
    """
    Parse property value, converting to appropriate type.

    Args:
        value: Property value string

    Returns:
        Parsed value (str, float, or int)
    """
    value = value.strip()

    # Try int
    try:
        return int(value)
    except ValueError:
        pass

    # Try float
    try:
        return float(value)
    except ValueError:
        pass

    # Return as string
    return value


def unescape_property(value: str) -> str:
    """
    Unescape property value (handle escaped commas, newlines).

    ACMI uses backslash escaping for special characters.

    Args:
        value: Escaped property value

    Returns:
        Unescaped value
    """
    return value.replace("\\,", ",").replace("\\n", "\n").replace("\\\\", "\\")


def parse_transform(transform_str: str) -> dict:
    """
    Parse transform string from ACMI.
    
    Supports 4 different forms:
    1. T=lon|lat|alt (3 fields) - Simple spherical
    2. T=lon|lat|alt|u|v (5 fields) - Simple flat world
    3. T=lon|lat|alt|roll|pitch|yaw (6 fields) - Complex spherical
    4. T=lon|lat|alt|roll|pitch|yaw|u|v|heading (9 fields) - Complex flat world (FULL)

    Args:
        transform_str: Transform string without 'T=' prefix

    Returns:
        Dictionary of transform fields (empty dict if malformed)
    """
    # Ensure we have a string (defensive check)
    if not isinstance(transform_str, str):
        return {}
    
    parts = transform_str.split("|")
    num_parts = len(parts)
    
    # Validate minimum transform requirements (at least lon|lat|alt)
    if num_parts < 3:
        # Malformed/partial transform (e.g., truncated file, network interruption)
        # Silently skip - this is expected at end of partial recordings
        return {}
    
    result = {}
    
    # Detect form by number of pipe-delimited parts
    if num_parts == 3:
        # Form 1: Simple spherical - T=lon|lat|alt
        fields = ["longitude", "latitude", "altitude"]
    elif num_parts == 5:
        # Form 2: Simple flat world - T=lon|lat|alt|u|v
        fields = ["longitude", "latitude", "altitude", "u", "v"]
    elif num_parts == 6:
        # Form 3: Complex spherical - T=lon|lat|alt|roll|pitch|yaw
        fields = ["longitude", "latitude", "altitude", "roll", "pitch", "yaw"]
    else:
        # Form 4 (9 parts) or delta updates (any count) - Use full field list
        fields = ["longitude", "latitude", "altitude", "roll", "pitch", "yaw", "u", "v", "heading"]
    
    # Parse available fields
    for i, field in enumerate(fields):
        if i < len(parts) and parts[i].strip():
            try:
                result[field] = float(parts[i])
            except ValueError:
                pass  # Skip invalid values

    return result

