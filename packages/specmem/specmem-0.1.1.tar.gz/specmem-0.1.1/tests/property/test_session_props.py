"""Property-based tests for Kiro session search.

Tests correctness properties defined in the design document using Hypothesis.
"""

import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from specmem.sessions.discovery import Platform, SessionDiscovery
from specmem.sessions.models import (
    MessageRole,
    SearchResult,
    Session,
    SessionMessage,
    normalize_timestamp,
)


# =============================================================================
# Property 15: Timestamp normalization correctness
# Validates: Requirements 6.4
# =============================================================================


@given(st.integers(min_value=0, max_value=int(1e15)))
def test_timestamp_normalization_from_milliseconds(ms_timestamp: int):
    """
    **Feature: kiro-session-search, Property 15: Timestamp normalization correctness**

    For any valid Unix milliseconds timestamp, normalization SHALL produce
    a positive integer representing Unix milliseconds.
    """
    # Large timestamps (>= 1e12) are treated as milliseconds
    if ms_timestamp >= 1e12:
        result = normalize_timestamp(ms_timestamp)
        assert result == ms_timestamp
        assert isinstance(result, int)
        assert result >= 0


@given(st.integers(min_value=0, max_value=int(1e9)))
def test_timestamp_normalization_from_seconds(sec_timestamp: int):
    """
    **Feature: kiro-session-search, Property 15: Timestamp normalization correctness**

    For any valid Unix seconds timestamp, normalization SHALL convert to milliseconds.
    """
    # Small timestamps (< 1e12) are treated as seconds
    result = normalize_timestamp(sec_timestamp)
    assert result == sec_timestamp * 1000
    assert isinstance(result, int)
    assert result >= 0


@given(st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False))
def test_timestamp_normalization_from_float_seconds(float_timestamp: float):
    """
    **Feature: kiro-session-search, Property 15: Timestamp normalization correctness**

    For any valid float seconds timestamp, normalization SHALL convert to milliseconds.
    """
    result = normalize_timestamp(float_timestamp)
    expected = int(float_timestamp * 1000)
    assert result == expected
    assert isinstance(result, int)


@given(
    st.datetimes(
        min_value=datetime(1970, 1, 1),
        max_value=datetime(2100, 1, 1),
        timezones=st.just(UTC),
    )
)
def test_timestamp_normalization_from_iso_string(dt: datetime):
    """
    **Feature: kiro-session-search, Property 15: Timestamp normalization correctness**

    For any valid ISO 8601 timestamp string, normalization SHALL produce
    a positive integer representing Unix milliseconds.
    """
    iso_string = dt.isoformat()
    result = normalize_timestamp(iso_string)

    # Result should be close to expected (within 1 second due to precision)
    expected = int(dt.timestamp() * 1000)
    assert abs(result - expected) < 1000
    assert isinstance(result, int)
    assert result >= 0


def test_timestamp_normalization_none():
    """Normalizing None returns None."""
    assert normalize_timestamp(None) is None


# =============================================================================
# Property 14: Role normalization correctness
# Validates: Requirements 6.2
# =============================================================================


@given(st.sampled_from(["user", "USER", "User", "human", "Human", "HUMAN"]))
def test_role_normalization_user_variants(role: str):
    """
    **Feature: kiro-session-search, Property 14: Role normalization correctness**

    For any user role variant, normalization SHALL map to MessageRole.USER.
    """
    result = SessionMessage.normalize_role(role)
    assert result == MessageRole.USER


@given(
    st.sampled_from(
        ["assistant", "ASSISTANT", "Assistant", "ai", "AI", "bot", "Bot", "agent", "Agent"]
    )
)
def test_role_normalization_assistant_variants(role: str):
    """
    **Feature: kiro-session-search, Property 14: Role normalization correctness**

    For any assistant role variant, normalization SHALL map to MessageRole.ASSISTANT.
    """
    result = SessionMessage.normalize_role(role)
    assert result == MessageRole.ASSISTANT


@given(st.sampled_from(["system", "SYSTEM", "System", "tool", "Tool", "TOOL"]))
def test_role_normalization_system_variants(role: str):
    """
    **Feature: kiro-session-search, Property 14: Role normalization correctness**

    For any system role variant, normalization SHALL map to MessageRole.SYSTEM.
    """
    result = SessionMessage.normalize_role(role)
    assert result == MessageRole.SYSTEM


