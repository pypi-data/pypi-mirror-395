"""コードベースのチャンク化モジュール

コードベースを意味のある単位（関数、クラス、セクション）に分割し、
RAGインデックス用のチャンクを生成します。
"""

from pathlib import Path
import re
from typing import Any

from ..utils.logger import get_logger

logger = get_logger(__name__)


class CodeChunker:
    """コードベースをチャンク化するクラス"""

    # 機密情報を含む可能性があるパターン
    DEFAULT_EXCLUDE_PATTERNS = [
        r".*\.env$",
        r"secrets/.*",
        r".*_SECRET.*",
        r".*API_KEY.*",
        r".*password.*",
        r".*token.*\.json$",
    ]

    # 無視すべきディレクトリ
    IGNORE_DIRS = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".idea",
        ".vscode",
        "dist",
        "build",
        "coverage",
        "docgen/index",  # インデックスディレクトリ自体を除外
    }

    def __init__(self, config: dict[str, Any] | None = None):
        """
        初期化

        Args:
            config: RAG設定（config.toml の rag セクション）
        """
        self.config = config or {}
        self.max_chunk_size = self.config.get("chunking", {}).get("max_chunk_size", 512)
        self.overlap = self.config.get("chunking", {}).get("overlap", 50)

        # カスタム除外パターン + デフォルトパターン
        custom_patterns = self.config.get("exclude_patterns", [])
        self.exclude_patterns = self.DEFAULT_EXCLUDE_PATTERNS + custom_patterns

        # 除外ファイル名リスト
        self.exclude_files = self.config.get("exclude_files", ["README.md", "AGENTS.md"])

    def should_process_file(self, file_path: Path) -> bool:
        """
        ファイルを処理すべきかどうかを判定

        Args:
            file_path: ファイルパス

        Returns:
            処理すべき場合True
        """
        str_path = str(file_path)

        # 除外パターンのチェック
        for pattern in self.exclude_patterns:
            if re.search(pattern, str_path):
                return False

        # 除外ファイル名のチェック
        if file_path.name in self.exclude_files:
            return False

        # バイナリファイルやテストファイルは除外
        excluded_suffixes = {".pyc", ".pyo", ".so", ".dylib", ".whl", ".egg"}
        if file_path.suffix in excluded_suffixes:
            return False

        # 一般的な除外ディレクトリ（.venv, .git, node_modules等）
        excluded_dirs = {
            ".venv",
            "venv",
            ".git",
            ".hg",
            ".svn",
            "node_modules",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            ".tox",
            "dist",
            "build",
            ".eggs",
            "*.egg-info",
            ".cache",
            "htmlcov",
            ".coverage",
            ".DS_Store",
        }

        # パスに除外ディレクトリが含まれているかチェック
        path_parts = file_path.parts
        for part in path_parts:
            if part in excluded_dirs or part.startswith("."):
                # ただし、プロジェクトルート直下の設定ファイル（.github等）は許可
                if len(path_parts) == 2 and part.startswith(".") and file_path.is_file():
                    continue
                return False

        # テストファイルを除外
        if file_path.name.lower().startswith("test_") or file_path.name.lower().endswith(
            "_test.py"
        ):
            return False
        if "tests" in path_parts:
            return False

        return True

    def chunk_file(self, file_path: Path, project_root: Path) -> list[dict[str, Any]]:
        """
        ファイルをチャンク化

        Args:
            file_path: ファイルパス
            project_root: プロジェクトルート

        Returns:
            チャンクのリスト
        """
        if not self.should_process_file(file_path):
            return []

        try:
            content = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError) as e:
            logger.warning(f"Failed to read file {file_path}: {e}")
            return []

        # Initialize strategies
        from .strategies import CodeChunkStrategy, MarkdownChunkStrategy, TextChunkStrategy

        code_strategy = CodeChunkStrategy(project_root)
        markdown_strategy = MarkdownChunkStrategy(project_root)
        text_strategy = TextChunkStrategy(project_root)

        # Dispatch to appropriate strategy
        if file_path.suffix in {".py", ".yaml", ".yml", ".toml"}:
            return code_strategy.chunk(content, file_path)
        elif file_path.suffix == ".md":
            return markdown_strategy.chunk(content, file_path)
        else:
            return text_strategy.chunk(content, file_path)

    def chunk_codebase(self, project_root: Path) -> list[dict[str, Any]]:
        """
        プロジェクト全体をチャンク化

        Args:
            project_root: プロジェクトルート

        Returns:
            すべてのチャンクのリスト
        """
        all_chunks = []

        # os.walkを使用してディレクトリを走査し、無視すべきディレクトリをスキップ
        import os

        for root, dirs, files in os.walk(project_root):
            # 無視すべきディレクトリを削除（in-place変更でos.walkの探索を制御）
            # 相対パスでチェックする必要があるため、少し工夫が必要
            # ここでは単純なディレクトリ名チェックと、パスチェックを行う

            # 1. ディレクトリ名でフィルタリング
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS and not d.startswith(".")]

            # 2. パスベースのフィルタリング（docgen/indexのようなネストされたパス用）
            # os.walkのdirsはディレクトリ名のみなので、ここで削除するとその下には行かない
            # ただし、docgen/indexのようなパスはここだけでは判定しにくい場合がある
            # 親ディレクトリ(root)と結合してチェック

            valid_dirs = []
            for d in dirs:
                dir_path = Path(root) / d
                rel_path = dir_path.relative_to(project_root)
                if str(rel_path) in self.IGNORE_DIRS:
                    continue
                # docgen/index のようなパスが含まれるかチェック
                if any(
                    str(rel_path).startswith(ignore) for ignore in self.IGNORE_DIRS if "/" in ignore
                ):
                    continue
                valid_dirs.append(d)
            dirs[:] = valid_dirs

            for file_name in files:
                file_path = Path(root) / file_name
                if self.should_process_file(file_path):
                    chunks = self.chunk_file(file_path, project_root)
                    all_chunks.extend(chunks)

        logger.info(f"Created {len(all_chunks)} chunks from codebase")
        return all_chunks
