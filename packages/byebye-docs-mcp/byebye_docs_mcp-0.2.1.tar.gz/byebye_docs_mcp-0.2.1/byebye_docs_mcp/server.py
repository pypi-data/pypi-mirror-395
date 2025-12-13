"""Byebye Docs MCP Server implementation."""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    Resource,
    TextContent,
    Tool,
)

from .core import DiffEngine, SyncManager
from .extractors import ApiExtractor, EntityExtractor
from .parsers import ParserRegistry

# Template structure definition (AI-optimized flat structure)
TEMPLATE_STRUCTURE = {
    ".agent": {
        "manifest.yaml": {"required": True, "description": "ファイルインデックス・タスクルーティング"},
        "context.yaml": {"required": True, "description": "プロダクト情報（ビジョン、要件、KPI）"},
        "architecture.yaml": {"required": True, "description": "システム設計（コンポーネント、ドメインモデル）"},
        "constraints.yaml": {"required": True, "description": "制約・禁止事項・セキュリティポリシー"},
        "codegen.yaml": {"required": True, "description": "コード生成ルール（言語規約、テスト、コミット）"},
        "schemas": {
            "api.yaml": {"required": False, "description": "OpenAPI仕様"},
            "entities.yaml": {"required": False, "description": "エンティティ定義"},
        },
    },
}

# Document schemas for validation (AI-optimized structure)
DOCUMENT_SCHEMAS = {
    "manifest.yaml": {
        "type": "object",
        "required": ["version", "files"],
        "properties": {
            "version": {"type": "string"},
            "files": {"type": "object"},
            "task_routing": {"type": "object"},
        },
    },
    "context.yaml": {
        "type": "object",
        "required": ["version", "product"],
        "properties": {
            "version": {"type": "string"},
            "product": {"type": "object"},
            "requirements": {"type": "array"},
            "kpis": {"type": "array"},
        },
    },
    "architecture.yaml": {
        "type": "object",
        "required": ["version", "system"],
        "properties": {
            "version": {"type": "string"},
            "system": {"type": "object"},
            "components": {"type": "object"},
            "domain_model": {"type": "object"},
        },
    },
    "constraints.yaml": {
        "type": "object",
        "required": ["version", "security"],
        "properties": {
            "version": {"type": "string"},
            "security": {"type": "object"},
            "file_policy": {"type": "object"},
            "escalation": {"type": "object"},
            "roles": {"type": "object"},
        },
    },
    "codegen.yaml": {
        "type": "object",
        "required": ["version", "languages"],
        "properties": {
            "version": {"type": "string"},
            "languages": {"type": "object"},
            "testing": {"type": "object"},
            "commit": {"type": "object"},
        },
    },
}


def get_project_root() -> Path:
    """Get the project root directory from environment or current directory."""
    env_path = os.environ.get("BYEBYE_DOCS_PROJECT_PATH")
    if env_path:
        return Path(env_path)
    return Path.cwd()


def flatten_structure(
    structure: dict[str, Any], prefix: str = ""
) -> list[dict[str, Any]]:
    """Flatten nested structure into a list of file entries."""
    result = []
    for key, value in structure.items():
        path = f"{prefix}/{key}" if prefix else key
        if isinstance(value, dict) and "required" in value:
            result.append({"path": path, **value})
        elif isinstance(value, dict):
            result.extend(flatten_structure(value, path))
    return result


def list_existing_docs(project_root: Path) -> list[dict[str, Any]]:
    """List all existing documentation files in the project."""
    docs = []
    agent_dir = project_root / ".agent"

    if not agent_dir.exists():
        return docs

    for file_path in agent_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix in (".yaml", ".yml"):
            rel_path = file_path.relative_to(project_root)
            stat = file_path.stat()
            docs.append({
                "path": str(rel_path),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })

    return sorted(docs, key=lambda x: x["path"])


