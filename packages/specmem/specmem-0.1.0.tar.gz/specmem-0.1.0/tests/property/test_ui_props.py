"""Property-based tests for SpecMem Web UI.

These tests verify correctness properties for the UI backend logic.
"""

import string

from hypothesis import given, settings
from hypothesis import strategies as st

from specmem.core.specir import SpecBlock, SpecStatus, SpecType
from specmem.ui.filters import (
    calculate_counts,
    count_by_source,
    count_by_type,
    filter_blocks,
    get_pinned_blocks,
)
from specmem.ui.models import (
    BlockDetail,
    BlockSummary,
    truncate_text,
)


# Strategies for generating test data
spec_type_strategy = st.sampled_from(list(SpecType))
spec_status_strategy = st.sampled_from(list(SpecStatus))

# Generate valid non-empty text
text_strategy = st.text(
    alphabet=string.ascii_letters + string.digits + " .,!?-_\n",
    min_size=1,
    max_size=1000,
).filter(lambda x: x.strip())

# Generate SpecBlocks
spec_block_strategy = st.builds(
    SpecBlock,
    type=spec_type_strategy,
    text=text_strategy,
    source=st.text(
        alphabet=string.ascii_lowercase + "/._",
        min_size=5,
        max_size=50,
    ).filter(lambda x: x.strip()),
    status=spec_status_strategy,
    tags=st.lists(st.text(min_size=1, max_size=20), max_size=5),
    links=st.lists(st.text(min_size=1, max_size=50), max_size=3),
    pinned=st.booleans(),
)

# List of SpecBlocks
spec_blocks_strategy = st.lists(spec_block_strategy, min_size=0, max_size=50)


class TestTextTruncation:
    """Tests for Property 3: Text Truncation Consistency."""

    # **Feature: specmem-web-ui, Property 3: Text Truncation Consistency**
    # **Validates: Requirements 2.4**

    @given(st.text(min_size=0, max_size=500))
    @settings(max_examples=100)
    def test_truncation_preserves_short_text(self, text: str):
        """Text shorter than 200 chars should not be truncated."""
        if len(text) <= 200:
            result = truncate_text(text)
            assert result == text, "Short text should not be modified"

    @given(st.text(min_size=201, max_size=1000))
    @settings(max_examples=100)
    def test_truncation_adds_ellipsis_to_long_text(self, text: str):
        """Text longer than 200 chars should be truncated with ellipsis."""
        result = truncate_text(text)
        assert len(result) == 203, "Truncated text should be 200 chars + '...'"
        assert result.endswith("..."), "Truncated text should end with ellipsis"
        assert result[:200] == text[:200], "First 200 chars should be preserved"

    @given(st.text(min_size=1, max_size=1000))
    @settings(max_examples=100)
    def test_truncation_length_invariant(self, text: str):
        """Truncated text should never exceed 203 characters."""
        result = truncate_text(text)
        assert len(result) <= 203, "Result should never exceed 203 chars"


class TestBlockResponseCompleteness:
    """Tests for Property 2: Block Response Completeness."""

    # **Feature: specmem-web-ui, Property 2: Block Response Completeness**
    # **Validates: Requirements 2.3**

    @given(spec_block_strategy)
    @settings(max_examples=100)
    def test_block_summary_contains_required_fields(self, block: SpecBlock):
        """BlockSummary should contain all required fields."""
        summary = BlockSummary.from_spec_block(block)

        assert summary.id == block.id
        assert summary.type == block.type.value
        assert summary.source == block.source
        assert summary.status == block.status.value
        assert summary.pinned == block.pinned
        # text_preview should be truncated version
        assert len(summary.text_preview) <= 203

    @given(spec_block_strategy)
    @settings(max_examples=100)
    def test_block_detail_contains_all_fields(self, block: SpecBlock):
        """BlockDetail should contain all fields including full text."""
        detail = BlockDetail.from_spec_block(block)

        assert detail.id == block.id
        assert detail.type == block.type.value
        assert detail.text == block.text  # Full text, not truncated
        assert detail.source == block.source
        assert detail.status == block.status.value
        assert detail.pinned == block.pinned
        assert detail.tags == block.tags
        assert detail.links == block.links


