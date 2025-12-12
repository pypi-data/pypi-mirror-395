"""Generator engine for creating specs from code."""

import ast
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from specmem.lifecycle.models import GeneratedSpec


class GeneratorEngine:
    """Engine for generating specs from existing code.

    Analyzes code files to extract:
    - Function signatures and docstrings
    - Class definitions and methods
    - Module-level comments
    - Type hints and annotations

    Generates specs in various formats (Kiro, SpecKit, etc.)
    """

    def __init__(
        self,
        default_format: str = "kiro",
        output_dir: Path | None = None,
    ) -> None:
        """Initialize the generator engine.

        Args:
            default_format: Default output format (kiro, speckit, etc.)
            output_dir: Directory for generated specs
        """
        self.default_format = default_format
        self.output_dir = output_dir or Path(".kiro/specs")

    def generate_from_file(
        self,
        file_path: Path,
        spec_name: str | None = None,
        output_format: str | None = None,
    ) -> GeneratedSpec:
        """Generate a spec from a single code file.

        Args:
            file_path: Path to the code file
            spec_name: Name for the generated spec (defaults to file stem)
            output_format: Output format (defaults to default_format)

        Returns:
            GeneratedSpec with generated content
        """
        file_path = Path(file_path)
        spec_name = spec_name or self._derive_spec_name(file_path)
        output_format = output_format or self.default_format

        # Extract metadata from file
        metadata = self.extract_metadata(file_path)

        # Generate spec content
        content = self._generate_content(
            metadata=metadata,
            spec_name=spec_name,
            output_format=output_format,
        )

        # Determine output path
        spec_path = self.output_dir / spec_name

        return GeneratedSpec(
            source_files=[file_path],
            spec_name=spec_name,
            spec_path=spec_path,
            content=content,
            adapter_format=output_format,
            metadata={
                "auto_generated": True,
                "generated_at": datetime.now().isoformat(),
                "source_files": [str(file_path)],
                "extracted_metadata": metadata,
            },
        )

    def generate_from_directory(
        self,
        dir_path: Path,
        group_by: Literal["file", "directory", "module"] = "directory",
        output_format: str | None = None,
        file_patterns: list[str] | None = None,
    ) -> list[GeneratedSpec]:
        """Generate specs from a directory of code files.

        Args:
            dir_path: Path to the directory
            group_by: How to group files into specs
            output_format: Output format (defaults to default_format)
            file_patterns: Glob patterns for files to include

        Returns:
            List of GeneratedSpec for each generated spec
        """
        dir_path = Path(dir_path)
        output_format = output_format or self.default_format
        file_patterns = file_patterns or ["*.py"]

        # Find all matching files
        files: list[Path] = []
        for pattern in file_patterns:
            files.extend(dir_path.rglob(pattern))

        # Filter out test files and __pycache__
        files = [
            f
            for f in files
            if "__pycache__" not in str(f)
            and not f.name.startswith("test_")
            and f.name != "__init__.py"
        ]

        if not files:
            return []

        if group_by == "file":
            # One spec per file
            return [self.generate_from_file(f, output_format=output_format) for f in files]
        elif group_by == "directory":
            # One spec per directory
            return self._generate_by_directory(files, output_format)
        else:  # module
            # One spec per top-level module
            return self._generate_by_module(files, dir_path, output_format)

    def extract_metadata(self, file_path: Path) -> dict[str, Any]:
        """Extract metadata from a code file.

        Args:
            file_path: Path to the code file

        Returns:
            Dictionary with extracted metadata
        """
        file_path = Path(file_path)

        if not file_path.exists():
            return {"error": "File not found"}

        content = file_path.read_text()

        metadata: dict[str, Any] = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "functions": [],
            "classes": [],
            "module_docstring": None,
            "imports": [],
            "comments": [],
        }

        # Parse Python files
        if file_path.suffix == ".py":
            metadata.update(self._parse_python(content))
        else:
            # For non-Python files, extract comments
            metadata["comments"] = self._extract_comments(content)

        return metadata

    def write_spec(self, spec: GeneratedSpec) -> Path:
        """Write a generated spec to disk.

        Args:
            spec: The generated spec to write

        Returns:
            Path where the spec was written
        """
        spec.spec_path.mkdir(parents=True, exist_ok=True)

        # Write requirements.md
        requirements_path = spec.spec_path / "requirements.md"
        requirements_path.write_text(spec.content)

        return spec.spec_path

    def _derive_spec_name(self, file_path: Path) -> str:
        """Derive a spec name from a file path."""
        # Use file stem, convert to kebab-case
        name = file_path.stem
        # Convert snake_case to kebab-case
        name = name.replace("_", "-")
        return name

    def _parse_python(self, content: str) -> dict[str, Any]:
        """Parse Python code and extract metadata."""
        result: dict[str, Any] = {
            "functions": [],
            "classes": [],
            "module_docstring": None,
            "imports": [],
        }

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return result

        # Get module docstring
        if (
            tree.body
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)
            and isinstance(tree.body[0].value.value, str)
        ):
            result["module_docstring"] = tree.body[0].value.value

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "docstring": ast.get_docstring(node),
                    "args": [arg.arg for arg in node.args.args],
                    "returns": self._get_return_annotation(node),
                }
                result["functions"].append(func_info)

            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "docstring": ast.get_docstring(node),
                    "methods": [],
                    "bases": [self._get_name(base) for base in node.bases],
                }

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_info = {
                            "name": item.name,
                            "docstring": ast.get_docstring(item),
                        }
                        class_info["methods"].append(method_info)

                result["classes"].append(class_info)

            elif isinstance(node, ast.Import | ast.ImportFrom):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result["imports"].append(alias.name)
                else:
                    module = node.module or ""
                    for alias in node.names:
                        result["imports"].append(f"{module}.{alias.name}")

        return result

    def _get_return_annotation(self, node: ast.FunctionDef) -> str | None:
        """Get return type annotation as string."""
        if node.returns:
            return ast.unparse(node.returns)
        return None

    def _get_name(self, node: ast.expr) -> str:
        """Get name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return ast.unparse(node)

    def _extract_comments(self, content: str) -> list[str]:
        """Extract comments from code."""
        comments = []
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("#"):
                comments.append(line[1:].strip())
            elif line.startswith("//"):
                comments.append(line[2:].strip())
        return comments

    def _generate_content(
        self,
        metadata: dict[str, Any],
        spec_name: str,
        output_format: str,
    ) -> str:
        """Generate spec content from metadata."""
        if output_format == "kiro":
            return self._generate_kiro_format(metadata, spec_name)
        else:
            # Default to Kiro format
            return self._generate_kiro_format(metadata, spec_name)

    def _generate_kiro_format(
        self,
        metadata: dict[str, Any],
        spec_name: str,
    ) -> str:
        """Generate Kiro-format spec content."""
        lines = [
            "# Requirements Document",
            "",
            "<!-- auto-generated: true -->",
            f"<!-- generated-at: {datetime.now().isoformat()} -->",
            f"<!-- source: {metadata.get('file_path', 'unknown')} -->",
            "",
            "## Introduction",
            "",
        ]

        # Add module docstring if available
        if metadata.get("module_docstring"):
            lines.append(metadata["module_docstring"])
            lines.append("")
        else:
            lines.append(f"Auto-generated spec for `{spec_name}`.")
            lines.append("")

        # Add glossary
        lines.extend(
            [
                "## Glossary",
                "",
            ]
        )

        # Add classes to glossary
        for cls in metadata.get("classes", []):
            lines.append(
                f"- **{cls['name']}**: {cls.get('docstring', 'No description')[:100] if cls.get('docstring') else 'No description'}"
            )

        if not metadata.get("classes"):
            lines.append("- *No classes defined*")

        lines.append("")

        # Generate requirements from functions
        lines.extend(
            [
                "## Requirements",
                "",
            ]
        )

        req_num = 1

        # Generate requirements from classes
        for cls in metadata.get("classes", []):
            lines.extend(
                [
                    f"### Requirement {req_num}: {cls['name']}",
                    "",
                    f"**User Story:** As a developer, I want to use {cls['name']}, so that I can {cls.get('docstring', 'accomplish the intended functionality')[:100] if cls.get('docstring') else 'accomplish the intended functionality'}.",
                    "",
                    "#### Acceptance Criteria",
                    "",
                ]
            )

            criteria_num = 1
            for method in cls.get("methods", []):
                if not method["name"].startswith("_"):
                    desc = (
                        method.get("docstring", f"perform {method['name']} operation")[:80]
                        if method.get("docstring")
                        else f"perform {method['name']} operation"
                    )
                    lines.append(
                        f"{criteria_num}. WHEN a user calls `{method['name']}()` THEN the system SHALL {desc}"
                    )
                    criteria_num += 1

            if criteria_num == 1:
                lines.append(
                    "1. WHEN the class is instantiated THEN the system SHALL initialize correctly"
                )

            lines.append("")
            req_num += 1

        # Generate requirements from standalone functions
        standalone_funcs = [
            f for f in metadata.get("functions", []) if not f["name"].startswith("_")
        ]

        if standalone_funcs:
            lines.extend(
                [
                    f"### Requirement {req_num}: Core Functions",
                    "",
                    "**User Story:** As a developer, I want to use the module functions, so that I can accomplish common tasks.",
                    "",
                    "#### Acceptance Criteria",
                    "",
                ]
            )

            for i, func in enumerate(standalone_funcs, 1):
                desc = (
                    func.get("docstring", f"perform {func['name']} operation")[:80]
                    if func.get("docstring")
                    else f"perform {func['name']} operation"
                )
                lines.append(
                    f"{i}. WHEN a user calls `{func['name']}()` THEN the system SHALL {desc}"
                )

            lines.append("")

        return "\n".join(lines)

    def _generate_by_directory(
        self,
        files: list[Path],
        output_format: str,
    ) -> list[GeneratedSpec]:
        """Generate specs grouped by directory."""
        # Group files by parent directory
        dir_files: dict[Path, list[Path]] = {}
        for f in files:
            parent = f.parent
            if parent not in dir_files:
                dir_files[parent] = []
            dir_files[parent].append(f)

        specs = []
        for dir_path, dir_file_list in dir_files.items():
            # Combine metadata from all files
            combined_metadata: dict[str, Any] = {
                "file_path": str(dir_path),
                "functions": [],
                "classes": [],
                "module_docstring": None,
                "imports": [],
            }

            for f in dir_file_list:
                file_meta = self.extract_metadata(f)
                combined_metadata["functions"].extend(file_meta.get("functions", []))
                combined_metadata["classes"].extend(file_meta.get("classes", []))
                combined_metadata["imports"].extend(file_meta.get("imports", []))

            spec_name = dir_path.name
            content = self._generate_content(combined_metadata, spec_name, output_format)
            spec_path = self.output_dir / spec_name

            specs.append(
                GeneratedSpec(
                    source_files=dir_file_list,
                    spec_name=spec_name,
                    spec_path=spec_path,
                    content=content,
                    adapter_format=output_format,
                    metadata={
                        "auto_generated": True,
                        "generated_at": datetime.now().isoformat(),
                        "source_files": [str(f) for f in dir_file_list],
                    },
                )
            )

        return specs

    def _generate_by_module(
        self,
        files: list[Path],
        base_dir: Path,
        output_format: str,
    ) -> list[GeneratedSpec]:
        """Generate specs grouped by top-level module."""
        # Group files by top-level module
        module_files: dict[str, list[Path]] = {}

        for f in files:
            try:
                rel_path = f.relative_to(base_dir)
                top_module = rel_path.parts[0] if len(rel_path.parts) > 1 else rel_path.stem
            except ValueError:
                top_module = f.stem

            if top_module not in module_files:
                module_files[top_module] = []
            module_files[top_module].append(f)

        specs = []
        for module_name, module_file_list in module_files.items():
            # Combine metadata from all files
            combined_metadata: dict[str, Any] = {
                "file_path": module_name,
                "functions": [],
                "classes": [],
                "module_docstring": None,
                "imports": [],
            }

            for f in module_file_list:
                file_meta = self.extract_metadata(f)
                combined_metadata["functions"].extend(file_meta.get("functions", []))
                combined_metadata["classes"].extend(file_meta.get("classes", []))

            content = self._generate_content(combined_metadata, module_name, output_format)
            spec_path = self.output_dir / module_name

            specs.append(
                GeneratedSpec(
                    source_files=module_file_list,
                    spec_name=module_name,
                    spec_path=spec_path,
                    content=content,
                    adapter_format=output_format,
                    metadata={
                        "auto_generated": True,
                        "generated_at": datetime.now().isoformat(),
                        "source_files": [str(f) for f in module_file_list],
                    },
                )
            )

        return specs
