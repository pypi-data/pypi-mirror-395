"""Parent-child relationship tracking."""

from typing import List

from ..parser.types import TacviewObject
from ..storage.duckdb_store import DuckDBStore
from .pipeline import Enricher


class RelationshipTracker(Enricher):
    """Enricher for tracking parent-child relationships."""

    def enrich(self, objects: List[TacviewObject], store: DuckDBStore):
        """
        Track parent-child relationships between objects.

        This is a placeholder for future implementation.

        Args:
            objects: List of TacviewObject instances
            store: DuckDB store instance
        """
        # Future implementation: track parent-child relationships
        # from ACMI Parent property
        pass

