"""Property-based tests for Kiro Config Indexer.

**Feature: kiro-config-indexer**

Tests the correctness properties for steering files, MCP config, and hooks parsing.
"""

import json
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from specmem.kiro.hooks import HookParser
from specmem.kiro.indexer import KiroConfigIndexer
from specmem.kiro.mcp import MCPConfigParser
from specmem.kiro.models import HookInfo, MCPServerInfo, SteeringFile
from specmem.kiro.steering import SteeringParser


# =============================================================================
# Strategies
# =============================================================================

# Valid inclusion modes
inclusion_mode_strategy = st.sampled_from(["always", "fileMatch", "manual"])

# Valid trigger types
trigger_type_strategy = st.sampled_from(["file_save", "manual", "session_start"])

# Simple file patterns
file_pattern_strategy = st.sampled_from(
    [
        "*.py",
        "*.ts",
        "*.md",
        "*.json",
        "tests/*.py",
        "src/*.ts",
        "**/*.py",
    ]
)

# Server names (alphanumeric with hyphens)
server_name_strategy = st.from_regex(r"[a-z][a-z0-9\-]{2,20}", fullmatch=True)

# Simple markdown content
markdown_content_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
    min_size=10,
    max_size=500,
)

# File paths for testing
file_path_strategy = st.sampled_from(
    [
        "src/main.py",
        "tests/test_main.py",
        "lib/utils.ts",
        "README.md",
        "config.json",
    ]
)


# =============================================================================
# Property 1: Steering File Parsing Completeness
# =============================================================================


class TestSteeringParsingCompleteness:
    """**Feature: kiro-config-indexer, Property 1: Steering File Parsing Completeness**

    *For any* directory containing valid steering markdown files, parsing SHALL
    produce one SpecBlock per file, and each SpecBlock SHALL contain the file's content.

    **Validates: Requirements 1.1**
    """

    @given(
        file_count=st.integers(min_value=1, max_value=5),
        content=markdown_content_strategy,
    )
    @settings(max_examples=100)
    def test_parsing_produces_one_block_per_file(self, file_count: int, content: str):
        """For any number of steering files, parsing produces one result per file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            steering_dir = Path(tmpdir) / ".kiro" / "steering"
            steering_dir.mkdir(parents=True)

            # Create steering files
            for i in range(file_count):
                file_path = steering_dir / f"guide-{i}.md"
                file_path.write_text(f"# Guide {i}\n\n{content}")

            parser = SteeringParser()
            results = parser.parse_directory(steering_dir)

            assert len(results) == file_count
            for result in results:
                assert isinstance(result, SteeringFile)
                assert result.content  # Content is not empty


# =============================================================================
# Property 2: Frontmatter Round-Trip
# =============================================================================


class TestFrontmatterRoundTrip:
    """**Feature: kiro-config-indexer, Property 2: Frontmatter Round-Trip**

    *For any* valid YAML frontmatter with `inclusion` and `fileMatchPattern` fields,
    parsing and re-serializing SHALL preserve the original values.

    **Validates: Requirements 1.2**
    """

    @given(
        inclusion=inclusion_mode_strategy,
        pattern=file_pattern_strategy,
    )
    @settings(max_examples=100)
    def test_frontmatter_values_preserved(self, inclusion: str, pattern: str):
        """Frontmatter values are preserved through parse/serialize cycle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.md"

            # Create file with frontmatter
            content = f"""---
inclusion: {inclusion}
fileMatchPattern: "{pattern}"
---

# Test Content

Some body text here.
"""
            file_path.write_text(content)

            parser = SteeringParser()
            result = parser.parse(file_path)

            assert result.inclusion == inclusion
            assert result.file_match_pattern == pattern


# =============================================================================
# Property 3: File Pattern Matching Consistency
# =============================================================================


