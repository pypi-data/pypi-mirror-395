# byebye-docs MCP Server

[![PyPI version](https://badge.fury.io/py/byebye-docs-mcp.svg)](https://badge.fury.io/py/byebye-docs-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

byebye-docs用のMCPサーバーです。
Claude CodeやClaude Desktopと連携して、`.agent/` ドキュメントの作成・更新・検証、およびコードとドキュメントの双方向同期をサポートします。

## インストール

### PyPIからインストール（推奨）

```bash
pip install byebye-docs-mcp
```

または uv を使用:

```bash
uv tool install byebye-docs-mcp
```

### プロジェクトへの適用

初期化スクリプトを使用して、既存プロジェクトにbyebye-docsを適用:

```bash
curl -sL https://raw.githubusercontent.com/pon-tanuki/byebye-docs/main/scripts/init-project.sh | bash -s /path/to/your-project
```

または手動で:

```bash
# 1. MCPサーバーをインストール
pip install byebye-docs-mcp

# 2. テンプレートをコピー（GitHubから）
git clone --depth 1 https://github.com/pon-tanuki/byebye-docs.git /tmp/byebye-docs
cp -r /tmp/byebye-docs/.agent /path/to/your-project/
cp /tmp/byebye-docs/CLAUDE.md /path/to/your-project/

# 3. .mcp.json を作成（下記参照）
```

## Claude Codeでの設定

プロジェクトルートに `.mcp.json` を作成:

```json
{
  "mcpServers": {
    "byebye-docs": {
      "command": "byebye-docs",
      "env": {
        "BYEBYE_DOCS_PROJECT_PATH": "."
      }
    }
  }
}
```

## 機能

### Resources（リソース）

| URI | 説明 |
|-----|------|
| `template://structure` | テンプレートの構造情報 |
| `template://schema` | 各ドキュメントの検証スキーマ |
| `project://current` | 現在のプロジェクト情報 |
| `docs://list` | プロジェクト内の既存ドキュメント一覧 |

### Tools（ツール）

#### ドキュメント管理

| ツール名 | 説明 |
|---------|------|
| `list_templates` | 利用可能なテンプレート一覧を取得 |
| `create_document` | テンプレートから新規ドキュメントを作成 |
| `get_section` | ドキュメントの特定セクションの内容を取得 |
| `update_section` | ドキュメントの特定セクションを更新（マーカーベース） |
| `validate_document` | ドキュメントが規定の構造に従っているか検証 |
| `fill_metadata` | プロジェクト情報からメタデータを自動入力 |

#### コード↔ドキュメント同期

| ツール名 | 説明 |
|---------|------|
| `diff_code_docs` | コードとドキュメント間の差分を検出 |
| `extract_from_code` | コードからAPI/エンティティ情報を抽出しYAML出力 |
| `auto_sync` | コード変更をドキュメントに自動反映（preview/apply） |

### Prompts（プロンプト）

| プロンプト名 | 説明 |
|-------------|------|
| `design-review` | 設計レビュー用のワークフロー |
| `update-architecture` | アーキテクチャ図更新のガイド |

## 使用例

### コードとドキュメントの差分検出

```python
diff_code_docs(
    code_path="src/",
    doc_type="all",  # "api", "entities", "all"
    language="auto"
)
```

### コードからドキュメント情報を抽出

```python
extract_from_code(
    code_path="src/",
    extract_type="all",  # "api", "entities", "all"
    output_format="yaml",
    merge_with_existing=True
)
```

### ドキュメントの自動同期

```python
# プレビュー（変更内容を確認）
auto_sync(mode="preview", code_path="src/")

# 適用（実際にドキュメントを更新）
auto_sync(mode="apply", code_path="src/", target_docs=["api.yaml", "entities.yaml"])
```

### テンプレートからドキュメント作成

```python
create_document(
    template_type="context.yaml",
    output_path=".agent/context.yaml",
    metadata={
        "project_name": "My Project",
        "author": "Claude Agent"
    }
)
```

## 更新方法

```bash
pip install --upgrade byebye-docs-mcp
# または
uv tool install byebye-docs-mcp --force
```

## 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| `BYEBYE_DOCS_PROJECT_PATH` | 対象プロジェクトのルートパス | カレントディレクトリ |

## 開発

### ソースからインストール

```bash
git clone https://github.com/pon-tanuki/byebye-docs.git
cd byebye-docs/mcp-server
uv sync
```

### テストの実行

```bash
uv run pytest
```

### Lintの実行

```bash
uv run ruff check .
uv run ruff format .
```

## 対応言語（コード解析）

- **Python** - FastAPI, Flask, SQLAlchemy, Pydantic, dataclass

## ライセンス

MIT License
