"""Enrichment pipeline orchestration."""

from abc import ABC, abstractmethod
from typing import List

from ..parser.types import TacviewObject
from ..storage.duckdb_store import DuckDBStore


class Enricher(ABC):
    """Abstract base class for enrichers."""

    @abstractmethod
    def enrich(self, objects: List[TacviewObject], store: DuckDBStore):
        """
        Enrich objects with additional data.

        Args:
            objects: List of TacviewObject instances to enrich
            store: DuckDB store for queries and updates
        """
        pass


class EnrichmentPipeline:
    """Pipeline for running multiple enrichers."""

    def __init__(self, store: DuckDBStore):
        """
        Initialize enrichment pipeline.

        Args:
            store: DuckDB store instance
        """
        self.store = store
        self.enrichers: List[Enricher] = []

    def add_enricher(self, enricher: Enricher):
        """
        Add enricher to pipeline.

        Args:
            enricher: Enricher instance
        """
        self.enrichers.append(enricher)

    def run(self, objects: List[TacviewObject]):
        """
        Run all enrichers in sequence.

        Args:
            objects: List of TacviewObject instances
        """
        for enricher in self.enrichers:
            enricher.enrich(objects, self.store)

