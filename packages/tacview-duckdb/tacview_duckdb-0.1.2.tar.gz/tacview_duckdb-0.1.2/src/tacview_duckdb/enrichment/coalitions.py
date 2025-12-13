"""Coalition propagation enrichment."""

from typing import List
import duckdb

from ..parser.types import TacviewObject
from ..storage.duckdb_store import DuckDBStore
from .pipeline import Enricher


class CoalitionPropagator(Enricher):
    """Enricher for propagating coalition information."""

    def enrich(self, objects: List[TacviewObject], store: DuckDBStore):
        """
        Propagate coalition information to objects without it.

        Uses color attribute as fallback for coalition determination.

        Args:
            objects: List of TacviewObject instances
            store: DuckDB store instance
        """
        for obj in objects:
            # If no coalition but has color, infer from color
            if not obj.coalition and obj.color:
                obj.coalition = self._infer_coalition_from_color(obj.color)

    def _infer_coalition_from_color(self, color: str) -> str:
        """Infer coalition from color attribute."""
        color_lower = color.lower()

        if "red" in color_lower:
            return "Enemies"
        elif "blue" in color_lower:
            return "Allies"
        else:
            return "Neutrals"


class CoalitionEnricher(Enricher):
    """
    SQL-based coalition enricher.
    
    Infers coalition from color attribute when coalition is missing:
    - Red → Enemies
    - Blue → Allies
    - Other → Neutrals
    """
    
    def enrich(self, objects: list, conn: duckdb.DuckDBPyConnection) -> int:
        """
        Run coalition enrichment using SQL.
        
        Args:
            objects: Not used (queries DB directly)
            conn: DuckDB connection
            
        Returns:
            Number of objects enriched
        """
        result = conn.execute("""
            UPDATE objects 
            SET coalition = CASE
                WHEN LOWER(color) LIKE '%red%' THEN 'Enemies'
                WHEN LOWER(color) LIKE '%blue%' THEN 'Allies'
                ELSE 'Neutrals'
            END
            WHERE (coalition IS NULL OR coalition = '')
              AND color IS NOT NULL
              AND color != ''
        """)
        
        enriched_count = result.fetchone()
        if enriched_count:
            return enriched_count[0] if isinstance(enriched_count, tuple) else 0
        return 0

