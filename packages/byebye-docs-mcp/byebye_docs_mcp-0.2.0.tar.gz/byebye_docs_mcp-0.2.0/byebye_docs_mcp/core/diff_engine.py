"""Engine for detecting differences between code and documentation."""

from pathlib import Path
from typing import Any

from ..extractors.api_extractor import ApiExtractor
from ..extractors.entity_extractor import EntityExtractor
from ..models.code_elements import ApiEndpoint, CodeElements, Entity
from ..models.diff_result import (
    DiffResult,
    DiffSummary,
    DriftAction,
    DriftItem,
    DriftType,
    ElementType,
)
from ..parsers import ParserRegistry


class DiffEngine:
    """Engine for detecting differences between code and documentation."""

    def __init__(self, project_root: Path):
        """Initialize diff engine with project root."""
        self.project_root = project_root
        self.api_extractor = ApiExtractor(project_root)
        self.entity_extractor = EntityExtractor(project_root)

    def diff(
        self,
        code_path: str,
        doc_type: str = "all",
        language: str = "auto",
    ) -> DiffResult:
        """Compare code with documentation and return differences.

        Args:
            code_path: Path to code directory/file (relative to project root).
            doc_type: Type of documentation to compare ("api", "entities", "all").
            language: Programming language ("python", "auto").

        Returns:
            DiffResult containing all detected differences.
        """
        result = DiffResult()
        code_dir = self.project_root / code_path

        if not code_dir.exists():
            result.errors.append(f"Code path not found: {code_path}")
            return result

        # Detect or validate language
        if language == "auto":
            detected = ParserRegistry.detect_language(code_dir)
            if not detected:
                result.errors.append("Could not detect programming language")
                return result
            language = detected

        # Get parser for the language
        parser = ParserRegistry.get_parser(language, self.project_root)
        if not parser:
            result.errors.append(f"No parser available for language: {language}")
            return result

        # Parse code
        if code_dir.is_file():
            code_elements = parser.parse_file(code_dir)
        else:
            code_elements = parser.parse_directory(code_dir)

        # Compare with documentation
        if doc_type in ("api", "all"):
            api_diffs = self._diff_api(code_elements)
            result.details.extend(api_diffs)

        if doc_type in ("entities", "all"):
            entity_diffs = self._diff_entities(code_elements)
            result.details.extend(entity_diffs)

        # Calculate summary
        result.summary = self._calculate_summary(result.details)
        result.status = "drift_detected" if result.summary.has_drift else "in_sync"

        return result

    def _diff_api(self, code_elements: CodeElements) -> list[DriftItem]:
        """Compare API endpoints between code and documentation."""
        diffs: list[DriftItem] = []

        # Load existing API spec
        api_path = self.project_root / ".agent" / "schemas" / "api.yaml"
        existing_spec = self.api_extractor.load_existing_spec(api_path)

        if not existing_spec:
            # No existing spec - all code endpoints are new
            for endpoint in code_elements.api_endpoints:
                diffs.append(
                    DriftItem(
                        element_type=ElementType.API_ENDPOINT,
                        drift_type=DriftType.ADDED_IN_CODE,
                        location=f"{endpoint.file_path}:{endpoint.line_number}",
                        identifier=endpoint.unique_key(),
                        code_value=endpoint.to_dict(),
                        doc_value=None,
                        action=DriftAction.ADD_TO_DOCS,
                        reason="エンドポイントがドキュメントに存在しない",
                    )
                )
            return diffs

        # Get endpoints from spec
        doc_endpoints = self.api_extractor.get_endpoints_from_spec(existing_spec)

        # Build lookup maps
        code_by_key = {ep.unique_key(): ep for ep in code_elements.api_endpoints}
        doc_by_key = {ep.unique_key(): ep for ep in doc_endpoints}

        # Find endpoints in code but not in docs
        for key, endpoint in code_by_key.items():
            if key not in doc_by_key:
                diffs.append(
                    DriftItem(
                        element_type=ElementType.API_ENDPOINT,
                        drift_type=DriftType.ADDED_IN_CODE,
                        location=f"{endpoint.file_path}:{endpoint.line_number}",
                        identifier=key,
                        code_value=endpoint.to_dict(),
                        doc_value=None,
                        action=DriftAction.ADD_TO_DOCS,
                        reason="エンドポイントがドキュメントに存在しない",
                    )
                )

        # Find endpoints in docs but not in code
        for key, endpoint in doc_by_key.items():
            if key not in code_by_key:
                diffs.append(
                    DriftItem(
                        element_type=ElementType.API_ENDPOINT,
                        drift_type=DriftType.REMOVED_FROM_CODE,
                        location="api.yaml",
                        identifier=key,
                        code_value=None,
                        doc_value=endpoint.to_dict(),
                        action=DriftAction.REMOVE_FROM_DOCS,
                        reason="エンドポイントがコードに存在しない",
                    )
                )

        # Find modified endpoints (same key but different details)
        for key in set(code_by_key.keys()) & set(doc_by_key.keys()):
            code_ep = code_by_key[key]
            doc_ep = doc_by_key[key]

            changes = self._compare_endpoints(code_ep, doc_ep)
            if changes:
                diffs.append(
                    DriftItem(
                        element_type=ElementType.API_ENDPOINT,
                        drift_type=DriftType.MODIFIED,
                        location=f"{code_ep.file_path}:{code_ep.line_number}",
                        identifier=key,
                        code_value=code_ep.to_dict(),
                        doc_value=doc_ep.to_dict(),
                        action=DriftAction.UPDATE_DOCS,
                        reason=f"変更点: {', '.join(changes)}",
                    )
                )

        return diffs

    def _compare_endpoints(
        self, code_ep: ApiEndpoint, doc_ep: ApiEndpoint
    ) -> list[str]:
        """Compare two endpoints and return list of differences."""
        changes = []

        # Compare function name / operationId
        if code_ep.function_name and doc_ep.function_name:
            if code_ep.function_name != doc_ep.function_name:
                changes.append("operationId")

        # Compare parameters (simplified comparison)
        code_params = {p.get("name"): p for p in code_ep.parameters}
        doc_params = {p.get("name"): p for p in doc_ep.parameters}

        if set(code_params.keys()) != set(doc_params.keys()):
            changes.append("parameters")

        return changes

    def _diff_entities(self, code_elements: CodeElements) -> list[DriftItem]:
        """Compare entities between code and documentation."""
        diffs: list[DriftItem] = []

        # Load existing entities spec
        entities_path = self.project_root / ".agent" / "schemas" / "entities.yaml"
        existing_spec = self.entity_extractor.load_existing_entities(entities_path)

        if not existing_spec:
            # No existing spec - all code entities are new
            for entity in code_elements.entities:
                diffs.append(
                    DriftItem(
                        element_type=ElementType.ENTITY,
                        drift_type=DriftType.ADDED_IN_CODE,
                        location=f"{entity.file_path}:{entity.line_number}",
                        identifier=entity.unique_key(),
                        code_value=entity.to_dict(),
                        doc_value=None,
                        action=DriftAction.ADD_TO_DOCS,
                        reason="エンティティがドキュメントに存在しない",
                    )
                )
            return diffs

        # Get entities from spec
        doc_entities = self.entity_extractor.get_entities_from_spec(existing_spec)

        # Build lookup maps
        code_by_key = {e.unique_key(): e for e in code_elements.entities}
        doc_by_key = {e.unique_key(): e for e in doc_entities}

        # Find entities in code but not in docs
        for key, entity in code_by_key.items():
            if key not in doc_by_key:
                diffs.append(
                    DriftItem(
                        element_type=ElementType.ENTITY,
                        drift_type=DriftType.ADDED_IN_CODE,
                        location=f"{entity.file_path}:{entity.line_number}",
                        identifier=key,
                        code_value=entity.to_dict(),
                        doc_value=None,
                        action=DriftAction.ADD_TO_DOCS,
                        reason="エンティティがドキュメントに存在しない",
                    )
                )

        # Find entities in docs but not in code
        for key, entity in doc_by_key.items():
            if key not in code_by_key:
                diffs.append(
                    DriftItem(
                        element_type=ElementType.ENTITY,
                        drift_type=DriftType.REMOVED_FROM_CODE,
                        location="entities.yaml",
                        identifier=key,
                        code_value=None,
                        doc_value=entity.to_dict(),
                        action=DriftAction.REMOVE_FROM_DOCS,
                        reason="エンティティがコードに存在しない",
                    )
                )

        # Find modified entities
        for key in set(code_by_key.keys()) & set(doc_by_key.keys()):
            code_entity = code_by_key[key]
            doc_entity = doc_by_key[key]

            changes = self._compare_entities(code_entity, doc_entity)
            if changes:
                diffs.append(
                    DriftItem(
                        element_type=ElementType.ENTITY,
                        drift_type=DriftType.MODIFIED,
                        location=f"{code_entity.file_path}:{code_entity.line_number}",
                        identifier=key,
                        code_value=code_entity.to_dict(),
                        doc_value=doc_entity.to_dict(),
                        action=DriftAction.UPDATE_DOCS,
                        reason=f"変更点: {', '.join(changes)}",
                    )
                )

        return diffs

    def _compare_entities(self, code_entity: Entity, doc_entity: Entity) -> list[str]:
        """Compare two entities and return list of differences."""
        changes = []

        # Compare table name
        if code_entity.table_name != doc_entity.table_name:
            if code_entity.table_name:  # Only report if code has a table name
                changes.append("table_name")

        # Compare fields
        code_fields = {f.name: f for f in code_entity.fields}
        doc_fields = {f.name: f for f in doc_entity.fields}

        # Check for added/removed fields
        added_fields = set(code_fields.keys()) - set(doc_fields.keys())
        removed_fields = set(doc_fields.keys()) - set(code_fields.keys())

        if added_fields:
            changes.append(f"added_fields({', '.join(added_fields)})")
        if removed_fields:
            changes.append(f"removed_fields({', '.join(removed_fields)})")

        # Check for modified fields
        for name in set(code_fields.keys()) & set(doc_fields.keys()):
            code_field = code_fields[name]
            doc_field = doc_fields[name]

            if code_field.field_type != doc_field.field_type:
                changes.append(f"field_type_changed({name})")
            if code_field.nullable != doc_field.nullable:
                changes.append(f"nullable_changed({name})")

        return changes

    def _calculate_summary(self, diffs: list[DriftItem]) -> DiffSummary:
        """Calculate summary statistics from diff items."""
        summary = DiffSummary()

        for diff in diffs:
            if diff.drift_type == DriftType.ADDED_IN_CODE:
                summary.added_in_code += 1
            elif diff.drift_type == DriftType.REMOVED_FROM_CODE:
                summary.removed_from_code += 1
            elif diff.drift_type == DriftType.MODIFIED:
                summary.modified += 1

        return summary

    def get_code_elements(
        self, code_path: str, language: str = "auto"
    ) -> tuple[CodeElements | None, list[str]]:
        """Parse code and return extracted elements.

        Args:
            code_path: Path to code directory/file.
            language: Programming language.

        Returns:
            Tuple of (CodeElements or None, list of error messages).
        """
        errors: list[str] = []
        code_dir = self.project_root / code_path

        if not code_dir.exists():
            errors.append(f"Code path not found: {code_path}")
            return None, errors

        if language == "auto":
            detected = ParserRegistry.detect_language(code_dir)
            if not detected:
                errors.append("Could not detect programming language")
                return None, errors
            language = detected

        parser = ParserRegistry.get_parser(language, self.project_root)
        if not parser:
            errors.append(f"No parser available for language: {language}")
            return None, errors

        if code_dir.is_file():
            return parser.parse_file(code_dir), errors
        return parser.parse_directory(code_dir), errors
