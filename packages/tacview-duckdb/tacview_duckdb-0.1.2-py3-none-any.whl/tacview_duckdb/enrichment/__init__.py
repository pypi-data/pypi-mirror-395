"""Enrichment pipeline module."""

from .pipeline import EnrichmentPipeline, Enricher
from .coalitions import CoalitionPropagator, CoalitionEnricher
from .ejection_events import EjectedPilotEnricher
from .weapons import WeaponEnricher
from .missed_weapons import MissedWeaponAnalyzer
from .spatial_clusters import SpatialClusterEnricher
from .lifecycle import FixedWingEnricher, RotorcraftEnricher, GroundSeaEnricher
from .containers import ContainerEnricher
from .decoys import DecoyEnricher
from .geodata import EventGeodataEnricher
from .projectile import ProjectileEnricher
from . import airports

__all__ = [
    "EnrichmentPipeline",
    "Enricher",
    "CoalitionPropagator",
    "CoalitionEnricher",
    "EjectedPilotEnricher",
    "WeaponEnricher",
    "MissedWeaponAnalyzer",
    "SpatialClusterEnricher",
    "FixedWingEnricher",
    "RotorcraftEnricher",
    "GroundSeaEnricher",
    "ContainerEnricher",
    "DecoyEnricher",
    "EventGeodataEnricher",
    "ProjectileEnricher",
    "airports",
]

