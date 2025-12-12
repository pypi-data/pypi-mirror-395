
import pytest
from unittest.mock import MagicMock, patch
from docgen.generators.services.rag_service import RAGService

class TestRAGService:
    @pytest.fixture
    def mock_indexer(self):
        with patch("docgen.rag.retriever.DocumentRetriever") as mock:
            yield mock

    @pytest.fixture
    def service(self, mock_indexer):
        config = {"rag": {"enabled": True}}
        project_root = MagicMock()
        return RAGService(project_root, config)

    def test_initialization_enabled(self, mock_indexer):
        config = {"rag": {"enabled": True}}
        project_root = MagicMock()
        service = RAGService(project_root, config)
        assert service.is_enabled is True
        mock_indexer.assert_not_called()

    def test_initialization_disabled(self, mock_indexer):
        config = {"rag": {"enabled": False}}
        project_root = MagicMock()
        service = RAGService(project_root, config)
        assert service.is_enabled is False
        mock_indexer.assert_not_called()

    def test_get_context_enabled(self, service, mock_indexer):
        mock_instance = mock_indexer.return_value
        mock_instance.retrieve.return_value = ["Result 1", "Result 2"]
        mock_instance.format_context.return_value = "Result 1\nResult 2"

        context = service.get_context("query")

        assert "Result 1" in context
        assert "Result 2" in context
        mock_instance.retrieve.assert_called_with("query", top_k=6)

    def test_get_context_disabled(self, mock_indexer):
        config = {"rag": {"enabled": False}}
        project_root = MagicMock()
        service = RAGService(project_root, config)

        context = service.get_context("query")

        assert context == ""
        mock_indexer.assert_not_called()

    def test_get_context_error(self, service, mock_indexer):
        mock_instance = mock_indexer.return_value
        mock_instance.retrieve.side_effect = Exception("Query error")

        context = service.get_context("query")

        assert context == ""
