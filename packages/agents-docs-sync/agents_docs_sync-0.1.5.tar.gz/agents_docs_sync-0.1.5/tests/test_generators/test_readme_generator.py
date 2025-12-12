"""ReadmeGeneratorのテスト（共通ヘルパー利用版）"""

from pathlib import Path
import sys

# Resolve repo root for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from test_utils.common import write_file
except Exception:
    from pathlib import Path as _Path

    def write_file(root, relative_path, content):
        path = _Path(root) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path


from docgen.generators.readme_generator import ReadmeGenerator


class TestReadmeGenerator:
    """ReadmeGeneratorクラスのテスト"""

    def test_readme_generator_initialization(self, temp_project):
        config = {"output": {"readme": "README.md"}}
        generator = ReadmeGenerator(temp_project, ["python"], config)
        assert generator.project_root == temp_project
        assert generator.languages == ["python"]
        assert generator.config == config
        assert generator.readme_path == temp_project / "README.md"

    def test_generate_readme_without_llm(self, temp_project):
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0\n")
        write_file(
            temp_project,
            "setup.py",
            """
from setuptools import setup
setup(
  name=\"test-project\",
  description=\"A test project\",
  install_requires=[\"pytest\"]
)
""",
        )

        config = {
            "output": {"readme": "README.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": False},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "README.md").exists()

        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert temp_project.name in content

    def test_generate_readme_empty_project(self, temp_project):
        config = {
            "output": {"readme": "README.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": False},
        }

        generator = ReadmeGenerator(temp_project, [], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "README.md").exists()

        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "#" in content  # タイトルが含まれていること

    def test_generate_readme_multiple_languages(self, temp_project):
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0\n")
        write_file(temp_project, "package.json", '{"name": "test-project", "version": "1.0.0"}')

        config = {
            "output": {"readme": "README.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": False},
        }

        generator = ReadmeGenerator(temp_project, ["python", "javascript"], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "README.md").exists()

        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "#" in content

    def test_generate_readme_with_project_info_error(self, temp_project):
        config = {
            "output": {"readme": "README.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": False},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        result = generator.generate()

        # 空プロジェクトでもREADMEは生成されるはず
        assert result is True
        assert (temp_project / "README.md").exists()

    def test_generate_readme_custom_output_path(self, temp_project):
        config = {
            "output": {"readme": "CUSTOM.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": False},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "CUSTOM.md").exists()

    def test_generate_readme_preserve_manual_sections(self, temp_project):
        existing_readme = """
# Project

<!-- MANUAL_START:description -->
This is a manual description that should be preserved.
<!-- MANUAL_END:description -->

## Installation

Standard installation instructions.
"""
        (temp_project / "README.md").write_text(existing_readme)

        config = {
            "output": {"readme": "README.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": True},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True

        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "This is a manual description that should be preserved." in content

    def test_generate_readme_with_llm(self, temp_project):
        # LLMを使用する場合のテスト（モックサービスを使用）
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0\n")

        from unittest.mock import MagicMock

        from docgen.models.readme import ReadmeDocument

        # LLMServiceをモック
        mock_llm_service = MagicMock()
        mock_llm_service.should_use_outlines.return_value = True
        mock_llm_service.get_client.return_value = MagicMock()

        # Outlinesモデルのモック
        mock_outlines_model = MagicMock()
        # 構造化データを返す
        mock_outlines_model.return_value = ReadmeDocument(
            title="Test Project",
            description="This is an LLM generated description.",
            technologies=["Python"],
            dependencies=None,
            setup_instructions=None,
            build_commands=[],
            test_commands=[],
            project_structure=[],
            key_features=[],
            architecture="",
            troubleshooting="",
        )
        mock_llm_service.create_outlines_model.return_value = mock_outlines_model

        # FormattingServiceのモック
        mock_formatting_service = MagicMock()
        mock_formatting_service.format_languages.return_value = "- Python"
        mock_formatting_service.extract_description_section.return_value = "Description"
        # clean_llm_outputなどはそのまま通す
        mock_formatting_service.clean_llm_output.side_effect = lambda x: x
        mock_formatting_service.validate_output.return_value = True
        mock_formatting_service.format_project_structure.return_value = ""
        mock_formatting_service.generate_footer.return_value = "Footer"

        # TemplateServiceのモック
        mock_template_service = MagicMock()
        mock_template_service.format_commands.return_value = ""
        mock_template_service.render.return_value = ""  # setup_templateなどで使われる

        config = {
            "output": {"readme": "README.md"},
            "agents": {"generation": {"readme_mode": "llm"}},
        }

        # コンストラクタでモックサービスを注入
        generator = ReadmeGenerator(
            temp_project,
            ["python"],
            config,
            llm_service=mock_llm_service,
            formatting_service=mock_formatting_service,
            template_service=mock_template_service,
        )

        # _convert_structured_data_to_markdown は内部で formatting_service などを呼ぶので
        # 実際のメソッドを使いたいが、formatting_serviceもモックしているので注意が必要
        # ここでは _convert_structured_data_to_markdown はモックせず、
        # 注入されたモックサービスが正しく呼ばれることを期待する

        # ただし、BaseGeneratorのgenerateメソッド内で formatting_service.validate_output が呼ばれる

        result = generator.generate()

        assert result is True
        assert (temp_project / "README.md").exists()

        # モックが呼ばれたか確認
        mock_llm_service.get_client.assert_called()
        mock_llm_service.create_outlines_model.assert_called()
        mock_outlines_model.assert_called()

    def test_create_overview_prompt(self, temp_project):
        """概要プロンプト作成のテスト"""
        config = {"output": {"readme": "README.md"}}

        # LLMServiceのモック（format_project_info用）
        from unittest.mock import MagicMock

        mock_llm_service = MagicMock()
        mock_llm_service.format_project_info.return_value = "Formatted Project Info"

        generator = ReadmeGenerator(temp_project, ["python"], config, llm_service=mock_llm_service)

        # プロジェクト情報を作成
        from docgen.models.project import ProjectInfo

        project_info = ProjectInfo(
            description="Test project",
            dependencies={"python": ["pytest"]},
            build_commands=["python setup.py build"],
            test_commands=["pytest"],
        )

        existing_overview = "This is existing overview."

        prompt = generator._create_overview_prompt(project_info, existing_overview)

        assert "Formatted Project Info" in prompt
        assert "This is existing overview." in prompt
        # プロンプトローダーの実装に依存するが、テンプレート名などが正しいか確認

    def test_generate_hybrid_readme(self, temp_project):
        """ハイブリッドモードのテスト"""
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0\n")

        config = {
            "output": {"readme": "README.md"},
            "agents": {"generation": {"readme_mode": "hybrid"}},
        }

        from unittest.mock import MagicMock

        # LLMServiceのモック
        mock_llm_service = MagicMock()
        mock_llm_service.generate.return_value = "LLM improved overview content."
        mock_llm_service.format_project_info.return_value = "Project Info"

        # FormattingServiceのモック
        mock_formatting_service = MagicMock()
        mock_formatting_service.clean_llm_output.side_effect = lambda x: x
        mock_formatting_service.validate_output.return_value = True
        # format_languagesなどはデフォルトの動作が必要かもしれないが、
        # _generate_template が呼ばれるので、そこでの呼び出しに対応する必要がある
        # ここでは TemplateService もモックして、_generate_template の結果を制御する方が簡単かも

        # しかし _generate_template は内部メソッドなのでモックしにくい（partial mockが必要）
        # むしろ TemplateService をモックして render の結果を制御する

        mock_template_service = MagicMock()
        mock_template_service.render.return_value = """# Test Project

## 概要

Original Description

## 使用技術
- Python
"""
        mock_template_service.format_commands.return_value = ""

        generator = ReadmeGenerator(
            temp_project,
            ["python"],
            config,
            llm_service=mock_llm_service,
            formatting_service=mock_formatting_service,
            template_service=mock_template_service,
        )

        # _get_project_overview_section で formatting_service.extract_description_section が呼ばれる
        mock_formatting_service.extract_description_section.return_value = "Original Description"

        result = generator.generate()

        assert result is True
        assert (temp_project / "README.md").exists()

        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "LLM improved overview content." in content

        mock_llm_service.generate.assert_called()
