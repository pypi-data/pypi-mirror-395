"""High-level API for parsing ACMI files."""

import math
from pathlib import Path
from typing import Union, Optional, List

import duckdb
from duckdb.typing import DOUBLE

from .__version__ import __version__
from .parser.acmi_parser import ACMIParser
from .storage.duckdb_store import DuckDBStore


def parse_acmi(
    filepath: Union[str, Path],
    output_dir: Union[str, Path] = "timeline_data",
    enrichments: Optional[List[str]] = None,
    async_enrichments: bool = True,
    progress: bool = False,
    drop_existing: bool = True,
) -> DuckDBStore:
    """
    Parse ACMI file and store in DuckDB database.

    Args:
        filepath: Path to ACMI file (.txt.acmi, .zip.acmi, or .acmi)
        output_dir: Directory for output database (default: 'timeline_data')
        enrichments: List of enrichment names to apply. None = use product defaults (recommended),
                    [] = no enrichments, ['weapons', ...] = specific enrichments
        async_enrichments: Run enrichments in background thread (default: False, experimental)
        progress: Show progress information
        drop_existing: Drop existing database if it exists (default: True)

    Returns:
        DuckDBStore instance with database_path property

    Example:
        >>> # Default: Use product-specific enrichments (e.g., DCS auto-enriches)
        >>> store = parse_acmi('recording.acmi', output_dir='data/')
        >>> aircraft = store.query_sql("SELECT * FROM objects WHERE type_basic = 'FixedWing'")
        
        >>> # Explicit: No enrichments
        >>> store = parse_acmi('recording.acmi', enrichments=[])
        
    Async Mode Example (Experimental):
        >>> # Set async_enrichments=True for background enrichments
        >>> store = parse_acmi('recording.acmi', async_enrichments=True)
        >>> # Query immediately (enrichments run in background)
        >>> aircraft = store.query_sql("SELECT * FROM objects WHERE type_basic = 'FixedWing'")
        >>> # Wait for enrichments if needed
        >>> store.wait_for_enrichments()
    """
    import time
    start_time = time.time()
    
    if progress:
        print(f"Parsing ACMI file: {filepath}")
    
    # Step 1: Quick scan to get metadata from header (first ~100 lines)
    metadata = {}
    from .parser.utils import open_acmi_file
    
    # Create temporary in-memory store just for metadata extraction
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_store = DuckDBStore(temp_dir)
        temp_parser = ACMIParser(temp_store)
        
        with open_acmi_file(filepath) as f:
            accumulated_line = ""
            for i, line in enumerate(f):
                if i > 100:  # Metadata is always at the top (unless multi-line)
                    # If we're accumulating a multi-line value, continue until complete
                    if not accumulated_line:
                        break
                
                line = line.rstrip("\n\r")
                
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
                
                if line.startswith("FileType=") or line.startswith("FileVersion="):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        metadata[key] = value
                elif line.startswith("0,"):
                    props_str = line[2:]
                    props = temp_parser._parse_properties(props_str)
                    metadata.update(props)
    
    # Fallback: Use filename as Title if not found in metadata
    if not metadata.get("Title") or metadata.get("Title", "").strip() == "":
        # Convert filepath to Path object to handle extensions properly
        filepath_obj = Path(filepath)
        filename = filepath_obj.name
        
        # Remove ACMI extensions (.txt.acmi, .zip.acmi, or .acmi)
        if filename.endswith(".txt.acmi"):
            mission_name = filename[:-9]  # Remove .txt.acmi
        elif filename.endswith(".zip.acmi"):
            mission_name = filename[:-9]  # Remove .zip.acmi
        elif filename.endswith(".acmi"):
            mission_name = filename[:-5]  # Remove .acmi
        else:
            # No known extension, use full filename
            mission_name = filename
        
        metadata["Title"] = mission_name
        
        if progress:
            print(f"No mission name found in file, using filename: {mission_name}")
    
    # Step 2: Initialize DB with metadata
    # Add parser version for debugging
    metadata['parser_version'] = __version__

    # create Custom metadata fields from
    # 0,ReferenceLongitude=32
    # 0,ReferenceLatitude=30
    metadata["MetersPerDegLat"] = 111320
    metadata["MetersPerDegLon"] = 111320
    if metadata.get("ReferenceLatitude"):
        metadata["MetersPerDegLon"] = 111320 * math.cos(math.radians(metadata['ReferenceLatitude']))
    
    def calculate_approximate_distance_squared(delta_lat: float, delta_lon: float) -> float:
        return (delta_lat * metadata["MetersPerDegLat"])**2 + (delta_lon * metadata["MetersPerDegLon"])**2

    store = DuckDBStore(output_dir)
    
    # Initialize database (drop_existing handled inside initialize_from_metadata)
    if drop_existing and progress:
        from .storage.hash_utils import generate_db_hash
        db_hash = generate_db_hash(metadata)
        db_path = Path(output_dir) / f"{db_hash}.duckdb"
        if db_path.exists():
            print(f"Dropping existing database: {db_hash}.duckdb")
    
    store.initialize_from_metadata(metadata, drop_existing=drop_existing)
    
    # Register UDF for approximate distance calculations (available in all queries)
    store.register_udf(
        "calculate_approximate_distance_squared", 
        calculate_approximate_distance_squared,
        [DOUBLE, DOUBLE],
        DOUBLE
    )
    
    store.begin_bulk_load()
    
    if progress:
        print(f"Created database: {store.database_path}")
        print("Parsing with streaming inserts (Parquet staging auto-enabled)...")
    
    # Step 3: Parse with streaming - states written to DB as we go
    parser = ACMIParser(store)
    # Configure streaming batch size (default: 50k for performance)
    import os as _os
    _batch_size = int(_os.getenv("TACVIEW_BATCH_SIZE", "50000"))
    parser.batch_size = _batch_size
    objects, _ = parser.parse(filepath)  # States are staged or written to DB in real-time

    if progress:
        parse_time = time.time() - start_time
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024
            print(f"Parsed {len(objects)} objects in {parse_time:.1f}s (Memory: {memory_mb:.0f} MB)")
        except ImportError:
            print(f"Parsed {len(objects)} objects in {parse_time:.1f}s")

    if progress:
        print(f"Created database: {store.database_path}")

    # Import states AND objects FIRST (enrichment needs both)
    if progress:
        print("Importing states and objects to database...")
    
    db_start = time.time()
    try:
        # If Parquet staging was used, import shards now in one SQL
        if store._staging_states_dir:
            store.import_staged_states()
        
        # Add objects metadata (enrichment SQL queries need this)
        store.add_objects_metadata_bulk(list(objects.values()))
    except Exception as e:
        print(f"Warning: Failed to import data: {e}")

    # Database is now ready - all objects and states are available for querying
    
    # CRITICAL: Commit data before enrichments run
    # Enrichments create separate connections and need to see committed data
    store.end_bulk_load()
    
    # ALWAYS build indexes BEFORE enrichments (they need indexes for performance!)
    # Enrichments do complex JOINs and WHERE clauses that are 1000x+ slower without indexes
    if progress:
        print("Building indexes...")
    store.create_indexes()
    
    # Cleanup staging files after bulk load
    if store._staging_states_dir:
        store.cleanup_parquet_staging()
    
    # NOW apply enrichments (after BOTH states and objects are in database)
    # Handle enrichment defaults based on product type
    data_source = metadata.get('DataSource', '')
    
    if enrichments is None:
        # None = Use product-specific defaults
        if data_source.startswith('DCS'):
            # DCS-specific enrichments with sensible defaults
            # Build enrichment list with lifecycle ALWAYS last
            enrichments = ['coalitions', 'ejections', 'containers', 'decoys', 'weapons', 'missed_weapons']
            
            # Add projectiles before lifecycle (only if async)
            if async_enrichments:
                enrichments.append('projectiles')
            
            # lifecycle MUST be last (depends on weapons creating WEAPON_HIT events)
            enrichments.append('lifecycle')

            if progress:
                print(f"DCS recording detected - auto-enabling {len(enrichments)} enrichments: {', '.join(enrichments)}")
        else:
            # Other products: no enrichments by default (can be extended in future)
            enrichments = []
            if progress and data_source:
                print(f"Product '{data_source}' - no default enrichments configured")
    elif isinstance(enrichments, list):
        # Explicit list provided by user
        if data_source.startswith('DCS') and enrichments and progress:
            print(f"DCS recording with user-specified enrichments: {', '.join(enrichments)}")
    else:
        # Invalid type
        raise ValueError(f"enrichments must be None or List[str], got {type(enrichments)}")
    
    # Helper function to run enrichments (can be sync or async)
    def _run_enrichments():
        """Run all enrichments and finalize database."""
        import time
        
        if not enrichments:
            # No enrichments requested, nothing to do (indexes already built)
            return
        
        enrich_start = time.time()
        
        if progress:
            print(f"Applying enrichments: {', '.join(enrichments)}")
        
        # Call store's apply_enrichments method (single source of truth)
        try:
            store.apply_enrichments(
                enrichments=enrichments,
                async_enrichments=False,  # We handle async at parse_acmi level
                progress=progress
            )
        except Exception as e:
            if progress:
                print(f"Error during enrichments: {e}")
            raise
        
        if progress:
            enrich_time = time.time() - enrich_start
            print(f"Enrichment completed in {enrich_time:.1f}s")
        
        # Mark enrichments as complete and release self-reference
        # (indexes were already built before enrichments started)
        store._enrichments_complete = True
        store._self_reference = None  # Allow GC
    
    # Decide whether to run enrichments sync or async
    if async_enrichments and enrichments:
        # Run enrichments in background thread
        import threading
        
        if progress:
            print("Starting enrichments in background...")
            print(f"Database ready for queries at: {store.database_path}")
            print("Use store.wait_for_enrichments() to wait for completion")
        
        # Keep self-reference to prevent GC while enrichment thread is running
        store._self_reference = store
        
        thread = threading.Thread(
            target=_run_enrichments,
            name="EnrichmentThread",
            daemon=True
        )
        thread.start()
        
        # Store thread reference for later access
        store._enrichment_thread = thread
        store._enrichments_complete = False
        store._async_mode = True
    else:
        # Run enrichments synchronously (current behavior)
        store._async_mode = False
        _run_enrichments()
        
        if progress:
            db_time = time.time() - db_start
            total_time = time.time() - start_time
            summary = store.get_summary()
            print(f"Stored {summary['object_count']} objects with {summary['state_count']} states")
            print(f"Total time: {total_time:.1f}s")
            print(f"Database created at: {store.database_path}")

    return store

