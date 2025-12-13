"""Abstract base class for code parsers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar

from ..models.code_elements import CodeElements


class CodeParser(ABC):
    """Abstract base class for language-specific code parsers."""

    language: ClassVar[str] = "unknown"
    file_extensions: ClassVar[list[str]] = []

    def __init__(self, project_root: Path):
        """Initialize parser with project root path."""
        self.project_root = project_root

    @abstractmethod
    def parse_file(self, file_path: Path) -> CodeElements:
        """Parse a single file and extract code elements.

        Args:
            file_path: Path to the file to parse.

        Returns:
            CodeElements containing extracted API endpoints and entities.
        """
        pass

    def parse_directory(self, directory: Path) -> CodeElements:
        """Parse all files in a directory recursively.

        Args:
            directory: Path to the directory to parse.

        Returns:
            CodeElements containing all extracted elements.
        """
        result = CodeElements(language=self.language)

        if not directory.exists():
            return result

        for ext in self.file_extensions:
            for file_path in directory.rglob(f"*{ext}"):
                # Skip common non-source directories
                if self._should_skip_path(file_path):
                    continue

                try:
                    file_elements = self.parse_file(file_path)
                    result.api_endpoints.extend(file_elements.api_endpoints)
                    result.entities.extend(file_elements.entities)
                    if file_elements.source_files:
                        result.source_files.extend(file_elements.source_files)
                except Exception:
                    # Log error but continue parsing other files
                    pass

        return result

    def _should_skip_path(self, path: Path) -> bool:
        """Check if a path should be skipped during parsing."""
        skip_dirs = {
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            "env",
            "node_modules",
            ".tox",
            ".pytest_cache",
            ".mypy_cache",
            "dist",
            "build",
            ".egg-info",
        }
        return any(part in skip_dirs for part in path.parts)

    @classmethod
    def supports_file(cls, file_path: Path) -> bool:
        """Check if this parser supports the given file."""
        return file_path.suffix in cls.file_extensions


class ParserRegistry:
    """Registry for code parsers."""

    _parsers: ClassVar[dict[str, type[CodeParser]]] = {}

    @classmethod
    def register(cls, parser_class: type[CodeParser]) -> type[CodeParser]:
        """Register a parser class."""
        cls._parsers[parser_class.language] = parser_class
        return parser_class

    @classmethod
    def get_parser(cls, language: str, project_root: Path) -> CodeParser | None:
        """Get a parser instance for the given language."""
        parser_class = cls._parsers.get(language)
        if parser_class:
            return parser_class(project_root)
        return None

    @classmethod
    def detect_language(cls, directory: Path) -> str | None:
        """Detect the primary language in a directory."""
        extension_counts: dict[str, int] = {}

        for parser_class in cls._parsers.values():
            for ext in parser_class.file_extensions:
                count = len(list(directory.rglob(f"*{ext}")))
                if count > 0:
                    extension_counts[parser_class.language] = (
                        extension_counts.get(parser_class.language, 0) + count
                    )

        if extension_counts:
            return max(extension_counts, key=extension_counts.get)  # type: ignore
        return None

    @classmethod
    def get_parser_for_file(cls, file_path: Path, project_root: Path) -> CodeParser | None:
        """Get a parser instance for the given file based on extension."""
        for parser_class in cls._parsers.values():
            if parser_class.supports_file(file_path):
                return parser_class(project_root)
        return None

    @classmethod
    def available_languages(cls) -> list[str]:
        """Get list of available parser languages."""
        return list(cls._parsers.keys())
