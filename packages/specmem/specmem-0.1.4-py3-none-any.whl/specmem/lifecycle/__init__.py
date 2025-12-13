"""Spec Lifecycle Management Module.

This module provides tools for managing the spec lifecycle:
- Health analysis: Calculate spec health scores
- Pruning: Archive or delete orphaned/stale specs
- Generation: Create specs from existing code
- Compression: Condense verbose specs
"""

from specmem.lifecycle.compressor import CompressorEngine
from specmem.lifecycle.generator import GeneratorEngine
from specmem.lifecycle.health import HealthAnalyzer
from specmem.lifecycle.models import (
    ArchiveMetadata,
    CompressedSpec,
    GeneratedSpec,
    PruneResult,
    SpecHealthScore,
    calculate_health_score,
)
from specmem.lifecycle.pruner import PrunerEngine


__all__ = [
    "ArchiveMetadata",
    "CompressedSpec",
    "CompressorEngine",
    "GeneratedSpec",
    "GeneratorEngine",
    # Engines
    "HealthAnalyzer",
    "PruneResult",
    "PrunerEngine",
    # Models
    "SpecHealthScore",
    # Functions
    "calculate_health_score",
]
