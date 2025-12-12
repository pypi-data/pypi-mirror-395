"""Container enrichment logic."""

import json
from typing import Optional
import duckdb

from .pipeline import Enricher


class ContainerEnricher(Enricher):
    """
    Enriches Misc+Container objects (drop tanks, etc.) with parent information.
    
    Uses spatial proximity at spawn time to identify the parent platform.
    Containers are typically neutral coalition but dropped by aircraft.
    """
    
    def __init__(
        self,
        time_window: float = 1.0,
        proximity_radius: float = 100.0
    ):
        """
        Initialize container enricher.
        
        Args:
            time_window: Time window to search for parent (default: 1.0s)
            proximity_radius: Maximum distance to search (default: 100m)
        """
        self.time_window = time_window
        self.proximity_radius = proximity_radius
    
    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run container enrichment.
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of containers enriched
        """
        # Find all container objects
        containers = conn.execute("""
            SELECT id, first_seen
            FROM objects 
            WHERE type_specific = 'Container'
              AND first_seen IS NOT NULL
        """).fetchall()
        
        if not containers:
            return 0
        
        enriched_count = 0
        
        for container_id, first_seen in containers:
            # Find platforms spatially close to container at spawn time
            proximity_query = """
            WITH container_pos AS (
                SELECT 
                    timestamp,
                    u as u_coord,
                    v as v_coord,
                    altitude
                FROM states
                WHERE object_id = ?
                  AND timestamp >= ?
                  AND u IS NOT NULL
                  AND v IS NOT NULL
                ORDER BY timestamp
                LIMIT 1
            )
            SELECT 
                s.object_id,
                o.name,
                o.type_class || '+' || COALESCE(o.type_basic, '') as type,
                o.pilot,
                o.coalition,
                SQRT(
                    POWER(s.u - cp.u_coord, 2) + 
                    POWER(s.v - cp.v_coord, 2) + 
                    POWER(s.altitude - cp.altitude, 2)
                ) AS distance_meters
            FROM states s
            CROSS JOIN container_pos cp
            JOIN objects o ON s.object_id = o.id
            WHERE s.timestamp BETWEEN cp.timestamp - ? AND cp.timestamp + ?
              AND o.type_class IN ('Air', 'Ground', 'Sea')
              AND s.u IS NOT NULL
              AND s.v IS NOT NULL
              AND s.object_id != ?
            ORDER BY distance_meters, ABS(s.timestamp - cp.timestamp)
            LIMIT 1
            """
            
            result = conn.execute(
                proximity_query, 
                [container_id, first_seen, self.time_window, self.time_window, container_id]
            ).fetchone()
            
            if result:
                parent_id, parent_name, parent_type, parent_pilot, parent_coalition, distance = result
                
                properties = {
                    "DropRange": distance
                }
                
                update_query = """
                UPDATE objects
                SET 
                    parent_id = ?,
                    properties = json_merge_patch(
                        COALESCE(properties, '{}'),
                        ?
                    )
                WHERE id = ?
                """
                
                conn.execute(update_query, [parent_id, json.dumps(properties), container_id])
                enriched_count += 1
        
        # Insert JETTISON tactical events after all enrichments
        if enriched_count > 0:
            self._insert_jettison_events(conn)
        
        return enriched_count
    
    def _insert_jettison_events(self, conn: duckdb.DuckDBPyConnection):
        """Insert JETTISON tactical events for all enriched containers."""
        insert_query = """
        INSERT INTO tactical_events 
        (event_type, timestamp, initiator_id, target_id,
         initiator_type, target_type, initiator_coalition, target_coalition,
         longitude, latitude, altitude,
         initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
        SELECT 
            'JETTISON',
            c.first_seen,
            p.id,                    -- initiator = parent aircraft
            c.id,                    -- target = container
            p.type_class,
            c.type_specific,
            p.coalition,
            c.coalition,
            cs.longitude, cs.latitude, cs.altitude,
            pstate.id,               -- parent aircraft state at jettison
            NULL,                    -- container state not needed
            NULL,                    -- no parent of parent
            '{}'::JSON
        FROM objects c
        JOIN objects p ON c.parent_id = p.id
        JOIN states cs ON cs.object_id = c.id AND cs.timestamp = c.first_seen
        JOIN LATERAL (
            SELECT id
            FROM states
            WHERE object_id = p.id AND timestamp <= c.first_seen
            ORDER BY timestamp DESC LIMIT 1
        ) pstate ON true
        WHERE c.type_specific = 'Container'
          AND c.parent_id IS NOT NULL
          AND c.first_seen IS NOT NULL
        """
        
        conn.execute(insert_query)

