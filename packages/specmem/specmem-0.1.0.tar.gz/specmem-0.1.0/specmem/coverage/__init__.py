"""Spec Coverage Analysis module.

Provides analysis of the gap between specification acceptance criteria
and existing tests.
"""

from specmem.coverage.engine import CoverageEngine
from specmem.coverage.extractor import CriteriaExtractor
from specmem.coverage.matcher import CriteriaMatcher
from specmem.coverage.models import (
    AcceptanceCriterion,
    CoverageResult,
    CriteriaMatch,
    ExtractedTest,
    FeatureCoverage,
    TestSuggestion,
)
from specmem.coverage.scanner import TestScanner


__all__ = [
    "AcceptanceCriterion",
    "CoverageEngine",
    "CoverageResult",
    "CriteriaExtractor",
    "CriteriaMatch",
    "CriteriaMatcher",
    "ExtractedTest",
    "FeatureCoverage",
    "TestScanner",
    "TestSuggestion",
]
