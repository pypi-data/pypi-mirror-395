"""
汎用コード解析モジュール
一般的なコメント形式をサポートする言語を解析
"""

from pathlib import Path
import re

from ...models import APIInfo
from .base_parser import BaseParser


class GenericParser(BaseParser):
    """汎用コード解析クラス"""

    # 言語別のコメントパターン
    COMMENT_PATTERNS = {
        "rust": (r"//!?\s*(.*)", r"fn\s+(\w+)", r"struct\s+(\w+)|impl\s+(\w+)"),
        "java": (
            r"/\*\*\s*\n(.*?)\*/",
            r"public\s+(?:static\s+)?(?:.*?\s+)?(\w+)\s*\(",
            r"public\s+class\s+(\w+)",
        ),
        "c": (r"/\*\*\s*\n(.*?)\*/", r"(\w+)\s*\([^)]*\)", r"struct\s+(\w+)|typedef\s+struct"),
        "cpp": (r"/\*\*\s*\n(.*?)\*/", r"(\w+)\s*\([^)]*\)", r"class\s+(\w+)"),
        "go": (r"//\s*(.*)", r"func\s+(\w+)", r"type\s+(\w+)\s+struct"),
        "ruby": (r"#\s*(.*)", r"def\s+(\w+)", r"class\s+(\w+)"),
        "php": (r"/\*\*\s*\n(.*?)\*/", r"function\s+(\w+)", r"class\s+(\w+)"),
    }

    def __init__(self, project_root: Path, language: str = "generic"):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            language: 言語名（'rust', 'java', 'c', 'cpp', 'go', 'ruby', 'php'など）
        """
        super().__init__(project_root)
        self.language = language

    def _parse_to_ast(self, content: str, file_path: Path) -> str:
        """ASTにパース（正規表現ベースなのでコンテンツをそのまま返す）"""
        return content

    def _extract_elements(self, content: str, file_path: Path) -> list[APIInfo]:
        """要素を抽出"""
        apis = []

        # 言語に応じたパターンを取得
        patterns = self.COMMENT_PATTERNS.get(self.language)
        if not patterns:
            # デフォルトパターン（Cスタイルコメント）
            patterns = (
                r"/\*\*\s*\n(.*?)\*/",
                r"(\w+)\s*\([^)]*\)",
                r"class\s+(\w+)|struct\s+(\w+)",
            )

        comment_pattern, func_pattern, class_pattern = patterns

        # コメント付き関数を抽出
        for match in re.finditer(comment_pattern, content, re.DOTALL):
            docstring = match.group(1).strip()
            start_pos = match.end()

            # 次の関数定義を探す
            func_match = re.search(func_pattern, content[start_pos : start_pos + 200])
            if func_match:
                name = func_match.group(1)
                line_num = content[: start_pos + func_match.start()].count("\n") + 1
                signature = self._extract_signature(
                    content, start_pos + func_match.start(), name, "function"
                )

                apis.append(
                    {
                        "name": name,
                        "type": "function",
                        "signature": signature,
                        "docstring": self._clean_docstring(docstring),
                        "line": line_num,
                        "file": str(file_path.relative_to(self.project_root)),
                    }
                )

        # クラス定義を抽出
        for match in re.finditer(class_pattern, content):
            name = match.group(1) or match.group(2) if match.lastindex else None
            if name:
                line_num = content[: match.start()].count("\n") + 1
                signature = f"class {name}" if "class" in match.group(0) else f"struct {name}"

                apis.append(
                    {
                        "name": name,
                        "type": "class",
                        "signature": signature,
                        "docstring": "",
                        "line": line_num,
                        "file": str(file_path.relative_to(self.project_root)),
                    }
                )

        return apis

    def _extract_signature(self, content: str, start_pos: int, name: str, api_type: str) -> str:
        """
        シグネチャを抽出

        Args:
            content: ファイル内容
            start_pos: 開始位置
            name: 関数/クラス名
            api_type: 'function' または 'class'

        Returns:
            シグネチャ文字列
        """
        lines = content[start_pos : start_pos + 5].split("\n")
        if lines:
            first_line = lines[0].strip()
            if "(" in first_line:
                end_pos = first_line.find(")") + 1
                return first_line[:end_pos] if end_pos > 0 else f"{name}(...)"

        return f"{name}(...)"

    def _clean_docstring(self, docstring: str) -> str:
        """
        ドキュメント文字列をクリーンアップ

        Args:
            docstring: 生のドキュメント文字列

        Returns:
            クリーンアップされた文字列
        """
        # コメント記号を削除
        lines = [line.strip().lstrip("*").lstrip("#").strip() for line in docstring.split("\n")]
        return "\n".join(lines).strip()

    def get_supported_extensions(self) -> list[str]:
        """
        サポートする拡張子を返す

        Returns:
            言語に応じた拡張子のリスト
        """
        extension_map = {
            "rust": [".rs"],
            "java": [".java"],
            "kotlin": [".kt", ".kts"],
            "scala": [".scala"],
            "ruby": [".rb"],
            "php": [".php"],
            "c": [".c", ".h"],
            "cpp": [".cpp", ".cc", ".cxx", ".hpp", ".hxx"],
            "csharp": [".cs"],
            "swift": [".swift"],
            "dart": [".dart"],
            "r": [".r", ".R"],
            "lua": [".lua"],
            "perl": [".pl", ".pm"],
            "go": [".go"],
        }

        return extension_map.get(self.language, [".txt"])