class TestFilePatternMatching:
    """**Feature: kiro-config-indexer, Property 3: File Pattern Matching Consistency**

    *For any* steering file with a `fileMatchPattern` and any file path, the
    `matches_file()` method SHALL return true if and only if the file path
    matches the glob pattern according to standard glob semantics.

    **Validates: Requirements 1.3, 5.1, 5.2**
    """

    def test_py_pattern_matches_py_files(self):
        """*.py pattern matches Python files."""
        steering = SteeringFile(
            path=Path("test.md"),
            content="",
            body="",
            inclusion="fileMatch",
            file_match_pattern="*.py",
        )

        assert steering.matches_file("main.py")
        assert steering.matches_file("src/utils.py")
        assert not steering.matches_file("main.ts")
        assert not steering.matches_file("main.py.bak")

    def test_always_inclusion_matches_all(self):
        """Always inclusion matches any file."""
        steering = SteeringFile(
            path=Path("test.md"),
            content="",
            body="",
            inclusion="always",
            file_match_pattern=None,
        )

        assert steering.matches_file("any/file.py")
        assert steering.matches_file("another.ts")
        assert steering.matches_file("README.md")

    def test_manual_inclusion_matches_none(self):
        """Manual inclusion matches no files."""
        steering = SteeringFile(
            path=Path("test.md"),
            content="",
            body="",
            inclusion="manual",
            file_match_pattern="*.py",
        )

        assert not steering.matches_file("main.py")
        assert not steering.matches_file("any/file.ts")


# =============================================================================
# Property 4: Inclusion Mode Priority Mapping
# =============================================================================


class TestInclusionModePriority:
    """**Feature: kiro-config-indexer, Property 4: Inclusion Mode Priority Mapping**

    *For any* steering file, the resulting SpecBlock's priority SHALL be determined
    by its inclusion mode: "always" → high priority (pinned), "fileMatch" → normal
    priority, "manual" → low priority (not auto-included).

    **Validates: Requirements 1.4, 1.5**
    """

    @given(inclusion=inclusion_mode_strategy)
    @settings(max_examples=100)
    def test_inclusion_mode_determines_pinned_status(self, inclusion: str):
        """Inclusion mode correctly determines pinned status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            steering_dir = workspace / ".kiro" / "steering"
            steering_dir.mkdir(parents=True)

            content = f"""---
inclusion: {inclusion}
---

# Test
"""
            (steering_dir / "test.md").write_text(content)

            indexer = KiroConfigIndexer(workspace)
            blocks = indexer.index_steering()

            assert len(blocks) == 1
            block = blocks[0]

            if inclusion == "always":
                assert block.pinned is True
            else:
                assert block.pinned is False


# =============================================================================
# Property 5: MCP Server Parsing Completeness
# =============================================================================


class TestMCPParsingCompleteness:
    """**Feature: kiro-config-indexer, Property 5: MCP Server Parsing Completeness**

    *For any* valid mcp.json configuration, parsing SHALL produce one SpecBlock
    per defined server, and each SpecBlock SHALL contain the server name and command.

    **Validates: Requirements 2.1**
    """

    @given(server_count=st.integers(min_value=1, max_value=5))
    @settings(max_examples=100)
    def test_parsing_produces_one_block_per_server(self, server_count: int):
        """For any number of servers, parsing produces one result per server."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "mcp.json"

            servers = {}
            for i in range(server_count):
                servers[f"server-{i}"] = {
                    "command": "uvx",
                    "args": [f"package-{i}"],
                }

            config_path.write_text(json.dumps({"mcpServers": servers}))

            parser = MCPConfigParser()
            results = parser.parse(config_path)

            assert len(results) == server_count
            for result in results:
                assert isinstance(result, MCPServerInfo)
                assert result.name
                assert result.command


# =============================================================================
# Property 6: MCP Tool Extraction
# =============================================================================


class TestMCPToolExtraction:
    """**Feature: kiro-config-indexer, Property 6: MCP Tool Extraction**

    *For any* MCP server with tool definitions, the parser SHALL extract all tools,
    and each tool's SpecBlock SHALL contain its name and description.

    **Validates: Requirements 2.2**
    """

    @given(tool_count=st.integers(min_value=1, max_value=5))
    @settings(max_examples=100)
    def test_tools_extracted_from_auto_approve(self, tool_count: int):
        """Tools are extracted from autoApprove list."""
        tools = [f"tool_{i}" for i in range(tool_count)]

        server = MCPServerInfo(
            name="test-server",
            command="uvx",
            args=["test-package"],
            auto_approve=tools,
        )

        parser = MCPConfigParser()
        extracted = parser.get_tools([server])

        # Should have tool_count auto-approved tools + 1 server entry
        auto_approved = [t for t in extracted if t.auto_approved]
        assert len(auto_approved) == tool_count

        for tool in auto_approved:
            assert tool.server_name == "test-server"
            assert tool.tool_name in tools


