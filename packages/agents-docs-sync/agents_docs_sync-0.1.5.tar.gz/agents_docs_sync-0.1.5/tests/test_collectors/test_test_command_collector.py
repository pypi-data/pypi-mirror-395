"""
Tests for TestingCommandScanner
"""

import pytest

from docgen.collectors.test_command_collector import TestingCommandScanner as CommandScanner


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project structure"""
    return tmp_path


def test_collect_from_scripts(temp_project):
    """Test collecting from scripts/run_tests.sh"""
    scripts_dir = temp_project / "scripts"
    scripts_dir.mkdir()
    run_tests = scripts_dir / "run_tests.sh"
    run_tests.write_text("pytest tests/\n", encoding="utf-8")

    collector = CommandScanner(temp_project)
    commands = collector.collect_test_commands()

    assert "pytest tests/" in commands


def test_collect_from_makefile(temp_project):
    """Test collecting from Makefile"""
    makefile = temp_project / "Makefile"
    makefile.write_text("test:\n\tpytest tests/\n", encoding="utf-8")

    collector = CommandScanner(temp_project)
    commands = collector.collect_test_commands()

    assert "pytest tests/" in commands


def test_collect_python_defaults(temp_project):
    """Test collecting Python defaults"""
    collector = CommandScanner(temp_project, package_managers={"python": "pip"})
    commands = collector.collect_test_commands()

    assert "pytest tests/ -v --tb=short" in commands


def test_collect_uv_defaults(temp_project):
    """Test collecting uv defaults"""
    collector = CommandScanner(temp_project, package_managers={"python": "uv"})
    commands = collector.collect_test_commands()

    assert "uv run pytest tests/ -v --tb=short" in commands


def test_collect_nodejs_defaults(temp_project):
    """Test collecting Node.js defaults"""
    package_json = temp_project / "package.json"
    package_json.write_text('{"scripts": {"test": "jest"}}', encoding="utf-8")

    collector = CommandScanner(temp_project, package_managers={"javascript": "npm"})
    commands = collector.collect_test_commands()

    assert "npm test" in commands