def get_project_info(project_root: Path) -> dict[str, Any]:
    """Get current project information."""
    info = {
        "root": str(project_root),
        "exists": project_root.exists(),
        "docs_count": 0,
        "has_claude_md": False,
        "has_agent_dir": False,
        "agent_files": [],
    }

    if not project_root.exists():
        return info

    # Check for CLAUDE.md
    info["has_claude_md"] = (project_root / "CLAUDE.md").exists()

    # Check for .agent directory
    agent_dir = project_root / ".agent"
    if agent_dir.exists():
        info["has_agent_dir"] = True
        agent_files = []
        for item in agent_dir.rglob("*.yaml"):
            if item.is_file():
                agent_files.append(str(item.relative_to(project_root)))
        info["agent_files"] = sorted(agent_files)
        info["docs_count"] = len(agent_files)

    return info


def read_document_content(project_root: Path, doc_path: str) -> str | None:
    """Read content of a document file."""
    full_path = project_root / doc_path
    if full_path.exists() and full_path.is_file():
        return full_path.read_text(encoding="utf-8")
    return None


def extract_section(content: str, section_name: str) -> str | None:
    """Extract a specific section from markdown content."""
    # Pattern to match markdown headers
    pattern = rf"^##\s+{re.escape(section_name)}\s*$"
    lines = content.split("\n")

    in_section = False
    section_lines = []

    for line in lines:
        if re.match(pattern, line, re.IGNORECASE):
            in_section = True
            section_lines.append(line)
        elif in_section:
            if re.match(r"^##\s+", line):
                break
            section_lines.append(line)

    if section_lines:
        return "\n".join(section_lines).strip()
    return None


def validate_yaml_document(
    content: str, schema_name: str
) -> dict[str, Any]:
    """Validate a YAML document against its schema."""
    result = {"valid": True, "errors": [], "warnings": []}

    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        result["valid"] = False
        result["errors"].append(f"YAML parse error: {e}")
        return result

    if schema_name not in DOCUMENT_SCHEMAS:
        result["warnings"].append(f"No schema defined for {schema_name}")
        return result

    schema = DOCUMENT_SCHEMAS[schema_name]

    # Basic validation
    if schema.get("type") == "object" and not isinstance(data, dict):
        result["valid"] = False
        result["errors"].append("Document must be an object")
        return result

    for required_field in schema.get("required", []):
        if required_field not in data:
            result["valid"] = False
            result["errors"].append(f"Missing required field: {required_field}")

    return result


def validate_markdown_document(content: str, doc_type: str) -> dict[str, Any]:
    """Validate a markdown document structure."""
    result = {"valid": True, "errors": [], "warnings": []}

    # Check for required sections based on doc type
    required_sections = {
        "vision.md": ["プロダクトの目的", "解決したい課題", "ターゲットユーザー"],
        "system_overview.md": ["システム全体図", "コンポーネント構成"],
        "coding_standards.md": ["言語別の基準"],
    }

    if doc_type in required_sections:
        for section in required_sections[doc_type]:
            if section not in content:
                result["warnings"].append(f"Missing section: {section}")

    # Check for update metadata
    if "_最終更新日:" not in content:
        result["warnings"].append("Missing update date metadata")

    return result


