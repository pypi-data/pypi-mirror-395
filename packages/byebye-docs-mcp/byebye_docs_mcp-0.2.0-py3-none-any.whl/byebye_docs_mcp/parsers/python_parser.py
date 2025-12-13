"""Python AST-based code parser."""

import ast
from pathlib import Path
from typing import Any, ClassVar

from ..models.code_elements import ApiEndpoint, CodeElements, Entity, EntityField
from .base import CodeParser, ParserRegistry


@ParserRegistry.register
class PythonParser(CodeParser):
    """Parser for Python source files using AST."""

    language: ClassVar[str] = "python"
    file_extensions: ClassVar[list[str]] = [".py"]

    # HTTP methods recognized in API frameworks
    HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}

    # Framework-specific decorator patterns
    API_DECORATORS = {
        # FastAPI patterns
        "app.get",
        "app.post",
        "app.put",
        "app.patch",
        "app.delete",
        "router.get",
        "router.post",
        "router.put",
        "router.patch",
        "router.delete",
        # Flask patterns
        "app.route",
        "blueprint.route",
        # Generic patterns
        "api.get",
        "api.post",
        "api.put",
        "api.patch",
        "api.delete",
    }

    # Base classes for entities
    ENTITY_BASE_CLASSES = {
        # SQLAlchemy
        "Base",
        "DeclarativeBase",
        "Model",
        "db.Model",
        # Pydantic
        "BaseModel",
        "BaseSettings",
        # dataclass (handled separately via decorator)
    }

    def parse_file(self, file_path: Path) -> CodeElements:
        """Parse a Python file and extract code elements."""
        result = CodeElements(language=self.language)
        result.source_files = [str(file_path)]

        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError):
            return result

        rel_path = str(file_path.relative_to(self.project_root))

        for node in ast.walk(tree):
            # Extract API endpoints from decorated functions
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                endpoints = self._extract_api_endpoints(node, rel_path)
                result.api_endpoints.extend(endpoints)

            # Extract entities from class definitions
            elif isinstance(node, ast.ClassDef):
                entity = self._extract_entity(node, rel_path)
                if entity:
                    result.entities.append(entity)

        return result

    def _extract_api_endpoints(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, file_path: str
    ) -> list[ApiEndpoint]:
        """Extract API endpoints from a function definition."""
        endpoints = []

        for decorator in node.decorator_list:
            endpoint = self._parse_api_decorator(decorator, node, file_path)
            if endpoint:
                endpoints.append(endpoint)

        return endpoints

    def _parse_api_decorator(
        self,
        decorator: ast.expr,
        func_node: ast.FunctionDef | ast.AsyncFunctionDef,
        file_path: str,
    ) -> ApiEndpoint | None:
        """Parse an API decorator and create an endpoint."""
        # Handle @app.get("/path") style decorators
        if isinstance(decorator, ast.Call):
            decorator_name = self._get_decorator_name(decorator.func)

            if decorator_name and self._is_api_decorator(decorator_name):
                method = self._extract_http_method(decorator_name)
                path = self._extract_path_from_decorator(decorator)

                if path:
                    # Extract docstring for summary/description
                    docstring = ast.get_docstring(func_node)
                    summary, description = self._parse_docstring(docstring)

                    # Extract parameters from function signature
                    parameters = self._extract_parameters(func_node, path)

                    return ApiEndpoint(
                        path=path,
                        method=method,
                        function_name=func_node.name,
                        file_path=file_path,
                        line_number=func_node.lineno,
                        summary=summary,
                        description=description,
                        parameters=parameters,
                    )

        # Handle @app.route("/path", methods=["GET", "POST"]) style
        if isinstance(decorator, ast.Call):
            decorator_name = self._get_decorator_name(decorator.func)
            if decorator_name and "route" in decorator_name.lower():
                path = self._extract_path_from_decorator(decorator)
                methods = self._extract_methods_from_route(decorator)

                if path:
                    docstring = ast.get_docstring(func_node)
                    summary, description = self._parse_docstring(docstring)
                    parameters = self._extract_parameters(func_node, path)

                    # Create an endpoint for each method
                    result = []
                    for method in methods or ["GET"]:
                        result.append(
                            ApiEndpoint(
                                path=path,
                                method=method.upper(),
                                function_name=func_node.name,
                                file_path=file_path,
                                line_number=func_node.lineno,
                                summary=summary,
                                description=description,
                                parameters=parameters,
                            )
                        )
                    return result[0] if len(result) == 1 else None

        return None

    def _get_decorator_name(self, node: ast.expr) -> str | None:
        """Get the full name of a decorator."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value_name = self._get_decorator_name(node.value)
            if value_name:
                return f"{value_name}.{node.attr}"
        return None

    def _is_api_decorator(self, name: str) -> bool:
        """Check if a decorator name is an API decorator."""
        name_lower = name.lower()
        # Check direct match
        if name_lower in self.API_DECORATORS:
            return True
        # Check pattern match (e.g., some_router.get)
        parts = name_lower.split(".")
        if len(parts) == 2 and parts[1] in self.HTTP_METHODS:
            return True
        return False

    def _extract_http_method(self, decorator_name: str) -> str:
        """Extract HTTP method from decorator name."""
        parts = decorator_name.split(".")
        if len(parts) >= 2:
            method = parts[-1].upper()
            if method in {m.upper() for m in self.HTTP_METHODS}:
                return method
        return "GET"

    def _extract_path_from_decorator(self, decorator: ast.Call) -> str | None:
        """Extract the path string from a decorator call."""
        if decorator.args:
            first_arg = decorator.args[0]
            if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
                return first_arg.value
        return None

    def _extract_methods_from_route(self, decorator: ast.Call) -> list[str] | None:
        """Extract methods from a route decorator."""
        for keyword in decorator.keywords:
            if keyword.arg == "methods":
                if isinstance(keyword.value, ast.List):
                    methods = []
                    for elt in keyword.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            methods.append(elt.value.upper())
                    return methods if methods else None
        return None

    def _parse_docstring(self, docstring: str | None) -> tuple[str | None, str | None]:
        """Parse docstring into summary and description."""
        if not docstring:
            return None, None

        lines = docstring.strip().split("\n")
        summary = lines[0].strip() if lines else None
        description = "\n".join(lines[1:]).strip() if len(lines) > 1 else None

        return summary, description if description else None

    def _extract_parameters(
        self, func_node: ast.FunctionDef | ast.AsyncFunctionDef, path: str
    ) -> list[dict[str, Any]]:
        """Extract parameters from function signature and path."""
        parameters = []

        # Extract path parameters from the path string
        import re

        path_params = re.findall(r"\{(\w+)\}", path)

        for param in path_params:
            parameters.append(
                {
                    "name": param,
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
            )

        # Extract query parameters from function arguments
        for arg in func_node.args.args:
            arg_name = arg.arg
            if arg_name in ("self", "cls", "request", "db", "session"):
                continue
            if arg_name in path_params:
                continue

            param_info: dict[str, Any] = {
                "name": arg_name,
                "in": "query",
                "required": arg.arg not in [
                    d.arg for d in func_node.args.defaults if hasattr(d, "arg")
                ],
                "schema": self._get_type_schema(arg.annotation),
            }
            parameters.append(param_info)

        return parameters

    def _get_type_schema(self, annotation: ast.expr | None) -> dict[str, Any]:
        """Convert a Python type annotation to OpenAPI schema."""
        if annotation is None:
            return {"type": "string"}

        if isinstance(annotation, ast.Name):
            type_map = {
                "str": {"type": "string"},
                "int": {"type": "integer"},
                "float": {"type": "number"},
                "bool": {"type": "boolean"},
                "list": {"type": "array"},
                "dict": {"type": "object"},
            }
            return type_map.get(annotation.id, {"type": "string"})

        if isinstance(annotation, ast.Constant):
            if isinstance(annotation.value, str):
                return {"type": "string"}

        return {"type": "string"}

    def _extract_entity(self, node: ast.ClassDef, file_path: str) -> Entity | None:
        """Extract entity information from a class definition."""
        # Check if this is an entity class
        is_entity = False
        is_dataclass = False

        # Check decorators for @dataclass
        for decorator in node.decorator_list:
            dec_name = self._get_decorator_name(decorator)
            if dec_name == "dataclass" or (
                isinstance(decorator, ast.Call)
                and self._get_decorator_name(decorator.func) == "dataclass"
            ):
                is_dataclass = True
                is_entity = True

        # Check base classes
        for base in node.bases:
            base_name = self._get_base_class_name(base)
            if base_name in self.ENTITY_BASE_CLASSES:
                is_entity = True
                break

        if not is_entity:
            return None

        # Extract docstring
        docstring = ast.get_docstring(node)

        # Extract table name (SQLAlchemy style)
        table_name = None
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id == "__tablename__":
                        if isinstance(item.value, ast.Constant):
                            table_name = item.value.value

        # Extract fields
        fields = self._extract_entity_fields(node, is_dataclass)

        if not fields:
            return None

        return Entity(
            name=node.name,
            table_name=table_name,
            file_path=file_path,
            line_number=node.lineno,
            description=docstring.split("\n")[0] if docstring else None,
            fields=fields,
        )

    def _get_base_class_name(self, base: ast.expr) -> str | None:
        """Get the name of a base class."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{self._get_base_class_name(base.value)}.{base.attr}"
        return None

    def _extract_entity_fields(self, node: ast.ClassDef, is_dataclass: bool) -> list[EntityField]:
        """Extract fields from an entity class."""
        fields = []

        for item in node.body:
            # Handle class-level assignments (SQLAlchemy style)
            if isinstance(item, ast.Assign):
                field = self._parse_sqlalchemy_field(item)
                if field:
                    fields.append(field)

            # Handle annotated assignments (Pydantic/dataclass style)
            elif isinstance(item, ast.AnnAssign):
                field = self._parse_annotated_field(item, is_dataclass)
                if field:
                    fields.append(field)

        return fields

    def _parse_sqlalchemy_field(self, node: ast.Assign) -> EntityField | None:
        """Parse a SQLAlchemy-style field definition."""
        if not node.targets or not isinstance(node.targets[0], ast.Name):
            return None

        field_name = node.targets[0].id
        if field_name.startswith("_"):
            return None

        # Check if it's a Column() call
        if not isinstance(node.value, ast.Call):
            return None

        func_name = self._get_decorator_name(node.value.func)
        if func_name not in ("Column", "mapped_column", "relationship"):
            return None

        if func_name == "relationship":
            return None  # Skip relationships for now

        # Extract column type and attributes
        field_type = "string"
        nullable = True
        primary_key = False
        unique = False
        max_length = None
        foreign_key = None

        if node.value.args:
            first_arg = node.value.args[0]
            field_type = self._parse_column_type(first_arg)

        for keyword in node.value.keywords:
            if keyword.arg == "primary_key":
                primary_key = self._get_bool_value(keyword.value)
            elif keyword.arg == "nullable":
                nullable = self._get_bool_value(keyword.value)
            elif keyword.arg == "unique":
                unique = self._get_bool_value(keyword.value)

        # Check for ForeignKey in args
        for arg in node.value.args:
            if isinstance(arg, ast.Call):
                fk_name = self._get_decorator_name(arg.func)
                if fk_name == "ForeignKey" and arg.args:
                    if isinstance(arg.args[0], ast.Constant):
                        fk_ref = arg.args[0].value
                        if "." in fk_ref:
                            table, field = fk_ref.rsplit(".", 1)
                            foreign_key = {"table": table, "field": field}

        return EntityField(
            name=field_name,
            field_type=field_type,
            nullable=nullable,
            primary_key=primary_key,
            unique=unique,
            max_length=max_length,
            foreign_key=foreign_key,
        )

    def _parse_annotated_field(self, node: ast.AnnAssign, is_dataclass: bool) -> EntityField | None:
        """Parse a type-annotated field (Pydantic/dataclass style)."""
        if not isinstance(node.target, ast.Name):
            return None

        field_name = node.target.id
        if field_name.startswith("_"):
            return None

        # Get the type from annotation
        field_type = self._annotation_to_field_type(node.annotation)
        nullable = self._is_optional_annotation(node.annotation)

        # Check for default value
        default = None
        if node.value is not None:
            if isinstance(node.value, ast.Constant):
                default = node.value.value

        return EntityField(
            name=field_name,
            field_type=field_type,
            nullable=nullable,
            default=default,
        )

    def _parse_column_type(self, type_node: ast.expr) -> str:
        """Parse SQLAlchemy column type to a simple type string."""
        if isinstance(type_node, ast.Name):
            type_map = {
                "Integer": "integer",
                "BigInteger": "integer",
                "SmallInteger": "integer",
                "String": "string",
                "Text": "text",
                "Boolean": "boolean",
                "Float": "float",
                "Numeric": "decimal",
                "DateTime": "datetime",
                "Date": "date",
                "Time": "time",
                "JSON": "json",
                "JSONB": "json",
                "UUID": "uuid",
                "LargeBinary": "binary",
            }
            return type_map.get(type_node.id, "string")

        elif isinstance(type_node, ast.Call):
            func_name = self._get_decorator_name(type_node.func)
            if func_name:
                return self._parse_column_type(type_node.func)
            # Check for String(length) pattern
            if isinstance(type_node.func, ast.Name):
                if type_node.func.id == "String" and type_node.args:
                    return "string"
                if type_node.func.id == "Enum":
                    return "enum"

        return "string"

    def _annotation_to_field_type(self, annotation: ast.expr) -> str:
        """Convert Python type annotation to field type."""
        if isinstance(annotation, ast.Name):
            type_map = {
                "str": "string",
                "int": "integer",
                "float": "float",
                "bool": "boolean",
                "datetime": "datetime",
                "date": "date",
                "UUID": "uuid",
                "dict": "json",
                "list": "array",
            }
            return type_map.get(annotation.id, "string")

        elif isinstance(annotation, ast.Subscript):
            # Handle Optional[X], List[X], etc.
            if isinstance(annotation.value, ast.Name):
                if annotation.value.id in ("Optional", "Union"):
                    if isinstance(annotation.slice, ast.Tuple):
                        # Union[X, None]
                        for elt in annotation.slice.elts:
                            if not (isinstance(elt, ast.Constant) and elt.value is None):
                                return self._annotation_to_field_type(elt)
                    else:
                        return self._annotation_to_field_type(annotation.slice)
                elif annotation.value.id == "List":
                    return "array"
                elif annotation.value.id == "Dict":
                    return "json"

        elif isinstance(annotation, ast.Attribute):
            # Handle datetime.datetime, uuid.UUID, etc.
            return annotation.attr.lower()

        return "string"

    def _is_optional_annotation(self, annotation: ast.expr) -> bool:
        """Check if a type annotation is Optional."""
        if isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name):
                if annotation.value.id == "Optional":
                    return True
                if annotation.value.id == "Union":
                    # Check if None is in the union
                    if isinstance(annotation.slice, ast.Tuple):
                        for elt in annotation.slice.elts:
                            if isinstance(elt, ast.Constant) and elt.value is None:
                                return True
        return False

    def _get_bool_value(self, node: ast.expr) -> bool:
        """Extract boolean value from an AST node."""
        if isinstance(node, ast.Constant):
            return bool(node.value)
        if isinstance(node, ast.Name):
            return node.id == "True"
        return False
