"""
Tests for CodingStandardsCollector
"""

import pytest

from docgen.collectors.coding_standards_collector import CodingStandardsCollector


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project structure"""
    return tmp_path


def test_collect_from_pyproject_toml(temp_project):
    """Test collecting from pyproject.toml"""
    pyproject = temp_project / "pyproject.toml"
    pyproject.write_text(
        """
[tool.black]
line-length = 88

[tool.ruff]
select = ["E", "F"]
""",
        encoding="utf-8",
    )

    collector = CodingStandardsCollector(temp_project)
    standards = collector.collect_coding_standards()

    assert standards.get("formatter") == "black"
    assert standards.get("linter") == "ruff"
    assert standards.get("black_config") == {"line-length": 88}


def test_collect_editorconfig(temp_project):
    """Test collecting .editorconfig"""
    editorconfig = temp_project / ".editorconfig"
    editorconfig.write_text("root = true", encoding="utf-8")

    collector = CodingStandardsCollector(temp_project)
    standards = collector.collect_coding_standards()

    assert standards.get("editorconfig") is True


def test_collect_prettier(temp_project):
    """Test collecting Prettier config"""
    prettier = temp_project / ".prettierrc"
    prettier.write_text("{}", encoding="utf-8")

    collector = CodingStandardsCollector(temp_project)
    standards = collector.collect_coding_standards()

    assert standards.get("formatter") == "prettier"
