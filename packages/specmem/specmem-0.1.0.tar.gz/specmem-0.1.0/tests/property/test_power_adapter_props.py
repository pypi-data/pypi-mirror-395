"""Property-based tests for Kiro Power Adapter.

Tests correctness properties defined in the kiro-powers-integration design document.
"""

import json
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from specmem.adapters.power import PowerAdapter, PowerInfo, ToolInfo
from specmem.core.specir import SpecType


# Strategies for generating test data
power_name_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_"),
    min_size=3,
    max_size=30,
).filter(lambda x: len(x.strip()) > 2)

description_strategy = st.text(min_size=10, max_size=200).filter(lambda x: len(x.strip()) > 5)

keyword_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N")),
    min_size=2,
    max_size=20,
).filter(lambda x: len(x.strip()) > 1)


def create_power_directory(
    tmpdir: Path,
    power_name: str,
    power_md_content: str | None = None,
    mcp_json_content: dict | None = None,
    steering_files: dict[str, str] | None = None,
) -> Path:
    """Helper to create a Power directory structure."""
    powers_dir = tmpdir / ".kiro" / "powers"
    power_dir = powers_dir / power_name
    power_dir.mkdir(parents=True, exist_ok=True)

    # Create POWER.md
    if power_md_content is not None:
        (power_dir / "POWER.md").write_text(power_md_content)

    # Create mcp.json
    if mcp_json_content is not None:
        (power_dir / "mcp.json").write_text(json.dumps(mcp_json_content))

    # Create steering files
    if steering_files:
        steering_dir = power_dir / "steering"
        steering_dir.mkdir(exist_ok=True)
        for filename, content in steering_files.items():
            (steering_dir / filename).write_text(content)

    return power_dir


class TestPowerDetection:
    """**Feature: kiro-powers-integration, Property 5: Power Detection**

    *For any* repository with a `.kiro/powers/` directory containing at least
    one Power with a POWER.md file, the PowerAdapter SHALL detect the Power.

    **Validates: Requirements 2.1**
    """

    def test_detect_returns_false_for_empty_directory(self):
        """Detection returns False for directory without Powers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter = PowerAdapter()
            assert adapter.detect(tmpdir) is False

    def test_detect_returns_false_for_missing_kiro_dir(self):
        """Detection returns False when .kiro directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter = PowerAdapter()
            assert adapter.detect(tmpdir) is False

    def test_detect_returns_false_for_empty_powers_dir(self):
        """Detection returns False when powers directory is empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            powers_dir = Path(tmpdir) / ".kiro" / "powers"
            powers_dir.mkdir(parents=True)

            adapter = PowerAdapter()
            assert adapter.detect(tmpdir) is False

    def test_detect_returns_false_for_power_without_power_md(self):
        """Detection returns False when Power has no POWER.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            power_dir = Path(tmpdir) / ".kiro" / "powers" / "test-power"
            power_dir.mkdir(parents=True)
            # Create mcp.json but no POWER.md
            (power_dir / "mcp.json").write_text("{}")

            adapter = PowerAdapter()
            assert adapter.detect(tmpdir) is False

    @given(power_name=power_name_strategy)
    @settings(max_examples=20)
    def test_detect_returns_true_for_valid_power(self, power_name: str):
        """For any valid Power with POWER.md, detection returns True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            create_power_directory(
                Path(tmpdir),
                power_name,
                power_md_content=f"# {power_name}\n\nA test power.",
            )

            adapter = PowerAdapter()
            assert adapter.detect(tmpdir) is True

    @given(power_names=st.lists(power_name_strategy, min_size=1, max_size=5, unique=True))
    @settings(max_examples=10)
    def test_detect_returns_true_for_multiple_powers(self, power_names: list[str]):
        """Detection returns True when multiple Powers are installed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            for name in power_names:
                create_power_directory(
                    Path(tmpdir),
                    name,
                    power_md_content=f"# {name}\n\nA test power.",
                )

            adapter = PowerAdapter()
            assert adapter.detect(tmpdir) is True


