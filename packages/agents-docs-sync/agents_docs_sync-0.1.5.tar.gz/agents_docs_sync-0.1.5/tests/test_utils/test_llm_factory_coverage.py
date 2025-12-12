"""
Coverage tests for LLMClientFactory.
"""

from unittest.mock import MagicMock, patch

from docgen.models.llm import LLMClientConfig, LLMConfig
from docgen.utils.llm.anthropic_client import AnthropicClient
from docgen.utils.llm.factory import LLMClientFactory
from docgen.utils.llm.openai_client import OpenAIClient


class TestLLMClientFactoryCoverage:
    def test_create_client_llm_config_openai(self):
        config = LLMClientConfig(openai=LLMConfig(provider="openai", api_key="test", model="gpt-4"))
        client = LLMClientFactory.create_client(config, mode="api")
        assert isinstance(client, OpenAIClient)

    def test_create_client_llm_config_anthropic(self):
        config = LLMClientConfig(
            anthropic=LLMConfig(provider="anthropic", api_key="test", model="claude-3")
        )
        client = LLMClientFactory.create_client(config, mode="api")
        assert isinstance(client, AnthropicClient)

    def test_create_client_dict_custom(self):
        config = {
            "api": {"provider": "custom", "api_key": "test", "base_url": "http://localhost:1234"}
        }
        client = LLMClientFactory.create_client(config, mode="api")
        assert isinstance(client, OpenAIClient)

    def test_create_client_dict_invalid_provider(self):
        config = {"api": {"provider": "invalid"}}
        client = LLMClientFactory.create_client(config, mode="api")
        assert client is None

    def test_create_client_local(self):
        config = {"local": {"model_path": "/tmp/model"}}
        with patch("docgen.utils.llm.factory.LocalLLMClient"):
            client = LLMClientFactory.create_client(config, mode="local")
            assert client is not None

    def test_create_client_invalid_mode(self):
        client = LLMClientFactory.create_client({}, mode="invalid")
        assert client is None

    def test_create_client_exception(self):
        with patch("docgen.utils.llm.factory.OpenAIClient", side_effect=Exception("Error")):
            config = {"api": {"provider": "openai"}}
            client = LLMClientFactory.create_client(config, mode="api")
            assert client is None

    def test_create_client_with_fallback_success(self):
        config = {"api": {"provider": "openai"}}
        with patch("docgen.utils.llm.factory.LLMClientFactory.create_client") as mock_create:
            mock_create.return_value = MagicMock()
            client = LLMClientFactory.create_client_with_fallback(config, preferred_mode="api")
            assert client is not None
            mock_create.assert_called_once_with(config, "api")

    def test_create_client_with_fallback_trigger(self):
        config = {"api": {"provider": "openai"}}
        with patch("docgen.utils.llm.factory.LLMClientFactory.create_client") as mock_create:
            # First call fails, second succeeds
            mock_create.side_effect = [None, MagicMock()]
            client = LLMClientFactory.create_client_with_fallback(config, preferred_mode="api")
            assert client is not None
            assert mock_create.call_count == 2
            mock_create.assert_any_call(config, "api")
            mock_create.assert_any_call(config, "local")
