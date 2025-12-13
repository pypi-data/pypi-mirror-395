"""Session indexer for vector embeddings.

Indexes session messages for semantic search using the vector store.
"""

import contextlib
from typing import Any

from specmem.sessions.models import Session
from specmem.sessions.storage import SessionStorage


class SessionIndexer:
    """Indexes sessions for semantic search.

    Creates vector embeddings for session messages and stores them
    in the vector database for similarity search.
    """

    def __init__(
        self,
        storage: SessionStorage,
        vector_store: Any | None = None,
    ):
        """Initialize the indexer.

        Args:
            storage: Session storage for persisting session data.
            vector_store: Optional vector store for embeddings.
        """
        self.storage = storage
        self.vector_store = vector_store

    def index_session(self, session: Session) -> None:
        """Index a single session.

        Stores the session in SQLite and creates vector embeddings
        for semantic search.

        Args:
            session: Session to index.
        """
        # Store in SQLite
        self.storage.store_session(session)

        # Create vector embeddings if vector store is available
        if self.vector_store is not None:
            self._create_embeddings(session)

    def index_sessions(self, sessions: list[Session]) -> int:
        """Batch index multiple sessions.

        Args:
            sessions: List of sessions to index.

        Returns:
            Number of sessions indexed.
        """
        count = 0
        for session in sessions:
            try:
                self.index_session(session)
                count += 1
            except Exception:
                # Skip failed sessions
                continue
        return count

    def remove_session(self, session_id: str) -> None:
        """Remove session from index.

        Args:
            session_id: ID of session to remove.
        """
        self.storage.delete_session(session_id)

        # Remove from vector store if available
        if self.vector_store is not None:
            self._remove_embeddings(session_id)

    def _create_embeddings(self, session: Session) -> None:
        """Create vector embeddings for session messages.

        Args:
            session: Session to create embeddings for.
        """
        if self.vector_store is None:
            return

        # Create embeddings for each message
        for i, msg in enumerate(session.messages):
            doc_id = f"session_{session.session_id}_msg_{i}"
            metadata = {
                "type": "session_message",
                "session_id": session.session_id,
                "message_index": i,
                "role": msg.role.value,
                "workspace": session.workspace_directory,
                "date_created_ms": session.date_created_ms,
            }

            try:
                # Use vector store's add method
                self.vector_store.add(
                    doc_id=doc_id,
                    content=msg.content,
                    metadata=metadata,
                )
            except Exception:
                # Skip failed embeddings
                continue

    def _remove_embeddings(self, session_id: str) -> None:
        """Remove embeddings for a session.

        Args:
            session_id: ID of session to remove embeddings for.
        """
        if self.vector_store is None:
            return

        with contextlib.suppress(Exception):
            # Remove all message embeddings for this session
            self.vector_store.delete_by_metadata({"session_id": session_id})

    def reindex_all(self, sessions: list[Session]) -> int:
        """Reindex all sessions, replacing existing index.

        Args:
            sessions: List of all sessions to index.

        Returns:
            Number of sessions indexed.
        """
        # Clear existing session embeddings
        if self.vector_store is not None:
            with contextlib.suppress(Exception):
                self.vector_store.delete_by_metadata({"type": "session_message"})

        return self.index_sessions(sessions)