class TestPowerParsingCompleteness:
    """**Feature: kiro-powers-integration, Property 6: Power Parsing Completeness**

    *For any* valid POWER.md file, parsing SHALL produce SpecBlocks containing
    the Power name, description, and tool information. *For any* Power with
    steering files, each steering file SHALL produce at least one SpecBlock.

    **Validates: Requirements 2.2, 2.3, 2.4**
    """

    @given(
        power_name=power_name_strategy,
        description=description_strategy,
    )
    @settings(max_examples=20)
    def test_power_md_produces_specblocks(self, power_name: str, description: str):
        """For any valid POWER.md, parsing produces SpecBlocks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            power_md_content = f"# {power_name}\n\n{description}\n\n## Usage\n\nHow to use."
            create_power_directory(
                Path(tmpdir),
                power_name,
                power_md_content=power_md_content,
            )

            adapter = PowerAdapter()
            blocks = adapter.load(tmpdir)

            assert len(blocks) > 0
            # Should have at least one KNOWLEDGE block (overview)
            knowledge_blocks = [b for b in blocks if b.type == SpecType.KNOWLEDGE]
            assert len(knowledge_blocks) >= 1

    @given(
        power_name=power_name_strategy,
        keywords=st.lists(keyword_strategy, min_size=1, max_size=5),
    )
    @settings(max_examples=10)
    def test_mcp_json_keywords_included_in_tags(self, power_name: str, keywords: list[str]):
        """Keywords from mcp.json are included in SpecBlock tags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mcp_config = {
                "name": power_name,
                "description": "Test power",
                "keywords": keywords,
            }
            create_power_directory(
                Path(tmpdir),
                power_name,
                power_md_content=f"# {power_name}\n\nTest power.",
                mcp_json_content=mcp_config,
            )

            adapter = PowerAdapter()
            blocks = adapter.load(tmpdir)

            # Find pinned KNOWLEDGE block (overview)
            overview_blocks = [b for b in blocks if b.type == SpecType.KNOWLEDGE and b.pinned]
            assert len(overview_blocks) >= 1

            overview = overview_blocks[0]
            for keyword in keywords:
                assert keyword in overview.tags

    @given(
        power_name=power_name_strategy,
        steering_count=st.integers(min_value=1, max_value=3),
    )
    @settings(max_examples=10)
    def test_steering_files_produce_specblocks(self, power_name: str, steering_count: int):
        """For any Power with steering files, each produces a SpecBlock."""
        with tempfile.TemporaryDirectory() as tmpdir:
            steering_files = {
                f"guide-{i}.md": f"# Guide {i}\n\nContent for guide {i}."
                for i in range(steering_count)
            }
            create_power_directory(
                Path(tmpdir),
                power_name,
                power_md_content=f"# {power_name}\n\nTest power.",
                steering_files=steering_files,
            )

            adapter = PowerAdapter()
            blocks = adapter.load(tmpdir)

            # Should have TASK type blocks for steering files
            steering_blocks = [
                b for b in blocks if b.type == SpecType.TASK and "steering" in b.tags
            ]
            assert len(steering_blocks) == steering_count

    def test_tool_info_creates_design_blocks(self):
        """Tool information from mcp.json creates DESIGN type blocks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mcp_config = {
                "name": "test-power",
                "description": "Test power",
                "tools": [
                    {
                        "name": "test_tool",
                        "description": "A test tool",
                        "inputSchema": {"type": "object"},
                    }
                ],
            }
            create_power_directory(
                Path(tmpdir),
                "test-power",
                power_md_content="# Test Power\n\nTest power.",
                mcp_json_content=mcp_config,
            )

            adapter = PowerAdapter()
            blocks = adapter.load(tmpdir)

            # Should have tool block with DESIGN type
            tool_blocks = [b for b in blocks if b.type == SpecType.DESIGN and "tool" in b.tags]
            assert len(tool_blocks) >= 1
            assert "test_tool" in tool_blocks[0].text


class TestPowerUpdateConsistency:
    """**Feature: kiro-powers-integration, Property 7: Power Update Consistency**

    *For any* Power whose POWER.md content changes, rescanning SHALL produce
    SpecBlocks with updated content that differs from the previous scan.

    **Validates: Requirements 2.5**
    """

    def test_content_change_updates_specblocks(self):
        """When POWER.md changes, rescanning produces updated blocks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            power_dir = create_power_directory(
                Path(tmpdir),
                "test-power",
                power_md_content="# Test Power\n\nOriginal description.",
            )

            adapter = PowerAdapter()

            # First scan
            blocks1 = adapter.load(tmpdir)
            original_text = blocks1[0].text

            # Update POWER.md
            (power_dir / "POWER.md").write_text("# Test Power\n\nUpdated description.")

            # Second scan
            blocks2 = adapter.load(tmpdir)
            updated_text = blocks2[0].text

            # Content should be different
            assert original_text != updated_text
            assert "Updated" in updated_text

    @given(
        original_desc=description_strategy,
        updated_desc=description_strategy,
    )
    @settings(max_examples=10)
    def test_description_change_reflected_in_blocks(self, original_desc: str, updated_desc: str):
        """For any description change, blocks reflect the update."""
        # Skip if descriptions are the same
        if original_desc == updated_desc:
            return

        with tempfile.TemporaryDirectory() as tmpdir:
            power_dir = create_power_directory(
                Path(tmpdir),
                "test-power",
                power_md_content=f"# Test Power\n\n{original_desc}",
            )

            adapter = PowerAdapter()

            # First scan
            blocks1 = adapter.load(tmpdir)

            # Update
            (power_dir / "POWER.md").write_text(f"# Test Power\n\n{updated_desc}")

            # Second scan
            blocks2 = adapter.load(tmpdir)

            # Find pinned KNOWLEDGE blocks (overview)
            overview1 = next(b for b in blocks1 if b.type == SpecType.KNOWLEDGE and b.pinned)
            overview2 = next(b for b in blocks2 if b.type == SpecType.KNOWLEDGE and b.pinned)

            # Content should differ
            assert overview1.text != overview2.text


