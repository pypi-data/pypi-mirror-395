"""Hash generation utilities for database naming."""

import hashlib
from typing import Dict, Any


def generate_db_hash(metadata: Dict[str, Any]) -> str:
    """
    Generate hash from recording metadata for database filename.

    Uses key metadata fields (Title, RecordingTime, Author) to create
    a unique identifier for the recording.

    Args:
        metadata: Recording metadata dictionary

    Returns:
        16-character hex hash string
    """
    # Use key metadata fields for hash
    title = metadata.get("Title", "")
    recording_time = metadata.get("RecordingTime", "")
    author = metadata.get("Author", "")

    hash_input = f"{title}-{recording_time}-{author}"
    return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

