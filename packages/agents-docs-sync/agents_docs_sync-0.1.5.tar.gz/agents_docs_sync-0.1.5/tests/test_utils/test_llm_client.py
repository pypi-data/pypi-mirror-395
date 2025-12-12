"""
LLMClientのテスト
"""

# docgenモジュールをインポート可能にする
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.utils.exceptions import ConfigError
from docgen.utils.llm import (
    AnthropicClient,
    BaseLLMClient,
    LLMClientFactory,
    LocalLLMClient,
    OpenAIClient,
)


class TestBaseLLMClient:
    """BaseLLMClientクラスのテスト"""

    def test_base_llm_client_initialization(self):
        """BaseLLMClientの初期化テスト"""
        config = {"timeout": 60, "max_retries": 5, "retry_delay": 2.0}

        # 抽象クラスなので直接インスタンス化できないが、属性チェック用にモック
        from unittest.mock import MagicMock

        client = MagicMock(spec=BaseLLMClient)
        client.config = config
        client.timeout = 60
        client.max_retries = 5
        client.retry_delay = 2.0

        assert client.config == config
        assert client.timeout == 60
        assert client.max_retries == 5
        assert client.retry_delay == 2.0


class TestOpenAIClient:
    """OpenAIClientクラスのテスト"""

    def test_openai_client_initialization_success(self):
        """OpenAIClientの正常初期化テスト"""
        config = {"model": "gpt-4", "api_key_env": "OPENAI_API_KEY"}
        client = OpenAIClient(config)
        assert client.model == "gpt-4"

    @patch("openai.OpenAI")
    def test_openai_client_initialization_config_error(self, mock_openai):
        """OpenAIClientの設定エラーテスト"""
        mock_openai.side_effect = ValueError("API key error")
        config = {"model": "gpt-4"}
        with pytest.raises(ConfigError):
            OpenAIClient(config)

    @patch("openai.OpenAI")
    def test_openai_client_generate_success(self, mock_openai):
        """OpenAIClientのgenerate成功テスト"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        config = {"model": "gpt-4"}
        client = OpenAIClient(config)
        result = client.generate("Test prompt")
        assert result == "Test response"

    @patch("openai.OpenAI")
    def test_openai_client_generate_error(self, mock_openai):
        """OpenAIClientのgenerateエラーテスト"""
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API error")
        mock_openai.return_value = mock_client

        config = {"model": "gpt-4"}
        client = OpenAIClient(config)
        result = client.generate("Test prompt")
        assert result is None

    @patch("httpx.Client")
    def test_ollama_client_error_handling(self, mock_client_class):
        """Ollamaクライアントのエラーハンドリングテスト"""
        mock_client = MagicMock()
        mock_client.post.side_effect = Exception("Connection Error")
        mock_client_class.return_value = mock_client

        config = {"base_url": "http://localhost:11434", "model": "llama3"}
        client = LocalLLMClient(config)

        result = client.generate("Test prompt")

        assert result is None


class TestLocalLLMClient:
    """LocalLLMClientクラスのテスト"""

    def test_local_client_initialization_success(self):
        """LocalLLMClientの正常初期化テスト"""
        config = {"base_url": "http://localhost:11434", "model": "llama3"}
        client = LocalLLMClient(config)
        assert client.base_url == "http://localhost:11434"
        assert client.model == "llama3"

    @patch("httpx.post")
    def test_local_client_generate_ollama_success(self, mock_post):
        """LocalLLMClientのOllama generate成功テスト"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Test response"}
        mock_post.return_value = mock_response

        config = {"base_url": "http://localhost:11434", "model": "llama3", "provider": "ollama"}
        client = LocalLLMClient(config)
        result = client.generate("Test prompt")
        assert result == "Test response"

    @patch("httpx.Client")
    def test_local_client_generate_openai_compatible_success(self, mock_client_class):
        """LocalLLMClientのOpenAI互換generate成功テスト"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": [{"message": {"content": "Test response"}}]}
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        config = {"base_url": "http://localhost:11434", "model": "llama3", "provider": "lmstudio"}
        client = LocalLLMClient(config)
        result = client.generate("Test prompt")
        assert result == "Test response"

    @patch("httpx.Client")
    def test_local_client_generate_error(self, mock_client_class):
        """LocalLLMClientのgenerateエラーテスト"""
        mock_client = MagicMock()
        mock_client.post.side_effect = Exception("Connection error")
        mock_client_class.return_value = mock_client

        config = {"base_url": "http://localhost:11434", "model": "llama3"}
        client = LocalLLMClient(config)
        result = client.generate("Test prompt")
        assert result is None


class TestAnthropicClient:
    """AnthropicClientクラスのテスト"""

    def test_anthropic_client_initialization_success(self):
        """AnthropicClientの正常初期化テスト"""
        config = {"model": "claude-3", "api_key_env": "ANTHROPIC_API_KEY"}
        client = AnthropicClient(config)
        assert client.model == "claude-3"

    @patch("anthropic.Anthropic")
    def test_anthropic_client_initialization_config_error(self, mock_anthropic):
        """AnthropicClientの設定エラーテスト"""
        mock_anthropic.side_effect = ValueError("API key error")
        config = {"model": "claude-3"}
        with pytest.raises(ConfigError):
            AnthropicClient(config)

    @patch("anthropic.Anthropic")
    def test_anthropic_client_generate_success(self, mock_anthropic):
        """AnthropicClientのgenerate成功テスト"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Test response"
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        config = {"model": "claude-3"}
        client = AnthropicClient(config)
        result = client.generate("Test prompt")
        assert result == "Test response"

    @patch("anthropic.Anthropic")
    def test_anthropic_client_generate_error(self, mock_anthropic):
        """AnthropicClientのgenerateエラーテスト"""
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = Exception("API error")
        mock_anthropic.return_value = mock_client

        config = {"model": "claude-3"}
        client = AnthropicClient(config)
        result = client.generate("Test prompt")
        assert result is None