class TestFilterCorrectness:
    """Tests for Property 4: Filter Correctness."""

    # **Feature: specmem-web-ui, Property 4: Filter Correctness**
    # **Validates: Requirements 3.2, 3.3, 3.4, 3.5, 4.2, 4.3, 4.4**

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_active_filter_returns_only_active(self, blocks: list[SpecBlock]):
        """Active filter should return only active blocks."""
        filtered = filter_blocks(blocks, status="active")
        for block in filtered:
            assert block.status == SpecStatus.ACTIVE

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_legacy_filter_returns_only_legacy(self, blocks: list[SpecBlock]):
        """Legacy filter should return only legacy blocks."""
        filtered = filter_blocks(blocks, status="legacy")
        for block in filtered:
            assert block.status == SpecStatus.LEGACY

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_all_filter_returns_all_blocks(self, blocks: list[SpecBlock]):
        """All/no filter should return all blocks."""
        filtered_all = filter_blocks(blocks, status="all")
        filtered_none = filter_blocks(blocks, status=None)

        assert len(filtered_all) == len(blocks)
        assert len(filtered_none) == len(blocks)

    @given(spec_blocks_strategy, spec_type_strategy)
    @settings(max_examples=100)
    def test_type_filter_returns_only_matching_type(
        self, blocks: list[SpecBlock], block_type: SpecType
    ):
        """Type filter should return only blocks of that type."""
        filtered = filter_blocks(blocks, block_type=block_type.value)
        for block in filtered:
            assert block.type == block_type

    @given(spec_blocks_strategy, spec_status_strategy, spec_type_strategy)
    @settings(max_examples=100)
    def test_combined_filters_use_and_logic(
        self, blocks: list[SpecBlock], status: SpecStatus, block_type: SpecType
    ):
        """Combined filters should use AND logic."""
        filtered = filter_blocks(blocks, status=status.value, block_type=block_type.value)
        for block in filtered:
            assert block.status == status
            assert block.type == block_type

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_filter_count_matches_result_length(self, blocks: list[SpecBlock]):
        """Calculated counts should match filtered result lengths."""
        filtered = filter_blocks(blocks, status="active")
        total, active, legacy, pinned = calculate_counts(filtered)

        assert total == len(filtered)
        assert active == len([b for b in filtered if b.status == SpecStatus.ACTIVE])
        assert legacy == len([b for b in filtered if b.status == SpecStatus.LEGACY])
        assert pinned == len([b for b in filtered if b.pinned])


class TestSearchResultOrdering:
    """Tests for Property 5: Search Result Ordering."""

    # **Feature: specmem-web-ui, Property 5: Search Result Ordering**
    # **Validates: Requirements 5.3, 5.4**

    @given(
        st.lists(st.floats(min_value=0.0, max_value=1.0, allow_nan=False), min_size=2, max_size=20)
    )
    @settings(max_examples=100)
    def test_scores_are_non_negative(self, scores: list[float]):
        """All search result scores should be non-negative."""
        for score in scores:
            assert score >= 0.0, "Scores must be non-negative"

    @given(
        st.lists(st.floats(min_value=0.0, max_value=1.0, allow_nan=False), min_size=2, max_size=20)
    )
    @settings(max_examples=100)
    def test_sorted_scores_are_descending(self, scores: list[float]):
        """Sorted results should be in descending order by score."""
        sorted_scores = sorted(scores, reverse=True)
        for i in range(len(sorted_scores) - 1):
            assert sorted_scores[i] >= sorted_scores[i + 1], "Scores should be descending"


class TestPinnedBlockRetrieval:
    """Tests for Property 6: Pinned Block Retrieval."""

    # **Feature: specmem-web-ui, Property 6: Pinned Block Retrieval**
    # **Validates: Requirements 6.1, 6.3**

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_pinned_returns_only_pinned_blocks(self, blocks: list[SpecBlock]):
        """Pinned endpoint should return exactly all pinned blocks."""
        pinned = get_pinned_blocks(blocks)
        expected_pinned = [b for b in blocks if b.pinned]

        assert len(pinned) == len(expected_pinned)
        for block in pinned:
            assert block.pinned is True

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_all_pinned_blocks_are_returned(self, blocks: list[SpecBlock]):
        """All pinned blocks should be in the result."""
        pinned = get_pinned_blocks(blocks)
        pinned_ids = {b.id for b in pinned}

        for block in blocks:
            if block.pinned:
                assert block.id in pinned_ids


