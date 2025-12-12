import os
from pathlib import Path
import shutil
import tempfile

import pytest

# Set environment variable for testing at module level to ensure it's set before logger initialization
os.environ["DOCGEN_TESTING"] = "1"


@pytest.fixture(autouse=True)
def set_test_env():
    """Ensure environment variable is set (redundant but safe)."""
    os.environ["DOCGEN_TESTING"] = "1"
    yield
    # Do not remove it as other tests might need it if run in same process
    # But for safety we can keep it. Or we can just rely on module level.
    # Let's keep the fixture to be explicit about scope if needed, but module level is key.


@pytest.fixture(scope="function")
def temp_project():
    """Create a temporary project directory with basic structure."""
    temp_dir = Path(tempfile.mkdtemp())

    (temp_dir / "docgen").mkdir()
    (temp_dir / "docgen" / "config.toml").write_text("""
[output]
agents_doc = "AGENTS.md"
api_doc = "api.md"
readme = "README.md"

[agents]
llm_mode = "both"

[agents.api]
provider = "openai"
api_key_env = "OPENAI_API_KEY"

[agents.local]
provider = "ollama"
model = "llama3"
base_url = "http://localhost:11434"

[project]
name = "test-project"
description = "Test project for agents-docs-sync"
languages = ["python"]
""")
    yield temp_dir

    # Clean up
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="function")
def sample_config():
    """Return a sample configuration dictionary."""
    return {
        "output": {"agents_doc": "AGENTS.md", "api_doc": "api.md", "readme": "README.md"},
        "agents": {
            " llm_mode": "both",
            "api": {"provider": "openai", "api_key_env": "OPENAI_API_KEY"},
            "local": {
                "provider": "ollama",
                "model": "llama3",
                "base_url": "http://localhost:11434",
            },
        },
        "project": {
            "name": "test-project",
            "description": "Test project for agents-docs-sync",
            "languages": ["python"],
        },
    }


@pytest.fixture(scope="function")
def mock_llm_client(mocker):
    """Mock LLMクライアント"""
    mock_client = mocker.Mock()
    mock_client.generate.return_value = "Mocked LLM response"
    return mock_client
