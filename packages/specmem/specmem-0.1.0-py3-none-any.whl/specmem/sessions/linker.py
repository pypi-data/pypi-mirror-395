"""Spec linker for session-spec relationships.

Detects and manages links between sessions and specifications.
"""

import re

from specmem.sessions.models import Session, SessionSpecLink
from specmem.sessions.storage import SessionStorage


class SpecLinker:
    """Links sessions to specifications.

    Detects spec file references in session content and creates
    bidirectional links between sessions and specs.
    """

    # Patterns for detecting spec references
    SPEC_PATTERNS = [
        # .kiro/specs/feature-name/
        r"\.kiro/specs/([a-zA-Z0-9_-]+)",
        # requirements.md, design.md, tasks.md
        r"(requirements|design|tasks)\.md",
        # Requirement references like "Requirement 1.2" or "REQ-001"
        r"[Rr]equirement\s+(\d+(?:\.\d+)?)",
        r"REQ-(\d+)",
        # Acceptance criteria references
        r"[Aa]cceptance\s+[Cc]riteria\s+(\d+(?:\.\d+)?)",
        r"AC-(\d+)",
    ]

    def __init__(self, storage: SessionStorage):
        """Initialize the linker.

        Args:
            storage: Session storage for persisting links.
        """
        self.storage = storage
        self._compiled_patterns = [re.compile(pattern) for pattern in self.SPEC_PATTERNS]

    def detect_spec_references(self, session: Session) -> list[str]:
        """Detect spec file references in session content.

        Args:
            session: Session to analyze.

        Returns:
            List of detected spec IDs.
        """
        spec_ids = set()

        # Search through all messages
        for msg in session.messages:
            content = msg.content

            # Check for .kiro/specs/ paths
            kiro_matches = re.findall(r"\.kiro/specs/([a-zA-Z0-9_-]+)", content)
            spec_ids.update(kiro_matches)

            # Check for spec file names with context
            if "requirements.md" in content or "design.md" in content or "tasks.md" in content:
                # Try to extract spec name from surrounding context
                spec_path_match = re.search(
                    r"([a-zA-Z0-9_-]+)/(requirements|design|tasks)\.md",
                    content,
                )
                if spec_path_match:
                    spec_ids.add(spec_path_match.group(1))

        return list(spec_ids)

    def create_links(self, session: Session) -> list[SessionSpecLink]:
        """Create links between session and detected specs.

        Args:
            session: Session to create links for.

        Returns:
            List of created SessionSpecLink objects.
        """
        spec_ids = self.detect_spec_references(session)
        links = []

        for spec_id in spec_ids:
            # Calculate confidence based on number of references
            reference_count = self._count_references(session, spec_id)
            confidence = min(1.0, 0.3 + reference_count * 0.1)

            link = SessionSpecLink(
                session_id=session.session_id,
                spec_id=spec_id,
                confidence=confidence,
                link_type="file_ref",
            )

            # Store the link
            self.storage.store_spec_link(link)
            links.append(link)

        return links

    def _count_references(self, session: Session, spec_id: str) -> int:
        """Count references to a spec in session content.

        Args:
            session: Session to search.
            spec_id: Spec ID to count references for.

        Returns:
            Number of references found.
        """
        count = 0
        for msg in session.messages:
            count += msg.content.lower().count(spec_id.lower())
        return count

    def get_sessions_for_spec(self, spec_id: str) -> list[Session]:
        """Get all sessions linked to a spec.

        Args:
            spec_id: The spec ID to query.

        Returns:
            List of sessions linked to the spec.
        """
        session_ids = self.storage.get_sessions_for_spec(spec_id)
        sessions = []

        for session_id in session_ids:
            session = self.storage.get_session(session_id)
            if session:
                sessions.append(session)

        return sessions

    def get_specs_for_session(self, session_id: str) -> list[str]:
        """Get all spec IDs linked to a session.

        Args:
            session_id: The session ID to query.

        Returns:
            List of spec IDs linked to the session.
        """
        return self.storage.get_specs_for_session(session_id)

    def create_manual_link(
        self,
        session_id: str,
        spec_id: str,
        confidence: float = 1.0,
    ) -> SessionSpecLink:
        """Create a manual link between session and spec.

        Args:
            session_id: Session ID to link.
            spec_id: Spec ID to link.
            confidence: Confidence score (default 1.0 for manual links).

        Returns:
            Created SessionSpecLink.
        """
        link = SessionSpecLink(
            session_id=session_id,
            spec_id=spec_id,
            confidence=confidence,
            link_type="manual",
        )
        self.storage.store_spec_link(link)
        return link
