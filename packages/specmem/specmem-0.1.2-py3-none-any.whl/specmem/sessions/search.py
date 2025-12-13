"""Session search engine.

Provides search functionality across indexed sessions.
"""

from pathlib import Path
from typing import Any

from specmem.sessions.exceptions import SessionNotFoundError
from specmem.sessions.models import (
    SearchFilters,
    SearchResult,
    Session,
)
from specmem.sessions.storage import SessionStorage


class SessionSearchEngine:
    """Searches indexed sessions.

    Provides semantic search, filtering, and result ranking for sessions.
    """

    def __init__(
        self,
        storage: SessionStorage,
        vector_store: Any | None = None,
    ):
        """Initialize the search engine.

        Args:
            storage: Session storage for retrieving sessions.
            vector_store: Optional vector store for semantic search.
        """
        self.storage = storage
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        filters: SearchFilters | None = None,
    ) -> list[SearchResult]:
        """Search sessions by query with optional filters.

        Args:
            query: Search query string.
            filters: Optional filters for workspace, time range, etc.

        Returns:
            List of SearchResult objects ordered by relevance.
        """
        filters = filters or SearchFilters()

        # Try semantic search first if vector store is available
        if self.vector_store is not None:
            results = self._semantic_search(query, filters)
            if results:
                return results

        # Fall back to text search
        return self._text_search(query, filters)

    def _semantic_search(
        self,
        query: str,
        filters: SearchFilters,
    ) -> list[SearchResult]:
        """Perform semantic search using vector store.

        Args:
            query: Search query.
            filters: Search filters.

        Returns:
            List of search results.
        """
        if self.vector_store is None:
            return []

        try:
            # Build metadata filter
            metadata_filter = {"type": "session_message"}
            if filters.workspace:
                metadata_filter["workspace"] = str(filters.workspace)

            # Search vector store
            results = self.vector_store.search(
                query=query,
                limit=filters.limit * 3,  # Get more to allow for deduplication
                metadata_filter=metadata_filter,
            )

            # Group results by session and build SearchResult objects
            session_scores: dict[str, tuple[float, list[int]]] = {}

            for result in results:
                session_id = result.get("metadata", {}).get("session_id")
                if not session_id:
                    continue

                score = result.get("score", 0.0)
                msg_index = result.get("metadata", {}).get("message_index", 0)

                if session_id not in session_scores:
                    session_scores[session_id] = (score, [msg_index])
                else:
                    existing_score, indices = session_scores[session_id]
                    # Keep highest score
                    new_score = max(existing_score, score)
                    indices.append(msg_index)
                    session_scores[session_id] = (new_score, indices)

            # Build search results
            search_results = []
            for session_id, (score, indices) in session_scores.items():
                session = self.storage.get_session(session_id)
                if session is None:
                    continue

                # Apply time filters
                if not self._passes_time_filter(session, filters):
                    continue

                search_results.append(
                    SearchResult(
                        session=session,
                        score=score,
                        matched_message_indices=sorted(set(indices)),
                    )
                )

            # Sort by score descending
            search_results.sort(key=lambda r: r.score, reverse=True)

            return search_results[: filters.limit]

        except Exception:
            return []

    def _text_search(
        self,
        query: str,
        filters: SearchFilters,
    ) -> list[SearchResult]:
        """Perform text-based search.

        Args:
            query: Search query.
            filters: Search filters.

        Returns:
            List of search results.
        """
        # Get all sessions matching filters
        sessions = self.storage.list_sessions(
            workspace=str(filters.workspace) if filters.workspace else None,
            since_ms=filters.since_ms,
            until_ms=filters.until_ms,
            limit=1000,  # Get more for text search
        )

        # Search through messages
        query_lower = query.lower()
        results = []

        for session in sessions:
            matched_indices = []
            max_score = 0.0

            for i, msg in enumerate(session.messages):
                content_lower = msg.content.lower()
                if query_lower in content_lower:
                    matched_indices.append(i)
                    # Simple scoring based on match position and frequency
                    count = content_lower.count(query_lower)
                    score = min(1.0, count * 0.2 + 0.3)
                    max_score = max(max_score, score)

            if matched_indices:
                results.append(
                    SearchResult(
                        session=session,
                        score=max_score,
                        matched_message_indices=matched_indices,
                    )
                )

        # Sort by score descending
        results.sort(key=lambda r: r.score, reverse=True)

        return results[: filters.limit]

    def _passes_time_filter(self, session: Session, filters: SearchFilters) -> bool:
        """Check if session passes time filters.

        Args:
            session: Session to check.
            filters: Filters with time constraints.

        Returns:
            True if session passes filters.
        """
        if filters.since_ms is not None:
            if session.date_created_ms < filters.since_ms:
                return False

        if filters.until_ms is not None:
            if session.date_created_ms > filters.until_ms:
                return False

        return True

    def list_recent(
        self,
        limit: int = 10,
        workspace: Path | None = None,
    ) -> list[Session]:
        """List recent sessions.

        Args:
            limit: Maximum number of sessions to return.
            workspace: Optional workspace filter.

        Returns:
            List of recent sessions.
        """
        return self.storage.list_sessions(
            workspace=str(workspace) if workspace else None,
            limit=limit,
        )

    def get_session(self, session_id: str) -> Session:
        """Get a specific session by ID.

        Args:
            session_id: The session ID to retrieve.

        Returns:
            The requested session.

        Raises:
            SessionNotFoundError: If session doesn't exist.
        """
        session = self.storage.get_session(session_id)
        if session is None:
            raise SessionNotFoundError(session_id)
        return session

    def filter_by_time(
        self,
        sessions: list[Session],
        since_ms: int | None = None,
        until_ms: int | None = None,
    ) -> list[Session]:
        """Filter sessions by time range.

        Args:
            sessions: Sessions to filter.
            since_ms: Only include sessions after this timestamp.
            until_ms: Only include sessions before this timestamp.

        Returns:
            Filtered sessions.
        """
        result = []
        for session in sessions:
            if since_ms is not None and session.date_created_ms < since_ms:
                continue
            if until_ms is not None and session.date_created_ms > until_ms:
                continue
            result.append(session)
        return result

    def sort_by_relevance(self, results: list[SearchResult]) -> list[SearchResult]:
        """Sort search results by relevance score descending.

        Args:
            results: Results to sort.

        Returns:
            Sorted results.
        """
        return sorted(results, key=lambda r: r.score, reverse=True)
