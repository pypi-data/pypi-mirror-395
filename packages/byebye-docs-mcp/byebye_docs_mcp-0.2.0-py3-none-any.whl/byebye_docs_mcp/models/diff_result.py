"""Data models for diff and sync results."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DriftType(str, Enum):
    """Type of drift between code and documentation."""

    ADDED_IN_CODE = "added_in_code"  # Exists in code but not in docs
    REMOVED_FROM_CODE = "removed_from_code"  # Exists in docs but not in code
    MODIFIED = "modified"  # Different between code and docs


class DriftAction(str, Enum):
    """Recommended action for a drift item."""

    ADD_TO_DOCS = "add_to_docs"
    REMOVE_FROM_DOCS = "remove_from_docs"
    UPDATE_DOCS = "update_docs"
    MANUAL_REVIEW = "manual_review"


class ElementType(str, Enum):
    """Type of element that has drifted."""

    API_ENDPOINT = "api_endpoint"
    ENTITY = "entity"
    FIELD = "field"


@dataclass
class DriftItem:
    """Represents a single difference between code and documentation."""

    element_type: ElementType
    drift_type: DriftType
    location: str  # file:line
    identifier: str  # e.g., "GET /users" or "User.email"
    code_value: dict[str, Any] | None = None
    doc_value: dict[str, Any] | None = None
    action: DriftAction = DriftAction.MANUAL_REVIEW
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "type": self.element_type.value,
            "drift_type": self.drift_type.value,
            "location": self.location,
            "identifier": self.identifier,
            "code_value": self.code_value,
            "doc_value": self.doc_value,
            "action": self.action.value,
            "reason": self.reason,
        }


@dataclass
class DiffSummary:
    """Summary of differences found."""

    added_in_code: int = 0
    removed_from_code: int = 0
    modified: int = 0

    @property
    def total(self) -> int:
        """Total number of differences."""
        return self.added_in_code + self.removed_from_code + self.modified

    @property
    def has_drift(self) -> bool:
        """Check if there are any differences."""
        return self.total > 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "added_in_code": self.added_in_code,
            "removed_from_code": self.removed_from_code,
            "modified": self.modified,
            "total": self.total,
        }


@dataclass
class DiffResult:
    """Complete result of a diff operation."""

    status: str = "in_sync"  # "in_sync" or "drift_detected"
    summary: DiffSummary = field(default_factory=DiffSummary)
    details: list[DriftItem] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "status": self.status,
            "summary": self.summary.to_dict(),
            "details": [d.to_dict() for d in self.details],
            "errors": self.errors,
            "warnings": self.warnings,
        }


class SyncOperation(str, Enum):
    """Type of sync operation."""

    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"


@dataclass
class SyncChange:
    """Represents a single change to be applied during sync."""

    file_path: str
    operation: SyncOperation
    section: str  # e.g., "paths./users.get" or "entities[0]"
    old_value: Any = None
    new_value: Any = None
    diff_text: str = ""
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "file": self.file_path,
            "operation": self.operation.value,
            "section": self.section,
            "diff": self.diff_text,
            "reason": self.reason,
        }


@dataclass
class SyncResult:
    """Result of a sync operation."""

    success: bool = True
    mode: str = "preview"  # "preview" or "apply"
    changes: list[SyncChange] = field(default_factory=list)
    applied: list[dict[str, str]] = field(default_factory=list)  # [{file, backup_path}]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        result: dict[str, Any] = {
            "success": self.success,
            "mode": self.mode,
        }
        if self.mode == "preview":
            result["changes"] = [c.to_dict() for c in self.changes]
        else:
            result["applied"] = self.applied
        result["warnings"] = self.warnings
        result["errors"] = self.errors
        return result