@given(
    st.text(min_size=1).filter(
        lambda x: x.lower().strip()
        not in ["user", "human", "assistant", "ai", "bot", "agent", "system", "tool"]
    )
)
def test_role_normalization_unknown_raises(role: str):
    """
    **Feature: kiro-session-search, Property 14: Role normalization correctness**

    For any unknown role string, normalization SHALL raise ValueError.
    """
    with pytest.raises(ValueError, match="Unknown role"):
        SessionMessage.normalize_role(role)


# =============================================================================
# Property 1: Platform path correctness
# Validates: Requirements 0.1.1, 0.1.2, 0.1.3
# =============================================================================


def test_platform_paths_macos():
    """
    **Feature: kiro-session-search, Property 1: Platform path correctness**

    For macOS, auto-discovery SHALL check exactly the documented default paths.
    """
    discovery = SessionDiscovery()
    paths = discovery.get_platform_paths(Platform.MACOS)

    # Should check exactly one path on macOS
    assert len(paths) == 1

    # Path should contain the expected components
    path_str = str(paths[0])
    assert "Library" in path_str
    assert "Application Support" in path_str
    assert "Kiro" in path_str
    assert "workspace-sessions" in path_str


def test_platform_paths_linux():
    """
    **Feature: kiro-session-search, Property 1: Platform path correctness**

    For Linux, auto-discovery SHALL check exactly the documented default paths.
    """
    discovery = SessionDiscovery()
    paths = discovery.get_platform_paths(Platform.LINUX)

    # Should check two paths on Linux
    assert len(paths) == 2

    # First path should be .config
    assert ".config" in str(paths[0])
    assert "Kiro" in str(paths[0])
    assert "workspace-sessions" in str(paths[0])

    # Second path should be .local/share
    assert ".local/share" in str(paths[1])
    assert "Kiro" in str(paths[1])
    assert "workspace-sessions" in str(paths[1])


def test_platform_paths_windows():
    """
    **Feature: kiro-session-search, Property 1: Platform path correctness**

    For Windows, auto-discovery SHALL check exactly the documented default paths.
    """
    discovery = SessionDiscovery()
    paths = discovery.get_platform_paths(Platform.WINDOWS)

    # Should check exactly one path on Windows
    assert len(paths) == 1

    # Path should contain Kiro and workspace-sessions
    path_str = str(paths[0])
    assert "Kiro" in path_str
    assert "workspace-sessions" in path_str


@given(st.sampled_from([Platform.MACOS, Platform.LINUX, Platform.WINDOWS]))
def test_platform_paths_all_contain_kiro(platform: Platform):
    """
    **Feature: kiro-session-search, Property 1: Platform path correctness**

    For any platform, all returned paths SHALL contain 'Kiro' and 'workspace-sessions'.
    """
    discovery = SessionDiscovery()
    paths = discovery.get_platform_paths(platform)

    assert len(paths) > 0
    for path in paths:
        path_str = str(path)
        assert "Kiro" in path_str
        assert "workspace-sessions" in path_str


# =============================================================================
# Property 2: Directory validation correctness
# Validates: Requirements 0.1.5, 0.8
# =============================================================================


def test_directory_validation_empty_dir():
    """
    **Feature: kiro-session-search, Property 2: Directory validation correctness**

    An empty directory SHALL NOT be considered valid.
    """
    discovery = SessionDiscovery()

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        assert discovery.validate_directory(path) is False


def test_directory_validation_nonexistent():
    """
    **Feature: kiro-session-search, Property 2: Directory validation correctness**

    A nonexistent path SHALL NOT be considered valid.
    """
    discovery = SessionDiscovery()
    path = Path("/nonexistent/path/that/does/not/exist")
    assert discovery.validate_directory(path) is False


def test_directory_validation_valid_structure():
    """
    **Feature: kiro-session-search, Property 2: Directory validation correctness**

    A directory with subdirectories containing JSON files SHALL be valid.
    """
    discovery = SessionDiscovery()

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)

        # Create a workspace subdirectory with a session JSON file
        workspace_dir = path / "workspace_abc123"
        workspace_dir.mkdir()

        session_file = workspace_dir / "session_001.json"
        session_file.write_text(json.dumps({"sessionId": "001"}))

        assert discovery.validate_directory(path) is True


