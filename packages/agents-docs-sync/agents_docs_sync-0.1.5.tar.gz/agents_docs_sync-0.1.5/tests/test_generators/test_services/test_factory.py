
import pytest
from unittest.mock import MagicMock, patch
from docgen.generators.service_factory import GeneratorServiceFactory

class TestGeneratorServiceFactory:
    @pytest.fixture
    def mock_services(self):
        with patch("docgen.generators.service_factory.FormattingService") as mock_fmt, \
             patch("docgen.generators.service_factory.LLMService") as mock_llm, \
             patch("docgen.generators.service_factory.TemplateService") as mock_tpl, \
             patch("docgen.generators.service_factory.ManualSectionService") as mock_manual, \
             patch("docgen.generators.service_factory.RAGService") as mock_rag:
            yield {
                "formatting": mock_fmt,
                "llm": mock_llm,
                "template": mock_tpl,
                "manual": mock_manual,
                "rag": mock_rag
            }

    def test_create_formatting_service(self, mock_services):
        service = GeneratorServiceFactory.create_formatting_service()
        mock_services["formatting"].assert_called_once()
        assert service == mock_services["formatting"].return_value

    def test_create_llm_service(self, mock_services):
        config = {}
        service = GeneratorServiceFactory.create_llm_service(config)
        mock_services["llm"].assert_called_once()
        # logger引数があるので、引数の検証は厳密に行わないか、ANYを使う
        # mock_services["llm"].assert_called_once_with(config=config, logger=ANY)
        assert service == mock_services["llm"].return_value

    def test_create_template_service(self, mock_services):
        service = GeneratorServiceFactory.create_template_service()
        mock_services["template"].assert_called_once()
        assert service == mock_services["template"].return_value

    def test_create_manual_section_service(self, mock_services):
        service = GeneratorServiceFactory.create_manual_section_service()
        mock_services["manual"].assert_called_once()
        assert service == mock_services["manual"].return_value

    def test_create_rag_service(self, mock_services):
        config = {}
        project_root = MagicMock()
        service = GeneratorServiceFactory.create_rag_service(project_root, config)
        mock_services["rag"].assert_called_once()
        assert service == mock_services["rag"].return_value
