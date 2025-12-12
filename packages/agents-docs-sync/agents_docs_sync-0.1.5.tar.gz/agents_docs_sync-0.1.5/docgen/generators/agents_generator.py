"""
AGENTS.md生成モジュール（OpenAI仕様準拠）
Outlines統合で構造化出力を実現
"""

from pathlib import Path
from typing import Any

# 相対インポートを使用（docgenがパッケージとして認識される場合）
# フォールバック: 絶対インポート
from ..models.agents import AgentsDocument
from ..models.project import ProjectInfo
from ..utils.markdown_utils import (
    get_current_timestamp,
)
from ..utils.prompt_loader import PromptLoader
from .base_generator import BaseGenerator


class AgentsGenerator(BaseGenerator):
    """AGENTS.md生成クラス（OpenAI仕様準拠）"""

    def __init__(
        self,
        project_root: Path,
        languages: list[str],
        config: dict[str, Any],
        package_managers: dict[str, str] | None = None,
        **kwargs: Any,
    ):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            languages: 検出された言語のリスト
            config: 設定辞書
            package_managers: 検出されたパッケージマネージャの辞書
            **kwargs: BaseGeneratorに渡す追加引数（サービスなど）
        """
        super().__init__(project_root, languages, config, package_managers, **kwargs)

    @property
    def agents_path(self):
        return self.output_path

    def _get_mode_key(self) -> str:
        return "agents_mode"

    def _get_output_key(self) -> str:
        return "agents_doc"

    def _get_document_type(self) -> str:
        return "AGENTS.md"

    def _get_structured_model(self):
        return AgentsDocument

    def _get_project_overview_section(self, content: str) -> str:
        return self.formatting_service.extract_description_section(content)

    def _create_overview_prompt(
        self, project_info: ProjectInfo, existing_overview: str, rag_context: str = ""
    ) -> str:
        """
        概要生成用のLLMプロンプトを作成（BaseGeneratorのオーバーライド）
        AGENTS.md専用のプロンプトを提供
        """
        return PromptLoader.load_prompt(
            "agents_prompts.toml",
            "overview",
            project_info=self._format_project_info_for_prompt(project_info),
            existing_overview=existing_overview,
            rag_context=rag_context,
        )

    def _replace_overview_section(self, content: str, new_overview: str) -> str:
        """
        プロジェクト概要セクションを置き換え（BaseGeneratorのオーバーライド）
        AGENTS.mdでは「プロジェクト概要」セクションを置き換える
        """
        import re

        # "## プロジェクト概要" セクションの内容を置き換え
        # パターン: マーカーの後から "**使用技術**" の前まで
        pattern = r"(<!-- MANUAL_START:description -->\s*<!-- MANUAL_END:description -->\s*)(.*?)(\n\*\*使用技術\*\*:)"
        replacement = r"\1\n" + new_overview + r"\3"

        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        # デバッグ: 置換が成功したか確認
        if updated_content == content:
            self.logger.warning(
                "Overview section replacement did not match. Pattern may need adjustment."
            )
        else:
            self.logger.debug("Overview section successfully replaced.")

        return updated_content

    def _create_llm_prompt(self, project_info: ProjectInfo, rag_context: str = "") -> str:
        if rag_context:
            return PromptLoader.load_prompt(
                "agents_prompts.toml",
                "full_with_rag",
                project_info=self._format_project_info_for_prompt(project_info),
                rag_context=rag_context,
            )
        else:
            return PromptLoader.load_prompt(
                "agents_prompts.toml",
                "full",
                project_info=self._format_project_info_for_prompt(project_info),
            )

    def _generate_template(self, project_info: ProjectInfo) -> str:
        """
        Jinja2テンプレートを使用してAGENTS.mdを生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        # Extract manual sections from existing AGENTS.md
        try:
            existing_content = self.agents_path.read_text()
            manual_sections = self.manual_section_service.extract(existing_content)
        except (FileNotFoundError, OSError):
            manual_sections = {}

        # コンテキストの準備
        context = {
            "timestamp": get_current_timestamp(),
            "description": self._generate_project_overview_content(project_info, manual_sections),
            "languages": self.languages,
            "javascript": "javascript" in self.languages,
            "go": "go" in self.languages,
            "llm_mode": self.agents_config.get("llm_mode", "both"),
            "package_managers": self.package_managers,
            "build_commands": self.template_service.format_commands(
                project_info.build_commands or []
            ),
            "test_commands": self.template_service.format_commands(
                project_info.test_commands or []
            ),
            "raw_test_commands": project_info.test_commands or [],
            "coding_standards": project_info.coding_standards or {},
            "custom_instructions": self._generate_custom_instructions_content(),
            "project_structure": self.formatting_service.format_project_structure(
                project_info.project_structure
            ),
            # テンプレートモードではLLMを使用せず、データから取得した値のみ使用
            "key_features": project_info.key_features or [],
            "architecture": self._generate_architecture(project_info),
            "troubleshooting": "",
            "scripts": project_info.scripts,
        }

        # Jinja2テンプレートでレンダリング
        return self.template_service.render("agents_template.md.j2", context)

    def _generate_project_overview_content(
        self, project_info: ProjectInfo, manual_sections: dict[str, str]
    ) -> str:
        """プロジェクト概要セクションの内容を生成"""
        if "description" in manual_sections:
            return manual_sections["description"]
        else:
            # デフォルトの説明を生成
            description = self._collect_project_description()
            if description:
                return f"## 概要\n\n{description}"
            else:
                return "## 概要\n\nPlease describe this project here."

    def _collect_project_description(self) -> str:
        """プロジェクトの説明を収集（MarkdownMixinから移行）"""
        # ここでは簡易的に実装。必要に応じてFormattingServiceに移動を検討
        # プロジェクトルートのREADMEなどから抽出するロジックがあればここに実装
        return ""

    def _generate_custom_instructions_content(self) -> str:
        """カスタム指示の内容を生成"""
        custom_instructions = self.agents_config.get("custom_instructions")
        if custom_instructions:
            return "\n".join(self.template_service.format_custom_instructions(custom_instructions))
        return ""

    def _convert_structured_data_to_markdown(
        self, data: AgentsDocument, project_info: ProjectInfo
    ) -> str:
        """
        構造化データをマークダウン形式に変換（テンプレート使用）

        Args:
            data: 構造化されたAGENTSドキュメントデータ
            project_info: プロジェクト情報

        Returns:
            マークダウン形式の文字列
        """
        # 構造化データをテンプレートコンテキストに変換
        # 注意: 構造化データからの変換ロジックは複雑なので、一旦既存の実装を維持しつつ
        # サービスのヘルパーメソッドがあればそれを使う形にする
        # ここでは簡略化のため、既存ロジックをそのまま使うが、フォーマット部分はサービスを使う

        # TODO: 構造化データのフォーマットメソッドをサービスに移動するか検討
        # 現状はAgentsGenerator固有のロジックとしてここに残す

        context = {
            "timestamp": get_current_timestamp(),
            "description": data.description,
            "languages": self.languages,
            "javascript": "javascript" in self.languages,
            "go": "go" in self.languages,
            # 以下のメソッドはAgentsGenerator内に実装が必要（またはサービスに移動）
            "installation_steps": self._format_structured_installation(data.setup_instructions),
            "llm_setup": self._format_structured_llm_setup(data.setup_instructions),
            "build_commands": self._format_structured_build_commands(data.build_test_instructions),
            "test_commands": self._format_structured_test_commands(data.build_test_instructions),
            "coding_standards": self._format_structured_coding_standards(data.coding_standards),
            "pr_guidelines": self._format_structured_pr_guidelines(data.pr_guidelines),
            "project_structure": data.project_structure
            or self.formatting_service.format_project_structure(project_info.project_structure),
            "key_features": data.key_features or self._generate_key_features(project_info),
            "architecture": data.architecture or self._generate_architecture(project_info),
            "troubleshooting": data.troubleshooting or self._generate_troubleshooting(project_info),
            "custom_instructions": "",
        }

        # テンプレートレンダリングはTemplateServiceを使用したいが、
        # ここではコンテキストを返すだけになっている（元の実装がそうだったため）
        # 元の実装: return context
        # しかし型ヒントは str なので、本来はレンダリングすべき。
        # 元の実装の `return context` はバグの可能性が高いが、
        # `_generate_with_outlines` (LLMMixin) が `_convert_structured_data_to_markdown` を呼んで
        # その結果を返している。
        # LLMMixinの実装を見ると:
        # markdown = self._convert_structured_data_to_markdown(structured_data, project_info)
        # return markdown
        # なので、文字列を返す必要がある。

        # テンプレートを使ってレンダリングする
        return self.template_service.render("agents_template.md.j2", context)

    # 構造化データのフォーマット用ヘルパーメソッド（本来はサービスに移動すべきだが、一旦ここに定義）
    def _format_structured_installation(self, instructions: Any) -> str:
        if not instructions:
            return ""
        return "\n".join([f"- {step}" for step in getattr(instructions, "installation", [])])

    def _format_structured_llm_setup(self, instructions: Any) -> str:
        if not instructions:
            return ""
        return "\n".join([f"- {step}" for step in getattr(instructions, "llm_setup", [])])

    def _format_structured_build_commands(self, instructions: Any) -> str:
        if not instructions:
            return ""
        return self.template_service.format_commands(getattr(instructions, "build_commands", []))

    def _format_structured_test_commands(self, instructions: Any) -> str:
        if not instructions:
            return ""
        return self.template_service.format_commands(getattr(instructions, "test_commands", []))

    def _format_structured_coding_standards(self, standards: Any) -> str:
        if not standards:
            return ""
        # 簡易実装
        return str(standards)

    def _format_structured_pr_guidelines(self, guidelines: Any) -> str:
        if not guidelines:
            return ""
        return str(guidelines)

    def _generate_key_features(self, project_info: ProjectInfo) -> list[str]:
        """主要機能を生成"""
        if not self._should_use_llm():
            return []
        content = self._generate_content_with_llm(
            "agents_prompts.toml", "key_features", project_info
        )
        # コンテンツをリストに変換するロジックが必要
        return [line.strip("- ") for line in content.splitlines() if line.strip()]

    def _generate_architecture(self, project_info: ProjectInfo) -> str:
        """アーキテクチャを生成"""
        # 設定ベースのアーキテクチャ図生成を試みる
        arch_content = self._get_architecture_diagram_content()
        if arch_content:
            return arch_content

        if not self._should_use_llm():
            return ""
        return self._generate_content_with_llm("agents_prompts.toml", "architecture", project_info)

    def _generate_troubleshooting(self, project_info: ProjectInfo) -> str:
        """トラブルシューティングを生成"""
        if not self._should_use_llm():
            return ""
        return self._generate_content_with_llm(
            "agents_prompts.toml", "troubleshooting", project_info
        )

    def _should_use_llm(self) -> bool:
        """LLMを使用すべきかどうかを判定"""
        return self.agents_config.get("generation", {}).get("agents_mode") in ["llm", "hybrid"]

    def _format_project_info_for_prompt(self, project_info: ProjectInfo) -> str:
        """プロジェクト情報をプロンプト用に整形"""
        base_info = self.llm_service.format_project_info(
            project_info, self.languages, self.package_managers
        )
        return f"Project Name: {self.project_root.name}\n{base_info}"

    def _generate_content_with_llm(
        self, prompt_file: str, prompt_name: str, project_info: ProjectInfo
    ) -> str:
        """LLMを使用してコンテンツを生成"""
        project_info_str = self._format_project_info_for_prompt(project_info)

        # RAGコンテキスト取得
        rag_context = ""
        if self.config.get("rag", {}).get("enabled", False):
            query = f"{prompt_name} for {self.project_root.name}"
            rag_context = self.rag_service.get_context(query)

        content = self.llm_service.generate_content(
            prompt_file, prompt_name, project_info_str, rag_context
        )
        return self.formatting_service.clean_llm_output(content)

    # LLMMixinのメソッドをここで再実装（サービス委譲）
    def _generate_with_llm(self, project_info: ProjectInfo) -> str:
        try:
            # Outlinesを使用するかどうか
            if self.llm_service.should_use_outlines():
                client = self.llm_service.get_client()
                if client:
                    outlines_model = self.llm_service.create_outlines_model(client)
                    if outlines_model:
                        # RAGコンテキスト
                        rag_context = ""
                        if self.config.get("rag", {}).get("enabled", False):
                            query = f"full documentation context for {self.project_root.name}"
                            rag_context = self.rag_service.get_context(query)

                        # プロンプト作成
                        prompt = self._create_llm_prompt(project_info, rag_context=rag_context)

                        # 生成
                        self.logger.info("Outlinesを使用して構造化されたドキュメントを生成中...")
                        structured_data = outlines_model(prompt, self._get_structured_model())

                        # 変換
                        return self._convert_structured_data_to_markdown(
                            structured_data, project_info
                        )

            # フォールバック: テンプレート生成
            self.logger.warning(
                "Outlinesが利用できないため、テンプレート生成にフォールバックします"
            )
            return self._generate_template(project_info)

        except Exception as e:
            self.logger.error(f"LLM生成エラー: {e}")
            return self._generate_template(project_info)

    def _generate_hybrid(self, project_info: ProjectInfo) -> str:
        # まずテンプレートでベースを生成
        content = self._generate_template(project_info)

        # 概要セクションをLLMで改善
        try:
            # 既存の概要を取得（テンプレート生成されたもの）
            existing_overview = self._get_project_overview_section(content)

            # RAGコンテキスト
            rag_context = ""
            if self.config.get("rag", {}).get("enabled", False):
                query = f"project overview for {self.project_root.name}"
                rag_context = self.rag_service.get_context(query)

            # プロンプト作成
            prompt = self._create_overview_prompt(project_info, existing_overview, rag_context)

            # 生成
            self.logger.info("LLMを使用して概要セクションを改善中...")
            new_overview = self.llm_service.generate(prompt)

            # クリーニング
            new_overview = self.formatting_service.clean_llm_output(new_overview)

            # 置換
            if new_overview:
                content = self._replace_overview_section(content, new_overview)

        except Exception as e:
            self.logger.warning(f"ハイブリッド生成（概要改善）中にエラーが発生しました: {e}")
            # エラーが発生してもテンプレート生成されたコンテンツを返す

        return content