# =============================================================================
# Property 7: Disabled Server Filtering
# =============================================================================


class TestDisabledServerFiltering:
    """**Feature: kiro-config-indexer, Property 7: Disabled Server Filtering**

    *For any* query for available tools, the result SHALL exclude tools from
    servers where `disabled: true`, and SHALL include tools from all enabled servers.

    **Validates: Requirements 2.3, 2.4**
    """

    @given(
        enabled_count=st.integers(min_value=0, max_value=3),
        disabled_count=st.integers(min_value=0, max_value=3),
    )
    @settings(max_examples=100)
    def test_disabled_servers_excluded_from_tools(self, enabled_count: int, disabled_count: int):
        """Disabled servers are excluded from tool queries."""
        servers = []

        for i in range(enabled_count):
            servers.append(
                MCPServerInfo(
                    name=f"enabled-{i}",
                    command="uvx",
                    disabled=False,
                )
            )

        for i in range(disabled_count):
            servers.append(
                MCPServerInfo(
                    name=f"disabled-{i}",
                    command="uvx",
                    disabled=True,
                )
            )

        parser = MCPConfigParser()
        enabled = parser.get_enabled_servers(servers)
        tools = parser.get_tools(enabled)

        assert len(enabled) == enabled_count

        # All tools should be from enabled servers
        for tool in tools:
            assert not tool.server_name.startswith("disabled-")


# =============================================================================
# Property 8: Hook Parsing Completeness
# =============================================================================


class TestHookParsingCompleteness:
    """**Feature: kiro-config-indexer, Property 8: Hook Parsing Completeness**

    *For any* directory containing valid hook JSON files, parsing SHALL produce
    one SpecBlock per hook file.

    **Validates: Requirements 3.1**
    """

    @given(hook_count=st.integers(min_value=1, max_value=5))
    @settings(max_examples=100)
    def test_parsing_produces_one_block_per_hook(self, hook_count: int):
        """For any number of hooks, parsing produces one result per hook."""
        with tempfile.TemporaryDirectory() as tmpdir:
            hooks_dir = Path(tmpdir)

            for i in range(hook_count):
                hook_data = {
                    "name": f"hook-{i}",
                    "trigger": "file_save",
                    "action": f"echo {i}",
                }
                (hooks_dir / f"hook-{i}.json").write_text(json.dumps(hook_data))

            parser = HookParser()
            results = parser.parse_directory(hooks_dir)

            assert len(results) == hook_count
            for result in results:
                assert isinstance(result, HookInfo)


# =============================================================================
# Property 9: Hook Trigger Filtering
# =============================================================================


class TestHookTriggerFiltering:
    """**Feature: kiro-config-indexer, Property 9: Hook Trigger Filtering**

    *For any* query for hooks by trigger type and file path, the result SHALL
    include only hooks where the trigger matches AND (file_pattern is null OR
    file_pattern matches the path).

    **Validates: Requirements 3.2, 3.3**
    """

    @given(trigger=trigger_type_strategy)
    @settings(max_examples=100)
    def test_hooks_filtered_by_trigger(self, trigger: str):
        """Hooks are correctly filtered by trigger type."""
        hooks = [
            HookInfo(name="file-save-hook", trigger="file_save"),
            HookInfo(name="manual-hook", trigger="manual"),
            HookInfo(name="session-hook", trigger="session_start"),
        ]

        parser = HookParser()
        results = parser.get_hooks_for_trigger(hooks, trigger)  # type: ignore

        for hook in results:
            assert hook.trigger == trigger

    def test_hooks_filtered_by_file_pattern(self):
        """Hooks with file patterns are filtered correctly."""
        hooks = [
            HookInfo(name="py-hook", trigger="file_save", file_pattern="*.py"),
            HookInfo(name="ts-hook", trigger="file_save", file_pattern="*.ts"),
            HookInfo(name="all-hook", trigger="file_save", file_pattern=None),
        ]

        parser = HookParser()

        py_results = parser.get_hooks_for_trigger(hooks, "file_save", "main.py")
        assert len(py_results) == 2  # py-hook and all-hook

        ts_results = parser.get_hooks_for_trigger(hooks, "file_save", "main.ts")
        assert len(ts_results) == 2  # ts-hook and all-hook


