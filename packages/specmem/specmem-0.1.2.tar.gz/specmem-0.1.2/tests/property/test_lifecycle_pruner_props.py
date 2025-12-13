"""Property-based tests for spec lifecycle pruner.

**Feature: pragmatic-spec-lifecycle**
"""

import json
import tempfile
from datetime import datetime
from pathlib import Path

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from specmem.lifecycle.health import HealthAnalyzer
from specmem.lifecycle.models import ArchiveMetadata
from specmem.lifecycle.pruner import PrunerEngine


def create_test_spec(spec_dir: Path, spec_name: str, content: str = "# Test Spec") -> Path:
    """Create a test spec directory with content."""
    spec_path = spec_dir / spec_name
    spec_path.mkdir(parents=True, exist_ok=True)
    (spec_path / "requirements.md").write_text(content)
    return spec_path


class MockImpactGraph:
    """Mock impact graph for testing."""

    def __init__(self, orphans: set[str] | None = None):
        self.orphans = orphans or set()

    def get_code_for_spec(self, spec_id: str) -> list[str]:
        if spec_id in self.orphans:
            return []
        return ["some_file.py"]


class MockVectorStore:
    """Mock vector store for testing."""

    def __init__(self):
        self.deleted: list[str] = []

    def delete(self, spec_id: str) -> None:
        self.deleted.append(spec_id)


class TestArchivePreservationProperties:
    """Property tests for archive preservation."""

    @given(
        spec_name=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_"),
            min_size=1,
            max_size=20,
        ).filter(lambda x: x.strip() and not x.startswith(".")),
        content=st.text(min_size=1, max_size=500),
    )
    @settings(max_examples=50)
    def test_archive_preserves_content(
        self,
        spec_name: str,
        content: str,
    ) -> None:
        """**Feature: pragmatic-spec-lifecycle, Property 3: Archive Preservation**

        *For any* archived spec, the archive SHALL contain the original content,
        preserve the directory structure, and include valid metadata with
        archived_at timestamp and original_path.

        **Validates: Requirements 2.2**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_base = Path(tmpdir) / "specs"
            archive_dir = Path(tmpdir) / "archive"

            # Create spec
            spec_path = create_test_spec(spec_base, spec_name, content)
            original_content = (spec_path / "requirements.md").read_text()

            # Create analyzer and pruner
            analyzer = HealthAnalyzer(
                impact_graph=MockImpactGraph(orphans={spec_name}),
                spec_base_path=spec_base,
            )
            pruner = PrunerEngine(
                health_analyzer=analyzer,
                archive_dir=archive_dir,
            )

            # Archive the spec
            results = pruner.prune_by_name(
                spec_names=[spec_name],
                mode="archive",
                dry_run=False,
                force=True,
            )

            assert len(results) == 1
            result = results[0]

            # Verify archive was created
            assert result.action == "archived"
            assert result.archive_path is not None
            assert result.archive_path.exists()

            # Verify content is preserved
            archived_content = (result.archive_path / "requirements.md").read_text()
            assert archived_content == original_content

            # Verify metadata exists and is valid
            metadata_path = result.archive_path / ".archive_metadata.json"
            assert metadata_path.exists()

            metadata_dict = json.loads(metadata_path.read_text())
            metadata = ArchiveMetadata.from_dict(metadata_dict)

            assert metadata.original_path == str(spec_path)
            assert metadata.archived_at is not None
            assert isinstance(metadata.archived_at, datetime)
            assert metadata.can_restore is True

    @given(
        num_files=st.integers(min_value=1, max_value=5),
    )
    @settings(max_examples=20)
    def test_archive_preserves_directory_structure(
        self,
        num_files: int,
    ) -> None:
        """Archive should preserve all files in spec directory.

        **Validates: Requirements 2.2**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_base = Path(tmpdir) / "specs"
            archive_dir = Path(tmpdir) / "archive"
            spec_name = "test-spec"

            # Create spec with multiple files
            spec_path = spec_base / spec_name
            spec_path.mkdir(parents=True)

            files_created = []
            for i in range(num_files):
                file_path = spec_path / f"file_{i}.md"
                file_path.write_text(f"Content {i}")
                files_created.append(f"file_{i}.md")

            # Create analyzer and pruner
            analyzer = HealthAnalyzer(
                impact_graph=MockImpactGraph(orphans={spec_name}),
                spec_base_path=spec_base,
            )
            pruner = PrunerEngine(
                health_analyzer=analyzer,
                archive_dir=archive_dir,
            )

            # Archive
            results = pruner.prune_by_name(
                spec_names=[spec_name],
                mode="archive",
                dry_run=False,
                force=True,
            )

            result = results[0]
            assert result.action == "archived"

            # Verify all files are preserved
            for filename in files_created:
                archived_file = result.archive_path / filename
                assert archived_file.exists(), f"File {filename} not preserved"