def test_directory_validation_no_json_files():
    """
    **Feature: kiro-session-search, Property 2: Directory validation correctness**

    A directory with subdirectories but no JSON files SHALL NOT be valid.
    """
    discovery = SessionDiscovery()

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)

        # Create a workspace subdirectory without JSON files
        workspace_dir = path / "workspace_abc123"
        workspace_dir.mkdir()

        # Create a non-JSON file
        other_file = workspace_dir / "readme.txt"
        other_file.write_text("Not a session file")

        assert discovery.validate_directory(path) is False


@given(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=("L", "N"))))
def test_directory_validation_with_random_workspace_names(workspace_name: str):
    """
    **Feature: kiro-session-search, Property 2: Directory validation correctness**

    For any workspace directory name, validation SHALL return True if and only if
    the directory contains at least one JSON file.
    """
    discovery = SessionDiscovery()

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)

        # Create workspace directory with random name
        workspace_dir = path / workspace_name
        workspace_dir.mkdir()

        # Without JSON file - should be invalid
        assert discovery.validate_directory(path) is False

        # Add JSON file - should become valid
        session_file = workspace_dir / "session.json"
        session_file.write_text("{}")

        assert discovery.validate_directory(path) is True


# =============================================================================
# Property 6: Session metadata extraction completeness
# Validates: Requirements 1.3
# =============================================================================


from specmem.sessions.parser import KiroSessionParser


@given(
    st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=("L", "N"))),
    st.text(min_size=1, max_size=50),
    st.text(min_size=1, max_size=100),
)
def test_session_metadata_extraction(session_id: str, title: str, workspace: str):
    """
    **Feature: kiro-session-search, Property 6: Session metadata extraction completeness**

    For any valid sessions.json file, parsing SHALL extract all required fields
    (sessionId, title, dateCreated, workspaceDirectory) for every session entry.
    """
    parser = KiroSessionParser()

    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = Path(tmpdir) / "sessions.json"

        # Create sessions.json with test data
        sessions_data = {
            "sessions": [
                {
                    "sessionId": session_id,
                    "title": title,
                    "dateCreated": "2025-01-15T10:30:00Z",
                    "workspaceDirectory": workspace,
                }
            ]
        }
        index_path.write_text(json.dumps(sessions_data))

        # Parse and verify
        result = parser.parse_sessions_index(index_path)

        assert len(result) == 1
        assert result[0]["sessionId"] == session_id
        assert result[0]["title"] == title
        assert result[0]["workspaceDirectory"] == workspace
        assert "dateCreated" in result[0]


# =============================================================================
# Property 7: Message history completeness
# Validates: Requirements 1.4, 3.1, 3.2
# =============================================================================


@given(
    st.lists(
        st.tuples(
            st.sampled_from(["user", "assistant"]),
            st.text(min_size=1, max_size=100),
        ),
        min_size=1,
        max_size=10,
    )
)
def test_message_history_completeness(messages: list[tuple[str, str]]):
    """
    **Feature: kiro-session-search, Property 7: Message history completeness**

    For any valid session JSON file, parsing SHALL preserve all messages
    in order with their roles intact.
    """
    parser = KiroSessionParser()

    with tempfile.TemporaryDirectory() as tmpdir:
        session_path = Path(tmpdir) / "session.json"

        # Create session with messages
        history = [{"role": role, "content": content} for role, content in messages]

        session_data = {
            "sessionId": "test_session",
            "title": "Test Session",
            "workspaceDirectory": "/test",
            "dateCreated": "2025-01-15T10:30:00Z",
            "history": history,
        }
        session_path.write_text(json.dumps(session_data))

        # Parse and verify
        session = parser.parse_session_file(session_path)

        # All messages should be preserved
        assert len(session.messages) == len(messages)

        # Order and roles should be preserved
        for i, (expected_role, expected_content) in enumerate(messages):
            assert session.messages[i].role.value == expected_role
            assert session.messages[i].content == expected_content


# =============================================================================
# Property 8: Content flattening produces readable text
# Validates: Requirements 3.3, 3.4, 6.3
# =============================================================================


