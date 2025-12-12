"""
Tests for DependencyCollector
"""

import pytest

from docgen.collectors.dependency_collector import DependencyCollector


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project structure"""
    return tmp_path


def test_collect_python_dependencies(temp_project):
    """Test collecting Python dependencies"""
    req_file = temp_project / "requirements.txt"
    req_file.write_text("pytest>=7.0.0\nrequests\n# comment\n", encoding="utf-8")

    collector = DependencyCollector(temp_project)
    deps = collector.collect_dependencies()

    assert "python" in deps
    assert "pytest>=7.0.0" in deps["python"]
    assert "requests" in deps["python"]
    assert "# comment" not in deps["python"]


def test_collect_nodejs_dependencies(temp_project):
    """Test collecting Node.js dependencies"""
    package_json = temp_project / "package.json"
    package_json.write_text(
        '{"dependencies": {"react": "^18.0.0", "axios": "^1.0.0"}}', encoding="utf-8"
    )

    collector = DependencyCollector(temp_project)
    deps = collector.collect_dependencies()

    assert "nodejs" in deps
    assert "react@^18.0.0" in deps["nodejs"]
    assert "axios@^1.0.0" in deps["nodejs"]


def test_collect_go_dependencies(temp_project):
    """Test collecting Go dependencies"""
    go_mod = temp_project / "go.mod"
    go_mod.write_text(
        """module example.com/myproject

go 1.21

require (
	github.com/gin-gonic/gin v1.9.1
	github.com/stretchr/testify v1.8.4
)

require github.com/google/uuid v1.3.1
""",
        encoding="utf-8",
    )

    collector = DependencyCollector(temp_project)
    deps = collector.collect_dependencies()

    assert "go" in deps
    assert "github.com/gin-gonic/gin" in deps["go"]
    assert "github.com/stretchr/testify" in deps["go"]
    assert "github.com/google/uuid" in deps["go"]


def test_deduplication(temp_project):
    """Test dependency deduplication"""
    req_file = temp_project / "requirements.txt"
    req_file.write_text("pytest\npytest\nrequests\n", encoding="utf-8")

    collector = DependencyCollector(temp_project)
    deps = collector.collect_dependencies()

    assert "python" in deps
    assert len(deps["python"]) == 2
    assert deps["python"] == ["pytest", "requests"]