class TestAdapterName:
    """Tests for adapter name property."""

    def test_adapter_name_is_kiro_power(self):
        """Adapter name is 'KiroPower'."""
        adapter = PowerAdapter()
        assert adapter.name == "KiroPower"


class TestSpecBlockTypes:
    """Tests for correct SpecBlock type assignment."""

    def test_overview_is_knowledge_type(self):
        """Power overview blocks are KNOWLEDGE type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            create_power_directory(
                Path(tmpdir),
                "test-power",
                power_md_content="# Test Power\n\nTest description.",
            )

            adapter = PowerAdapter()
            blocks = adapter.load(tmpdir)

            # Find pinned KNOWLEDGE blocks
            overview_blocks = [b for b in blocks if b.type == SpecType.KNOWLEDGE and b.pinned]
            assert len(overview_blocks) >= 1

    def test_steering_is_task_type(self):
        """Steering file blocks are TASK type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            create_power_directory(
                Path(tmpdir),
                "test-power",
                power_md_content="# Test Power\n\nTest description.",
                steering_files={"guide.md": "# Guide\n\nHow to use."},
            )

            adapter = PowerAdapter()
            blocks = adapter.load(tmpdir)

            steering_blocks = [
                b for b in blocks if b.type == SpecType.TASK and "steering" in b.tags
            ]
            assert len(steering_blocks) >= 1

    def test_tool_is_design_type(self):
        """Tool blocks are DESIGN type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mcp_config = {
                "name": "test-power",
                "tools": [{"name": "test_tool", "description": "A tool"}],
            }
            create_power_directory(
                Path(tmpdir),
                "test-power",
                power_md_content="# Test Power\n\nTest description.",
                mcp_json_content=mcp_config,
            )

            adapter = PowerAdapter()
            blocks = adapter.load(tmpdir)

            tool_blocks = [b for b in blocks if b.type == SpecType.DESIGN and "tool" in b.tags]
            assert len(tool_blocks) >= 1


class TestPinnedStatus:
    """Tests for pinned status assignment."""

    def test_overview_is_pinned(self):
        """Power overview blocks are pinned."""
        with tempfile.TemporaryDirectory() as tmpdir:
            create_power_directory(
                Path(tmpdir),
                "test-power",
                power_md_content="# Test Power\n\nTest description.",
            )

            adapter = PowerAdapter()
            blocks = adapter.load(tmpdir)

            # Find KNOWLEDGE blocks that are pinned
            pinned_blocks = [b for b in blocks if b.type == SpecType.KNOWLEDGE and b.pinned]
            assert len(pinned_blocks) >= 1

    def test_steering_is_not_pinned(self):
        """Steering file blocks are not pinned."""
        with tempfile.TemporaryDirectory() as tmpdir:
            create_power_directory(
                Path(tmpdir),
                "test-power",
                power_md_content="# Test Power\n\nTest description.",
                steering_files={"guide.md": "# Guide\n\nHow to use."},
            )

            adapter = PowerAdapter()
            blocks = adapter.load(tmpdir)

            steering_blocks = [
                b for b in blocks if b.type == SpecType.TASK and "steering" in b.tags
            ]
            assert len(steering_blocks) >= 1
            assert steering_blocks[0].pinned is False


# =============================================================================
# Power Graph Integration Tests
# =============================================================================


class TestPowerGraphNodes:
    """**Feature: kiro-powers-integration, Property 8: Power Graph Nodes**

    *For any* set of installed Powers, building the SpecImpact graph SHALL
    create exactly one node of type POWER for each Power.

    **Validates: Requirements 3.1**
    """

    @given(power_names=st.lists(power_name_strategy, min_size=1, max_size=5, unique=True))
    @settings(max_examples=10)
    def test_power_nodes_created_for_each_power(self, power_names: list[str]):
        """For any set of Powers, one node is created per Power."""
        from specmem.impact.power_builder import PowerGraphBuilder

        with tempfile.TemporaryDirectory() as tmpdir:
            builder = PowerGraphBuilder(tmpdir)

            # Create PowerInfo objects
            powers = [
                PowerInfo(
                    name=name,
                    path=Path(tmpdir) / ".kiro" / "powers" / name,
                    description=f"Test power {name}",
                )
                for name in power_names
            ]

            nodes = builder.build_power_nodes(powers)

            # Should have exactly one node per Power
            assert len(nodes) == len(power_names)

            # Each node should have correct type
            from specmem.impact.graph_models import NodeType

            for node in nodes:
                assert node.type == NodeType.POWER

    def test_power_node_contains_metadata(self):
        """Power nodes contain expected metadata."""
        from specmem.impact.power_builder import PowerGraphBuilder

        with tempfile.TemporaryDirectory() as tmpdir:
            builder = PowerGraphBuilder(tmpdir)

            power = PowerInfo(
                name="test-power",
                path=Path(tmpdir) / ".kiro" / "powers" / "test-power",
                description="A test power",
                keywords=["test", "example"],
                tools=[ToolInfo(name="test_tool", description="A tool")],
                version="1.0.0",
            )

            nodes = builder.build_power_nodes([power])

            assert len(nodes) == 1
            node = nodes[0]

            assert node.id == "power:test-power"
            assert node.data["name"] == "test-power"
            assert node.data["description"] == "A test power"
            assert node.data["keywords"] == ["test", "example"]
            assert "test_tool" in node.data["tools"]
            assert node.data["version"] == "1.0.0"


class TestPowerCodeEdgeCreation:
    """**Feature: kiro-powers-integration, Property 9: Power-Code Edge Creation**

    *For any* Power steering file that contains file path patterns, the graph
    SHALL contain edges from the Power node to all matching code files.

    **Validates: Requirements 3.2**
    """

    def test_pattern_extraction_from_steering(self):
        """Patterns are extracted from steering file content."""
        from specmem.impact.power_builder import PowerGraphBuilder

        with tempfile.TemporaryDirectory() as tmpdir:
            builder = PowerGraphBuilder(tmpdir)

            content = """
