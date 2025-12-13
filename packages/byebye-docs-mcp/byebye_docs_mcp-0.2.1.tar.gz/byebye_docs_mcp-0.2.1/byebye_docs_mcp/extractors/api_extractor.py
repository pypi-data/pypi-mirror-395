"""Extractor for converting API endpoints to OpenAPI format."""

from pathlib import Path
from typing import Any

import yaml

from ..models.code_elements import ApiEndpoint, CodeElements


class ApiExtractor:
    """Extract and convert API endpoints to OpenAPI YAML format."""

    def __init__(self, project_root: Path):
        """Initialize extractor with project root."""
        self.project_root = project_root

    def extract_to_openapi(
        self,
        code_elements: CodeElements,
        existing_spec: dict[str, Any] | None = None,
        merge: bool = False,
    ) -> dict[str, Any]:
        """Convert extracted API endpoints to OpenAPI specification.

        Args:
            code_elements: Extracted code elements containing API endpoints.
            existing_spec: Existing OpenAPI spec to merge with (if merge=True).
            merge: Whether to merge with existing spec.

        Returns:
            OpenAPI specification dictionary.
        """
        if merge and existing_spec:
            spec = existing_spec.copy()
        else:
            spec = self._create_base_spec()

        # Ensure paths exists
        if "paths" not in spec:
            spec["paths"] = {}

        # Ensure components exists
        if "components" not in spec:
            spec["components"] = {"schemas": {}, "responses": {}}

        # Add endpoints
        for endpoint in code_elements.api_endpoints:
            self._add_endpoint_to_spec(spec, endpoint, merge)

        return spec

    def _create_base_spec(self) -> dict[str, Any]:
        """Create a base OpenAPI specification."""
        return {
            "openapi": "3.0.3",
            "info": {
                "title": "API Specification",
                "description": "Auto-generated from code",
                "version": "1.0.0",
            },
            "servers": [
                {"url": "http://localhost:8000", "description": "Development server"}
            ],
            "paths": {},
            "components": {
                "schemas": {},
                "responses": {
                    "BadRequest": {
                        "description": "リクエスト不正",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        },
                    },
                    "NotFound": {
                        "description": "リソース未発見",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        },
                    },
                    "InternalError": {
                        "description": "サーバーエラー",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        },
                    },
                },
            },
        }

    def _add_endpoint_to_spec(
        self, spec: dict[str, Any], endpoint: ApiEndpoint, merge: bool
    ) -> None:
        """Add an endpoint to the OpenAPI specification."""
        path = endpoint.path
        method = endpoint.method.lower()

        # Initialize path if not exists
        if path not in spec["paths"]:
            spec["paths"][path] = {}

        # Skip if already exists and not merging
        if method in spec["paths"][path] and not merge:
            return

        # Build operation object
        operation: dict[str, Any] = {
            "operationId": endpoint.function_name,
        }

        if endpoint.summary:
            operation["summary"] = endpoint.summary
        if endpoint.description:
            operation["description"] = endpoint.description
        if endpoint.tags:
            operation["tags"] = endpoint.tags

        # Add parameters
        if endpoint.parameters:
            operation["parameters"] = endpoint.parameters

        # Add request body for methods that support it
        if method in ("post", "put", "patch") and endpoint.request_body:
            operation["requestBody"] = endpoint.request_body

        # Add default responses
        operation["responses"] = endpoint.responses or self._default_responses(method)

        # Set the operation
        spec["paths"][path][method] = operation

    def _default_responses(self, method: str) -> dict[str, Any]:
        """Generate default responses for an HTTP method."""
        responses: dict[str, Any] = {
            "200": {
                "description": "成功",
                "content": {"application/json": {"schema": {"type": "object"}}},
            }
        }

        if method == "post":
            responses["201"] = {
                "description": "作成成功",
                "content": {"application/json": {"schema": {"type": "object"}}},
            }
            del responses["200"]

        responses["400"] = {"$ref": "#/components/responses/BadRequest"}
        responses["500"] = {"$ref": "#/components/responses/InternalError"}

        return responses

    def to_yaml(self, spec: dict[str, Any]) -> str:
        """Convert OpenAPI spec to YAML string."""
        return yaml.dump(
            spec,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=100,
        )

    def load_existing_spec(self, file_path: Path) -> dict[str, Any] | None:
        """Load existing OpenAPI specification from file."""
        if not file_path.exists():
            return None

        try:
            content = file_path.read_text(encoding="utf-8")
            return yaml.safe_load(content)
        except (yaml.YAMLError, OSError):
            return None

    def get_endpoints_from_spec(self, spec: dict[str, Any]) -> list[ApiEndpoint]:
        """Extract ApiEndpoint objects from an OpenAPI spec."""
        endpoints = []

        paths = spec.get("paths", {})
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.upper() not in ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"):
                    continue

                endpoint = ApiEndpoint(
                    path=path,
                    method=method.upper(),
                    function_name=operation.get("operationId", ""),
                    file_path="",  # Not available from spec
                    line_number=0,
                    summary=operation.get("summary"),
                    description=operation.get("description"),
                    parameters=operation.get("parameters", []),
                    request_body=operation.get("requestBody"),
                    responses=operation.get("responses", {}),
                    tags=operation.get("tags", []),
                )
                endpoints.append(endpoint)

        return endpoints
