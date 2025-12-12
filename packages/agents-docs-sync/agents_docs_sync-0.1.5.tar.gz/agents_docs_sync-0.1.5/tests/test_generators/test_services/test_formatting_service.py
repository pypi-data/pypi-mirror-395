"""
FormattingService のテスト
"""

import pytest

from docgen.generators.services.formatting_service import FormattingService


class TestFormattingService:
    """FormattingService のテストクラス"""

    @pytest.fixture
    def service(self):
        """FormattingService インスタンス"""
        return FormattingService()

    def test_format_languages_empty(self, service):
        """空の言語リストのフォーマット"""
        result = service.format_languages([])
        assert result == "- Not detected"

    def test_format_languages_single(self, service):
        """単一言語のフォーマット"""
        result = service.format_languages(["python"])
        assert result == "- Python"

    def test_format_languages_multiple(self, service):
        """複数言語のフォーマット"""
        result = service.format_languages(["python", "javascript"])
        assert "- Python" in result
        assert "- JavaScript" in result

    def test_format_languages_unknown(self, service):
        """未知の言語のフォーマット"""
        result = service.format_languages(["unknownlang"])
        assert "- Unknownlang" in result

    def test_format_commands_empty(self, service):
        """空のコマンドリスト"""
        result = service.format_commands(None)
        assert result == ""

        result = service.format_commands([])
        assert result == ""

    def test_format_commands_single(self, service):
        """単一コマンド"""
        result = service.format_commands(["pip install package"])
        assert "```bash" in result
        assert "pip install package" in result
        assert "```" in result

    def test_format_project_structure_empty(self, service):
        """空の構造"""
        result = service.format_project_structure(None)
        assert result == ""

        result = service.format_project_structure({})
        assert result == ""

    def test_format_project_structure_simple(self, service):
        """シンプルな構造"""
        structure = {"src": {"main.py": None}, "README.md": None}
        result = service.format_project_structure(structure)
        assert "src" in result
        assert "main.py" in result
        assert "README.md" in result

    def test_clean_llm_output_markdown_block(self, service):
        """LLM出力のマークダウンブロック除去"""
        content = "```markdown\n# Hello\n```"
        result = service.clean_llm_output(content)
        assert result == "# Hello"

    def test_clean_llm_output_code_block(self, service):
        """LLM出力のコードブロック除去"""
        content = "```\nsome code\n```"
        result = service.clean_llm_output(content)
        assert result == "some code"

    def test_validate_output_empty(self, service):
        """空コンテンツの検証"""
        assert service.validate_output("") is False
        assert service.validate_output(None) is False

    def test_validate_output_too_short(self, service):
        """短すぎるコンテンツの検証"""
        assert service.validate_output("Hello") is False

    def test_validate_output_valid(self, service):
        """有効なコンテンツの検証"""
        content = "This is a valid document content that has more than 50 characters."
        assert service.validate_output(content) is True

    def test_generate_footer(self, service):
        """フッター生成"""
        result = service.generate_footer("README")
        assert "README" in result
        assert "自動生成" in result