# Guide

This applies to `*.py` files and `**/*.ts` files.
Also check `src/auth.py` for examples.
"""
            patterns = builder._extract_patterns_from_content(content)

            assert "*.py" in patterns
            assert "**/*.ts" in patterns

    def test_edges_created_for_matching_files(self):
        """Edges are created for files matching patterns."""
        from specmem.impact.graph_models import EdgeType
        from specmem.impact.power_builder import PowerGraphBuilder

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test files
            (tmppath / "test.py").write_text("# test")
            (tmppath / "other.js").write_text("// test")

            # Create steering file with pattern
            steering_dir = tmppath / ".kiro" / "powers" / "test-power" / "steering"
            steering_dir.mkdir(parents=True)
            (steering_dir / "guide.md").write_text("Use `*.py` files.")

            builder = PowerGraphBuilder(tmpdir)

            power = PowerInfo(
                name="test-power",
                path=tmppath / ".kiro" / "powers" / "test-power",
                description="Test",
                steering_files=[steering_dir / "guide.md"],
            )

            edges = builder.build_power_edges(
                power,
                code_files=[tmppath / "test.py", tmppath / "other.js"],
                specs=[],
            )

            # Should have edge to test.py but not other.js
            py_edges = [e for e in edges if "test.py" in e.target_id]
            js_edges = [e for e in edges if "other.js" in e.target_id]

            assert len(py_edges) == 1
            assert len(js_edges) == 0
            assert py_edges[0].relationship == EdgeType.PROVIDES


class TestPowerImpactQuery:
    """**Feature: kiro-powers-integration, Property 10: Power Impact Query**

    *For any* Power node in the graph, querying impact for that Power SHALL
    return all directly and transitively connected specs, code, and tests.

    **Validates: Requirements 3.4**
    """

    def test_power_removal_cleans_up_edges(self):
        """Removing a Power removes its nodes and edges."""
        from specmem.impact.graph_models import EdgeType, GraphEdge, GraphNode, NodeType
        from specmem.impact.power_builder import PowerGraphBuilder

        with tempfile.TemporaryDirectory() as tmpdir:
            builder = PowerGraphBuilder(tmpdir)

            # Create initial nodes and edges
            nodes = {
                "power:test-power": GraphNode(
                    id="power:test-power",
                    type=NodeType.POWER,
                    data={"name": "test-power"},
                ),
                "code:test.py": GraphNode(
                    id="code:test.py",
                    type=NodeType.CODE,
                    data={},
                ),
            }
            edges = [
                GraphEdge(
                    source_id="power:test-power",
                    target_id="code:test.py",
                    relationship=EdgeType.PROVIDES,
                ),
            ]

            # Remove the Power
            updated_nodes, updated_edges = builder.remove_power_nodes("test-power", nodes, edges)

            # Power node should be removed
            assert "power:test-power" not in updated_nodes
            # Code node should remain
            assert "code:test.py" in updated_nodes
            # Edge should be removed
            assert len(updated_edges) == 0
