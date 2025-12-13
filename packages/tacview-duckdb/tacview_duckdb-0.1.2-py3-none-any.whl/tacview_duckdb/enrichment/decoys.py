"""Decoy enrichment logic."""

import json
from typing import Optional
import duckdb

from .pipeline import Enricher


class DecoyEnricher(Enricher):
    """
    Enriches Decoy objects with parent platform information.
    
    Uses spatial proximity at spawn time. Decoys don't have U/V coordinates,
    so we use haversine distance (lat/lon) instead.
    """
    
    def __init__(
        self,
        time_window: float = 1.0,
        proximity_radius: float = 50.0,
        batch_size: int = 500
    ):
        """
        Initialize decoy enricher.
        
        Args:
            time_window: Time window to search for parent (default: 1.0s)
            proximity_radius: Maximum distance to search (default: 50m)
            batch_size: Objects per batch for chunked processing (default: 500). Fixed count ensures consistent performance regardless of mission action density.
        """
        self.time_window = time_window
        self.proximity_radius = proximity_radius
        self.batch_size = batch_size
    
    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run decoy enrichment with object count-based batching for memory efficiency.
        
        Two-stage matching:
        1. Stage 1 (Dynamic): Process ALL unmatched with ±0.2s window (fast, catches most aircraft)
        2. Stage 2 (Static): Process remaining unmatched with last-state matching (slower, edge cases)
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of decoys enriched
        """
        # Install and load spatial extension
        try:
            conn.execute("INSTALL spatial")
        except Exception:
            pass  # Already installed
        try:
            conn.execute("LOAD spatial")
        except Exception:
            pass  # Already loaded
        
        total_enriched = 0
        
        # Stage 1: Dynamic window (±0.2s) - catches most aircraft flares/chaff
        while True:
            # print(f"Enriching decoys (dynamic) - {total_enriched}/{total_enriched}")
            enriched = self._enrich_batched(conn, self.batch_size, use_dynamic=True)
            if enriched == 0:
                break
            total_enriched += enriched
        
        # Stage 2: Static last-state - catches remaining (ships, ground vehicles)
        # Use smaller batch size to avoid OOM from large pair explosion
        static_batch_size = round(self.batch_size / 4)
        while True:
            # print(f"Enriching decoys (static) - {total_enriched}/{total_enriched}")
            enriched = self._enrich_batched(conn, static_batch_size, use_dynamic=False)
            if enriched == 0:
                break
            total_enriched += enriched
        
        return total_enriched
    
    def _enrich_batched(self, conn: duckdb.DuckDBPyConnection, limit: int, use_dynamic: bool = True) -> int:
        """
        Object count-based batching using LIMIT without OFFSET.
        Filter automatically excludes already-enriched decoys.
        
        Args:
            conn: DuckDB connection
            limit: Batch size (LIMIT clause)
            use_dynamic: If True, use ±0.2s window. If False, use last-state before spawn.
            
        Returns:
            Number of decoys enriched in this batch
        """
        # Choose query based on dynamic vs static matching
        if use_dynamic:
            # DYNAMIC: Use ±0.2s time window with LATERAL JOIN (fast, memory efficient)
            bulk_query = f"""
            WITH decoy_batch AS (
              SELECT id
              FROM objects
              WHERE type_basic = 'Decoy'
                AND parent_id IS NULL
              ORDER BY first_seen
              LIMIT ?
            ),
            decoy_first AS (
              SELECT 
                d.id as decoy_id,
                d.first_seen,
                s.longitude as decoy_lon,
                s.latitude as decoy_lat,
                s.altitude as decoy_alt
              FROM decoy_batch db
              JOIN objects d ON d.id = db.id
              JOIN states s ON d.id = s.object_id
                AND s.timestamp = d.first_seen
              WHERE s.longitude IS NOT NULL
                AND s.latitude IS NOT NULL
            ),
            decoy_parent_pairs AS (
              SELECT
                d.decoy_id,
                d.first_seen,
                d.decoy_lon,
                d.decoy_lat,
                d.decoy_alt,
                p.id as parent_id
              FROM decoy_first d
              JOIN objects p ON p.type_class IN ('Air', 'Sea', 'Ground')
                AND p.first_seen <= d.first_seen
                AND (p.removed_at IS NULL OR p.removed_at >= d.first_seen)
            ),
            parent_state_per_pair AS (
              SELECT
                dpp.decoy_id,
                dpp.parent_id,
                dpp.decoy_lon,
                dpp.decoy_lat,
                dpp.decoy_alt,
                ps.longitude,
                ps.latitude,
                ps.altitude,
                calculate_approximate_distance_squared(
                  ps.latitude - dpp.decoy_lat,
                  ps.longitude - dpp.decoy_lon
                ) + POWER(ps.altitude - dpp.decoy_alt, 2) as distance_sq
              FROM decoy_parent_pairs dpp
              JOIN LATERAL (
                SELECT longitude, latitude, altitude
                FROM states
                WHERE object_id = dpp.parent_id
                  AND timestamp BETWEEN dpp.first_seen - 0.2 AND dpp.first_seen + 0.2
                ORDER BY ABS(timestamp - dpp.first_seen)
                LIMIT 1
              ) ps ON ps.longitude IS NOT NULL
                  AND ABS(ps.altitude - dpp.decoy_alt) <= 200
            ),
            ranked_parents AS (
              SELECT
                decoy_id,
                parent_id,
                distance_sq,
                ROW_NUMBER() OVER (PARTITION BY decoy_id ORDER BY distance_sq) as rn
              FROM parent_state_per_pair
              WHERE distance_sq <= POWER(?, 2)
            )
            SELECT 
              decoy_id,
              parent_id,
              SQRT(distance_sq) as distance
            FROM ranked_parents
            WHERE rn = 1
            """
            matches = conn.execute(bulk_query, [limit, self.proximity_radius]).fetchall()
        else:
            # STATIC: Use last state before spawn with LATERAL JOIN (slower, for edge cases)
            bulk_query = f"""
            WITH decoy_batch AS (
              SELECT id
              FROM objects
              WHERE type_basic = 'Decoy'
                AND parent_id IS NULL
              ORDER BY first_seen
              LIMIT ?
            ),
            decoy_first AS (
              SELECT 
                d.id as decoy_id,
                d.first_seen,
                s.longitude as decoy_lon,
                s.latitude as decoy_lat,
                s.altitude as decoy_alt
              FROM decoy_batch db
              JOIN objects d ON d.id = db.id
              JOIN states s ON d.id = s.object_id
                AND s.timestamp = d.first_seen
              WHERE s.longitude IS NOT NULL
                AND s.latitude IS NOT NULL
            ),
            decoy_parent_pairs AS (
              SELECT
                d.decoy_id,
                d.first_seen,
                d.decoy_lon,
                d.decoy_lat,
                d.decoy_alt,
                p.id as parent_id
              FROM decoy_first d
              JOIN objects p ON p.type_class IN ('Sea', 'Ground')
                AND p.first_seen <= d.first_seen
                AND (p.removed_at IS NULL OR p.removed_at >= d.first_seen)
            ),
            parent_state_per_pair AS (
              SELECT
                dpp.decoy_id,
                dpp.parent_id,
                dpp.decoy_lon,
                dpp.decoy_lat,
                dpp.decoy_alt,
                ps.longitude,
                ps.latitude,
                ps.altitude,
                calculate_approximate_distance_squared(
                  ps.latitude - dpp.decoy_lat,
                  ps.longitude - dpp.decoy_lon
                ) + POWER(ps.altitude - dpp.decoy_alt, 2) as distance_sq
              FROM decoy_parent_pairs dpp
              JOIN LATERAL (
                SELECT longitude, latitude, altitude
                FROM states
                WHERE object_id = dpp.parent_id
                  AND timestamp <= dpp.first_seen
                ORDER BY timestamp DESC
                LIMIT 1
              ) ps ON ps.longitude IS NOT NULL
                  AND ABS(ps.altitude - dpp.decoy_alt) <= 200
            ),
            ranked_parents AS (
              SELECT
                decoy_id,
                parent_id,
                distance_sq,
                ROW_NUMBER() OVER (PARTITION BY decoy_id ORDER BY distance_sq) as rn
              FROM parent_state_per_pair
              WHERE distance_sq <= POWER(?, 2)
            )
            SELECT 
              decoy_id,
              parent_id,
              SQRT(distance_sq) as distance
            FROM ranked_parents
            WHERE rn = 1
            """
            matches = conn.execute(bulk_query, [limit, self.proximity_radius]).fetchall()
        
        # Get parent coalitions for matched decoys
        parent_ids = [parent_id for _, parent_id, _ in matches]
        parent_coalitions = {}
        if parent_ids:
            coalition_query = "SELECT id, coalition FROM objects WHERE id IN ({})".format(
                ','.join(['?'] * len(parent_ids))
            )
            for parent_id, coalition in conn.execute(coalition_query, parent_ids).fetchall():
                parent_coalitions[parent_id] = coalition
        
        # Bulk update parent_id, coalition, and properties
        updates = []
        for decoy_id, parent_id, distance in matches:
            parent_coalition = parent_coalitions.get(parent_id)
            properties = {"DeploymentRange": distance}
            updates.append((parent_id, parent_coalition, json.dumps(properties), decoy_id))
        
        if updates:
            conn.executemany(
                """
                UPDATE objects
                SET 
                    parent_id = ?,
                    coalition = ?,  -- Set coalition from parent
                    properties = json_merge_patch(COALESCE(properties, '{}'), ?)
                WHERE id = ?
                """,
                updates
            )
        
        # Return number of decoys matched (not batch size)
        return len(matches)

