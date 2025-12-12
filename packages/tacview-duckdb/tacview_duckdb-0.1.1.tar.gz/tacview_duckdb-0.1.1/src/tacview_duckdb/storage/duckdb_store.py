"""DuckDB storage implementation - Refactored version."""

import os
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

try:
    import duckdb
    import duckdb.typing
except ImportError:
    raise ImportError("duckdb is required. Install with: pip install duckdb>=1.4.0")

from ..parser.types import TacviewObject, ObjectState
from .hash_utils import generate_db_hash
from .schema import get_schema_sql, get_index_sql


class DuckDBStore:
    """
    DuckDB storage for Tacview data with multi-threaded support.
    
    Attributes:
        db_path: Path to the DuckDB database file
        db_hash: 16-character hash identifier for this database (derived from metadata)
        output_dir: Directory containing database files
    
    Architecture (based on DuckDB's MVCC concurrency model):
        - Internal writer connection (_write_conn): Used by parser and enrichments (single write thread)
        - Consumer connections: Created on-demand via get_query_connection() for concurrent queries
    
    DuckDB Concurrency (automatic via MVCC):
        - Single write thread: Parser + enrichments share _write_conn (no write conflicts)
        - Multiple readers: Each get_query_connection() call returns a new connection
        - No locks needed: DuckDB's MVCC handles concurrent reads during writes
        - All connections are read-write (DuckDB requirement - cannot mix configurations)
    
    Perfect for websocket streaming: write continuously, query concurrently.
    See: https://duckdb.org/docs/stable/connect/concurrency
    """

    def __init__(self, output_dir: Union[str, Path]):
        """
        Initialize DuckDB store.

        Args:
            output_dir: Directory where database files will be stored
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.db_path: Optional[Path] = None
        self.db_hash: Optional[str] = None  # Hash identifier for this database
        
        # Internal RW connection for parser/writer operations (shared with enrichments)
        self._write_conn: Optional[duckdb.DuckDBPyConnection] = None
        
        # Async enrichment tracking
        self._async_mode: bool = False
        self._enrichment_thread = None
        self._enrichments_complete: bool = True
        self._self_reference = None
        
        # Progress tracking
        self._enrichment_progress: float = 0.0
        self._current_enrichment: str = ""
        self._total_enrichments: int = 0
        self._completed_enrichments: int = 0
        
        # Batch insert tracking (DuckDB 1.4+ uses executemany, not Appender)
        self._rows_since_commit: int = 0
        self._commit_every_rows: int = 100000
        
        # User-defined functions to register on all connections
        self._registered_udfs: List[tuple] = []  # List of (name, func, param_types, return_type)

    @classmethod
    def from_path(cls, db_path: Union[str, Path]) -> "DuckDBStore":
        """
        Open existing database directly.

        Args:
            db_path: Path to existing DuckDB file

        Returns:
            DuckDBStore instance connected to database
        """
        db_path = Path(db_path)
        if not db_path.exists():
            raise FileNotFoundError(f"Database not found: {db_path}")

        store = cls(db_path.parent)
        store.db_path = db_path
        # Extract hash from filename (format: {hash}.duckdb)
        store.db_hash = db_path.stem
        store._write_conn = duckdb.connect(str(db_path))
        return store

    def initialize_from_metadata(self, metadata: Dict[str, Any], drop_existing: bool = True):
        """
        Create database with hash-based name from metadata.

        Args:
            metadata: Recording metadata dictionary
            drop_existing: If True, delete existing database file before connecting (default: True)
        """
        db_hash = generate_db_hash(metadata)
        self.db_hash = db_hash  # Store hash for external access
        self.db_path = self.output_dir / f"{db_hash}.duckdb"
        
        # Delete existing database file if requested
        if drop_existing and self.db_path.exists():
            import shutil
            
            if hasattr(self, '_write_conn') and self._write_conn:
                try:
                    self._write_conn.close()
                except Exception:
                    pass
                self._write_conn = None
            
            self.db_path.unlink()
            
            wal_path = Path(str(self.db_path) + ".wal")
            if wal_path.exists():
                wal_path.unlink()
            
            tmp_path = Path(str(self.db_path) + ".tmp")
            if tmp_path.exists():
                tmp_path.unlink()
            
            staging_dir = self.output_dir / ".staging"
            if staging_dir.exists():
                shutil.rmtree(staging_dir, ignore_errors=True)
        
        self._write_conn = duckdb.connect(str(self.db_path))
        
        # DuckDB automatically supports concurrent reads while writing
        # No explicit WAL configuration needed
        
        # Set memory limit to prevent OOM
        mem_limit = os.getenv("TACVIEW_MEMORY_LIMIT", None)
        if mem_limit:   
            self._write_conn.execute(f"SET memory_limit='{mem_limit}'")
        
        threads = os.getenv("TACVIEW_THREADS", None)
        if threads:
            self._write_conn.execute(f"SET threads={threads}")
        
        tmp_dir = os.getenv("TACVIEW_TEMP_DIRECTORY")
        if tmp_dir:
            try:
                self._write_conn.execute(f"SET temp_directory='{tmp_dir}'")
                self._write_conn.execute("SET allow_persistent_secrets=true")
            except Exception:
                pass
        
        self._write_conn.execute("SET preserve_insertion_order=false")
        
        self._create_schema()
        self._store_metadata(metadata)
        self._staging_dir: Optional[Path] = None
        self._staging_states_dir: Optional[Path] = None
        self._staging_shard_index: int = 0

    def _create_schema(self):
        """Create database schema."""
        if not self._write_conn:
            raise RuntimeError("Database not initialized")

        for sql in get_schema_sql():
            self._write_conn.execute(sql)

    def create_indexes(self):
        """Create indexes after bulk load."""
        if not self._write_conn:
            raise RuntimeError("Database not initialized")
        for sql in get_index_sql():
            self._write_conn.execute(sql)

    def _store_metadata(self, metadata: Dict[str, Any]):
        """Store metadata in database."""
        if not self._write_conn:
            raise RuntimeError("Database not initialized")

        for key, value in metadata.items():
            self._write_conn.execute(
                "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
                [key, str(value)],
            )

    def begin_bulk_load(self):
        """Begin bulk load transaction."""
        if not self._write_conn:
            raise RuntimeError("Database not initialized")
        self._write_conn.execute("BEGIN TRANSACTION")
        self._rows_since_commit = 0
        import os as _os
        try:
            self._commit_every_rows = int(_os.getenv("TACVIEW_COMMIT_EVERY", "100000"))
        except Exception:
            self._commit_every_rows = 100000

    def end_bulk_load(self):
        """End bulk load transaction and optimize database."""
        if not self._write_conn:
            raise RuntimeError("Database not initialized")
        self._write_conn.execute("COMMIT")
        
        # Optimize database storage after bulk load
        # CHECKPOINT consolidates the database state
        self._write_conn.execute("CHECKPOINT")
        
        # VACUUM reclaims unused space and optimizes storage
        # This can significantly reduce file size after bulk inserts
        self._write_conn.execute("VACUUM")

    # Parquet staging methods
    def prepare_parquet_staging(self):
        """Prepare directories for staging states and objects as Parquet shards."""
        if not self.db_path:
            raise RuntimeError("Database not initialized")
        base = self.output_dir / ".staging" / self.db_path.stem
        base.mkdir(parents=True, exist_ok=True)
        states_dir = base / "states"
        states_dir.mkdir(parents=True, exist_ok=True)
        objects_dir = base / "objects"
        objects_dir.mkdir(parents=True, exist_ok=True)
        self._staging_dir = base
        self._staging_states_dir = states_dir
        self._staging_objects_dir = objects_dir
        self._staging_shard_index = 0

    def stage_states_batch(self, states_batch: List[tuple]):
        """Write a batch of states to a Parquet shard on disk.
        
        Automatically initializes Parquet staging on first call (lazy initialization).
        """
        if not states_batch:
            return
        
        # Lazy initialization: Auto-prepare Parquet staging on first call
        if not self._staging_states_dir:
            try:
                self.prepare_parquet_staging()
            except Exception as e:
                raise RuntimeError(f"Failed to initialize Parquet staging: {e}") from e

        # Build columnar arrays for Arrow
        object_id_col = []
        ts_col = []
        lon_col = []
        lat_col = []
        alt_col = []
        roll_col = []
        pitch_col = []
        yaw_col = []
        u_col = []
        v_col = []
        heading_col = []
        speed_col = []
        vs_col = []
        turn_rate_col = []
        turn_radius_col = []
        ax_col = []
        ay_col = []
        az_col = []
        g_load_col = []
        pe_col = []
        ke_col = []
        se_col = []

        for object_id, state in states_batch:
            object_id_col.append(object_id)
            ts_col.append(state.timestamp)
            t = state.transform
            lon_col.append(t.longitude)
            lat_col.append(t.latitude)
            alt_col.append(t.altitude)
            roll_col.append(t.roll)
            pitch_col.append(t.pitch)
            yaw_col.append(t.yaw)
            u_col.append(t.u)
            v_col.append(t.v)
            heading_col.append(t.heading)
            speed_col.append(t.speed)
            vs_col.append(t.vertical_speed)
            turn_rate_col.append(t.turn_rate)
            turn_radius_col.append(t.turn_radius)
            ax_col.append(t.ax)
            ay_col.append(t.ay)
            az_col.append(t.az)
            g_load_col.append(t.g_load)
            pe_col.append(t.potential_energy)
            ke_col.append(t.kinetic_energy)
            se_col.append(t.specific_energy)

        # Write Parquet file
        shard_path = self._staging_states_dir / f"states_{self._staging_shard_index:06d}.parquet"
        self._staging_shard_index += 1
        try:
            import pyarrow as pa
            import pyarrow.parquet as pq
        except ImportError as e:
            raise ImportError("pyarrow is required for Parquet staging. Install with: pip install pyarrow") from e
        
        table = pa.table({
            "object_id": pa.array(object_id_col, type=pa.string()),
            "timestamp": pa.array(ts_col, type=pa.float64()),
            "longitude": pa.array(lon_col, type=pa.float64()),
            "latitude": pa.array(lat_col, type=pa.float64()),
            "altitude": pa.array(alt_col, type=pa.float64()),
            "roll": pa.array(roll_col, type=pa.float64()),
            "pitch": pa.array(pitch_col, type=pa.float64()),
            "yaw": pa.array(yaw_col, type=pa.float64()),
            "u": pa.array(u_col, type=pa.float64()),
            "v": pa.array(v_col, type=pa.float64()),
            "heading": pa.array(heading_col, type=pa.float64()),
            "speed": pa.array(speed_col, type=pa.float64()),
            "vertical_speed": pa.array(vs_col, type=pa.float64()),
            "turn_rate": pa.array(turn_rate_col, type=pa.float64()),
            "turn_radius": pa.array(turn_radius_col, type=pa.float64()),
            "ax": pa.array(ax_col, type=pa.float64()),
            "ay": pa.array(ay_col, type=pa.float64()),
            "az": pa.array(az_col, type=pa.float64()),
            "g_load": pa.array(g_load_col, type=pa.float64()),
            "potential_energy": pa.array(pe_col, type=pa.float64()),
            "kinetic_energy": pa.array(ke_col, type=pa.float64()),
            "specific_energy": pa.array(se_col, type=pa.float64()),
        })
        pq.write_table(table, shard_path, compression="zstd", use_dictionary=False)

    def stage_objects_to_parquet(self, objects: List):
        """Write objects metadata to Parquet file for bulk import."""
        if not objects:
            return
        if not self._staging_objects_dir:
            raise RuntimeError("Parquet staging not prepared. Call prepare_parquet_staging() first.")
        
        import pyarrow as pa
        import pyarrow.parquet as pq
        
        # Build columnar arrays
        object_ids = []
        names = []
        type_classes = []
        type_attributes = []
        type_basics = []
        type_specifics = []
        pilots = []
        groups = []
        coalitions = []
        colors = []
        countries = []
        parent_ids = []
        first_seens = []
        last_seens = []
        removed_ats = []
        properties = []
        
        for obj in objects:
            object_ids.append(obj.object_id)
            names.append(obj.name)
            type_classes.append(obj.type_class)
            type_attributes.append(obj.type_attributes)
            type_basics.append(obj.type_basic)
            type_specifics.append(obj.type_specific)
            pilots.append(obj.pilot)
            groups.append(obj.group)
            coalitions.append(obj.coalition)
            colors.append(obj.color)
            countries.append(obj.country)
            parent_ids.append(obj.parent_id)
            first_seens.append(obj.first_seen)
            last_seens.append(obj.last_seen)
            removed_ats.append(obj.removed_at)
            properties.append(json.dumps(obj.properties) if obj.properties else "{}")
        
        table = pa.table({
            "id": pa.array(object_ids, type=pa.string()),
            "name": pa.array(names, type=pa.string()),
            "type_class": pa.array(type_classes, type=pa.string()),
            "type_attributes": pa.array(type_attributes, type=pa.string()),
            "type_basic": pa.array(type_basics, type=pa.string()),
            "type_specific": pa.array(type_specifics, type=pa.string()),
            "pilot": pa.array(pilots, type=pa.string()),
            "group_name": pa.array(groups, type=pa.string()),
            "coalition": pa.array(coalitions, type=pa.string()),
            "color": pa.array(colors, type=pa.string()),
            "country": pa.array(countries, type=pa.string()),
            "parent_id": pa.array(parent_ids, type=pa.string()),
            "first_seen": pa.array(first_seens, type=pa.float64()),
            "last_seen": pa.array(last_seens, type=pa.float64()),
            "removed_at": pa.array(removed_ats, type=pa.float64()),
            "properties": pa.array(properties, type=pa.string()),
        })
        
        parquet_path = self._staging_objects_dir / "objects.parquet"
        pq.write_table(table, parquet_path, compression="zstd", use_dictionary=False)
    
    def import_staged_objects(self):
        """Import staged objects Parquet file into the objects table."""
        if not self._staging_objects_dir:
            return
        
        parquet_path = self._staging_objects_dir / "objects.parquet"
        if not parquet_path.exists():
            return
        
        self._write_conn.execute(
            f"""
            INSERT INTO objects
            SELECT id, name, type_class, type_attributes, type_basic, type_specific,
                   pilot, group_name, coalition, color, country, parent_id,
                   first_seen, last_seen, removed_at, properties::JSON
            FROM read_parquet('{parquet_path}')
            """
        )
    
    def import_staged_states(self):
        """Import all staged Parquet shards into the states table."""
        if not self._staging_states_dir:
            return
        
        try:
            self._write_conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_states_object_ts ON states(object_id, timestamp)"
            )
        except Exception:
            pass
        
        pattern = str(self._staging_states_dir / "states_*.parquet")
        self._write_conn.execute(
            f"""
            INSERT INTO states (object_id, timestamp, longitude, latitude, altitude,
                   roll, pitch, yaw, u, v, heading,
                   speed, vertical_speed, turn_rate, turn_radius,
                   ax, ay, az, g_load,
                   potential_energy, kinetic_energy, specific_energy)
            SELECT object_id, timestamp, longitude, latitude, altitude,
                   roll, pitch, yaw, u, v, heading,
                   speed, vertical_speed, turn_rate, turn_radius,
                   ax, ay, az, g_load,
                   potential_energy, kinetic_energy, specific_energy
            FROM read_parquet('{pattern}')
            ON CONFLICT (object_id, timestamp) DO UPDATE SET
                longitude = EXCLUDED.longitude,
                latitude = EXCLUDED.latitude,
                altitude = EXCLUDED.altitude,
                roll = EXCLUDED.roll,
                pitch = EXCLUDED.pitch,
                yaw = EXCLUDED.yaw,
                u = EXCLUDED.u,
                v = EXCLUDED.v,
                heading = EXCLUDED.heading,
                speed = EXCLUDED.speed,
                vertical_speed = EXCLUDED.vertical_speed,
                turn_rate = EXCLUDED.turn_rate,
                turn_radius = EXCLUDED.turn_radius,
                ax = EXCLUDED.ax,
                ay = EXCLUDED.ay,
                az = EXCLUDED.az,
                g_load = EXCLUDED.g_load,
                potential_energy = EXCLUDED.potential_energy,
                kinetic_energy = EXCLUDED.kinetic_energy,
                specific_energy = EXCLUDED.specific_energy
            """
        )

    def cleanup_parquet_staging(self):
        """Remove staged Parquet files and directories."""
        if self._staging_dir and self._staging_dir.exists():
            import shutil
            shutil.rmtree(self._staging_dir, ignore_errors=True)
        self._staging_dir = None
        self._staging_states_dir = None
        self._staging_shard_index = 0
    
    def add_events(self, events: List[tuple]):
        """
        Add events to database.
        
        Args:
            events: List of (object_id, timestamp, event_name, event_params) tuples
        """
        if not self._write_conn:
            raise RuntimeError("Database not initialized")
        
        if not events:
            return
        
        self._write_conn.executemany(
            """
            INSERT OR REPLACE INTO events (
                object_id, timestamp, event_name, event_params
            ) VALUES (?, ?, ?, ?)
            """,
            events,
        )

    def add_states_batch(self, states_batch: List[tuple], commit_every: int = 10):
        """Add states batch during streaming parse (fallback when Parquet staging not enabled)."""
        if not self._write_conn:
            raise RuntimeError("Database not initialized")
        
        if not states_batch:
            return
        
        # FALLBACK: Direct insert via executemany (DuckDB 1.4+)
        # Note: Parser prefers stage_states_batch() when Parquet staging is enabled
        states_data = []
        for object_id, state in states_batch:
            states_data.append(
                (
                    object_id,
                    state.timestamp,
                    state.transform.longitude,
                    state.transform.latitude,
                    state.transform.altitude,
                    state.transform.roll,
                    state.transform.pitch,
                    state.transform.yaw,
                    state.transform.u,
                    state.transform.v,
                    state.transform.heading,
                    state.transform.speed,
                    state.transform.vertical_speed,
                    state.transform.turn_rate,
                    state.transform.turn_radius,
                    state.transform.ax,
                    state.transform.ay,
                    state.transform.az,
                    state.transform.g_load,
                    state.transform.potential_energy,
                    state.transform.kinetic_energy,
                    state.transform.specific_energy,
                )
            )
        
        self._write_conn.executemany(
            """
            INSERT INTO states (
                object_id, timestamp, longitude, latitude, altitude,
                roll, pitch, yaw, u, v, heading,
                speed, vertical_speed, turn_rate, turn_radius,
                ax, ay, az, g_load,
                potential_energy, kinetic_energy, specific_energy
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (object_id, timestamp) DO UPDATE SET
                longitude = EXCLUDED.longitude,
                latitude = EXCLUDED.latitude,
                altitude = EXCLUDED.altitude,
                roll = EXCLUDED.roll,
                pitch = EXCLUDED.pitch,
                yaw = EXCLUDED.yaw,
                u = EXCLUDED.u,
                v = EXCLUDED.v,
                heading = EXCLUDED.heading,
                speed = EXCLUDED.speed,
                vertical_speed = EXCLUDED.vertical_speed,
                turn_rate = EXCLUDED.turn_rate,
                turn_radius = EXCLUDED.turn_radius,
                ax = EXCLUDED.ax,
                ay = EXCLUDED.ay,
                az = EXCLUDED.az,
                g_load = EXCLUDED.g_load,
                potential_energy = EXCLUDED.potential_energy,
                kinetic_energy = EXCLUDED.kinetic_energy,
                specific_energy = EXCLUDED.specific_energy
            """,
            states_data,
        )
        self._rows_since_commit += len(states_data)

        # Periodic commit to manage memory
        if self._rows_since_commit >= self._commit_every_rows:
            self._write_conn.execute("COMMIT")
            self._write_conn.execute("BEGIN TRANSACTION")
            self._rows_since_commit = 0

    def add_objects_metadata_bulk(self, objects: List[TacviewObject]):
        """Add objects metadata via Parquet staging or direct insert."""
        if not self._write_conn:
            raise RuntimeError("Database not initialized")
        
        if not objects:
            return
        
        # Use Parquet staging if available (faster)
        if hasattr(self, '_staging_objects_dir') and self._staging_objects_dir is not None:
            self.stage_objects_to_parquet(objects)
            self.import_staged_objects()
        else:
            # Fallback to direct insert
            objects_data = []
            for obj in objects:
                objects_data.append(
                    (
                        obj.object_id,
                        obj.name,
                        obj.type_class,
                        obj.type_attributes,
                        obj.type_basic,
                        obj.type_specific,
                        obj.pilot,
                        obj.group,
                        obj.coalition,
                        obj.color,
                        obj.country,
                        obj.parent_id,
                        obj.first_seen,
                        obj.last_seen,
                        obj.removed_at,
                        json.dumps(obj.properties) if obj.properties else "{}",
                    )
                )
            
            if objects_data:
                self._write_conn.executemany(
                    """
                    INSERT INTO objects (
                        id, name, type_class, type_attributes, type_basic, type_specific,
                        pilot, group_name, coalition, color, country, parent_id,
                        first_seen, last_seen, removed_at, properties
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    objects_data,
                )
    
    def get_object(self, object_id: str) -> Optional[TacviewObject]:
        """Get object by ID."""
        with self.get_query_connection() as conn:
            result = conn.execute(
                "SELECT * FROM objects WHERE id = ?", [object_id]
            ).fetchone()

            if not result:
                return None

            obj = TacviewObject(
                object_id=result[0],
                name=result[1],
                type=result[2],
                pilot=result[3],
                group=result[4],
                coalition=result[5],
                color=result[6],
                country=result[7],
                properties=json.loads(result[8]) if result[8] else {},
                first_seen=result[9],
                last_seen=result[10],
            )

            return obj

    def query_time_range(self, start: float, end: float) -> List[Dict[str, Any]]:
        """Query states in time range."""
        with self.get_query_connection() as conn:
            result = conn.execute(
                """
                SELECT * FROM states
                WHERE timestamp >= ? AND timestamp <= ?
                ORDER BY timestamp
                """,
                [start, end],
            ).fetchall()

            return [self._state_row_to_dict(row) for row in result]

    def query_sql(self, sql: str) -> List[Dict[str, Any]]:
        """Execute raw SQL query with temporary connection."""
        with self.get_query_connection() as conn:
            result = conn.execute(sql).fetchall()
            if not result:
                return []

            columns = [desc[0] for desc in conn.description]

            return [dict(zip(columns, row)) for row in result]

    def get_summary(self) -> Dict[str, Any]:
        """Get database summary statistics."""
        with self.get_query_connection() as conn:
            summary = {}

            result = conn.execute("SELECT COUNT(*) FROM objects").fetchone()
            summary["object_count"] = result[0] if result else 0

            result = conn.execute("SELECT COUNT(*) FROM states").fetchone()
            summary["state_count"] = result[0] if result else 0

            result = conn.execute("SELECT MIN(timestamp), MAX(timestamp) FROM states").fetchone()
            if result and result[0] is not None:
                summary["start_time"] = result[0]
                summary["end_time"] = result[1]
                summary["duration"] = result[1] - result[0]

            metadata_result = conn.execute("SELECT key, value FROM metadata").fetchall()
            summary["metadata"] = {row[0]: row[1] for row in metadata_result}

            return summary

    @property
    def database_path(self) -> Optional[str]:
        """Full path to the database file."""
        return str(self.db_path) if self.db_path else None
    
    def register_udf(self, name: str, func, param_types, return_type):
        """
        Register a user-defined function for use in SQL queries.
        
        The UDF will be registered on the internal write connection and automatically
        registered on all future query connections created via get_query_connection().
        
        Args:
            name: Name of the function as it will be called in SQL
            func: Python function to execute
            param_types: List of parameter types (use None for auto-inference, requires numpy)
            return_type: Return type of the function (use None for auto-inference, requires numpy)
        
        Note:
            Type inference (param_types=None, return_type=None) requires numpy to be installed.
        
        Example:
            def my_distance(x1: float, x2: float) -> float:
                return abs(x2 - x1)
            
            # Let DuckDB infer types (requires numpy)
            store.register_udf("my_distance", my_distance, None, None)
            
            # Now available in all queries:
            result = conn.execute("SELECT my_distance(lat1, lat2) FROM objects").fetchall()
        """
        # Store the registration for future connections
        self._registered_udfs.append((name, func, param_types, return_type))
        
        # Register on existing write connection if available
        if self._write_conn:
            try:
                self._write_conn.create_function(name, func, param_types, return_type)
            except Exception as e:
                # Ignore if function already exists (DuckDB catalog may persist across connections)
                if "already exists" not in str(e).lower():
                    raise
    
    def get_query_connection(self, read_only: bool = False, skip_udfs: bool = False) -> duckdb.DuckDBPyConnection:
        """
        Get a new connection for querying.
        
        Returns a fresh connection that the consumer should close when done.
        Can be used as a context manager.
        
        DuckDB Concurrency Model:
        - All connections to the same database must have the same configuration
        - Cannot mix read-only and read-write connections to the same file
        - Within a single process, DuckDB uses MVCC for concurrent access
        - Multiple readers + one writer work automatically within same process
        
        MVCC Visibility (Important for Web APIs):
        - Committed changes are visible to ALL connections immediately
        - Existing connections see new commits (no need to reconnect)
        - Uncommitted changes are isolated (not visible to other connections)
        - Consumer connections DO NOT need to be released/refreshed to see enrichment results
        
        See: https://duckdb.org/docs/stable/connect/concurrency
        
        Args:
            read_only: Deprecated (kept for API compatibility). All connections
                      are read-write to avoid configuration conflicts.
        
        Returns:
            New DuckDB connection to the database
        
        Example:
            # Long-lived connection sees background enrichment results automatically
            conn = store.get_query_connection()
            
            # Query before enrichment
            result1 = conn.execute("SELECT COUNT(*) FROM objects WHERE parent_id IS NOT NULL").fetchone()
            # Returns: (0,)
            
            # [Background enrichment runs: store.apply_enrichments(['weapons'])]
            
            # Query after enrichment (SAME connection)
            result2 = conn.execute("SELECT COUNT(*) FROM objects WHERE parent_id IS NOT NULL").fetchone()
            # Returns: (150,)  <- Automatically sees enrichment results!
            
            conn.close()
        """
        if not self.db_path:
            raise RuntimeError("Database not initialized")
        
        # All connections must have same configuration - DuckDB limitation
        if skip_udfs:
            return duckdb.connect(str(self.db_path))

        conn = duckdb.connect(str(self.db_path))
        
        # Register any user-defined functions on this new connection
        for name, func, param_types, return_type in self._registered_udfs:
            try:
                conn.create_function(name, func, param_types, return_type)
            except Exception as e:
                # Ignore if function already exists (DuckDB catalog may persist across connections)
                if "already exists" not in str(e).lower():
                    raise
        
        return conn

    def apply_enrichments(
        self, 
        enrichments: List[str],
        async_enrichments: bool = True,
        progress: bool = False,
        airbase_database: Optional[Dict[str, Dict]] = None,
        use_airport_database: bool = False,
        airport_max_distance_km: float = 5.0
    ) -> Dict[str, int]:
        """
        Apply enrichments to an already-parsed database.
        
        This allows running enrichments on-demand without re-parsing the entire file.
        Enrichments run in background by default (async_enrichments=True).
        
        Args:
            enrichments: List of enrichment names to apply
            async_enrichments: Run enrichments in background thread (default: True)
            progress: Show progress messages
            airbase_database: Optional airbase locations (legacy)
            use_airport_database: Use OurAirports database (default: False)
            airport_max_distance_km: Maximum distance to search for airports (default: 5 km)
            
        Returns:
            Dictionary mapping enrichment names to counts (empty if async_enrichments=True)
        """
        if not self._write_conn:
            raise RuntimeError("Database not initialized")
        
        # Wait for any existing enrichments to complete first
        if self._async_mode and not self._enrichments_complete:
            if progress:
                print("Waiting for existing enrichments to complete...")
            self.wait_for_enrichments()
        
        # Define the actual enrichment work
        def _run_enrichments_work():
            """Run enrichments with own connection (thread-safe for async mode)."""
            # Use get_query_connection for proper connection management
            enrichment_conn = self.get_query_connection()
            
            try:
                results = {}
                
                # Initialize progress tracking
                self._total_enrichments = len(enrichments)
                self._completed_enrichments = 0
                self._enrichment_progress = 0.0
                self._current_enrichment = ""
                
                for idx, enrichment in enumerate(enrichments):
                    # Update progress
                    self._current_enrichment = enrichment
                    self._enrichment_progress = idx / self._total_enrichments
                    
                    try:
                        # Import enricher classes
                        from ..enrichment import (
                            WeaponEnricher,
                            CoalitionEnricher,
                            ContainerEnricher,
                            EjectedPilotEnricher,
                            FixedWingEnricher,
                            RotorcraftEnricher,
                            GroundSeaEnricher,
                            MissedWeaponAnalyzer,
                            EventGeodataEnricher,
                            SpatialClusterEnricher
                        )
                        
                        # Use enrichment_conn (separate from parser's _write_conn)
                        if enrichment == 'weapons':
                            # Weapon enrichment uses 3 passes for comprehensive detection:
                            # Pass 1: Launcher detection (weapons need owners first)
                            # Pass 2: Spatial clustering (detect multi-target impacts, intercepts, collisions)
                            # Pass 3: Target detection (catch non-lethal hits not detected by clustering)
                            
                            # Pass 1: Launcher detection
                            launcher_enricher = WeaponEnricher(
                                time_window=1.0,
                                proximity_radius=100.0,
                                find_launchers=True,
                                find_targets=False
                            )
                            launcher_count = launcher_enricher.enrich([], enrichment_conn)
                            if progress:
                                print(f"  Found launchers for {launcher_count} weapons")
                            
                            # Pass 2: Spatial clustering (detect impacts, intercepts, collisions)
                            cluster_enricher = SpatialClusterEnricher(
                                proximity_radius=50.0,
                                collision_speed_threshold=50.0,
                                time_window=1.0  # Allow ±1.0s timing differences (increased from 0.5s for AGM-88 pattern)
                            )
                            cluster_count = cluster_enricher.enrich([], enrichment_conn)
                            if progress:
                                print(f"  Detected {cluster_count} spatial cluster events")
                            
                            # Pass 3: Target detection (for non-lethal hits)
                            target_enricher = WeaponEnricher(
                                time_window=1.0,
                                proximity_radius=100.0,
                                find_launchers=False,
                                find_targets=True
                            )
                            target_count = target_enricher.enrich([], enrichment_conn)
                            if progress:
                                print(f"  Found targets for {target_count} weapons")
                            
                            results['weapons'] = launcher_count + target_count
                        
                        elif enrichment == 'coalitions':
                            enricher = CoalitionEnricher()
                            count = enricher.enrich([], enrichment_conn)
                            results['coalitions'] = count
                            if progress:
                                print(f"  Enriched {count} objects with coalition data")
                        
                        elif enrichment == 'containers':
                            enricher = ContainerEnricher()
                            count = enricher.enrich([], enrichment_conn)
                            results['containers'] = count
                            if progress:
                                print(f"  Enriched {count} containers with parent data")
                        
                        elif enrichment == 'ejections':
                            enricher = EjectedPilotEnricher()
                            count = enricher.enrich([], enrichment_conn)
                            results['ejections'] = count
                            if progress:
                                print(f"  Enriched {count} ejected pilots")
                        
                        elif enrichment == 'lifecycle':
                            if progress:
                                print("  Detecting lifecycle events (takeoff/landing/destruction)...")
                            
                            # Fixed-wing aircraft
                            fw_enricher = FixedWingEnricher(
                                airbase_database=airbase_database,
                                use_airport_database=use_airport_database,
                                airport_max_distance_km=airport_max_distance_km
                            )
                            fw_count = fw_enricher.enrich([], enrichment_conn)
                            
                            # Rotorcraft
                            rc_enricher = RotorcraftEnricher(
                                airbase_database=airbase_database,
                                use_airport_database=use_airport_database,
                                airport_max_distance_km=airport_max_distance_km
                            )
                            rc_count = rc_enricher.enrich([], enrichment_conn)
                            
                            # Ground/Sea destruction (links weapon hits to removal)
                            gs_enricher = GroundSeaEnricher(time_window=120.0)
                            gs_result = gs_enricher.enrich([], enrichment_conn)
                            gs_count = gs_result.get('ground_sea_destroyed_created', 0)
                            
                            # Show comprehensive summary
                            if progress:
                                print(f"    Fixed-wing: {fw_count} aircraft")
                                print(f"    Rotorcraft: {rc_count} aircraft")
                                print(f"    Ground/Sea: {gs_count} destruction events linked to weapon hits")
                            
                            results['lifecycle'] = fw_count + rc_count + gs_count
                        
                        elif enrichment == 'missed_weapons':
                            enricher = MissedWeaponAnalyzer(
                                detect_proximity_kills=True,
                                proximity_kill_threshold=25.0,
                                proximity_kill_time_window=1.0
                            )
                            count = enricher.enrich([], enrichment_conn)
                            results['missed_weapons'] = count
                            if progress:
                                print(f"  Enriched {count} missed weapons with proximity data")
                                # Note: Kinematic defeat detection and proximity kill detection run automatically within analyzer
                        
                        elif enrichment == 'decoys':
                            from ..enrichment import DecoyEnricher
                            enricher = DecoyEnricher(
                                time_window=1.0,
                                proximity_radius=50.0  # Flares/chaff deploy very close
                            )
                            count = enricher.enrich([], enrichment_conn)
                            results['decoys'] = count
                            if progress:
                                print(f"  Found parent platforms for {count} decoys")
                        
                        elif enrichment == 'projectiles':
                            from ..enrichment import ProjectileEnricher
                            if progress:
                                print("  Enriching projectiles (launchers, hits, bursts)...")
                            
                            # Query projectile counts before enrichment
                            pre_stats = enrichment_conn.execute("""
                                SELECT
                                    COUNT(*) as total,
                                    SUM(CASE WHEN parent_id IS NOT NULL THEN 1 ELSE 0 END) as with_launcher,
                                    SUM(CASE WHEN json_extract_string(properties, '$.Fate') = 'HIT' THEN 1 ELSE 0 END) as hits,
                                    SUM(CASE WHEN json_extract_string(properties, '$.Fate') = 'MISS' THEN 1 ELSE 0 END) as misses
                                FROM objects
                                WHERE type_basic = 'Projectile'
                            """).fetchone()
                            
                            enricher = ProjectileEnricher(
                                launcher_radius=150.0,  # Increased for better cannon round matching
                                hit_radius=10.0,
                                hit_altitude_tolerance=25.0,
                                burst_time_gap=1.0,
                                detect_launchers=True,
                                detect_hits=True,
                                create_bursts=True,
                                analyze_misses=False
                            )
                            enricher.enrich([], enrichment_conn)
                            
                            # Query results after enrichment
                            post_stats = enrichment_conn.execute("""
                                SELECT
                                    COUNT(*) as total,
                                    SUM(CASE WHEN parent_id IS NOT NULL THEN 1 ELSE 0 END) as with_launcher,
                                    SUM(CASE WHEN json_extract_string(properties, '$.Fate') = 'HIT' THEN 1 ELSE 0 END) as hits,
                                    SUM(CASE WHEN json_extract_string(properties, '$.Fate') = 'MISS' THEN 1 ELSE 0 END) as misses,
                                    (SELECT COUNT(*) FROM objects WHERE type_specific = 'Burst') as burst_count
                                FROM objects
                                WHERE type_basic = 'Projectile'
                            """).fetchone()
                            
                            total = post_stats[0]
                            with_launcher = post_stats[1]
                            hits = post_stats[2]
                            misses = post_stats[3]
                            bursts = post_stats[4] or 0
                            
                            launcher_pct = (with_launcher / total * 100) if total > 0 else 0
                            with_fate = hits + misses
                            fate_pct = (with_fate / total * 100) if total > 0 else 0
                            
                            results['projectiles'] = with_fate
                            
                            if progress:
                                print(f"    {total} projectiles: {with_launcher} linked to launchers ({launcher_pct:.0f}%), {hits} hits + {misses} misses ({fate_pct:.0f}%), {bursts} bursts")
                        
                        elif enrichment in ('geodata', 'event_geodata', 'airports'):
                            if progress:
                                print("  Enriching event locations with airport data...")
                            enricher = EventGeodataEnricher(
                                max_distance_km=airport_max_distance_km
                            )
                            count = enricher.enrich([], enrichment_conn)
                            results['geodata'] = count
                            if progress:
                                print(f"  Enriched {count} events with airport names")
                        
                        else:
                            if progress:
                                print(f"  Warning: Unknown enrichment '{enrichment}'")
                    
                    except Exception as e:
                        if progress:
                            print(f"  Error in {enrichment} enrichment: {e}")
                        import traceback
                        traceback.print_exc()
                    
                    # Update progress after each enrichment
                    self._completed_enrichments = idx + 1
                    self._enrichment_progress = self._completed_enrichments / self._total_enrichments
                
                # Mark as complete
                self._current_enrichment = ""
                self._enrichment_progress = 1.0
                self._enrichments_complete = True
                self._self_reference = None
                
                return results
            
            finally:
                # Always close enrichment connection
                enrichment_conn.close()
        
        # Run enrichments async or sync
        if async_enrichments:
            import threading
            
            if progress:
                print(f"Starting enrichments in background...")
            
            self._async_mode = True
            self._enrichments_complete = False
            self._self_reference = self
            
            thread = threading.Thread(
                target=_run_enrichments_work,
                name="EnrichmentThread",
                daemon=True
            )
            thread.start()
            self._enrichment_thread = thread
            
            return {}
        else:
            self._async_mode = False
            return _run_enrichments_work()

    def _state_row_to_dict(self, row) -> Dict[str, Any]:
        """Convert state row to dictionary."""
        return {
            "state_id": row[0],
            "object_id": row[1],
            "timestamp": row[2],
            "longitude": row[3],
            "latitude": row[4],
            "altitude": row[5],
            "roll": row[6],
            "pitch": row[7],
            "yaw": row[8],
            "heading": row[9],
            "u": row[10],
            "v": row[11],
            "speed": row[12],
            "vertical_speed": row[13],
            "turn_rate": row[14],
            "turn_radius": row[15],
        }

    # Geopy convenience methods
    def reverse_geocode(
        self,
        latitude: float,
        longitude: float,
        language: str = "en",
        timeout: int = 2
    ) -> Optional[str]:
        """Get human-readable location name from coordinates (reverse geocoding)."""
        try:
            from ..enrichment import geocoding
            return geocoding.reverse_geocode(latitude, longitude, language, timeout)
        except ImportError:
            print("Warning: geopy not installed. Install with: pip install geopy")
            return None
    
    def geocode(
        self,
        location_name: str,
        timeout: int = 2
    ) -> Optional[tuple]:
        """Get coordinates from a location name (forward geocoding)."""
        try:
            from ..enrichment import geocoding
            return geocoding.forward_geocode(location_name, timeout=timeout)
        except ImportError:
            print("Warning: geopy not installed. Install with: pip install geopy")
            return None
    
    def clear_geocoding_cache(self):
        """Clear the geocoding cache."""
        try:
            from ..enrichment import geocoding
            geocoding.clear_geocoding_cache()
        except ImportError:
            pass

    def close(self):
        """Close database connection."""
        if self._write_conn:
            try:
                self._write_conn.close()
            except Exception:
                pass
            finally:
                self._write_conn = None
    
    def wait_for_enrichments(self, timeout: Optional[float] = None) -> bool:
        """Wait for background enrichments to complete."""
        if not self._async_mode:
            return True
        
        if self._enrichments_complete:
            return True
        
        if self._enrichment_thread and self._enrichment_thread.is_alive():
            # Don't try to join if we're already in the enrichment thread
            import threading
            if threading.current_thread() == self._enrichment_thread:
                return False  # Still running, but can't wait for ourselves
            
            self._enrichment_thread.join(timeout=timeout)
            return not self._enrichment_thread.is_alive()
        
        return True
    
    def enrichments_complete(self) -> bool:
        """Check if background enrichments have completed."""
        if not self._async_mode:
            return True
        return self._enrichments_complete
    
    def enrichment_status(self) -> dict:
        """Get status of enrichments."""
        status = {
            'async_mode': self._async_mode,
            'complete': self._enrichments_complete,
        }
        
        if self._async_mode:
            if self._enrichment_thread:
                status['thread_alive'] = self._enrichment_thread.is_alive()
                status['thread_name'] = self._enrichment_thread.name
            else:
                status['thread_alive'] = False
                status['thread_name'] = None
        
        return status
    
    def get_enrichment_progress(self) -> dict:
        """Get enrichment progress information."""
        return {
            'progress': self._enrichment_progress,
            'percent': int(self._enrichment_progress * 100),
            'current': self._current_enrichment,
            'completed': self._completed_enrichments,
            'total': self._total_enrichments,
            'complete': self._enrichments_complete
        }

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

