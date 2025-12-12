"""DuckDB schema definitions."""

# SQL for creating objects table
CREATE_OBJECTS_TABLE = """
CREATE TABLE IF NOT EXISTS objects (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    type_class VARCHAR,
    type_attributes VARCHAR,
    type_basic VARCHAR,
    type_specific VARCHAR,
    pilot VARCHAR,
    group_name VARCHAR,
    coalition VARCHAR,
    color VARCHAR,
    country VARCHAR,
    parent_id VARCHAR,
    first_seen DOUBLE,
    last_seen DOUBLE,
    removed_at DOUBLE,
    properties JSON
)
"""

# SQL for creating states table with spatial support
CREATE_STATES_TABLE = """
CREATE SEQUENCE IF NOT EXISTS states_id_seq START 1;
CREATE TABLE IF NOT EXISTS states (
    id BIGINT PRIMARY KEY DEFAULT nextval('states_id_seq'),
    object_id VARCHAR,
    timestamp DOUBLE,
    longitude DOUBLE,
    latitude DOUBLE,
    altitude DOUBLE,
    roll DOUBLE,
    pitch DOUBLE,
    yaw DOUBLE,
    u DOUBLE,
    v DOUBLE,
    heading DOUBLE,
    speed DOUBLE,
    vertical_speed DOUBLE,
    turn_rate DOUBLE,
    turn_radius DOUBLE,
    ax DOUBLE,
    ay DOUBLE,
    az DOUBLE,
    g_load DOUBLE,
    potential_energy DOUBLE,
    kinetic_energy DOUBLE,
    specific_energy DOUBLE,
    UNIQUE (object_id, timestamp)
)
"""

# SQL for creating metadata table
CREATE_METADATA_TABLE = """
CREATE TABLE IF NOT EXISTS metadata (
    key VARCHAR PRIMARY KEY,
    value VARCHAR
)
"""

# SQL for creating events table
CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS events (
    object_id VARCHAR,
    timestamp DOUBLE,
    event_name VARCHAR,
    event_params VARCHAR,
    PRIMARY KEY (object_id, timestamp, event_name)
)
"""

# SQL for creating tactical_events table
CREATE_TACTICAL_EVENTS_TABLE = """
CREATE SEQUENCE IF NOT EXISTS tactical_events_id_seq START 1;
CREATE TABLE IF NOT EXISTS tactical_events (
    id BIGINT PRIMARY KEY DEFAULT nextval('tactical_events_id_seq'),
    event_type VARCHAR NOT NULL,
    timestamp DOUBLE NOT NULL,
    initiator_id VARCHAR NOT NULL,
    target_id VARCHAR,
    initiator_type VARCHAR,
    target_type VARCHAR,
    initiator_coalition VARCHAR,
    target_coalition VARCHAR,
    longitude DOUBLE,
    latitude DOUBLE,
    altitude DOUBLE,
    initiator_state_id BIGINT,
    target_state_id BIGINT,
    initiator_parent_state_id BIGINT,
    metadata JSON
)
"""

# SQL for creating indexes (now created as part of table definitions for optimal bulk load)
# Additional secondary indexes for query performance
CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_states_object_id ON states(object_id)",
    "CREATE INDEX IF NOT EXISTS idx_states_timestamp ON states(timestamp)",
    "CREATE INDEX IF NOT EXISTS idx_objects_type_class ON objects(type_class)",
    "CREATE INDEX IF NOT EXISTS idx_objects_type_basic ON objects(type_basic)",
    "CREATE INDEX IF NOT EXISTS idx_objects_type_specific ON objects(type_specific)",
    "CREATE INDEX IF NOT EXISTS idx_objects_coalition ON objects(coalition)",
    "CREATE INDEX IF NOT EXISTS idx_objects_parent_id ON objects(parent_id)",
    "CREATE INDEX IF NOT EXISTS idx_objects_first_seen ON objects(first_seen)",
    "CREATE INDEX IF NOT EXISTS idx_objects_last_seen ON objects(last_seen)",
    "CREATE INDEX IF NOT EXISTS idx_objects_removed_at ON objects(removed_at)",
    "CREATE INDEX IF NOT EXISTS idx_events_object_id ON events(object_id)",
    "CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)",
    "CREATE INDEX IF NOT EXISTS idx_events_event_name ON events(event_name)",
    # Projectile burst enrichment indexes
    "CREATE INDEX IF NOT EXISTS idx_objects_type_basic_parent ON objects(type_basic, parent_id)",
    "CREATE INDEX IF NOT EXISTS idx_states_object_timestamp ON states(object_id, timestamp)",
    # Tactical events indexes
    "CREATE INDEX IF NOT EXISTS idx_tactical_events_type ON tactical_events(event_type)",
    "CREATE INDEX IF NOT EXISTS idx_tactical_events_timestamp ON tactical_events(timestamp)",
    "CREATE INDEX IF NOT EXISTS idx_tactical_events_initiator ON tactical_events(initiator_id)",
    "CREATE INDEX IF NOT EXISTS idx_tactical_events_target ON tactical_events(target_id)",
    "CREATE INDEX IF NOT EXISTS idx_tactical_events_coalition_pair ON tactical_events(initiator_coalition, target_coalition)",
    "CREATE INDEX IF NOT EXISTS idx_tactical_events_type_time ON tactical_events(event_type, timestamp)",
    "CREATE INDEX IF NOT EXISTS idx_tactical_events_initiator_state ON tactical_events(initiator_state_id)",
    "CREATE INDEX IF NOT EXISTS idx_tactical_events_target_state ON tactical_events(target_state_id)",
]


def get_schema_sql() -> list:
    """Get list of SQL statements to create tables with primary keys."""
    return [
        CREATE_OBJECTS_TABLE,
        CREATE_STATES_TABLE,
        CREATE_EVENTS_TABLE,
        CREATE_TACTICAL_EVENTS_TABLE,
        CREATE_METADATA_TABLE,
    ]


def get_index_sql() -> list:
    """Get list of SQL statements to create secondary indexes (to be run post-load)."""
    return CREATE_INDEXES