def get_template_for_doc(doc_type: str) -> str | None:
    """Get a template for creating a new document."""
    templates = {
        "manifest.yaml": """version: "2.0"
format: ai-optimized

files:
  context:
    path: context.yaml
    priority: 1
    description: product vision, requirements, kpis
  architecture:
    path: architecture.yaml
    priority: 2
    description: system design, components, domain model
  constraints:
    path: constraints.yaml
    priority: 1
    description: security, file policy, escalation rules
  codegen:
    path: codegen.yaml
    priority: 2
    description: coding standards, testing, commit rules
  api:
    path: schemas/api.yaml
    priority: 3
    on_demand: true
    description: OpenAPI specification
  entities:
    path: schemas/entities.yaml
    priority: 3
    on_demand: true
    description: database entity definitions

task_routing:
  implement_feature:
    files: [context, architecture, codegen]
  fix_bug:
    files: [architecture, codegen, constraints]
  add_api:
    files: [api, entities, codegen]
  security_review:
    files: [constraints]

read_order:
  - constraints
  - codegen
  - context
  - architecture
""",
        "context.yaml": """version: "1.0"

product:
  name: "[PROJECT_NAME]"
  vision: "[ONE_LINE_VISION]"

requirements:
  - id: F001
    name: "[FEATURE_NAME]"
    priority: high
    status: draft
    acceptance:
      - "[CRITERIA_1]"

kpis:
  - metric: "[METRIC_NAME]"
    target: "[TARGET_VALUE]"
""",
        "architecture.yaml": """version: "1.0"

system:
  name: "[SYSTEM_NAME]"
  type: "[web_app|api|cli|library]"

components:
  frontend: []
  backend: []
  data: []

domain_model:
  aggregates: []
  relationships: []
""",
        "constraints.yaml": """version: "1.0"

security:
  critical:
    - id: SEC001
      action: deny
      pattern: "**/.env*"
      reason: credentials exposure

file_policy:
  editable:
    - "src/**/*"
    - "tests/**/*"
  forbidden:
    - ".env*"
    - "credentials.*"

escalation:
  mandatory:
    - database_schema_change
    - public_api_change
    - security_config_change

roles:
  developer:
    permissions:
      read: [source_code, tests, docs]
      write: [source_code, tests]
      execute: [tests, linters]
""",
        "codegen.yaml": """version: "1.0"

languages:
  typescript:
    style: airbnb
    formatter: prettier
    linter: eslint
    indent: 2
    max_line: 100

testing:
  required: true
  coverage_min: 80

commit:
  format: "<type>(<scope>): <subject>"
  types: [feat, fix, docs, refactor, test, chore]
""",
        "schemas/api.yaml": """openapi: 3.0.3
info:
  title: "[PROJECT_NAME] API"
  description: API definition
  version: 1.0.0

servers:
  - url: http://localhost:3000/v1
    description: Development server

paths:
  /example:
    get:
      summary: Example endpoint
      operationId: getExample
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string

components:
  schemas:
    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
""",
        "schemas/entities.yaml": """version: "1.0"
last_updated: "[DATE]"

entities:
  - schema: "[EntityName]"
    description: "[Description]"
    table_name: "[table_name]"
    fields:
      - name: id
        type: uuid
        primary_key: true
        auto_generate: true
        description: "Primary key"

      - name: created_at
        type: datetime
        auto_now_add: true
        nullable: false

      - name: updated_at
        type: datetime
        auto_now: true
        nullable: false

    indexes:
      - fields: [id]
        unique: true
""",
    }

    return templates.get(doc_type)