class TestPruneIndexConsistencyProperties:
    """Property tests for prune index consistency."""

    @given(
        spec_names=st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_"),
                min_size=1,
                max_size=10,
            ).filter(lambda x: x.strip() and not x.startswith(".")),
            min_size=1,
            max_size=5,
            unique=True,
        ),
    )
    @settings(max_examples=30)
    def test_prune_removes_from_vector_store(
        self,
        spec_names: list[str],
    ) -> None:
        """**Feature: pragmatic-spec-lifecycle, Property 4: Prune Index Consistency**

        *For any* pruned spec (archived or deleted), the vector store SHALL no
        longer contain embeddings for that spec after the prune operation completes.

        **Validates: Requirements 2.4**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_base = Path(tmpdir) / "specs"
            archive_dir = Path(tmpdir) / "archive"

            # Create specs
            for name in spec_names:
                create_test_spec(spec_base, name)

            # Create mock vector store
            vector_store = MockVectorStore()

            # Create analyzer and pruner
            analyzer = HealthAnalyzer(
                impact_graph=MockImpactGraph(orphans=set(spec_names)),
                spec_base_path=spec_base,
            )
            pruner = PrunerEngine(
                health_analyzer=analyzer,
                vector_store=vector_store,
                archive_dir=archive_dir,
            )

            # Prune all specs
            results = pruner.prune_by_name(
                spec_names=spec_names,
                mode="archive",
                dry_run=False,
                force=True,
            )

            # Verify all pruned specs were removed from vector store
            for result in results:
                if result.action in ("archived", "deleted"):
                    assert result.spec_id in vector_store.deleted


class TestDryRunImmutabilityProperties:
    """Property tests for dry run immutability."""

    @given(
        spec_names=st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_"),
                min_size=1,
                max_size=10,
            ).filter(lambda x: x.strip() and not x.startswith(".")),
            min_size=1,
            max_size=3,
            unique=True,
        ),
    )
    @settings(max_examples=30)
    def test_dry_run_does_not_modify_files(
        self,
        spec_names: list[str],
    ) -> None:
        """**Feature: pragmatic-spec-lifecycle, Property 5: Dry Run Immutability**

        *For any* prune operation with dry_run=True, the file system and vector
        store SHALL remain unchanged after the operation.

        **Validates: Requirements 2.5**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_base = Path(tmpdir) / "specs"
            archive_dir = Path(tmpdir) / "archive"

            # Create specs and record original state
            original_files: dict[str, str] = {}
            for name in spec_names:
                spec_path = create_test_spec(spec_base, name, f"Content for {name}")
                original_files[name] = (spec_path / "requirements.md").read_text()

            # Create mock vector store
            vector_store = MockVectorStore()

            # Create analyzer and pruner
            analyzer = HealthAnalyzer(
                impact_graph=MockImpactGraph(orphans=set(spec_names)),
                spec_base_path=spec_base,
            )
            pruner = PrunerEngine(
                health_analyzer=analyzer,
                vector_store=vector_store,
                archive_dir=archive_dir,
            )

            # Dry run prune
            pruner.prune_by_name(
                spec_names=spec_names,
                mode="archive",
                dry_run=True,  # DRY RUN
                force=True,
            )

            # Verify files are unchanged
            for name, original_content in original_files.items():
                spec_path = spec_base / name / "requirements.md"
                assert spec_path.exists(), f"Spec {name} was deleted during dry run"
                assert spec_path.read_text() == original_content

            # Verify vector store was not modified
            assert len(vector_store.deleted) == 0

            # Verify archive was not created
            assert not archive_dir.exists() or not any(archive_dir.iterdir())


class TestExplicitPruneTargetingProperties:
    """Property tests for explicit prune targeting."""

    @given(
        all_specs=st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_"),
                min_size=1,
                max_size=10,
            ).filter(lambda x: x.strip() and not x.startswith(".")),
            min_size=2,
            max_size=5,
            unique=True,
        ),
        target_indices=st.lists(st.integers(min_value=0, max_value=4), min_size=1, max_size=3),
    )
    @settings(max_examples=30)
    def test_explicit_prune_only_affects_specified_specs(
        self,
        all_specs: list[str],
        target_indices: list[int],
    ) -> None:
        """**Feature: pragmatic-spec-lifecycle, Property 6: Explicit Prune Targeting**

        *For any* prune operation with explicit spec names, only the specified
        specs SHALL be affected and all other specs SHALL remain unchanged.

        **Validates: Requirements 2.6, 2.7**
        """
        # Filter valid indices
        valid_indices = [i for i in target_indices if i < len(all_specs)]
        assume(len(valid_indices) > 0)

        target_specs = [all_specs[i] for i in set(valid_indices)]
        non_target_specs = [s for s in all_specs if s not in target_specs]

        with tempfile.TemporaryDirectory() as tmpdir:
            spec_base = Path(tmpdir) / "specs"
            archive_dir = Path(tmpdir) / "archive"

            # Create all specs
            for name in all_specs:
                create_test_spec(spec_base, name, f"Content for {name}")

            # Create analyzer and pruner
            analyzer = HealthAnalyzer(
                impact_graph=MockImpactGraph(orphans=set(all_specs)),
                spec_base_path=spec_base,
            )
            pruner = PrunerEngine(
                health_analyzer=analyzer,
                archive_dir=archive_dir,
            )

            # Prune only target specs
            results = pruner.prune_by_name(
                spec_names=target_specs,
                mode="archive",
                dry_run=False,
                force=True,
            )

            # Verify only target specs were affected
            pruned_ids = {r.spec_id for r in results if r.action == "archived"}
            assert pruned_ids == set(target_specs)

            # Verify non-target specs still exist
            for name in non_target_specs:
                spec_path = spec_base / name
                assert spec_path.exists(), f"Non-target spec {name} was affected"
