"""
Coverage tests for BaseGenerator.
"""

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from docgen.generators.base_generator import BaseGenerator
from docgen.models.project import ProjectInfo


class ConcreteGenerator(BaseGenerator):
    def _get_mode_key(self) -> str:
        return "test_mode"

    def _get_output_key(self) -> str:
        return "test_output"

    def _get_document_type(self) -> str:
        return "TestDoc"

    def _convert_structured_data_to_markdown(
        self, structured_data: Any, project_info: ProjectInfo
    ) -> str:
        return "Converted Markdown"

    def _get_project_overview_section(self, content: str) -> str:
        return "Overview"

    def _get_structured_model(self) -> Any:
        return MagicMock()

    def _create_llm_prompt(self, project_info: ProjectInfo, rag_context: str = "") -> str:
        return "Prompt"

    def _generate_template(self, project_info: ProjectInfo) -> str:
        return "Template Markdown"


class TestBaseGeneratorCoverage:
    @pytest.fixture
    def project_root(self, tmp_path):
        return tmp_path

    @pytest.fixture
    def config(self):
        return {
            "agents": {"generation": {"test_mode": "template"}},
            "output": {"test_output": "TEST.md"},
        }

    @pytest.fixture
    def generator(self, project_root, config):
        return ConcreteGenerator(project_root, ["python"], config)

    def test_extract_manual_sections_from_existing_no_file(self, generator):
        """Test extraction when file does not exist."""
        sections = generator._extract_manual_sections_from_existing()
        assert sections == {}

    def test_extract_manual_sections_from_existing_error(self, generator):
        """Test extraction when read fails."""
        # Create file but make it unreadable (simulated by patch)
        generator.output_path.write_text("content")
        with patch.object(Path, "read_text", side_effect=Exception("Read error")):
            sections = generator._extract_manual_sections_from_existing()
            assert sections == {}

    def test_generate_success(self, generator, project_root):
        """Test successful generation."""
        # Mock collector
        generator.collector = MagicMock()
        generator.collector.collect_all.return_value = ProjectInfo()

        # Mock formatting_service
        generator.formatting_service = MagicMock()
        generator.formatting_service.validate_output.return_value = True

        success = generator.generate()
        assert success is True
        assert (project_root / "TEST.md").exists()
        assert (project_root / "TEST.md").read_text() == "Template Markdown"

    def test_generate_validation_failure(self, generator):
        """Test generation with validation failure."""
        generator.collector = MagicMock()
        generator.collector.collect_all.return_value = ProjectInfo()

        # Mock formatting_service
        generator.formatting_service = MagicMock()
        generator.formatting_service.validate_output.return_value = False

        success = generator.generate()
        assert success is False

    def test_generate_exception(self, generator):
        """Test generation with exception."""
        generator.collector = MagicMock()
        generator.collector.collect_all.side_effect = Exception("Collection error")

        success = generator.generate()
        assert success is False

    def test_get_output_path_absolute(self, project_root, config):
        """Test _get_output_path with absolute path."""
        abs_path = project_root / "ABS.md"
        config["output"]["test_output"] = str(abs_path)
        gen = ConcreteGenerator(project_root, ["python"], config)
        assert gen.output_path == abs_path

    def test_generate_markdown_llm_mode(self, generator):
        """Test _generate_markdown in LLM mode."""
        generator.agents_config["generation"]["test_mode"] = "llm"
        generator._generate_with_llm = MagicMock(return_value="LLM Markdown")

        md = generator._generate_markdown(ProjectInfo())
        assert md == "LLM Markdown"
        generator._generate_with_llm.assert_called_once()

    def test_generate_markdown_hybrid_mode(self, generator):
        """Test _generate_markdown in hybrid mode."""
        generator.agents_config["generation"]["test_mode"] = "hybrid"
        generator._generate_hybrid = MagicMock(return_value="Hybrid Markdown")

        md = generator._generate_markdown(ProjectInfo())
        assert md == "Hybrid Markdown"
        generator._generate_hybrid.assert_called_once()
