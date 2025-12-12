"""
OutlinesUtilsのテスト
"""

# docgenモジュールをインポート可能にする
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.utils.outlines_utils import create_outlines_model, should_use_outlines


class TestOutlinesUtils:
    """OutlinesUtils関数のテスト"""

    def test_should_use_outlines_enabled_in_config(self):
        """設定でOutlinesが有効な場合のテスト"""
        config = {"use_outlines": True}

        with patch("docgen.utils.outlines_utils.OUTLINES_AVAILABLE", True):
            result = should_use_outlines(config)
            assert result is True

    def test_should_use_outlines_disabled_in_config(self):
        """設定でOutlinesが無効な場合のテスト"""
        config = {"use_outlines": False}

        result = should_use_outlines(config)
        assert result is False

    def test_should_use_outlines_not_in_config(self):
        """設定にOutlines設定がない場合のテスト"""
        config = {}

        result = should_use_outlines(config)
        assert result is False

    def test_should_use_outlines_not_available(self):
        """Outlinesライブラリが利用できない場合のテスト"""
        config = {"use_outlines": True}

        with patch("docgen.utils.outlines_utils.OUTLINES_AVAILABLE", False):
            result = should_use_outlines(config)
            assert result is False

    @patch("docgen.utils.outlines_utils.outlines")
    def test_create_outlines_model_openai(self, mock_outlines):
        """OpenAIプロバイダーのOutlinesモデル作成テスト"""
        mock_client = MagicMock()
        mock_client.client = MagicMock()
        mock_client.client.api_key = "test-key"
        mock_client.model = "gpt-4"
        mock_model = MagicMock()
        mock_outlines.from_openai.return_value = mock_model

        result = create_outlines_model(mock_client, "openai")

        assert result == mock_model
        mock_outlines.from_openai.assert_called_once_with(mock_client.client, mock_client.model)

    def test_create_outlines_model_anthropic(self):
        """AnthropicプロバイダーのOutlinesモデル作成テスト"""
        mock_client = MagicMock()

        result = create_outlines_model(mock_client, "anthropic")

        # Anthropicは現在サポートされていないのでNoneが返される
        assert result is None

    def test_create_outlines_model_local(self):
        """LocalプロバイダーのOutlinesモデル作成テスト"""
        mock_client = MagicMock()
        mock_client.base_url = "http://localhost:11434"
        mock_client.model = "llama3"

        # openaiが利用できない場合を想定
        with patch("builtins.__import__", side_effect=ImportError("No module named 'openai'")):
            result = create_outlines_model(mock_client, "local")

            # openaiが利用できないのでNoneが返される
            assert result is None

    def test_create_outlines_model_unknown_provider(self):
        """未知のプロバイダーのテスト"""
        mock_client = MagicMock()

        result = create_outlines_model(mock_client, "unknown")

        assert result is None

    def test_create_outlines_model_outlines_not_available(self):
        """Outlinesライブラリが利用できない場合のテスト"""
        mock_client = MagicMock()

        with patch("docgen.utils.outlines_utils.outlines", None):
            result = create_outlines_model(mock_client, "openai")
            assert result is None

    @patch("docgen.utils.outlines_utils.outlines")
    def test_create_outlines_model_exception_handling(self, mock_outlines):
        """例外発生時のエラーハンドリングテスト"""
        mock_client = MagicMock()
        mock_client.client = MagicMock()
        mock_client.client.api_key = "test-key"
        mock_client.model = "gpt-4"
        mock_outlines.from_openai.side_effect = Exception("Model creation failed")

        result = create_outlines_model(mock_client, "openai")

        assert result is None

    @patch("docgen.utils.outlines_utils.outlines")
    @patch("docgen.utils.outlines_utils.OUTLINES_AVAILABLE", True)
    def test_integration_with_llm_client_factory(self, mock_outlines, temp_project):
        """LLMClientFactoryとの統合テスト"""
        from docgen.utils.llm import LLMClientFactory

        # OpenAIクライアント設定
        config = {"provider": "openai", "api_key": "test-key", "model": "gpt-4"}

        # モック設定
        mock_client = MagicMock()
        mock_client.client = MagicMock()
        mock_client.client.api_key = "test-key"
        mock_client.model = "gpt-4"
        mock_model = MagicMock()
        mock_outlines.from_openai.return_value = mock_model

        with patch.object(LLMClientFactory, "create_client", return_value=mock_client):
            client = LLMClientFactory.create_client(config)
            model = create_outlines_model(client, "openai")

            assert model == mock_model
            mock_outlines.from_openai.assert_called_once_with(mock_client.client, mock_client.model)
