"""Extractor for converting entities to YAML format."""

from pathlib import Path
from typing import Any

import yaml

from ..models.code_elements import CodeElements, Entity


class EntityExtractor:
    """Extract and convert entities to entities.yaml format."""

    def __init__(self, project_root: Path):
        """Initialize extractor with project root."""
        self.project_root = project_root

    def extract_to_entities_yaml(
        self,
        code_elements: CodeElements,
        existing_entities: dict[str, Any] | None = None,
        merge: bool = False,
    ) -> dict[str, Any]:
        """Convert extracted entities to entities.yaml format.

        Args:
            code_elements: Extracted code elements containing entities.
            existing_entities: Existing entities spec to merge with (if merge=True).
            merge: Whether to merge with existing spec.

        Returns:
            Entities specification dictionary.
        """
        if merge and existing_entities:
            spec = existing_entities.copy()
        else:
            spec = self._create_base_spec()

        # Ensure entities list exists
        if "entities" not in spec:
            spec["entities"] = []

        # Build lookup for existing entities
        existing_by_name: dict[str, int] = {}
        for idx, entity in enumerate(spec["entities"]):
            name = entity.get("schema")
            if name:
                existing_by_name[name] = idx

        # Add or update entities
        for entity in code_elements.entities:
            entity_dict = entity.to_dict()

            if entity.name in existing_by_name:
                if merge:
                    # Update existing entity
                    idx = existing_by_name[entity.name]
                    spec["entities"][idx] = self._merge_entity(
                        spec["entities"][idx], entity_dict
                    )
            else:
                # Add new entity
                spec["entities"].append(entity_dict)
                existing_by_name[entity.name] = len(spec["entities"]) - 1

        return spec

    def _create_base_spec(self) -> dict[str, Any]:
        """Create a base entities specification."""
        return {
            "version": "1.0",
            "last_updated": "YYYY-MM-DD",
            "entities": [],
        }

    def _merge_entity(
        self, existing: dict[str, Any], new: dict[str, Any]
    ) -> dict[str, Any]:
        """Merge new entity data into existing entity."""
        result = existing.copy()

        # Update basic fields
        if new.get("description"):
            result["description"] = new["description"]
        if new.get("table_name"):
            result["table_name"] = new["table_name"]

        # Merge fields
        existing_fields = {f["name"]: f for f in result.get("fields", [])}
        new_fields = {f["name"]: f for f in new.get("fields", [])}

        # Update existing fields and add new ones
        merged_fields = []
        for name, field in existing_fields.items():
            if name in new_fields:
                # Merge field data, preferring new values for type info
                merged_field = field.copy()
                merged_field.update(new_fields[name])
                merged_fields.append(merged_field)
            else:
                merged_fields.append(field)

        # Add completely new fields
        for name, field in new_fields.items():
            if name not in existing_fields:
                merged_fields.append(field)

        result["fields"] = merged_fields

        # Merge indexes
        if new.get("indexes"):
            existing_indexes = set(
                tuple(sorted(idx.get("fields", [])))
                for idx in result.get("indexes", [])
            )
            for idx in new["indexes"]:
                fields_tuple = tuple(sorted(idx.get("fields", [])))
                if fields_tuple not in existing_indexes:
                    if "indexes" not in result:
                        result["indexes"] = []
                    result["indexes"].append(idx)

        return result

    def to_yaml(self, spec: dict[str, Any]) -> str:
        """Convert entities spec to YAML string."""
        return yaml.dump(
            spec,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=100,
        )

    def load_existing_entities(self, file_path: Path) -> dict[str, Any] | None:
        """Load existing entities specification from file."""
        if not file_path.exists():
            return None

        try:
            content = file_path.read_text(encoding="utf-8")
            return yaml.safe_load(content)
        except (yaml.YAMLError, OSError):
            return None

    def get_entities_from_spec(self, spec: dict[str, Any]) -> list[Entity]:
        """Extract Entity objects from an entities.yaml spec."""
        entities = []

        for entity_dict in spec.get("entities", []):
            entity = Entity(
                name=entity_dict.get("schema", ""),
                table_name=entity_dict.get("table_name"),
                description=entity_dict.get("description"),
            )

            # Parse fields
            for field_dict in entity_dict.get("fields", []):
                from ..models.code_elements import EntityField

                enum_values = None
                if "enum" in field_dict:
                    enum_values = field_dict["enum"].get("values", [])

                field = EntityField(
                    name=field_dict.get("name", ""),
                    field_type=field_dict.get("type", "string"),
                    nullable=field_dict.get("nullable", True),
                    primary_key=field_dict.get("primary_key", False),
                    auto_generate=field_dict.get("auto_generate", False),
                    unique=field_dict.get("unique", False),
                    max_length=field_dict.get("max_length"),
                    default=field_dict.get("default"),
                    foreign_key=field_dict.get("foreign_key"),
                    enum_values=enum_values,
                    sensitive=field_dict.get("sensitive", False),
                    description=field_dict.get("description"),
                )
                entity.fields.append(field)

            # Parse indexes
            entity.indexes = entity_dict.get("indexes", [])

            # Parse validations
            entity.validations = entity_dict.get("validations", [])

            entities.append(entity)

        return entities
