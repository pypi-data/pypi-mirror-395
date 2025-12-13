"""Ejection event enrichment."""

import json
import duckdb

from .pipeline import Enricher


class EjectedPilotEnricher(Enricher):
    """
    Enriches ejected pilot objects (parachutists) with parent aircraft information.
    
    Finds objects with Type=Ground+Light+Human+Air+Parachutist and Name=Pilot,
    identifies their parent aircraft using spatial proximity at spawn time,
    and creates EJECTION tactical events.
    """
    
    def __init__(
        self,
        time_window: float = 0.5,
        proximity_radius: float = 500.0
    ):
        """
        Initialize ejected pilot enricher.
        
        Args:
            time_window: Time window to search for parent (default: 0.5s)
            proximity_radius: Maximum distance to search (default: 500m)
        """
        self.time_window = time_window
        self.proximity_radius = proximity_radius
    
    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run ejected pilot enrichment.
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of ejected pilots enriched
        """
        # Install and load spatial extension
        conn.execute("INSTALL spatial")
        conn.execute("LOAD spatial")
        
        # Find all ejected pilot objects
        ejected_pilots = conn.execute("""
            SELECT id, first_seen, name, coalition
            FROM objects 
            WHERE type_specific = 'Parachutist'
              AND name = 'Pilot'
              AND first_seen IS NOT NULL
        """).fetchall()
        
        if not ejected_pilots:
            return 0
        
        enriched_count = 0
        
        for pilot_id, first_seen, pilot_name, pilot_coalition in ejected_pilots:
            # Find the closest aircraft at spawn time
            proximity_query = """
            WITH pilot_pos AS (
                SELECT 
                    timestamp,
                    u as u_coord,
                    v as v_coord,
                    altitude,
                    ST_Point3D(u, v, altitude) AS point_3d
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
                o.last_seen,
                SQRT(
                    POWER(s.u - pp.u_coord, 2) + 
                    POWER(s.v - pp.v_coord, 2) + 
                    POWER(s.altitude - pp.altitude, 2)
                ) AS distance_meters
            FROM states s
            CROSS JOIN pilot_pos pp
            JOIN objects o ON s.object_id = o.id
            WHERE s.timestamp BETWEEN pp.timestamp - ? AND pp.timestamp + ?
              AND ST_DWithin(
                    ST_Point3D(s.u, s.v, s.altitude), 
                    pp.point_3d, 
                    ?
                  )
              AND o.type_class = 'Air'
              AND s.u IS NOT NULL
              AND s.v IS NOT NULL
              AND s.object_id != ?
              AND o.first_seen <= pp.timestamp
              AND (o.last_seen >= pp.timestamp AND o.last_seen <= pp.timestamp + 120.0)
              AND SQRT(
                    POWER(s.u - pp.u_coord, 2) + 
                    POWER(s.v - pp.v_coord, 2) + 
                    POWER(s.altitude - pp.altitude, 2)
                  ) <= ?
            ORDER BY distance_meters, ABS(s.timestamp - pp.timestamp)
            LIMIT 1
            """
            
            result = conn.execute(
                proximity_query, 
                [pilot_id, first_seen, self.time_window, self.time_window, self.proximity_radius, pilot_id, self.proximity_radius]
            ).fetchone()
            
            if result:
                aircraft_id, aircraft_name, aircraft_type, aircraft_pilot, aircraft_coalition, aircraft_last_seen, distance = result
                
                # Build properties JSON for the parachutist
                pilot_properties = {
                    "ParentAircraftName": aircraft_name,
                    "ParentAircraftType": aircraft_type,
                    "ParentAircraftPilot": aircraft_pilot,
                    "ParentAircraftCoalition": aircraft_coalition,
                    "EjectionDistance": distance
                }
                
                # Update parachutist with parent information
                update_pilot_query = """
                UPDATE objects
                SET 
                    parent_id = ?,
                    properties = json_merge_patch(
                        COALESCE(properties, '{}'),
                        ?
                    )
                WHERE id = ?
                """
                
                conn.execute(update_pilot_query, [aircraft_id, json.dumps(pilot_properties), pilot_id])
                enriched_count += 1
        
        # Insert EJECTION tactical events after all enrichments
        if enriched_count > 0:
            self._insert_ejection_events(conn)
        
        return enriched_count
    
    def _insert_ejection_events(self, conn: duckdb.DuckDBPyConnection):
        """Insert EJECTION tactical events for all enriched parachutists."""
        insert_query = """
        INSERT INTO tactical_events 
        (event_type, timestamp, initiator_id, target_id,
         initiator_type, target_type, initiator_coalition, target_coalition,
         longitude, latitude, altitude,
         initiator_state_id, target_state_id, initiator_parent_state_id, metadata)
        SELECT 
            'EJECTION',
            p.first_seen,
            a.id,                    -- initiator = aircraft
            p.id,                    -- target = pilot/parachutist
            a.type_class,
            p.type_specific,
            a.coalition,
            p.coalition,
            ps.longitude, ps.latitude, ps.altitude,
            astate.id,               -- aircraft state at ejection
            NULL,                    -- pilot state not needed
            NULL,                    -- no parent
            '{}'::JSON
        FROM objects p
        JOIN objects a ON p.parent_id = a.id
        JOIN states ps ON ps.object_id = p.id AND ps.timestamp = p.first_seen
        JOIN LATERAL (
            SELECT id
            FROM states
            WHERE object_id = a.id AND timestamp <= p.first_seen
            ORDER BY timestamp DESC LIMIT 1
        ) astate ON true
        WHERE p.type_specific = 'Parachutist'
          AND p.name = 'Pilot'
          AND p.parent_id IS NOT NULL
          AND p.first_seen IS NOT NULL
        """
        
        conn.execute(insert_query)

