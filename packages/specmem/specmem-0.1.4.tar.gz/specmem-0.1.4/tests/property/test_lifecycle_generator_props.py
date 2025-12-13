"""Property-based tests for spec lifecycle generator.

**Feature: pragmatic-spec-lifecycle**
"""

import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from specmem.lifecycle.generator import GeneratorEngine
from specmem.lifecycle.models import GeneratedSpec


def create_python_file(dir_path: Path, name: str, content: str) -> Path:
    """Create a Python file with given content."""
    file_path = dir_path / f"{name}.py"
    file_path.write_text(content)
    return file_path


class TestGeneratedSpecValidityProperties:
    """Property tests for generated spec validity."""

    @given(
        func_name=st.text(
            alphabet=st.characters(whitelist_categories=("L",), whitelist_characters="_"),
            min_size=1,
            max_size=20,
        ).filter(lambda x: x.isidentifier() and not x.startswith("_")),
        docstring=st.text(min_size=1, max_size=100).filter(lambda x: '"' not in x and "'" not in x),
    )
    @settings(max_examples=50)
    def test_generated_spec_is_valid_markdown(
        self,
        func_name: str,
        docstring: str,
    ) -> None:
        """**Feature: pragmatic-spec-lifecycle, Property 7: Generated Spec Validity**

        *For any* code file, the generated spec SHALL be valid markdown,
        contain the auto-generated marker in metadata, and conform to the
        configured adapter format.

        **Validates: Requirements 3.1, 3.3, 3.4**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            code_dir = Path(tmpdir) / "code"
            code_dir.mkdir()

            # Create a Python file with a function
            code_content = f'''
def {func_name}():
    """{docstring}"""
    pass
'''
            file_path = create_python_file(code_dir, "module", code_content)

            # Generate spec
            generator = GeneratorEngine(
                default_format="kiro",
                output_dir=Path(tmpdir) / "specs",
            )

            spec = generator.generate_from_file(file_path)

            # Verify it's a GeneratedSpec
            assert isinstance(spec, GeneratedSpec)

            # Verify content is valid markdown (has headers)
            assert spec.content.startswith("#")
            assert "## " in spec.content or "### " in spec.content

            # Verify auto-generated marker is present
            assert (
                "auto-generated" in spec.content.lower()
                or spec.metadata.get("auto_generated") is True
            )

            # Verify adapter format matches
            assert spec.adapter_format == "kiro"

            # Verify metadata contains auto_generated flag
            assert spec.metadata.get("auto_generated") is True
            assert "generated_at" in spec.metadata

    @given(
        class_name=st.from_regex(r"[A-Z][a-z]{2,14}", fullmatch=True),
        method_names=st.lists(
            st.from_regex(r"[a-z][a-z_]{2,14}", fullmatch=True).filter(
                lambda x: x
                not in {
                    "if",
                    "in",
                    "is",
                    "or",
                    "and",
                    "not",
                    "for",
                    "try",
                    "def",
                    "del",
                    "elif",
                    "else",
                    "from",
                    "pass",
                    "with",
                    "as",
                    "class",
                    "break",
                    "while",
                    "yield",
                    "raise",
                    "return",
                    "import",
                    "except",
                    "finally",
                    "continue",
                    "global",
                    "lambda",
                    "assert",
                    "nonlocal",
                }
            ),
            min_size=1,
            max_size=3,
            unique=True,
        ),
    )
    @settings(max_examples=30)
    def test_generated_spec_contains_class_info(
        self,
        class_name: str,
        method_names: list[str],
    ) -> None:
        """Generated spec should contain information about classes.

        **Validates: Requirements 3.1, 3.2**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            code_dir = Path(tmpdir) / "code"
            code_dir.mkdir()

            # Create a Python file with a class
            methods_code = "\n".join(
                [f"    def {name}(self):\n        pass" for name in method_names]
            )
            code_content = f'''
class {class_name}:
    """A test class."""
{methods_code}
'''
            file_path = create_python_file(code_dir, "module", code_content)

            # Generate spec
            generator = GeneratorEngine(output_dir=Path(tmpdir) / "specs")
            spec = generator.generate_from_file(file_path)

            # Verify class name appears in spec
            assert class_name in spec.content

            # Verify at least some methods appear
            methods_found = sum(1 for m in method_names if m in spec.content)
            assert methods_found > 0 or "Acceptance Criteria" in spec.content

    def test_generated_spec_has_requirements_structure(self) -> None:
        """Generated spec should have proper Kiro requirements structure.

        **Validates: Requirements 3.3**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            code_dir = Path(tmpdir) / "code"
            code_dir.mkdir()

            code_content = '''
"""Module for user authentication."""

class AuthService:
    """Handles user authentication."""

    def login(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        pass

    def logout(self) -> None:
        """Log out the current user."""
        pass
'''
            file_path = create_python_file(code_dir, "auth", code_content)

            generator = GeneratorEngine(output_dir=Path(tmpdir) / "specs")
            spec = generator.generate_from_file(file_path)

            # Verify Kiro structure
            assert "# Requirements Document" in spec.content
            assert "## Introduction" in spec.content
            assert "## Glossary" in spec.content
            assert "## Requirements" in spec.content
            assert "**User Story:**" in spec.content
            assert "#### Acceptance Criteria" in spec.content

    @given(
        num_files=st.integers(min_value=1, max_value=3),
    )
    @settings(max_examples=20)
    def test_generate_from_directory_groups_files(
        self,
        num_files: int,
    ) -> None:
        """Directory generation should group files correctly.

        **Validates: Requirements 3.5**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            code_dir = Path(tmpdir) / "code" / "mymodule"
            code_dir.mkdir(parents=True)

            # Create multiple Python files
            for i in range(num_files):
                code_content = f'''
def function_{i}():
    """Function {i} docstring."""
    pass
'''
                create_python_file(code_dir, f"file_{i}", code_content)

            generator = GeneratorEngine(output_dir=Path(tmpdir) / "specs")
            specs = generator.generate_from_directory(
                code_dir,
                group_by="directory",
            )

            # Should produce one spec for the directory
            assert len(specs) == 1

            # Spec should reference multiple source files
            assert len(specs[0].source_files) == num_files

    def test_metadata_extraction_from_python(self) -> None:
        """Metadata extraction should capture functions and classes.

        **Validates: Requirements 3.2**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            code_dir = Path(tmpdir)

            code_content = '''
"""Module docstring."""

import os
from pathlib import Path

def my_function(arg1: str, arg2: int) -> bool:
    """Function docstring."""
    return True

class MyClass:
    """Class docstring."""

    def method(self) -> None:
        """Method docstring."""
        pass
'''
            file_path = create_python_file(code_dir, "module", code_content)

            generator = GeneratorEngine()
            metadata = generator.extract_metadata(file_path)

            # Verify module docstring
            assert metadata["module_docstring"] == "Module docstring."

            # Verify function extraction
            assert len(metadata["functions"]) >= 1
            func = next(f for f in metadata["functions"] if f["name"] == "my_function")
            assert func["docstring"] == "Function docstring."
            assert "arg1" in func["args"]
            assert func["returns"] == "bool"

            # Verify class extraction
            assert len(metadata["classes"]) >= 1
            cls = next(c for c in metadata["classes"] if c["name"] == "MyClass")
            assert cls["docstring"] == "Class docstring."
            assert len(cls["methods"]) >= 1
