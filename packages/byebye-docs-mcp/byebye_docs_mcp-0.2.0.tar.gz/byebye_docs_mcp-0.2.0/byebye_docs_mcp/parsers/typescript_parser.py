"""TypeScript/JavaScript code parser using regex patterns."""

import re
from pathlib import Path
from typing import Any, ClassVar

from ..models.code_elements import ApiEndpoint, CodeElements, Entity, EntityField
from .base import CodeParser, ParserRegistry


@ParserRegistry.register
class TypeScriptParser(CodeParser):
    """Parser for TypeScript/JavaScript source files using regex patterns.

    Supports:
    - Express.js routes (app.get, router.post, etc.)
    - NestJS decorators (@Get, @Post, @Controller, etc.)
    - TypeORM entities (@Entity, @Column, etc.)
    - Prisma models (from schema inspection)
    - TypeScript interfaces and type definitions
    """

    language: ClassVar[str] = "typescript"
    file_extensions: ClassVar[list[str]] = [".ts", ".tsx", ".js", ".jsx", ".mjs"]

    # HTTP methods
    HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}

    # Express-style route patterns
    EXPRESS_ROUTE_PATTERN = re.compile(
        r"(?:app|router|route)\s*\.\s*(get|post|put|patch|delete|head|options)\s*\("
        r"\s*['\"`]([^'\"`]+)['\"`]",
        re.IGNORECASE,
    )

    # NestJS decorator patterns
    NESTJS_ROUTE_PATTERN = re.compile(
        r"@(Get|Post|Put|Patch|Delete|Head|Options)\s*\(\s*['\"`]?([^'\"`\)]*)['\"`]?\s*\)",
        re.IGNORECASE,
    )

    # NestJS Controller decorator
    NESTJS_CONTROLLER_PATTERN = re.compile(
        r"@Controller\s*\(\s*['\"`]([^'\"`]*)['\"`]\s*\)",
        re.IGNORECASE,
    )

    # Function/method patterns (for endpoint names)
    FUNCTION_PATTERN = re.compile(
        r"(?:async\s+)?(?:function\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{",
    )

    # Arrow function patterns
    ARROW_FUNCTION_PATTERN = re.compile(
        r"(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*(?::\s*[^=]+)?\s*=>",
    )

    # TypeORM Entity decorator
    TYPEORM_ENTITY_PATTERN = re.compile(
        r"@Entity\s*\(\s*(?:['\"`]([^'\"`]*)['\"`])?\s*\)",
        re.IGNORECASE,
    )

    # TypeORM Column patterns
    TYPEORM_COLUMN_PATTERN = re.compile(
        r"@(Column|PrimaryGeneratedColumn|PrimaryColumn|CreateDateColumn|UpdateDateColumn)"
        r"\s*\(\s*(?:\{([^}]*)\}|['\"`]?([^'\"`\)]*)['\"`]?)?\s*\)\s*\n?\s*(\w+)\s*[!?]?\s*:\s*([^;=]+)",
        re.IGNORECASE,
    )

    # TypeScript interface pattern
    INTERFACE_PATTERN = re.compile(
        r"(?:export\s+)?interface\s+(\w+)\s*(?:extends\s+[^{]+)?\s*\{([^}]+)\}",
        re.MULTILINE | re.DOTALL,
    )

    # TypeScript type alias pattern
    TYPE_ALIAS_PATTERN = re.compile(
        r"(?:export\s+)?type\s+(\w+)\s*=\s*\{([^}]+)\}",
        re.MULTILINE | re.DOTALL,
    )

    # TypeScript class pattern
    CLASS_PATTERN = re.compile(
        r"(?:export\s+)?(?:abstract\s+)?class\s+(\w+)\s*(?:extends\s+(\w+))?\s*"
        r"(?:implements\s+[^{]+)?\s*\{",
        re.MULTILINE,
    )

    # Property pattern (for interfaces, types, classes)
    PROPERTY_PATTERN = re.compile(
        r"^\s*(?:readonly\s+)?(\w+)\s*[?!]?\s*:\s*([^;,\n]+)",
        re.MULTILINE,
    )

    # Prisma model pattern (for .prisma files)
    PRISMA_MODEL_PATTERN = re.compile(
        r"model\s+(\w+)\s*\{([^}]+)\}",
        re.MULTILINE | re.DOTALL,
    )

    PRISMA_FIELD_PATTERN = re.compile(
        r"^\s*(\w+)\s+(\w+)(\[\])?\s*(\?)?\s*(@[^\n]+)?",
        re.MULTILINE,
    )

    def __init__(self, project_root: Path):
        """Initialize parser with project root path."""
        super().__init__(project_root)
        # Prisma schema file extension
        self.file_extensions = list(self.file_extensions) + [".prisma"]

    def parse_file(self, file_path: Path) -> CodeElements:
        """Parse a TypeScript/JavaScript file and extract code elements."""
        result = CodeElements(language=self.language)
        result.source_files = [str(file_path)]

        try:
            content = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return result

        rel_path = str(file_path.relative_to(self.project_root))

        # Handle Prisma schema files
        if file_path.suffix == ".prisma":
            entities = self._extract_prisma_models(content, rel_path)
            result.entities.extend(entities)
            return result

        # Extract API endpoints
        endpoints = self._extract_api_endpoints(content, rel_path)
        result.api_endpoints.extend(endpoints)

        # Extract entities
        entities = self._extract_entities(content, rel_path)
        result.entities.extend(entities)

        return result

    def _extract_api_endpoints(self, content: str, file_path: str) -> list[ApiEndpoint]:
        """Extract API endpoints from file content."""
        endpoints = []

        # Get base path from NestJS Controller if present
        controller_match = self.NESTJS_CONTROLLER_PATTERN.search(content)
        base_path = controller_match.group(1) if controller_match else ""

        # Extract Express-style routes
        for match in self.EXPRESS_ROUTE_PATTERN.finditer(content):
            method = match.group(1).upper()
            path = match.group(2)
            line_number = content[: match.start()].count("\n") + 1

            # Try to find the function name
            function_name = self._find_function_name(content, match.end())

            endpoints.append(
                ApiEndpoint(
                    path=path,
                    method=method,
                    function_name=function_name or "anonymous",
                    file_path=file_path,
                    line_number=line_number,
                    parameters=self._extract_path_params(path),
                )
            )

        # Extract NestJS-style routes
        for match in self.NESTJS_ROUTE_PATTERN.finditer(content):
            method = match.group(1).upper()
            path = match.group(2) or ""
            full_path = f"/{base_path}/{path}".replace("//", "/").rstrip("/") or "/"
            line_number = content[: match.start()].count("\n") + 1

            # Try to find the method name (next function after decorator)
            function_name = self._find_function_name(content, match.end())

            endpoints.append(
                ApiEndpoint(
                    path=full_path,
                    method=method,
                    function_name=function_name or "anonymous",
                    file_path=file_path,
                    line_number=line_number,
                    parameters=self._extract_path_params(full_path),
                )
            )

        return endpoints

    def _find_function_name(self, content: str, start_pos: int) -> str | None:
        """Find the function name after a given position."""
        # Look for function definition within next 500 characters
        search_content = content[start_pos : start_pos + 500]

        # Try regular function
        func_match = self.FUNCTION_PATTERN.search(search_content)
        if func_match:
            return func_match.group(1)

        # Try arrow function
        arrow_match = self.ARROW_FUNCTION_PATTERN.search(search_content)
        if arrow_match:
            return arrow_match.group(1)

        # Try method definition (methodName() or async methodName())
        method_pattern = re.compile(r"(?:async\s+)?(\w+)\s*\([^)]*\)")
        method_match = method_pattern.search(search_content)
        if method_match:
            name = method_match.group(1)
            if name not in ("if", "for", "while", "switch", "catch", "function"):
                return name

        return None

    def _extract_path_params(self, path: str) -> list[dict[str, Any]]:
        """Extract path parameters from a route path."""
        parameters = []

        # Express-style :param
        for match in re.finditer(r":(\w+)", path):
            parameters.append(
                {
                    "name": match.group(1),
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
            )

        # NestJS-style :param or {param}
        for match in re.finditer(r"\{(\w+)\}", path):
            param_name = match.group(1)
            if not any(p["name"] == param_name for p in parameters):
                parameters.append(
                    {
                        "name": param_name,
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                )

        return parameters

    def _extract_entities(self, content: str, file_path: str) -> list[Entity]:
        """Extract entity definitions from file content."""
        entities = []

        # Extract TypeORM entities
        entities.extend(self._extract_typeorm_entities(content, file_path))

        # Extract TypeScript interfaces (likely data models)
        entities.extend(self._extract_interfaces(content, file_path))

        # Extract type aliases that look like models
        entities.extend(self._extract_type_aliases(content, file_path))

        return entities

    def _extract_typeorm_entities(self, content: str, file_path: str) -> list[Entity]:
        """Extract TypeORM entity definitions."""
        entities = []

        # Find @Entity decorators and their associated classes
        entity_matches = list(self.TYPEORM_ENTITY_PATTERN.finditer(content))

        for entity_match in entity_matches:
            table_name = entity_match.group(1) if entity_match.group(1) else None
            entity_start = entity_match.start()
            line_number = content[:entity_start].count("\n") + 1

            # Find the class definition after the @Entity decorator
            class_search = content[entity_match.end() :]
            class_match = self.CLASS_PATTERN.search(class_search)

            if not class_match:
                continue

            class_name = class_match.group(1)
            class_start = entity_match.end() + class_match.start()

            # Find class body (content between { and matching })
            class_body_start = content.find("{", class_start)
            if class_body_start == -1:
                continue

            class_body = self._extract_balanced_braces(content[class_body_start:])

            # Extract columns
            fields = self._extract_typeorm_columns(class_body)

            if fields:
                entities.append(
                    Entity(
                        name=class_name,
                        table_name=table_name or self._to_snake_case(class_name),
                        file_path=file_path,
                        line_number=line_number,
                        fields=fields,
                    )
                )

        return entities

    def _extract_typeorm_columns(self, class_body: str) -> list[EntityField]:
        """Extract column definitions from TypeORM entity class body."""
        fields = []

        for match in self.TYPEORM_COLUMN_PATTERN.finditer(class_body):
            decorator_type = match.group(1)
            options_str = match.group(2) or ""
            type_arg = match.group(3) or ""
            field_name = match.group(4)
            ts_type = match.group(5).strip()

            # Determine field type
            field_type = self._ts_type_to_field_type(ts_type)
            if type_arg:
                field_type = self._column_type_to_field_type(type_arg)

            # Parse options
            nullable = "nullable: true" in options_str or "nullable:true" in options_str
            unique = "unique: true" in options_str or "unique:true" in options_str
            primary_key = decorator_type.lower() in (
                "primarygeneratedcolumn",
                "primarycolumn",
            )
            auto_generate = decorator_type.lower() == "primarygeneratedcolumn"

            fields.append(
                EntityField(
                    name=field_name,
                    field_type=field_type,
                    nullable=nullable,
                    primary_key=primary_key,
                    auto_generate=auto_generate,
                    unique=unique,
                )
            )

        return fields

    def _extract_interfaces(self, content: str, file_path: str) -> list[Entity]:
        """Extract TypeScript interface definitions."""
        entities = []

        # Only extract interfaces that look like data models
        model_suffixes = ("Model", "Entity", "Schema", "Record", "Data", "Dto", "DTO")

        for match in self.INTERFACE_PATTERN.finditer(content):
            interface_name = match.group(1)
            interface_body = match.group(2)
            line_number = content[: match.start()].count("\n") + 1

            # Skip interfaces that don't look like data models
            if not any(interface_name.endswith(suffix) for suffix in model_suffixes):
                # Also check if it has at least 2 properties (likely a model)
                props = self.PROPERTY_PATTERN.findall(interface_body)
                if len(props) < 2:
                    continue

            # Extract fields
            fields = self._extract_interface_fields(interface_body)

            if fields:
                entities.append(
                    Entity(
                        name=interface_name,
                        file_path=file_path,
                        line_number=line_number,
                        fields=fields,
                    )
                )

        return entities

    def _extract_interface_fields(self, body: str) -> list[EntityField]:
        """Extract fields from interface/type body."""
        fields = []

        for match in self.PROPERTY_PATTERN.finditer(body):
            field_name = match.group(1)
            ts_type = match.group(2).strip()

            # Skip methods
            if "(" in ts_type and "=>" in ts_type:
                continue

            nullable = "?" in body.split(field_name)[0][-5:] if field_name in body else False
            field_type = self._ts_type_to_field_type(ts_type)

            fields.append(
                EntityField(
                    name=field_name,
                    field_type=field_type,
                    nullable=nullable or "null" in ts_type.lower(),
                )
            )

        return fields

    def _extract_type_aliases(self, content: str, file_path: str) -> list[Entity]:
        """Extract TypeScript type alias definitions that look like models."""
        entities = []

        model_suffixes = ("Model", "Entity", "Schema", "Record", "Data", "Dto", "DTO")

        for match in self.TYPE_ALIAS_PATTERN.finditer(content):
            type_name = match.group(1)
            type_body = match.group(2)
            line_number = content[: match.start()].count("\n") + 1

            # Only include types that look like data models
            if not any(type_name.endswith(suffix) for suffix in model_suffixes):
                props = self.PROPERTY_PATTERN.findall(type_body)
                if len(props) < 2:
                    continue

            fields = self._extract_interface_fields(type_body)

            if fields:
                entities.append(
                    Entity(
                        name=type_name,
                        file_path=file_path,
                        line_number=line_number,
                        fields=fields,
                    )
                )

        return entities

    def _extract_prisma_models(self, content: str, file_path: str) -> list[Entity]:
        """Extract Prisma model definitions from schema file."""
        entities = []

        for match in self.PRISMA_MODEL_PATTERN.finditer(content):
            model_name = match.group(1)
            model_body = match.group(2)
            line_number = content[: match.start()].count("\n") + 1

            fields = self._extract_prisma_fields(model_body)

            if fields:
                entities.append(
                    Entity(
                        name=model_name,
                        table_name=self._to_snake_case(model_name),
                        file_path=file_path,
                        line_number=line_number,
                        fields=fields,
                    )
                )

        return entities

    def _extract_prisma_fields(self, body: str) -> list[EntityField]:
        """Extract fields from Prisma model body."""
        fields = []

        for match in self.PRISMA_FIELD_PATTERN.finditer(body):
            field_name = match.group(1)
            prisma_type = match.group(2)
            is_array = match.group(3) is not None
            is_optional = match.group(4) is not None
            attributes = match.group(5) or ""

            # Skip relation fields
            if prisma_type[0].isupper() and "@relation" in attributes:
                continue

            field_type = self._prisma_type_to_field_type(prisma_type)
            if is_array:
                field_type = "array"

            primary_key = "@id" in attributes
            unique = "@unique" in attributes
            auto_generate = (
                "@default(autoincrement())" in attributes or "@default(uuid())" in attributes
            )

            # Extract foreign key
            foreign_key = None
            fk_match = re.search(r"@relation\([^)]*references:\s*\[(\w+)\]", attributes)
            if fk_match:
                # This is the referencing side
                pass

            fields.append(
                EntityField(
                    name=field_name,
                    field_type=field_type,
                    nullable=is_optional,
                    primary_key=primary_key,
                    auto_generate=auto_generate,
                    unique=unique,
                    foreign_key=foreign_key,
                )
            )

        return fields

    def _ts_type_to_field_type(self, ts_type: str) -> str:
        """Convert TypeScript type to field type."""
        ts_type = ts_type.strip().lower()

        # Remove generic parameters
        if "<" in ts_type:
            ts_type = ts_type.split("<")[0]

        # Remove union with null/undefined
        ts_type = re.sub(r"\s*\|\s*(null|undefined)", "", ts_type)

        type_map = {
            "string": "string",
            "number": "integer",
            "boolean": "boolean",
            "date": "datetime",
            "bigint": "integer",
            "object": "json",
            "any": "json",
            "array": "array",
            "buffer": "binary",
        }

        for key, value in type_map.items():
            if key in ts_type:
                return value

        return "string"

    def _column_type_to_field_type(self, col_type: str) -> str:
        """Convert TypeORM column type to field type."""
        col_type = col_type.strip().lower()

        type_map = {
            "varchar": "string",
            "text": "text",
            "int": "integer",
            "integer": "integer",
            "bigint": "integer",
            "float": "float",
            "double": "float",
            "decimal": "decimal",
            "boolean": "boolean",
            "bool": "boolean",
            "date": "date",
            "datetime": "datetime",
            "timestamp": "datetime",
            "time": "time",
            "json": "json",
            "jsonb": "json",
            "uuid": "uuid",
            "bytea": "binary",
            "blob": "binary",
        }

        for key, value in type_map.items():
            if key in col_type:
                return value

        return "string"

    def _prisma_type_to_field_type(self, prisma_type: str) -> str:
        """Convert Prisma type to field type."""
        type_map = {
            "String": "string",
            "Int": "integer",
            "BigInt": "integer",
            "Float": "float",
            "Decimal": "decimal",
            "Boolean": "boolean",
            "DateTime": "datetime",
            "Json": "json",
            "Bytes": "binary",
        }
        return type_map.get(prisma_type, "string")

    def _to_snake_case(self, name: str) -> str:
        """Convert CamelCase to snake_case."""
        result = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
        result = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", result)
        return result.lower()

    def _extract_balanced_braces(self, content: str) -> str:
        """Extract content within balanced braces."""
        if not content or content[0] != "{":
            return ""

        depth = 0
        for i, char in enumerate(content):
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return content[1:i]

        return content[1:]
