"""Criteria Matcher for Spec Coverage Analysis.

Matches acceptance criteria to tests using semantic similarity
and explicit requirement links.
"""

from __future__ import annotations

import logging
import re
from difflib import SequenceMatcher

from specmem.coverage.models import (
    AcceptanceCriterion,
    CriteriaMatch,
    ExtractedTest,
)


logger = logging.getLogger(__name__)


class CriteriaMatcher:
    """Matches acceptance criteria to tests.

    Uses explicit requirement links (confidence 1.0) and text similarity
    for matching criteria to tests.
    """

    CONFIDENCE_THRESHOLD = 0.5

    def __init__(self) -> None:
        """Initialize the matcher."""
        pass

    def match(
        self,
        criteria: list[AcceptanceCriterion],
        tests: list[ExtractedTest],
    ) -> list[CriteriaMatch]:
        """Match criteria to tests.

        Args:
            criteria: List of acceptance criteria
            tests: List of extracted tests

        Returns:
            List of CriteriaMatch objects
        """
        matches: list[CriteriaMatch] = []

        for criterion in criteria:
            best_match: ExtractedTest | None = None
            best_confidence = 0.0

            for test in tests:
                confidence = self._calculate_match_confidence(criterion, test)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = test

            matches.append(
                CriteriaMatch(
                    criterion=criterion,
                    test=best_match if best_confidence >= self.CONFIDENCE_THRESHOLD else None,
                    confidence=best_confidence,
                )
            )

        return matches

    def _calculate_match_confidence(
        self,
        criterion: AcceptanceCriterion,
        test: ExtractedTest,
    ) -> float:
        """Calculate confidence score for a criterion-test match.

        Args:
            criterion: Acceptance criterion
            test: Extracted test

        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Check for explicit link first
        if self._check_explicit_link(criterion, test):
            return 1.0

        # Calculate text similarity
        return self.calculate_similarity(criterion, test)

    def _check_explicit_link(
        self,
        criterion: AcceptanceCriterion,
        test: ExtractedTest,
    ) -> bool:
        """Check if test explicitly links to criterion.

        Args:
            criterion: Acceptance criterion
            test: Extracted test

        Returns:
            True if explicit link exists
        """
        if not test.requirement_links:
            return False

        # Check if criterion number matches any link
        for link in test.requirement_links:
            if link == criterion.number:
                return True
            # Also check partial match (e.g., "1" matches "1.2")
            if criterion.number.startswith(f"{link}."):
                return True

        return False

    def calculate_similarity(
        self,
        criterion: AcceptanceCriterion,
        test: ExtractedTest,
    ) -> float:
        """Calculate text similarity between criterion and test.

        Args:
            criterion: Acceptance criterion
            test: Extracted test

        Returns:
            Similarity score between 0.0 and 1.0
        """
        # Combine test name and docstring for matching
        test_text = self._normalize_text(test.name)
        if test.docstring:
            test_text += " " + self._normalize_text(test.docstring)

        criterion_text = self._normalize_text(criterion.text)

        # Use SequenceMatcher for basic similarity
        base_similarity = SequenceMatcher(None, criterion_text, test_text).ratio()

        # Boost score if key terms match
        criterion_terms = self._extract_key_terms(criterion_text)
        test_terms = self._extract_key_terms(test_text)

        if criterion_terms and test_terms:
            term_overlap = len(criterion_terms & test_terms) / len(criterion_terms)
            # Weighted combination
            similarity = 0.4 * base_similarity + 0.6 * term_overlap
        else:
            similarity = base_similarity

        return min(similarity, 1.0)

    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison.

        Args:
            text: Text to normalize

        Returns:
            Normalized text
        """
        # Convert to lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        # Normalize whitespace
        text = " ".join(text.split())
        return text

    def _extract_key_terms(self, text: str) -> set[str]:
        """Extract key terms from text.

        Args:
            text: Text to extract terms from

        Returns:
            Set of key terms
        """
        # Common stop words to ignore
        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "shall",
            "can",
            "need",
            "to",
            "of",
            "in",
            "for",
            "on",
            "with",
            "at",
            "by",
            "from",
            "as",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "between",
            "under",
            "again",
            "further",
            "then",
            "once",
            "when",
            "where",
            "why",
            "how",
            "all",
            "each",
            "every",
            "both",
            "few",
            "more",
            "most",
            "other",
            "some",
            "such",
            "no",
            "nor",
            "not",
            "only",
            "own",
            "same",
            "so",
            "than",
            "too",
            "very",
            "just",
            "and",
            "but",
            "if",
            "or",
            "because",
            "until",
            "while",
            "that",
            "this",
            "these",
            "those",
            "system",
            "user",
        }

        words = text.split()
        # Filter out stop words and short words
        terms = {w for w in words if w not in stop_words and len(w) > 2}
        return terms
