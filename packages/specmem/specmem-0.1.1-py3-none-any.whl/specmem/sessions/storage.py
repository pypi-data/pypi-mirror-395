"""SQLite storage for session data.

Provides persistent storage for indexed sessions and session-spec links.
"""

import json
import sqlite3
import time
from pathlib import Path
from typing import Any

from specmem.sessions.models import (
    MessageRole,
    Session,
    SessionMessage,
    SessionSpecLink,
)


class SessionStorage:
    """SQLite-based storage for session data.

    Stores sessions, messages, and session-spec links in a local SQLite database.
    """

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        workspace_directory TEXT NOT NULL,
        date_created_ms INTEGER NOT NULL,
        message_count INTEGER NOT NULL,
        metadata_json TEXT,
        indexed_at_ms INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS session_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        message_index INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp_ms INTEGER,
        FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS session_spec_links (
        session_id TEXT NOT NULL,
        spec_id TEXT NOT NULL,
        confidence REAL NOT NULL,
        link_type TEXT NOT NULL,
        PRIMARY KEY (session_id, spec_id),
        FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_sessions_workspace ON sessions(workspace_directory);
    CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(date_created_ms);
    CREATE INDEX IF NOT EXISTS idx_messages_session ON session_messages(session_id);
    CREATE INDEX IF NOT EXISTS idx_links_spec ON session_spec_links(spec_id);
    """

    def __init__(self, db_path: Path):
        """Initialize the storage.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create database schema if it doesn't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(self.SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        """Create a database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def store_session(self, session: Session) -> None:
        """Store a session in the database.

        Args:
            session: Session to store.
        """
        with self._connect() as conn:
            # Insert or replace session
            conn.execute(
                """
                INSERT OR REPLACE INTO sessions
                (session_id, title, workspace_directory, date_created_ms,
                 message_count, metadata_json, indexed_at_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session.session_id,
                    session.title,
                    session.workspace_directory,
                    session.date_created_ms,
                    session.message_count,
                    json.dumps(session.metadata),
                    int(time.time() * 1000),
                ),
            )

            # Delete existing messages for this session
            conn.execute(
                "DELETE FROM session_messages WHERE session_id = ?",
                (session.session_id,),
            )

            # Insert messages
            for i, msg in enumerate(session.messages):
                conn.execute(
                    """
                    INSERT INTO session_messages
                    (session_id, message_index, role, content, timestamp_ms)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        session.session_id,
                        i,
                        msg.role.value,
                        msg.content,
                        msg.timestamp_ms,
                    ),
                )

            conn.commit()

    def get_session(self, session_id: str) -> Session | None:
        """Get a session by ID.

        Args:
            session_id: The session ID to retrieve.

        Returns:
            Session if found, None otherwise.
        """
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()

            if row is None:
                return None

            # Get messages
            messages = self._get_messages(conn, session_id)

            return Session(
                session_id=row["session_id"],
                title=row["title"],
                workspace_directory=row["workspace_directory"],
                date_created_ms=row["date_created_ms"],
                messages=messages,
                metadata=json.loads(row["metadata_json"] or "{}"),
            )

    def _get_messages(self, conn: sqlite3.Connection, session_id: str) -> list[SessionMessage]:
        """Get messages for a session."""
        rows = conn.execute(
            """
            SELECT * FROM session_messages
            WHERE session_id = ?
            ORDER BY message_index
            """,
            (session_id,),
        ).fetchall()

        return [
            SessionMessage(
                role=MessageRole(row["role"]),
                content=row["content"],
                timestamp_ms=row["timestamp_ms"],
            )
            for row in rows
        ]

    def list_sessions(
        self,
        workspace: str | None = None,
        since_ms: int | None = None,
        until_ms: int | None = None,
        limit: int = 100,
    ) -> list[Session]:
        """List sessions with optional filters.

        Args:
            workspace: Filter by workspace directory.
            since_ms: Only sessions created after this timestamp.
            until_ms: Only sessions created before this timestamp.
            limit: Maximum number of sessions to return.

        Returns:
            List of matching sessions.
        """
        query = "SELECT * FROM sessions WHERE 1=1"
        params: list[Any] = []

        if workspace:
            query += " AND workspace_directory = ?"
            params.append(workspace)

        if since_ms is not None:
            query += " AND date_created_ms >= ?"
            params.append(since_ms)

        if until_ms is not None:
            query += " AND date_created_ms <= ?"
            params.append(until_ms)

        query += " ORDER BY date_created_ms DESC LIMIT ?"
        params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

            sessions = []
            for row in rows:
                messages = self._get_messages(conn, row["session_id"])
                sessions.append(
                    Session(
                        session_id=row["session_id"],
                        title=row["title"],
                        workspace_directory=row["workspace_directory"],
                        date_created_ms=row["date_created_ms"],
                        messages=messages,
                        metadata=json.loads(row["metadata_json"] or "{}"),
                    )
                )

            return sessions

    def delete_session(self, session_id: str) -> bool:
        """Delete a session.

        Args:
            session_id: The session ID to delete.

        Returns:
            True if session was deleted, False if not found.
        """
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM sessions WHERE session_id = ?",
                (session_id,),
            )
            conn.commit()
            return cursor.rowcount > 0

    def store_spec_link(self, link: SessionSpecLink) -> None:
        """Store a session-spec link.

        Args:
            link: The link to store.
        """
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO session_spec_links
                (session_id, spec_id, confidence, link_type)
                VALUES (?, ?, ?, ?)
                """,
                (link.session_id, link.spec_id, link.confidence, link.link_type),
            )
            conn.commit()

    def get_sessions_for_spec(self, spec_id: str) -> list[str]:
        """Get session IDs linked to a spec.

        Args:
            spec_id: The spec ID to query.

        Returns:
            List of session IDs linked to the spec.
        """
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT session_id FROM session_spec_links WHERE spec_id = ?",
                (spec_id,),
            ).fetchall()
            return [row["session_id"] for row in rows]

    def get_specs_for_session(self, session_id: str) -> list[str]:
        """Get spec IDs linked to a session.

        Args:
            session_id: The session ID to query.

        Returns:
            List of spec IDs linked to the session.
        """
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT spec_id FROM session_spec_links WHERE session_id = ?",
                (session_id,),
            ).fetchall()
            return [row["spec_id"] for row in rows]

    def session_count(self) -> int:
        """Get total number of stored sessions."""
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) as count FROM sessions").fetchone()
            return row["count"]
