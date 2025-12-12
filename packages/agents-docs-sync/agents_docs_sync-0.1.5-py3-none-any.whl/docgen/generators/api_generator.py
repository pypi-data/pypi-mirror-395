"""
APIドキュメント生成モジュール
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

from ..detectors.detector_patterns import DetectorPatterns
from ..models.api import APIInfo
from ..models.project import ProjectInfo
from ..utils.cache import CacheManager
from ..utils.markdown_utils import (
    GENERATION_TIMESTAMP_LABEL,
    SECTION_SEPARATOR,
    get_current_timestamp,
)
from .base_generator import BaseGenerator
from .parsers.generic_parser import GenericParser
from .parsers.js_parser import JSParser
from .parsers.python_parser import PythonParser

if TYPE_CHECKING:
    from .parsers.base_parser import BaseParser


class APIGenerator(BaseGenerator):
    """APIドキュメント生成クラス"""

    def __init__(
        self,
        project_root: Path,
        languages: list[str],
        config: dict[str, Any],
        package_managers: dict[str, str] | None = None,
    ):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            languages: 検出された言語のリスト
            config: 設定辞書
            package_managers: 検出されたパッケージマネージャの辞書
        """
        super().__init__(project_root, languages, config, package_managers)

        # キャッシュマネージャーの初期化
        cache_enabled = self.config.get("cache", {}).get("enabled", True)
        self.cache_manager = (
            CacheManager(project_root=self.project_root, enabled=cache_enabled)
            if cache_enabled
            else None
        )

    def _get_mode_key(self) -> str:
        return "api_mode"

    def _get_output_key(self) -> str:
        return "api_doc"

    def _get_document_type(self) -> str:
        return "APIドキュメント"

    def _get_structured_model(self) -> Any:
        # 現在は構造化出力を使用していないためNoneを返す
        return None

    def _create_llm_prompt(self, project_info: ProjectInfo) -> str:
        # 現在はLLM生成を使用していないため空文字を返す
        return ""

    def _generate_template(self, project_info: ProjectInfo) -> str:
        # テンプレート生成の代わりにパーサーベースの生成を行う
        # BaseGeneratorのgenerateフローから呼ばれる場合、ここが実質的な生成ロジックの一部になる
        # ただし、API生成は特殊なので、_generate_markdownで処理する
        return ""

    def _get_project_overview_section(self, content: str) -> str:
        return ""

    def _convert_structured_data_to_markdown(
        self, structured_data: Any, project_info: ProjectInfo
    ) -> str:
        return ""

    def _generate_markdown(self, project_info: ProjectInfo) -> str:
        """
        API情報からマークダウンを生成

        Args:
            project_info: プロジェクト情報（このクラスでは主に使用しないが、インターフェースとして必要）

        Returns:
            マークダウンの文字列
        """
        # 各言語のパーサーでAPI情報を収集
        all_apis = []
        parsers = self._get_parsers()

        # 除外ディレクトリとファイルパターンを設定
        exclude_dirs = self.config.get("exclude", {}).get(
            "directories",
            list(DetectorPatterns.EXCLUDE_DIRS) + ["venv"],
        )

        # キャッシュの使用設定
        use_cache = self.config.get("cache", {}).get("enabled", True)

        for parser in parsers:
            apis = parser.parse_project(
                exclude_dirs=exclude_dirs,
                use_cache=use_cache,
                cache_manager=self.cache_manager,
            )
            all_apis.extend(apis)

        # API情報をソート（ファイル名、行番号順）
        all_apis.sort(key=lambda x: (x["file"], x["line"]))

        return self._render_api_markdown(all_apis)

    def _render_api_markdown(self, apis: list[APIInfo]) -> str:
        """
        API情報のリストからマークダウンをレンダリング

        Args:
            apis: API情報のリスト

        Returns:
            マークダウン文字列
        """
        lines = []

        # ヘッダー
        lines.append("# API ドキュメント")
        lines.append("")
        lines.append(f"{GENERATION_TIMESTAMP_LABEL} {get_current_timestamp()}")
        lines.append("")
        lines.append(SECTION_SEPARATOR)
        lines.append("")

        if not apis:
            lines.append("APIが見つかりませんでした。")
            return "\n".join(lines)

        # ファイルごとにグループ化
        current_file = None
        for api in apis:
            file_path = api["file"]

            # 新しいファイルセクション
            if file_path != current_file:
                if current_file is not None:
                    lines.append("")
                current_file = file_path
                lines.append(f"## {file_path}")
                lines.append("")

            # API情報を出力
            lines.append(f"### {api['name']}")
            lines.append("")
            lines.append(f"**型**: `{api['type']}`")
            lines.append("")
            lines.append("**シグネチャ**:")
            lines.append("```")
            lines.append(api["signature"])
            lines.append("```")
            lines.append("")

            if api["docstring"]:
                lines.append("**説明**:")
                lines.append("")
                # docstringを整形（インデントを調整）
                docstring_lines = api["docstring"].split("\n")
                for doc_line in docstring_lines:
                    lines.append(doc_line)
                lines.append("")
            else:
                lines.append("*説明なし*")
                lines.append("")

            lines.append(f"*定義場所: {file_path}:{api['line']}*")
            lines.append("")
            lines.append(SECTION_SEPARATOR)
            lines.append("")

        return "\n".join(lines)

    def _get_parsers(self) -> list["BaseParser"]:
        """
        言語に応じたパーサーのリストを取得

        Returns:
            パーサーのリスト
        """
        parsers = []

        for lang in self.languages:
            if lang == "python":
                parsers.append(PythonParser(self.project_root))
            elif lang in ["javascript", "typescript"]:
                parsers.append(JSParser(self.project_root))
            else:
                parsers.append(GenericParser(self.project_root, language=lang))

        return parsers