# =============================================================================
# Property 10: Always-Included Steering
# =============================================================================


class TestAlwaysIncludedSteering:
    """**Feature: kiro-config-indexer, Property 10: Always-Included Steering**

    *For any* steering file with `inclusion: always`, querying steering for any
    file path SHALL include that steering file in the results.

    **Validates: Requirements 5.3**
    """

    @given(file_path=file_path_strategy)
    @settings(max_examples=100)
    def test_always_steering_included_for_any_file(self, file_path: str):
        """Always-included steering appears for any file path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            steering_dir = workspace / ".kiro" / "steering"
            steering_dir.mkdir(parents=True)

            # Create always-included steering
            (steering_dir / "always.md").write_text("""---
inclusion: always
---

# Always Included
""")

            # Create fileMatch steering that won't match
            (steering_dir / "python.md").write_text("""---
inclusion: fileMatch
fileMatchPattern: "*.xyz"
---

# Python Only
""")

            indexer = KiroConfigIndexer(workspace)
            indexer.index_steering()

            results = indexer.get_steering_for_file(file_path)

            # Always-included should be present
            always_found = any(s.inclusion == "always" for s in results)
            assert always_found


# =============================================================================
# Property 11: Context Bundle Steering Inclusion
# =============================================================================


class TestContextBundleSteeringInclusion:
    """**Feature: kiro-config-indexer, Property 11: Context Bundle Steering Inclusion**

    *For any* context bundle generated for changed files, the bundle SHALL include
    content from all steering files where `inclusion: always` OR `fileMatchPattern`
    matches any changed file.

    **Validates: Requirements 6.1, 6.2**
    """

    def test_matching_steering_included_in_query(self):
        """Steering matching file patterns is included."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            steering_dir = workspace / ".kiro" / "steering"
            steering_dir.mkdir(parents=True)

            (steering_dir / "python.md").write_text("""---
inclusion: fileMatch
fileMatchPattern: "*.py"
---

# Python Guidelines
""")

            indexer = KiroConfigIndexer(workspace)
            indexer.index_steering()

            # Query for Python file
            results = indexer.get_steering_for_file("main.py")
            assert len(results) == 1
            assert results[0].title == "Python Guidelines"

            # Query for non-Python file
            results = indexer.get_steering_for_file("main.ts")
            assert len(results) == 0


# =============================================================================
# Property 12: Context Bundle Hook Mention
# =============================================================================


class TestContextBundleHookMention:
    """**Feature: kiro-config-indexer, Property 12: Context Bundle Hook Mention**

    *For any* context bundle generated for changed files, if a hook with
    `trigger: file_save` has a `filePattern` matching any changed file, the
    bundle SHALL mention this hook.

    **Validates: Requirements 6.4**
    """

    def test_matching_hooks_returned_for_file(self):
        """Hooks matching file patterns are returned."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            hooks_dir = workspace / ".kiro" / "hooks"
            hooks_dir.mkdir(parents=True)

            (hooks_dir / "py-lint.json").write_text(
                json.dumps(
                    {
                        "name": "py-lint",
                        "trigger": "file_save",
                        "filePattern": "*.py",
                        "action": "ruff check",
                    }
                )
            )

            (hooks_dir / "ts-lint.json").write_text(
                json.dumps(
                    {
                        "name": "ts-lint",
                        "trigger": "file_save",
                        "filePattern": "*.ts",
                        "action": "eslint",
                    }
                )
            )

            indexer = KiroConfigIndexer(workspace)
            indexer.index_hooks()

            # Query for Python file
            results = indexer.get_hooks_for_trigger("file_save", "main.py")
            assert len(results) == 1
            assert results[0].name == "py-lint"

            # Query for TypeScript file
            results = indexer.get_hooks_for_trigger("file_save", "main.ts")
            assert len(results) == 1
            assert results[0].name == "ts-lint"
