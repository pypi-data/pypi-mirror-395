"""
TemplateService のテスト
"""

import pytest
from pathlib import Path

from docgen.generators.services.template_service import TemplateService


class TestTemplateService:
    """TemplateService のテストクラス"""

    @pytest.fixture
    def service(self):
        """TemplateService インスタンス"""
        return TemplateService()

    def test_initialization_default_template_dir(self, service):
        """デフォルトテンプレートディレクトリの初期化"""
        assert service._template_dir is not None
        assert isinstance(service._template_dir, Path)

    def test_initialization_custom_template_dir(self, tmp_path):
        """カスタムテンプレートディレクトリの初期化"""
        service = TemplateService(template_dir=tmp_path)
        assert service._template_dir == tmp_path

    def test_format_commands_empty(self, service):
        """空コマンドリスト"""
        result = service.format_commands([])
        assert result == ""

    def test_format_commands_single(self, service):
        """単一コマンド"""
        result = service.format_commands(["npm install"])
        assert "```bash" in result
        assert "npm install" in result
        assert "```" in result

    def test_format_commands_multiple(self, service):
        """複数コマンド"""
        commands = ["npm install", "npm run build", "npm test"]
        result = service.format_commands(commands)
        assert "npm install" in result
        assert "npm run build" in result
        assert "npm test" in result

    def test_format_commands_more_than_five(self, service):
        """5つ以上のコマンド（切り詰め）"""
        commands = [f"command{i}" for i in range(10)]
        result = service.format_commands(commands)
        assert "その他のコマンド" in result

    def test_format_custom_instructions_string(self, service):
        """文字列形式のカスタム指示"""
        result = service.format_custom_instructions("Follow these rules.")
        assert "プロジェクト固有の指示" in result[0]
        assert "Follow these rules." in result

    def test_format_custom_instructions_dict(self, service):
        """辞書形式のカスタム指示"""
        instructions = {
            "Coding Style": "Use PEP8",
            "Testing": "Write unit tests"
        }
        result = service.format_custom_instructions(instructions)
        lines = result
        joined = "\n".join(lines)
        assert "Coding Style" in joined
        assert "Use PEP8" in joined
        assert "Testing" in joined
