"""Compressor engine for condensing verbose specs."""

import re
from pathlib import Path

from specmem.lifecycle.models import CompressedSpec


class CompressorEngine:
    """Engine for compressing verbose specs.

    Compresses specs by:
    - Removing verbose descriptions while preserving acceptance criteria
    - Generating concise summaries
    - Storing both original and compressed versions
    """

    def __init__(
        self,
        max_summary_tokens: int = 500,
        preserve_acceptance_criteria: bool = True,
        verbose_threshold_chars: int = 5000,
        compression_storage_dir: Path | None = None,
    ) -> None:
        """Initialize the compressor engine.

        Args:
            max_summary_tokens: Maximum tokens in compressed summary
            preserve_acceptance_criteria: Whether to preserve all acceptance criteria
            verbose_threshold_chars: Character count above which a spec is verbose
            compression_storage_dir: Directory to store compressed versions
        """
        self.max_summary_tokens = max_summary_tokens
        self.preserve_acceptance_criteria = preserve_acceptance_criteria
        self.verbose_threshold_chars = verbose_threshold_chars
        self.compression_storage_dir = compression_storage_dir or Path(".specmem/compressed")
        self._compressed_cache: dict[str, CompressedSpec] = {}

    def compress_spec(
        self,
        spec_id: str,
        spec_path: Path,
        content: str | None = None,
    ) -> CompressedSpec:
        """Compress a single spec.

        Args:
            spec_id: Unique identifier for the spec
            spec_path: Path to the spec file or directory
            content: Optional content (if not provided, reads from path)

        Returns:
            CompressedSpec with compressed content
        """
        spec_path = Path(spec_path)

        # Read content if not provided
        if content is None:
            content = self._read_spec_content(spec_path)

        original_size = len(content.encode("utf-8"))

        # Extract acceptance criteria
        criteria = self._extract_acceptance_criteria(content)

        # Generate compressed content
        compressed_content = self._compress_content(content, criteria)
        compressed_size = len(compressed_content.encode("utf-8"))

        # Calculate compression ratio
        compression_ratio = compressed_size / original_size if original_size > 0 else 1.0

        result = CompressedSpec(
            spec_id=spec_id,
            original_path=spec_path,
            original_size=original_size,
            compressed_content=compressed_content,
            compressed_size=compressed_size,
            compression_ratio=compression_ratio,
            preserved_criteria=criteria,
        )

        # Cache the result
        self._compressed_cache[spec_id] = result

        return result

    def compress_all(
        self,
        specs: list[tuple[str, Path]],
        threshold_ratio: float = 0.5,
    ) -> list[CompressedSpec]:
        """Compress all specs that exceed the verbose threshold.

        Args:
            specs: List of (spec_id, spec_path) tuples
            threshold_ratio: Only compress if ratio would be below this

        Returns:
            List of CompressedSpec for compressed specs
        """
        results: list[CompressedSpec] = []

        for spec_id, spec_path in specs:
            content = self._read_spec_content(spec_path)

            # Only compress if verbose
            if len(content) > self.verbose_threshold_chars:
                compressed = self.compress_spec(spec_id, spec_path, content)

                # Only keep if compression is effective
                if compressed.compression_ratio <= threshold_ratio:
                    results.append(compressed)

        return results

    def get_verbose_specs(
        self,
        specs: list[tuple[str, Path]],
        threshold_chars: int | None = None,
    ) -> list[str]:
        """Get list of specs that exceed the verbose threshold.

        Args:
            specs: List of (spec_id, spec_path) tuples
            threshold_chars: Character threshold (defaults to verbose_threshold_chars)

        Returns:
            List of spec IDs that are verbose
        """
        threshold = threshold_chars or self.verbose_threshold_chars
        verbose_specs: list[str] = []

        for spec_id, spec_path in specs:
            content = self._read_spec_content(spec_path)
            if len(content) > threshold:
                verbose_specs.append(spec_id)

        return verbose_specs

    def get_compressed(self, spec_id: str) -> CompressedSpec | None:
        """Get cached compressed version of a spec.

        Args:
            spec_id: The spec ID to look up

        Returns:
            CompressedSpec if cached, None otherwise
        """
        return self._compressed_cache.get(spec_id)

    def get_original(self, spec_id: str) -> str | None:
        """Get original content for a compressed spec.

        Args:
            spec_id: The spec ID to look up

        Returns:
            Original content if available, None otherwise
        """
        compressed = self._compressed_cache.get(spec_id)
        if compressed:
            return self._read_spec_content(compressed.original_path)
        return None

    def is_verbose(self, spec_id: str, spec_path: Path) -> bool:
        """Check if a spec is considered verbose.

        Args:
            spec_id: The spec ID
            spec_path: Path to the spec

        Returns:
            True if spec exceeds verbose threshold
        """
        content = self._read_spec_content(spec_path)
        return len(content) > self.verbose_threshold_chars

    def save_compressed(self, compressed: CompressedSpec) -> Path:
        """Save compressed version to storage.

        Args:
            compressed: The compressed spec to save

        Returns:
            Path where compressed version was saved
        """
        self.compression_storage_dir.mkdir(parents=True, exist_ok=True)

        output_path = self.compression_storage_dir / f"{compressed.spec_id}_compressed.md"
        output_path.write_text(compressed.compressed_content)

        return output_path

    def _read_spec_content(self, spec_path: Path) -> str:
        """Read content from a spec path."""
        spec_path = Path(spec_path)

        if spec_path.is_file():
            return spec_path.read_text()
        elif spec_path.is_dir():
            # Read all markdown files in directory
            content_parts = []
            for md_file in sorted(spec_path.glob("*.md")):
                content_parts.append(md_file.read_text())
            return "\n\n".join(content_parts)

        return ""

    def _extract_acceptance_criteria(self, content: str) -> list[str]:
        """Extract acceptance criteria from spec content."""
        criteria: list[str] = []

        # Look for numbered criteria (1. WHEN..., 2. WHEN..., etc.)
        pattern = r"^\d+\.\s*(WHEN|IF|WHERE|WHILE|THE)\s+.+$"
        for line in content.split("\n"):
            line = line.strip()
            if re.match(pattern, line, re.IGNORECASE):
                criteria.append(line)

        # Also look for bullet point criteria
        bullet_pattern = r"^[-*]\s*(WHEN|IF|WHERE|WHILE|THE)\s+.+$"
        for line in content.split("\n"):
            line = line.strip()
            if re.match(bullet_pattern, line, re.IGNORECASE):
                criteria.append(line)

        return criteria

    def _compress_content(self, content: str, criteria: list[str]) -> str:
        """Generate compressed version of content."""
        lines = []

        # Extract title
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            lines.append(f"# {title_match.group(1)}")
            lines.append("")

        # Add compression marker
        lines.append("<!-- compressed: true -->")
        lines.append("")

        # Extract introduction/summary (first paragraph after title)
        intro_match = re.search(
            r"##\s*Introduction\s*\n+(.+?)(?=\n##|\Z)", content, re.DOTALL | re.IGNORECASE
        )
        if intro_match:
            intro = intro_match.group(1).strip()
            # Truncate if too long
            if len(intro) > 500:
                intro = intro[:497] + "..."
            lines.append("## Summary")
            lines.append("")
            lines.append(intro)
            lines.append("")

        # Add preserved acceptance criteria
        if criteria and self.preserve_acceptance_criteria:
            lines.append("## Acceptance Criteria")
            lines.append("")
            for i, criterion in enumerate(criteria, 1):
                # Remove existing numbering and re-number
                clean = re.sub(r"^\d+\.\s*", "", criterion)
                clean = re.sub(r"^[-*]\s*", "", clean)
                lines.append(f"{i}. {clean}")
            lines.append("")

        # Extract any glossary terms
        glossary_match = re.search(
            r"##\s*Glossary\s*\n+(.+?)(?=\n##|\Z)", content, re.DOTALL | re.IGNORECASE
        )
        if glossary_match:
            glossary = glossary_match.group(1).strip()
            # Only include if not too long
            if len(glossary) < 500:
                lines.append("## Key Terms")
                lines.append("")
                lines.append(glossary)
                lines.append("")

        return "\n".join(lines)