def test_content_flattening_plain_string():
    """
    **Feature: kiro-session-search, Property 8: Content flattening produces readable text**

    Plain string content SHALL be returned unchanged.
    """
    parser = KiroSessionParser()

    content = "Hello, this is a test message."
    result = parser.flatten_content(content)

    assert result == content


def test_content_flattening_text_array():
    """
    **Feature: kiro-session-search, Property 8: Content flattening produces readable text**

    Text arrays SHALL be flattened to readable text.
    """
    parser = KiroSessionParser()

    content = [
        {"type": "text", "text": "First part."},
        {"type": "text", "text": "Second part."},
    ]
    result = parser.flatten_content(content)

    assert "First part." in result
    assert "Second part." in result


def test_content_flattening_tool_use():
    """
    **Feature: kiro-session-search, Property 8: Content flattening produces readable text**

    Tool use items SHALL include tool name in flattened output.
    """
    parser = KiroSessionParser()

    content = [
        {"type": "text", "text": "Let me read that file."},
        {"type": "tool_use", "name": "readFile", "input": {"path": "test.py"}},
    ]
    result = parser.flatten_content(content)

    assert "Let me read that file." in result
    assert "readFile" in result


@given(st.text(min_size=1, max_size=200))
def test_content_flattening_always_produces_string(text: str):
    """
    **Feature: kiro-session-search, Property 8: Content flattening produces readable text**

    For any content, flattening SHALL produce a string.
    """
    parser = KiroSessionParser()

    # Test with plain string
    result = parser.flatten_content(text)
    assert isinstance(result, str)

    # Test with array
    result = parser.flatten_content([{"type": "text", "text": text}])
    assert isinstance(result, str)
    assert text in result


# =============================================================================
# Property 5: Base64 workspace path round-trip
# Validates: Requirements 1.2
# =============================================================================


from specmem.sessions.scanner import decode_workspace_path, encode_workspace_path


@given(st.text(min_size=1, max_size=200))
def test_workspace_path_roundtrip(path: str):
    """
    **Feature: kiro-session-search, Property 5: Base64 workspace path round-trip**

    For any workspace path, encoding to base64 then decoding SHALL produce
    the original path.
    """
    encoded = encode_workspace_path(path)
    decoded = decode_workspace_path(encoded)

    assert decoded == path


@given(
    st.text(
        min_size=1, max_size=200, alphabet=st.characters(whitelist_categories=("L", "N", "P", "S"))
    )
)
def test_workspace_path_roundtrip_special_chars(path: str):
    """
    **Feature: kiro-session-search, Property 5: Base64 workspace path round-trip**

    For any workspace path with special characters, round-trip SHALL preserve the path.
    """
    encoded = encode_workspace_path(path)
    decoded = decode_workspace_path(encoded)

    assert decoded == path


def test_workspace_path_roundtrip_real_paths():
    """
    **Feature: kiro-session-search, Property 5: Base64 workspace path round-trip**

    Real-world workspace paths SHALL round-trip correctly.
    """
    test_paths = [
        "/Users/dev/projects/myapp",
        "/home/user/code/project",
        "C:\\Users\\Dev\\Projects\\App",
        "/Users/dev/My Project (2025)",
        "/path/with spaces/and-dashes",
    ]

    for path in test_paths:
        encoded = encode_workspace_path(path)
        decoded = decode_workspace_path(encoded)
        assert decoded == path, f"Failed for path: {path}"


# =============================================================================
# Property 12: Workspace filter correctness
# Validates: Requirements 2.5, 7.2
# =============================================================================


from specmem.sessions.models import SessionConfig
from specmem.sessions.scanner import SessionScanner


