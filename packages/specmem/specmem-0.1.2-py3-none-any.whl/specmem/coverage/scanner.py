"""Test Scanner for Spec Coverage Analysis.

Scans test files and extracts test information for matching
against acceptance criteria.
"""

from __future__ import annotations

import ast
import logging
import re
from pathlib import Path

from specmem.coverage.models import ExtractedTest
from specmem.testing.frameworks import TestFramework, detect_frameworks


logger = logging.getLogger(__name__)


class TestScanner:
    """Scans test files and extracts test information.

    Leverages the existing TestMappingEngine for framework detection
    and adds docstring/comment extraction for requirement links.
    """

    # Pattern to match requirement links in docstrings/comments
    # Matches: "Validates: 1.2", "Requirements: 1.2, 1.3", "Req 1.2"
    REQUIREMENT_LINK_PATTERN = re.compile(
        r"(?:Validates|Requirements?|Req)[\s:]+([0-9]+(?:\.[0-9]+)?(?:\s*,\s*[0-9]+(?:\.[0-9]+)?)*)",
        re.IGNORECASE,
    )

    # Framework-specific test file patterns
    FRAMEWORK_PATTERNS: dict[TestFramework, list[str]] = {
        TestFramework.PYTEST: ["test_*.py", "*_test.py", "tests/**/test_*.py"],
        TestFramework.JEST: ["*.test.js", "*.test.ts", "*.spec.js", "*.spec.ts"],
        TestFramework.VITEST: ["*.test.ts", "*.spec.ts"],
        TestFramework.PLAYWRIGHT: ["*.spec.ts", "e2e/**/*.ts"],
        TestFramework.MOCHA: ["test/**/*.js", "*.test.js"],
    }

    def __init__(self, workspace_path: Path | str) -> None:
        """Initialize the test scanner.

        Args:
            workspace_path: Path to the workspace root
        """
        self.workspace_path = Path(workspace_path).resolve()
        self._frameworks: list[TestFramework] | None = None

    @property
    def frameworks(self) -> list[TestFramework]:
        """Get detected test frameworks."""
        if self._frameworks is None:
            self._frameworks = detect_frameworks(self.workspace_path)
        return self._frameworks

    def scan_tests(self) -> list[ExtractedTest]:
        """Scan all test files in workspace.

        Returns:
            List of ExtractedTest objects
        """
        tests: list[ExtractedTest] = []

        for framework in self.frameworks:
            patterns = self.FRAMEWORK_PATTERNS.get(framework, [])
            for pattern in patterns:
                for test_file in self.workspace_path.glob(pattern):
                    if test_file.is_file():
                        file_tests = self._parse_test_file(test_file, framework)
                        tests.extend(file_tests)

        # Deduplicate by (file_path, name, line_number)
        seen: set[tuple[str, str, int]] = set()
        unique_tests: list[ExtractedTest] = []
        for test in tests:
            key = (test.file_path, test.name, test.line_number)
            if key not in seen:
                seen.add(key)
                unique_tests.append(test)

        return unique_tests

    def extract_requirement_links(self, text: str | None) -> list[str]:
        """Extract requirement links from docstring or comment.

        Args:
            text: Docstring or comment text

        Returns:
            List of requirement numbers (e.g., ["1.2", "1.3"])
        """
        if not text:
            return []

        links: list[str] = []
        for match in self.REQUIREMENT_LINK_PATTERN.finditer(text):
            # Split by comma and clean up
            refs = match.group(1).split(",")
            for ref in refs:
                ref = ref.strip()
                if ref:
                    links.append(ref)

        return links

    def _parse_test_file(
        self,
        path: Path,
        framework: TestFramework,
    ) -> list[ExtractedTest]:
        """Parse a test file and extract tests.

        Args:
            path: Path to the test file
            framework: Test framework

        Returns:
            List of ExtractedTest objects
        """
        try:
            content = path.read_text()
            rel_path = str(path.relative_to(self.workspace_path))
        except Exception as e:
            logger.warning(f"Failed to read test file {path}: {e}")
            return []

        if framework == TestFramework.PYTEST:
            return self._parse_pytest_file(content, rel_path)
        elif framework in (TestFramework.JEST, TestFramework.VITEST):
            return self._parse_jest_file(content, rel_path, framework.value)
        elif framework == TestFramework.PLAYWRIGHT:
            return self._parse_playwright_file(content, rel_path)
        elif framework == TestFramework.MOCHA:
            return self._parse_mocha_file(content, rel_path)
        else:
            return self._parse_generic_file(content, rel_path)

    def _parse_pytest_file(self, content: str, path: str) -> list[ExtractedTest]:
        """Parse pytest test file using AST."""
        tests: list[ExtractedTest] = []

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logger.warning(f"Failed to parse Python file {path}: {e}")
            return tests

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                docstring = ast.get_docstring(node)
                requirement_links = self.extract_requirement_links(docstring)

                tests.append(
                    ExtractedTest(
                        name=node.name,
                        file_path=path,
                        line_number=node.lineno,
                        docstring=docstring,
                        requirement_links=requirement_links,
                        framework="pytest",
                        selector=f"{path}::{node.name}",
                    )
                )
            elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
                # Extract test methods from test classes
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                        docstring = ast.get_docstring(item)
                        requirement_links = self.extract_requirement_links(docstring)

                        tests.append(
                            ExtractedTest(
                                name=f"{node.name}.{item.name}",
                                file_path=path,
                                line_number=item.lineno,
                                docstring=docstring,
                                requirement_links=requirement_links,
                                framework="pytest",
                                selector=f"{path}::{node.name}::{item.name}",
                            )
                        )

        return tests

    def _parse_jest_file(
        self,
        content: str,
        path: str,
        framework: str = "jest",
    ) -> list[ExtractedTest]:
        """Parse jest/vitest test file using regex."""
        tests: list[ExtractedTest] = []

        # Pattern for test/it blocks
        test_pattern = r"(?:it|test)\s*\(\s*['\"]([^'\"]+)['\"]"

        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            match = re.search(test_pattern, line)
            if match:
                test_name = match.group(1)
                # Look for comment above
                docstring = None
                if i > 1:
                    prev_line = lines[i - 2].strip()
                    if prev_line.startswith("//") or prev_line.startswith("/*"):
                        # Strip comment markers one at a time
                        docstring = prev_line.lstrip("/").lstrip("*").strip()

                requirement_links = self.extract_requirement_links(docstring)

                tests.append(
                    ExtractedTest(
                        name=test_name,
                        file_path=path,
                        line_number=i,
                        docstring=docstring,
                        requirement_links=requirement_links,
                        framework=framework,
                        selector=test_name,
                    )
                )

        return tests

    def _parse_playwright_file(self, content: str, path: str) -> list[ExtractedTest]:
        """Parse playwright test file."""
        return self._parse_jest_file(content, path, "playwright")

    def _parse_mocha_file(self, content: str, path: str) -> list[ExtractedTest]:
        """Parse mocha test file."""
        return self._parse_jest_file(content, path, "mocha")

    def _parse_generic_file(self, content: str, path: str) -> list[ExtractedTest]:
        """Parse generic test file."""
        tests: list[ExtractedTest] = []

        # Look for common test patterns
        patterns = [
            (r"def\s+(test_\w+)", "python"),
            (r"(?:it|test)\s*\(\s*['\"]([^'\"]+)['\"]", "javascript"),
        ]

        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            for pattern, lang in patterns:
                match = re.search(pattern, line)
                if match:
                    test_name = match.group(1)
                    tests.append(
                        ExtractedTest(
                            name=test_name,
                            file_path=path,
                            line_number=i,
                            framework="unknown",
                            selector=test_name,
                        )
                    )
                    break

        return tests
