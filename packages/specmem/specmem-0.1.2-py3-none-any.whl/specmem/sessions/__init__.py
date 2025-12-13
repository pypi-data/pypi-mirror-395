"""Kiro session search and indexing.

This module provides functionality for discovering, parsing, indexing,
and searching Kiro agent coding sessions.
"""

from specmem.sessions.config import SessionConfigManager
from specmem.sessions.discovery import DiscoveryResult, Platform, SessionDiscovery
from specmem.sessions.exceptions import (
    DiscoveryFailedError,
    InvalidSessionPathError,
    SessionError,
    SessionNotConfiguredError,
    SessionNotFoundError,
    SessionParseError,
)
from specmem.sessions.indexer import SessionIndexer
from specmem.sessions.linker import SpecLinker
from specmem.sessions.models import (
    MessageRole,
    SearchFilters,
    SearchResult,
    Session,
    SessionConfig,
    SessionMessage,
    SessionSpecLink,
    normalize_timestamp,
)
from specmem.sessions.parser import KiroSessionParser
from specmem.sessions.scanner import SessionScanner, decode_workspace_path, encode_workspace_path
from specmem.sessions.search import SessionSearchEngine
from specmem.sessions.storage import SessionStorage


__all__ = [
    "DiscoveryFailedError",
    "DiscoveryResult",
    "InvalidSessionPathError",
    # Parser
    "KiroSessionParser",
    "MessageRole",
    "Platform",
    "SearchFilters",
    "SearchResult",
    # Models
    "Session",
    "SessionConfig",
    # Config
    "SessionConfigManager",
    # Discovery
    "SessionDiscovery",
    # Exceptions
    "SessionError",
    "SessionIndexer",
    "SessionMessage",
    "SessionNotConfiguredError",
    "SessionNotFoundError",
    "SessionParseError",
    # Scanner
    "SessionScanner",
    # Search
    "SessionSearchEngine",
    "SessionSpecLink",
    # Storage & Indexing
    "SessionStorage",
    # Linker
    "SpecLinker",
    "decode_workspace_path",
    "encode_workspace_path",
    "normalize_timestamp",
]