def test_workspace_filter_correctness():
    """
    **Feature: kiro-session-search, Property 12: Workspace filter correctness**

    For any workspace filter, all returned sessions SHALL have workspaceDirectory
    matching the filter path.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        sessions_path = Path(tmpdir)

        # Create two workspace directories
        workspace1 = "/Users/dev/project1"
        workspace2 = "/Users/dev/project2"

        ws1_dir = sessions_path / encode_workspace_path(workspace1)
        ws2_dir = sessions_path / encode_workspace_path(workspace2)
        ws1_dir.mkdir()
        ws2_dir.mkdir()

        # Create sessions in each workspace
        session1 = {
            "sessionId": "session1",
            "title": "Session 1",
            "workspaceDirectory": workspace1,
            "dateCreated": "2025-01-15T10:00:00Z",
            "history": [{"role": "user", "content": "Hello"}],
        }
        session2 = {
            "sessionId": "session2",
            "title": "Session 2",
            "workspaceDirectory": workspace2,
            "dateCreated": "2025-01-15T11:00:00Z",
            "history": [{"role": "user", "content": "Hi"}],
        }

        (ws1_dir / "session1.json").write_text(json.dumps(session1))
        (ws2_dir / "session2.json").write_text(json.dumps(session2))

        # Create scanner
        config = SessionConfig(sessions_path=sessions_path, enabled=True)
        scanner = SessionScanner(config)

        # Scan all sessions
        all_sessions = scanner.scan()
        assert len(all_sessions) == 2

        # Filter by workspace1
        filtered = scanner.filter_by_workspace(all_sessions, Path(workspace1))
        assert len(filtered) == 1
        assert filtered[0].workspace_directory == workspace1

        # Filter by workspace2
        filtered = scanner.filter_by_workspace(all_sessions, Path(workspace2))
        assert len(filtered) == 1
        assert filtered[0].workspace_directory == workspace2


# =============================================================================
# Property 4: Configured path restriction
# Validates: Requirements 0.9, 1.1
# =============================================================================


def test_configured_path_restriction():
    """
    **Feature: kiro-session-search, Property 4: Configured path restriction**

    For any session operation, the system SHALL only access files within
    the configured sessions directory path.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        sessions_path = Path(tmpdir) / "sessions"
        sessions_path.mkdir()

        # Create a workspace directory with a session
        workspace = "/Users/dev/project"
        ws_dir = sessions_path / encode_workspace_path(workspace)
        ws_dir.mkdir()

        session_data = {
            "sessionId": "test_session",
            "title": "Test",
            "workspaceDirectory": workspace,
            "dateCreated": "2025-01-15T10:00:00Z",
            "history": [{"role": "user", "content": "Hello"}],
        }
        (ws_dir / "test_session.json").write_text(json.dumps(session_data))

        # Create scanner with configured path
        config = SessionConfig(sessions_path=sessions_path, enabled=True)
        scanner = SessionScanner(config)

        # Scanner should only access the configured path
        sessions = scanner.scan()

        # Verify we found the session
        assert len(sessions) == 1
        assert sessions[0].session_id == "test_session"

        # Verify the session file is within the configured path
        assert sessions[0].session_path is not None
        assert (
            str(sessions[0].session_path).startswith(str(sessions_path))
            if sessions[0].session_path
            else True
        )


def test_scanner_rejects_unconfigured_path():
    """
    **Feature: kiro-session-search, Property 4: Configured path restriction**

    Scanner SHALL raise error if sessions_path is not configured.
    """
    from specmem.sessions.exceptions import InvalidSessionPathError

    config = SessionConfig(sessions_path=None, enabled=False)

    with pytest.raises(InvalidSessionPathError):
        SessionScanner(config)


# =============================================================================
# Property 10: Search results are ordered by relevance
# Validates: Requirements 2.3
# =============================================================================


from specmem.sessions.search import SessionSearchEngine
from specmem.sessions.storage import SessionStorage


@given(st.lists(st.floats(min_value=0.0, max_value=1.0, allow_nan=False), min_size=2, max_size=10))
def test_search_results_ordered_by_relevance(scores: list[float]):
    """
    **Feature: kiro-session-search, Property 10: Search results are ordered by relevance**

    For any search query returning multiple results, results SHALL be ordered
    by descending relevance score.
    """
    # Create mock search results with given scores
    results = []
    for i, score in enumerate(scores):
        session = Session(
            session_id=f"session_{i}",
            title=f"Session {i}",
            workspace_directory="/test",
            date_created_ms=1000000 + i,
            messages=[],
        )
        results.append(SearchResult(session=session, score=score))

    # Create search engine with temp storage
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = SessionStorage(Path(tmpdir) / "sessions.db")
        engine = SessionSearchEngine(storage)

        # Sort results
        sorted_results = engine.sort_by_relevance(results)

        # Verify descending order
        for i in range(len(sorted_results) - 1):
            assert sorted_results[i].score >= sorted_results[i + 1].score