# Create MCP server
server = Server("byebye-docs")


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="template://structure",
            name="Template Structure",
            description="テンプレートの構造情報（どのセクションがあるか、必須項目は何か）",
            mimeType="application/json",
        ),
        Resource(
            uri="template://schema",
            name="Document Schemas",
            description="各ドキュメントの検証スキーマ",
            mimeType="application/json",
        ),
        Resource(
            uri="project://current",
            name="Current Project",
            description="現在のプロジェクト情報",
            mimeType="application/json",
        ),
        Resource(
            uri="docs://list",
            name="Document List",
            description="プロジェクト内の既存ドキュメント一覧",
            mimeType="application/json",
        ),
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource."""
    project_root = get_project_root()

    if uri == "template://structure":
        flat_structure = flatten_structure(TEMPLATE_STRUCTURE)
        return json.dumps(flat_structure, indent=2, ensure_ascii=False)

    elif uri == "template://schema":
        return json.dumps(DOCUMENT_SCHEMAS, indent=2, ensure_ascii=False)

    elif uri == "project://current":
        info = get_project_info(project_root)
        return json.dumps(info, indent=2, ensure_ascii=False)

    elif uri == "docs://list":
        docs = list_existing_docs(project_root)
        return json.dumps(docs, indent=2, ensure_ascii=False)

    else:
        raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="list_templates",
            description="利用可能なテンプレート一覧を取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "フィルタするカテゴリ（product, architecture, dev_process, agent, ops）",
                    }
                },
            },
        ),
        Tool(
            name="create_document",
            description="テンプレートから新規ドキュメントを作成",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_type": {
                        "type": "string",
                        "description": "テンプレートタイプ（vision.md, requirements.yaml, roles.yaml など）",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "出力先パス（docs/ からの相対パス）",
                    },
                    "metadata": {
                        "type": "object",
                        "description": "自動入力するメタデータ",
                        "properties": {
                            "project_name": {"type": "string"},
                            "author": {"type": "string"},
                            "date": {"type": "string"},
                        },
                    },
                },
                "required": ["template_type", "output_path"],
            },
        ),
        Tool(
            name="get_section",
            description="ドキュメントの特定セクションの内容を取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "ドキュメントのパス",
                    },
                    "section_name": {
                        "type": "string",
                        "description": "セクション名（markdownの場合はヘッダー名）",
                    },
                },
                "required": ["document_path", "section_name"],
            },
        ),
        Tool(
            name="update_section",
            description="ドキュメントの特定セクションを更新（マーカーベース）",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "ドキュメントのパス",
                    },
                    "section_name": {
                        "type": "string",
                        "description": "セクション名（AI_EDITABLE マーカー名）",
                    },
                    "new_content": {
                        "type": "string",
                        "description": "新しいセクション内容",
                    },
                },
                "required": ["document_path", "section_name", "new_content"],
            },
        ),
        Tool(
            name="validate_document",
            description="ドキュメントが規定の構造に従っているか検証",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "検証するドキュメントのパス",
                    },
                },
                "required": ["document_path"],
            },
        ),
        Tool(
            name="fill_metadata",
            description="プロジェクト情報からメタデータを自動入力",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "メタデータを入力するドキュメントのパス",
                    },
                    "metadata": {
                        "type": "object",
                        "description": "入力するメタデータ",
                        "properties": {
                            "date": {"type": "string"},
                            "author": {"type": "string"},
                            "version": {"type": "string"},
                        },
                    },
                },
                "required": ["document_path"],
            },
        ),
        Tool(
            name="diff_code_docs",
            description="コードとドキュメント間の差分を検出",
            inputSchema={
                "type": "object",
                "properties": {
                    "code_path": {
                        "type": "string",
                        "description": "検査対象のコードパス（ディレクトリまたはファイル）",
                    },
                    "doc_type": {
                        "type": "string",
                        "enum": ["api", "entities", "all"],
                        "description": "比較対象のドキュメントタイプ",
                        "default": "all",
                    },
                    "language": {
                        "type": "string",
                        "enum": ["python", "typescript", "auto"],
                        "description": "コードの言語（autoで自動検出）",
                        "default": "auto",
                    },
                },
                "required": ["code_path"],
            },
        ),
        Tool(
            name="extract_from_code",
            description="コードからドキュメント情報を抽出してYAML形式で出力",
            inputSchema={
                "type": "object",
                "properties": {
                    "code_path": {
                        "type": "string",
                        "description": "抽出対象のコードパス",
                    },
                    "extract_type": {
                        "type": "string",
                        "enum": ["api", "entities", "all"],
                        "description": "抽出する情報の種類",
                        "default": "all",
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["yaml", "json"],
                        "description": "出力形式",
                        "default": "yaml",
                    },
                    "merge_with_existing": {
                        "type": "boolean",
                        "description": "既存ドキュメントとマージするか",
                        "default": False,
                    },
                },
                "required": ["code_path"],
            },
        ),
        Tool(
            name="auto_sync",
            description="コード変更をドキュメントに自動反映（プレビュー/適用モード）",
            inputSchema={
                "type": "object",
                "properties": {
                    "code_path": {
                        "type": "string",
                        "description": "スキャン対象のコードパス",
                        "default": "src/",
                    },
                    "target_docs": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "対象ドキュメント（api.yaml, entities.yaml等）",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["preview", "apply"],
                        "description": "プレビューのみか実際に適用するか",
                        "default": "preview",
                    },
                    "language": {
                        "type": "string",
                        "enum": ["python", "typescript", "auto"],
                        "description": "コードの言語",
                        "default": "auto",
                    },
                },
                "required": ["mode"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    project_root = get_project_root()

    if name == "list_templates":
        category = arguments.get("category")
        flat_structure = flatten_structure(TEMPLATE_STRUCTURE)

        if category:
            flat_structure = [
                item for item in flat_structure
                if item["path"].startswith(f"docs/{category}/") or
                   item["path"].startswith(f"{category}/")
            ]

        return [TextContent(
            type="text",
            text=json.dumps(flat_structure, indent=2, ensure_ascii=False),
        )]

    elif name == "create_document":
        template_type = arguments["template_type"]
        output_path = arguments["output_path"]
        metadata = arguments.get("metadata", {})

        template = get_template_for_doc(template_type)
        if not template:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Unknown template type: {template_type}",
                }),
            )]

        # Fill in metadata
        today = datetime.now().strftime("%Y-%m-%d")
        template = template.replace("YYYY-MM-DD", metadata.get("date", today))
        if "author" in metadata:
            template = template.replace("[担当者/AIエージェント名]", metadata["author"])

        # Write file
        full_path = project_root / output_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(template, encoding="utf-8")

        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "path": str(full_path),
                "template_type": template_type,
            }, ensure_ascii=False),
        )]

    elif name == "get_section":
        doc_path = arguments["document_path"]
        section_name = arguments["section_name"]

        content = read_document_content(project_root, doc_path)
        if content is None:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Document not found: {doc_path}",
                }),
            )]

        section = extract_section(content, section_name)
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "section": section,
            }, ensure_ascii=False),
        )]

    elif name == "update_section":
        doc_path = arguments["document_path"]
        section_name = arguments["section_name"]
        new_content = arguments["new_content"]

        full_path = project_root / doc_path
        if not full_path.exists():
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Document not found: {doc_path}",
                }),
            )]

        content = full_path.read_text(encoding="utf-8")

        # Look for AI_EDITABLE markers
        marker_start = f"<!-- AI_EDITABLE_START: {section_name} -->"
        marker_end = f"<!-- AI_EDITABLE_END: {section_name} -->"

        if marker_start in content and marker_end in content:
            # Replace content between markers
            pattern = re.compile(
                rf"{re.escape(marker_start)}.*?{re.escape(marker_end)}",
                re.DOTALL,
            )
            replacement = f"{marker_start}\n{new_content}\n{marker_end}"
            new_full_content = pattern.sub(replacement, content)
            full_path.write_text(new_full_content, encoding="utf-8")

            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "message": f"Section '{section_name}' updated successfully",
                }, ensure_ascii=False),
            )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"AI_EDITABLE markers not found for section: {section_name}",
                }),
            )]

    elif name == "validate_document":
        doc_path = arguments["document_path"]

        content = read_document_content(project_root, doc_path)
        if content is None:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Document not found: {doc_path}",
                }),
            )]

        doc_name = Path(doc_path).name

        if doc_path.endswith((".yaml", ".yml")):
            result = validate_yaml_document(content, doc_name)
        else:
            result = validate_markdown_document(content, doc_name)

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False),
        )]

    elif name == "fill_metadata":
        doc_path = arguments["document_path"]
        metadata = arguments.get("metadata", {})

        full_path = project_root / doc_path
        if not full_path.exists():
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Document not found: {doc_path}",
                }),
            )]

        content = full_path.read_text(encoding="utf-8")

        # Fill in metadata fields
        today = datetime.now().strftime("%Y-%m-%d")
        content = content.replace("YYYY-MM-DD", metadata.get("date", today))

        if "author" in metadata:
            content = content.replace("[担当者/AIエージェント名]", metadata["author"])

        if "version" in metadata:
            content = re.sub(
                r'version:\s*"[^"]*"',
                f'version: "{metadata["version"]}"',
                content,
            )

        full_path.write_text(content, encoding="utf-8")

        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "message": "Metadata filled successfully",
            }, ensure_ascii=False),
        )]

    elif name == "diff_code_docs":
        code_path = arguments["code_path"]
        doc_type = arguments.get("doc_type", "all")
        language = arguments.get("language", "auto")

        diff_engine = DiffEngine(project_root)
        result = diff_engine.diff(code_path, doc_type, language)

        return [TextContent(
            type="text",
            text=json.dumps(result.to_dict(), indent=2, ensure_ascii=False),
        )]

    elif name == "extract_from_code":
        code_path = arguments["code_path"]
        extract_type = arguments.get("extract_type", "all")
        output_format = arguments.get("output_format", "yaml")
        merge_with_existing = arguments.get("merge_with_existing", False)

        diff_engine = DiffEngine(project_root)
        code_elements, errors = diff_engine.get_code_elements(code_path)

        if errors:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "errors": errors,
                }, ensure_ascii=False),
            )]

        if code_elements is None:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "errors": ["Failed to parse code"],
                }, ensure_ascii=False),
            )]

        result: dict[str, Any] = {"success": True, "extracted": {}}

        # Extract API endpoints
        if extract_type in ("api", "all"):
            api_extractor = ApiExtractor(project_root)
            api_path = project_root / ".agent" / "schemas" / "api.yaml"
            existing_spec = api_extractor.load_existing_spec(api_path) if merge_with_existing else None
            api_spec = api_extractor.extract_to_openapi(code_elements, existing_spec, merge_with_existing)
            result["extracted"]["api"] = api_spec
            if output_format == "yaml":
                result["api_yaml"] = api_extractor.to_yaml(api_spec)

        # Extract entities
        if extract_type in ("entities", "all"):
            entity_extractor = EntityExtractor(project_root)
            entities_path = project_root / ".agent" / "schemas" / "entities.yaml"
            existing_entities = entity_extractor.load_existing_entities(entities_path) if merge_with_existing else None
            entities_spec = entity_extractor.extract_to_entities_yaml(code_elements, existing_entities, merge_with_existing)
            result["extracted"]["entities"] = entities_spec
            if output_format == "yaml":
                result["entities_yaml"] = entity_extractor.to_yaml(entities_spec)

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False),
        )]

    elif name == "auto_sync":
        code_path = arguments.get("code_path", "src/")
        target_docs = arguments.get("target_docs")
        mode = arguments.get("mode", "preview")
        language = arguments.get("language", "auto")

        sync_manager = SyncManager(project_root)
        result = sync_manager.sync(code_path, target_docs, mode, language)

        return [TextContent(
            type="text",
            text=json.dumps(result.to_dict(), indent=2, ensure_ascii=False),
        )]

    else:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"}),
        )]


@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available prompts."""
    return [
        Prompt(
            name="design-review",
            description="設計レビュー用のワークフロー",
            arguments=[
                PromptArgument(
                    name="document_path",
                    description="レビュー対象のドキュメントパス",
                    required=True,
                ),
            ],
        ),
        Prompt(
            name="update-architecture",
            description="アーキテクチャ図更新のガイド",
            arguments=[
                PromptArgument(
                    name="change_description",
                    description="変更内容の説明",
                    required=True,
                ),
            ],
        ),
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
    """Get a specific prompt."""
    if name == "design-review":
        doc_path = arguments.get("document_path", "") if arguments else ""
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"""設計ドキュメントのレビューを行います。

対象ドキュメント: {doc_path}

以下の観点でレビューしてください：

1. **完全性チェック**
   - 必須セクションが全て記載されているか
   - 各セクションに十分な情報があるか

2. **整合性チェック**
   - 他のドキュメントとの矛盾がないか
   - 用語が統一されているか

3. **実現可能性チェック**
   - 技術的に実現可能か
   - リソース制約を考慮しているか

4. **セキュリティチェック**
   - セキュリティ上の問題点はないか
   - 機密情報の取り扱いは適切か

5. **改善提案**
   - より良い設計の提案
   - 不足している考慮事項

レビュー結果を構造化して報告してください。
""",
                    ),
                ),
            ],
        )

    elif name == "update-architecture":
        change_desc = arguments.get("change_description", "") if arguments else ""
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"""アーキテクチャドキュメントの更新を行います。

変更内容: {change_desc}

以下の手順で更新してください：

1. **現状の確認**
   - .agent/architecture.yaml を読み込む
   - system, components, domain_model セクションを確認

2. **影響範囲の特定**
   - 変更が影響するコンポーネントを特定
   - 依存関係を確認

3. **ドキュメント更新**
   - .agent/architecture.yaml の該当セクションを更新

4. **整合性確認**
   - .agent/schemas/api.yaml との整合性を確認
   - .agent/schemas/entities.yaml との整合性を確認

更新後、変更サマリを報告してください。
""",
                    ),
                ),
            ],
        )

    else:
        raise ValueError(f"Unknown prompt: {name}")


async def run_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main():
    """Main entry point."""
    import asyncio
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
