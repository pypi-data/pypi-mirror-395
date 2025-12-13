"""Manager for synchronizing code and documentation."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from ..extractors.api_extractor import ApiExtractor
from ..extractors.entity_extractor import EntityExtractor
from ..models.diff_result import SyncChange, SyncOperation, SyncResult
from .diff_engine import DiffEngine


class SyncManager:
    """Manager for synchronizing code changes to documentation."""

    def __init__(self, project_root: Path):
        """Initialize sync manager with project root."""
        self.project_root = project_root
        self.diff_engine = DiffEngine(project_root)
        self.api_extractor = ApiExtractor(project_root)
        self.entity_extractor = EntityExtractor(project_root)
        self.backup_dir = project_root / ".agent" / ".backups"

    def sync(
        self,
        code_path: str = "src",
        target_docs: list[str] | None = None,
        mode: str = "preview",
        language: str = "auto",
    ) -> SyncResult:
        """Synchronize code to documentation.

        Args:
            code_path: Path to code directory.
            target_docs: List of target documents (e.g., ["api.yaml", "entities.yaml"]).
            mode: "preview" for dry run, "apply" to make changes.
            language: Programming language.

        Returns:
            SyncResult with changes and status.
        """
        result = SyncResult(mode=mode)

        # Default target docs
        if target_docs is None:
            target_docs = ["api.yaml", "entities.yaml"]

        # Parse code
        code_elements, errors = self.diff_engine.get_code_elements(code_path, language)
        if errors:
            result.errors.extend(errors)
            result.success = False
            return result

        if code_elements is None:
            result.errors.append("Failed to parse code")
            result.success = False
            return result

        # Process each target document
        for doc_name in target_docs:
            if doc_name == "api.yaml":
                changes = self._sync_api(code_elements, mode)
                result.changes.extend(changes)
            elif doc_name == "entities.yaml":
                changes = self._sync_entities(code_elements, mode)
                result.changes.extend(changes)
            else:
                result.warnings.append(f"Unknown target document: {doc_name}")

        # If applying, track applied changes
        if mode == "apply":
            for change in result.changes:
                result.applied.append(
                    {
                        "file": change.file_path,
                        "backup_path": str(
                            self.backup_dir / f"{Path(change.file_path).name}.bak"
                        ),
                    }
                )

        return result

    def _sync_api(self, code_elements: Any, mode: str) -> list[SyncChange]:
        """Synchronize API endpoints to api.yaml."""
        changes: list[SyncChange] = []
        api_path = self.project_root / ".agent" / "schemas" / "api.yaml"
        rel_path = ".agent/schemas/api.yaml"

        # Load existing spec
        existing_spec = self.api_extractor.load_existing_spec(api_path)

        # Generate new spec
        new_spec = self.api_extractor.extract_to_openapi(
            code_elements, existing_spec, merge=True
        )

        # Compare and generate changes
        if existing_spec:
            old_paths = set(existing_spec.get("paths", {}).keys())
            new_paths = set(new_spec.get("paths", {}).keys())

            # Added endpoints
            for path in new_paths - old_paths:
                changes.append(
                    SyncChange(
                        file_path=rel_path,
                        operation=SyncOperation.ADD,
                        section=f"paths.{path}",
                        new_value=new_spec["paths"][path],
                        reason=f"新しいエンドポイント: {path}",
                    )
                )

            # Check for modified endpoints
            for path in old_paths & new_paths:
                old_methods = set(existing_spec["paths"][path].keys())
                new_methods = set(new_spec["paths"][path].keys())

                for method in new_methods - old_methods:
                    changes.append(
                        SyncChange(
                            file_path=rel_path,
                            operation=SyncOperation.ADD,
                            section=f"paths.{path}.{method}",
                            new_value=new_spec["paths"][path][method],
                            reason=f"新しいメソッド: {method.upper()} {path}",
                        )
                    )
        else:
            # All endpoints are new
            for path, path_item in new_spec.get("paths", {}).items():
                for method in path_item:
                    changes.append(
                        SyncChange(
                            file_path=rel_path,
                            operation=SyncOperation.ADD,
                            section=f"paths.{path}.{method}",
                            new_value=path_item[method],
                            reason=f"新しいエンドポイント: {method.upper()} {path}",
                        )
                    )

        # Apply changes if in apply mode
        if mode == "apply" and changes:
            self._apply_yaml_changes(api_path, new_spec)

        # Generate diff text for preview
        if existing_spec:
            for change in changes:
                change.diff_text = self._generate_diff_text(
                    change.old_value, change.new_value
                )

        return changes

    def _sync_entities(self, code_elements: Any, mode: str) -> list[SyncChange]:
        """Synchronize entities to entities.yaml."""
        changes: list[SyncChange] = []
        entities_path = self.project_root / ".agent" / "schemas" / "entities.yaml"
        rel_path = ".agent/schemas/entities.yaml"

        # Load existing spec
        existing_spec = self.entity_extractor.load_existing_entities(entities_path)

        # Generate new spec
        new_spec = self.entity_extractor.extract_to_entities_yaml(
            code_elements, existing_spec, merge=True
        )

        # Compare and generate changes
        if existing_spec:
            old_entities = {e.get("schema"): e for e in existing_spec.get("entities", [])}
            new_entities = {e.get("schema"): e for e in new_spec.get("entities", [])}

            # Added entities
            for name in set(new_entities.keys()) - set(old_entities.keys()):
                changes.append(
                    SyncChange(
                        file_path=rel_path,
                        operation=SyncOperation.ADD,
                        section=f"entities.{name}",
                        new_value=new_entities[name],
                        reason=f"新しいエンティティ: {name}",
                    )
                )

            # Modified entities
            for name in set(old_entities.keys()) & set(new_entities.keys()):
                old_entity = old_entities[name]
                new_entity = new_entities[name]

                # Check for field changes
                old_fields = {f.get("name"): f for f in old_entity.get("fields", [])}
                new_fields = {f.get("name"): f for f in new_entity.get("fields", [])}

                for field_name in set(new_fields.keys()) - set(old_fields.keys()):
                    changes.append(
                        SyncChange(
                            file_path=rel_path,
                            operation=SyncOperation.ADD,
                            section=f"entities.{name}.fields.{field_name}",
                            new_value=new_fields[field_name],
                            reason=f"新しいフィールド: {name}.{field_name}",
                        )
                    )
        else:
            # All entities are new
            for entity in new_spec.get("entities", []):
                name = entity.get("schema", "Unknown")
                changes.append(
                    SyncChange(
                        file_path=rel_path,
                        operation=SyncOperation.ADD,
                        section=f"entities.{name}",
                        new_value=entity,
                        reason=f"新しいエンティティ: {name}",
                    )
                )

        # Apply changes if in apply mode
        if mode == "apply" and changes:
            # Update last_updated
            new_spec["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            self._apply_yaml_changes(entities_path, new_spec)

        # Generate diff text for preview
        for change in changes:
            change.diff_text = self._generate_diff_text(change.old_value, change.new_value)

        return changes

    def _apply_yaml_changes(self, file_path: Path, new_spec: dict[str, Any]) -> None:
        """Apply changes to a YAML file with backup."""
        # Create backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Backup existing file
        if file_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"{file_path.stem}_{timestamp}.yaml"
            shutil.copy2(file_path, backup_path)

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write new spec
        content = yaml.dump(
            new_spec,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=100,
        )
        file_path.write_text(content, encoding="utf-8")

    def _generate_diff_text(self, old_value: Any, new_value: Any) -> str:
        """Generate a simple diff text for preview."""
        if old_value is None and new_value is not None:
            new_yaml = yaml.dump(
                new_value, allow_unicode=True, default_flow_style=False
            )
            lines = [f"+ {line}" for line in new_yaml.split("\n") if line]
            return "\n".join(lines)

        if old_value is not None and new_value is None:
            old_yaml = yaml.dump(
                old_value, allow_unicode=True, default_flow_style=False
            )
            lines = [f"- {line}" for line in old_yaml.split("\n") if line]
            return "\n".join(lines)

        # For modifications, show both
        old_yaml = yaml.dump(old_value, allow_unicode=True, default_flow_style=False)
        new_yaml = yaml.dump(new_value, allow_unicode=True, default_flow_style=False)

        old_lines = [f"- {line}" for line in old_yaml.split("\n") if line]
        new_lines = [f"+ {line}" for line in new_yaml.split("\n") if line]

        return "\n".join(old_lines + new_lines)