# =============================================================================
# Property 11: Time filter correctness
# Validates: Requirements 2.4
# =============================================================================


@given(
    st.integers(min_value=1000000, max_value=2000000),
    st.integers(min_value=2000000, max_value=3000000),
    st.lists(st.integers(min_value=500000, max_value=3500000), min_size=1, max_size=10),
)
def test_time_filter_correctness(since_ms: int, until_ms: int, dates: list[int]):
    """
    **Feature: kiro-session-search, Property 11: Time filter correctness**

    For any time filter (since/until), all returned sessions SHALL have
    dateCreated within the specified range.
    """
    # Create sessions with given dates
    sessions = []
    for i, date_ms in enumerate(dates):
        sessions.append(
            Session(
                session_id=f"session_{i}",
                title=f"Session {i}",
                workspace_directory="/test",
                date_created_ms=date_ms,
                messages=[],
            )
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        storage = SessionStorage(Path(tmpdir) / "sessions.db")
        engine = SessionSearchEngine(storage)

        # Filter sessions
        filtered = engine.filter_by_time(sessions, since_ms=since_ms, until_ms=until_ms)

        # Verify all filtered sessions are within range
        for session in filtered:
            assert session.date_created_ms >= since_ms
            assert session.date_created_ms <= until_ms


# =============================================================================
# Property 9: Search results contain required metadata
# Validates: Requirements 2.2
# =============================================================================


def test_search_results_contain_required_metadata():
    """
    **Feature: kiro-session-search, Property 9: Search results contain required metadata**

    For any search result, the result SHALL include session title, workspace
    directory, and date created.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = SessionStorage(Path(tmpdir) / "sessions.db")

        # Create and store a session
        session = Session(
            session_id="test_session",
            title="Test Session Title",
            workspace_directory="/Users/dev/project",
            date_created_ms=1705312200000,
            messages=[
                SessionMessage(
                    role=MessageRole.USER,
                    content="Hello, this is a test message about authentication.",
                )
            ],
        )
        storage.store_session(session)

        # Create search engine and search
        engine = SessionSearchEngine(storage)
        results = engine.search("authentication")

        # Verify results contain required metadata
        assert len(results) >= 1
        result = results[0]

        # Required metadata must be present
        assert result.session.title == "Test Session Title"
        assert result.session.workspace_directory == "/Users/dev/project"
        assert result.session.date_created_ms == 1705312200000

        # Score must be present
        assert isinstance(result.score, float)
        assert 0.0 <= result.score <= 1.0


# =============================================================================
# Property 13: Bidirectional spec linking
# Validates: Requirements 4.2, 4.3, 4.4
# =============================================================================


from specmem.sessions.linker import SpecLinker


def test_bidirectional_spec_linking():
    """
    **Feature: kiro-session-search, Property 13: Bidirectional spec linking**

    For any session-spec link, querying sessions for that spec SHALL include
    the session, AND querying specs for that session SHALL include the spec.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = SessionStorage(Path(tmpdir) / "sessions.db")
        linker = SpecLinker(storage)

        # Create a session that references a spec
        session = Session(
            session_id="test_session",
            title="Test Session",
            workspace_directory="/test",
            date_created_ms=1705312200000,
            messages=[
                SessionMessage(
                    role=MessageRole.USER,
                    content="Let's work on the .kiro/specs/user-auth/requirements.md file.",
                ),
                SessionMessage(
                    role=MessageRole.ASSISTANT,
                    content="I'll help you with the user-auth spec.",
                ),
            ],
        )

        # Store session first
        storage.store_session(session)

        # Create links
        links = linker.create_links(session)

        # Should have detected the user-auth spec
        assert len(links) >= 1
        spec_ids = [link.spec_id for link in links]
        assert "user-auth" in spec_ids

        # Bidirectional check: sessions for spec
        sessions_for_spec = linker.get_sessions_for_spec("user-auth")
        session_ids = [s.session_id for s in sessions_for_spec]
        assert "test_session" in session_ids

        # Bidirectional check: specs for session
        specs_for_session = linker.get_specs_for_session("test_session")
        assert "user-auth" in specs_for_session


def test_manual_link_bidirectional():
    """
    **Feature: kiro-session-search, Property 13: Bidirectional spec linking**

    Manual links SHALL also be bidirectional.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = SessionStorage(Path(tmpdir) / "sessions.db")
        linker = SpecLinker(storage)

        # Create and store a session
        session = Session(
            session_id="manual_session",
            title="Manual Link Test",
            workspace_directory="/test",
            date_created_ms=1705312200000,
            messages=[],
        )
        storage.store_session(session)

        # Create manual link
        link = linker.create_manual_link("manual_session", "custom-spec")

        assert link.link_type == "manual"
        assert link.confidence == 1.0

        # Verify bidirectional
        sessions = linker.get_sessions_for_spec("custom-spec")
        assert any(s.session_id == "manual_session" for s in sessions)

        specs = linker.get_specs_for_session("manual_session")
        assert "custom-spec" in specs


# =============================================================================
# Property 16: Workspace-only mode isolation
# Validates: Requirements 7.1, 7.3
# =============================================================================


def test_workspace_only_mode_isolation():
    """
    **Feature: kiro-session-search, Property 16: Workspace-only mode isolation**

    For any session search in workspace-only mode, no sessions from other
    workspaces SHALL be returned or accessed.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        sessions_path = Path(tmpdir) / "sessions"
        sessions_path.mkdir()

        # Create sessions for two different workspaces
        workspace1 = "/Users/dev/project1"
        workspace2 = "/Users/dev/project2"

        ws1_dir = sessions_path / encode_workspace_path(workspace1)
        ws2_dir = sessions_path / encode_workspace_path(workspace2)
        ws1_dir.mkdir()
        ws2_dir.mkdir()

        # Session in workspace1
        session1 = {
            "sessionId": "session_ws1",
            "title": "Session in Project 1",
            "workspaceDirectory": workspace1,
            "dateCreated": "2025-01-15T10:00:00Z",
            "history": [{"role": "user", "content": "Working on project 1"}],
        }
        (ws1_dir / "session_ws1.json").write_text(json.dumps(session1))

        # Session in workspace2
        session2 = {
            "sessionId": "session_ws2",
            "title": "Session in Project 2",
            "workspaceDirectory": workspace2,
            "dateCreated": "2025-01-15T11:00:00Z",
            "history": [{"role": "user", "content": "Working on project 2"}],
        }
        (ws2_dir / "session_ws2.json").write_text(json.dumps(session2))

        # Create scanner with workspace-only config
        config = SessionConfig(
            sessions_path=sessions_path,
            workspace_only=True,
            enabled=True,
        )
        scanner = SessionScanner(config)

        # Scan with workspace1 filter
        sessions = scanner.scan(workspace_filter=Path(workspace1))

        # Should only return session from workspace1
        assert len(sessions) == 1
        assert sessions[0].session_id == "session_ws1"
        assert sessions[0].workspace_directory == workspace1

        # Verify no sessions from workspace2 are returned
        session_ids = [s.session_id for s in sessions]
        assert "session_ws2" not in session_ids


def test_workspace_only_excludes_other_workspaces():
    """
    **Feature: kiro-session-search, Property 16: Workspace-only mode isolation**

    When filtering by workspace, sessions from other workspaces SHALL NOT be included.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = SessionStorage(Path(tmpdir) / "sessions.db")

        # Store sessions from different workspaces
        session1 = Session(
            session_id="session_a",
            title="Session A",
            workspace_directory="/workspace/a",
            date_created_ms=1705312200000,
            messages=[SessionMessage(role=MessageRole.USER, content="Test A")],
        )
        session2 = Session(
            session_id="session_b",
            title="Session B",
            workspace_directory="/workspace/b",
            date_created_ms=1705312300000,
            messages=[SessionMessage(role=MessageRole.USER, content="Test B")],
        )

        storage.store_session(session1)
        storage.store_session(session2)

        # Query with workspace filter
        filtered = storage.list_sessions(workspace="/workspace/a")

        # Should only return session from workspace A
        assert len(filtered) == 1
        assert filtered[0].session_id == "session_a"

        # Verify workspace B session is not included
        assert all(s.workspace_directory == "/workspace/a" for s in filtered)
