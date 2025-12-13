"""Data models for code elements extracted from source files."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ApiEndpoint:
    """Represents an API endpoint extracted from code."""

    path: str
    method: str  # GET, POST, PATCH, DELETE, PUT
    function_name: str
    file_path: str
    line_number: int
    summary: str | None = None
    description: str | None = None
    parameters: list[dict[str, Any]] = field(default_factory=list)
    request_body: dict[str, Any] | None = None
    responses: dict[str, dict[str, Any]] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "path": self.path,
            "method": self.method,
            "function_name": self.function_name,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "summary": self.summary,
            "description": self.description,
            "parameters": self.parameters,
            "request_body": self.request_body,
            "responses": self.responses,
            "tags": self.tags,
        }

    def unique_key(self) -> str:
        """Generate a unique key for comparison."""
        return f"{self.method.upper()} {self.path}"


@dataclass
class EntityField:
    """Represents a field in an entity/model."""

    name: str
    field_type: str  # uuid, string, integer, datetime, enum, json, etc.
    nullable: bool = True
    primary_key: bool = False
    auto_generate: bool = False
    unique: bool = False
    max_length: int | None = None
    default: Any = None
    foreign_key: dict[str, str] | None = None  # {table, field, on_delete}
    enum_values: list[str] | None = None
    sensitive: bool = False
    description: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        result: dict[str, Any] = {
            "name": self.name,
            "type": self.field_type,
        }
        if self.primary_key:
            result["primary_key"] = True
        if self.auto_generate:
            result["auto_generate"] = True
        if self.unique:
            result["unique"] = True
        if not self.nullable:
            result["nullable"] = False
        if self.max_length is not None:
            result["max_length"] = self.max_length
        if self.default is not None:
            result["default"] = self.default
        if self.foreign_key:
            result["foreign_key"] = self.foreign_key
        if self.enum_values:
            result["enum"] = {"values": self.enum_values}
        if self.sensitive:
            result["sensitive"] = True
        if self.description:
            result["description"] = self.description
        return result


@dataclass
class Entity:
    """Represents an entity/model extracted from code."""

    name: str  # Class name / schema name
    table_name: str | None = None
    file_path: str = ""
    line_number: int = 0
    description: str | None = None
    fields: list[EntityField] = field(default_factory=list)
    indexes: list[dict[str, Any]] = field(default_factory=list)
    validations: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        result: dict[str, Any] = {
            "schema": self.name,
        }
        if self.description:
            result["description"] = self.description
        if self.table_name:
            result["table_name"] = self.table_name
        result["fields"] = [f.to_dict() for f in self.fields]
        if self.indexes:
            result["indexes"] = self.indexes
        if self.validations:
            result["validations"] = self.validations
        return result

    def unique_key(self) -> str:
        """Generate a unique key for comparison."""
        return self.name


@dataclass
class CodeElements:
    """Container for all extracted code elements."""

    api_endpoints: list[ApiEndpoint] = field(default_factory=list)
    entities: list[Entity] = field(default_factory=list)
    language: str = "python"
    source_files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "language": self.language,
            "source_files": self.source_files,
            "api_endpoints": [e.to_dict() for e in self.api_endpoints],
            "entities": [e.to_dict() for e in self.entities],
        }