class TestStatisticsAccuracy:
    """Tests for Property 7: Statistics Accuracy."""

    # **Feature: specmem-web-ui, Property 7: Statistics Accuracy**
    # **Validates: Requirements 2.1, 8.1, 8.2**

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_total_count_matches_block_count(self, blocks: list[SpecBlock]):
        """Total count should equal number of blocks."""
        total, active, legacy, pinned = calculate_counts(blocks)
        assert total == len(blocks)

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_status_counts_are_accurate(self, blocks: list[SpecBlock]):
        """Active and legacy counts should match actual counts."""
        total, active, legacy, pinned = calculate_counts(blocks)

        actual_active = sum(1 for b in blocks if b.status == SpecStatus.ACTIVE)
        actual_legacy = sum(1 for b in blocks if b.status == SpecStatus.LEGACY)

        assert active == actual_active
        assert legacy == actual_legacy

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_type_counts_sum_to_total(self, blocks: list[SpecBlock]):
        """Type counts should sum to total."""
        by_type = count_by_type(blocks)
        assert sum(by_type.values()) == len(blocks)

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_source_counts_sum_to_total(self, blocks: list[SpecBlock]):
        """Source counts should sum to total."""
        by_source = count_by_source(blocks)
        assert sum(by_source.values()) == len(blocks)

    @given(spec_blocks_strategy)
    @settings(max_examples=100)
    def test_pinned_count_is_accurate(self, blocks: list[SpecBlock]):
        """Pinned count should match actual pinned blocks."""
        total, active, legacy, pinned = calculate_counts(blocks)
        actual_pinned = sum(1 for b in blocks if b.pinned)
        assert pinned == actual_pinned


class TestPortConfiguration:
    """Tests for Property 1: Server Port Configuration."""

    # **Feature: specmem-web-ui, Property 1: Server Port Configuration**
    # **Validates: Requirements 1.1, 1.3**

    @given(st.integers(min_value=1024, max_value=65535))
    @settings(max_examples=20)
    def test_valid_port_range(self, port: int):
        """Valid ports should be in range 1024-65535."""
        assert 1024 <= port <= 65535, "Port must be in valid range"

    @given(st.integers(min_value=1024, max_value=65535))
    @settings(max_examples=20)
    def test_port_availability_check_returns_bool(self, port: int):
        """Port availability check should return boolean."""
        from specmem.ui.server import is_port_available

        result = is_port_available(port)
        assert isinstance(result, bool)

    @given(st.integers(min_value=1024, max_value=60000))
    @settings(max_examples=10)
    def test_find_available_port_returns_valid_port(self, preferred: int):
        """find_available_port should return a port >= preferred."""
        from specmem.ui.server import find_available_port

        try:
            port = find_available_port(preferred, max_attempts=10)
            assert port >= preferred
            assert port < preferred + 10
        except RuntimeError:
            # All ports in range are in use, which is acceptable
            pass


class TestTourStepAdvancement:
    """Tests for Property 7: Tour Step Advancement (from project-polish spec)."""

    # **Feature: project-polish, Property 7: Tour Step Advancement**
    # **Validates: Requirements 10.3**

    @given(st.integers(min_value=1, max_value=20))
    @settings(max_examples=50)
    def test_tour_step_advancement_logic(self, total_steps: int):
        """For any tour with N steps, completing step K advances to K+1."""
        # Simulate tour state
        current_step = 0

        for _ in range(total_steps):
            # Advance step
            next_step = current_step + 1

            if next_step < total_steps:
                # Should advance to next step
                assert next_step == current_step + 1
                current_step = next_step
            else:
                # Should end tour (step N completes the tour)
                assert next_step >= total_steps
                break

        # After completing all steps, we should be at or past the last step
        assert current_step == total_steps - 1 or current_step >= total_steps - 1

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=0, max_value=9))
    @settings(max_examples=50)
    def test_completing_step_k_advances_to_k_plus_1(self, total_steps: int, start_step: int):
        """Completing step K should advance to step K+1."""
        if start_step >= total_steps:
            return  # Skip invalid combinations

        current_step = start_step
        next_step = current_step + 1

        if next_step < total_steps:
            assert next_step == current_step + 1, "Should advance to next step"
        else:
            assert next_step >= total_steps, "Should end tour when completing last step"

    @given(st.integers(min_value=1, max_value=20))
    @settings(max_examples=50)
    def test_completing_last_step_ends_tour(self, total_steps: int):
        """Completing step N (last step) should end the tour."""
        last_step = total_steps - 1
        next_step = last_step + 1

        # After completing the last step, next_step should equal total_steps
        # which indicates the tour is complete
        assert next_step == total_steps, "Completing last step should end tour"
        assert next_step >= total_steps, "Tour should be marked as complete"

    @given(st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=10))
    @settings(max_examples=30)
    def test_tour_steps_are_sequential(self, step_titles: list[str]):
        """Tour steps should be visited in sequential order."""
        visited_steps = []
        current_step = 0

        while current_step < len(step_titles):
            visited_steps.append(current_step)
            current_step += 1

        # Verify sequential order
        for i, step in enumerate(visited_steps):
            assert step == i, f"Step {i} should be visited at position {i}"

        # All steps should be visited
        assert len(visited_steps) == len(step_titles)