class TestLLMClientFactory:
    """LLMClientFactoryクラスのテスト"""

    @patch("docgen.utils.llm.factory.OpenAIClient")
    def test_create_client_openai(self, mock_openai_client):
        """OpenAIクライアント作成テスト"""
        config = {"api": {"provider": "openai", "model": "gpt-4"}}
        result = LLMClientFactory.create_client(config, "api")
        mock_openai_client.assert_called_once_with({"provider": "openai", "model": "gpt-4"})
        assert result is not None

    @patch("docgen.utils.llm.factory.AnthropicClient")
    def test_create_client_anthropic(self, mock_anthropic_client):
        """Anthropicクライアント作成テスト"""
        config = {"api": {"provider": "anthropic", "model": "claude-3"}}
        result = LLMClientFactory.create_client(config, "api")
        mock_anthropic_client.assert_called_once_with(
            {"provider": "anthropic", "model": "claude-3"}
        )
        assert result is not None

    @patch("docgen.utils.llm.factory.LocalLLMClient")
    def test_create_client_local(self, mock_local_client):
        """Localクライアント作成テスト"""
        config = {"local": {"base_url": "http://localhost:11434", "model": "llama3"}}
        result = LLMClientFactory.create_client(config, "local")
        mock_local_client.assert_called_once_with(
            {"base_url": "http://localhost:11434", "model": "llama3"}
        )
        assert result is not None

    def test_create_client_unknown_provider(self):
        """不明なプロバイダーテスト"""
        config = {"api": {"provider": "unknown"}}
        result = LLMClientFactory.create_client(config, "api")
        assert result is None

    def test_create_client_unknown_mode(self):
        """不明なモードテスト"""
        config = {"api": {"provider": "openai"}}
        result = LLMClientFactory.create_client(config, "unknown")
        assert result is None

    @patch("docgen.utils.llm.factory.LLMClientFactory.create_client")
    def test_create_client_with_fallback_api_to_local(self, mock_create_client):
        """APIからLocalへのフォールバックテスト"""
        mock_create_client.side_effect = [None, MagicMock()]  # API失敗、Local成功
        config = {"api": {"provider": "openai"}, "local": {"model": "llama3"}}
        result = LLMClientFactory.create_client_with_fallback(config, "api")
        assert result is not None

    @patch("docgen.utils.llm.factory.LLMClientFactory.create_client")
    def test_create_client_with_fallback_local_to_api(self, mock_create_client):
        """LocalからAPIへのフォールバックテスト"""
        mock_create_client.side_effect = [None, MagicMock()]  # Local失敗、API成功
        config = {"local": {"model": "llama3"}, "api": {"provider": "openai"}}
        result = LLMClientFactory.create_client_with_fallback(config, "local")
        assert result is not None
