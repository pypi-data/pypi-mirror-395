"""UnifiedDetectorのテスト（統合版）

個別の言語detectorをUnifiedDetectorに統合したため、
すべての言語検出テストをこのファイルに統合します。
"""

try:
    from test_utils.common import write_file
except Exception:
    from pathlib import Path as _Path

    def write_file(root, relative_path, content):
        path = _Path(root) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path


from docgen.detectors.unified_detector import UnifiedDetector, UnifiedDetectorFactory


class TestUnifiedDetectorPython:
    """Python言語検出のテスト"""

    def test_detect_with_requirements_txt(self, temp_project):
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0")
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect() is True
        assert detector.get_language() == "python"

    def test_detect_with_setup_py(self, temp_project):
        write_file(temp_project, "setup.py", "from setuptools import setup\nsetup(name='test')\n")
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect() is True

    def test_detect_with_pyproject_toml(self, temp_project):
        write_file(temp_project, "pyproject.toml", '[build-system]\nrequires = ["setuptools"]\n')
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect() is True

    def test_detect_with_py_files(self, temp_project):
        write_file(temp_project, "script.py", "print('hello')\n")
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect() is True

    def test_detect_without_python(self, temp_project):
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect() is False

    def test_get_language(self, temp_project):
        detector = UnifiedDetector(temp_project, "python")
        assert detector.get_language() == "python"

    def test_detect_package_manager_uv(self, temp_project):
        write_file(temp_project, "uv.lock", "# uv lock file")
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect_package_manager() == "uv"

    def test_detect_package_manager_poetry(self, temp_project):
        write_file(temp_project, "poetry.lock", "# poetry lock file")
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect_package_manager() == "poetry"

    def test_detect_package_manager_poetry_pyproject(self, temp_project):
        write_file(temp_project, "pyproject.toml", '[tool.poetry]\nname = "test"\n')
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect_package_manager() == "poetry"

    def test_detect_package_manager_conda(self, temp_project):
        write_file(temp_project, "environment.yml", "name: test\n")
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect_package_manager() == "conda"

    def test_detect_package_manager_pip_requirements(self, temp_project):
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0")
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect_package_manager() == "pip"

    def test_detect_package_manager_pip_setup_py(self, temp_project):
        write_file(temp_project, "setup.py", "from setuptools import setup\nsetup(name='test')\n")
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect_package_manager() == "pip"

    def test_detect_package_manager_none(self, temp_project):
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect_package_manager() is None

    def test_detect_with_nested_python_files(self, temp_project):
        write_file(temp_project, "src/package/sub/module.py", "def func(): pass\n")
        detector = UnifiedDetector(temp_project, "python")
        assert detector.detect() is True


class TestUnifiedDetectorJavaScript:
    """JavaScript/TypeScript言語検出のテスト"""

    def test_detect_with_package_json(self, temp_project):
        write_file(temp_project, "package.json", '{"name": "test"}')
        detector = UnifiedDetector(temp_project, "javascript")
        assert detector.detect() is True
        assert detector.get_language() == "javascript"

    def test_detect_with_js_files(self, temp_project):
        write_file(temp_project, "index.js", "console.log('test');")
        detector = UnifiedDetector(temp_project, "javascript")
        assert detector.detect() is True

    def test_detect_with_jsx_files(self, temp_project):
        write_file(temp_project, "App.jsx", "export default () => <div>Test</div>;")
        detector = UnifiedDetector(temp_project, "javascript")
        assert detector.detect() is True

    def test_detect_without_javascript(self, temp_project):
        detector = UnifiedDetector(temp_project, "javascript")
        assert detector.detect() is False

    def test_detect_package_manager_pnpm(self, temp_project):
        write_file(temp_project, "pnpm-lock.yaml", "lockfileVersion: '6.0'")
        detector = UnifiedDetector(temp_project, "javascript")
        assert detector.detect_package_manager() == "pnpm"

    def test_detect_package_manager_yarn(self, temp_project):
        write_file(temp_project, "yarn.lock", "# yarn lockfile v1")
        detector = UnifiedDetector(temp_project, "javascript")
        assert detector.detect_package_manager() == "yarn"

    def test_detect_package_manager_npm(self, temp_project):
        write_file(temp_project, "package-lock.json", '{"lockfileVersion": 2}')
        detector = UnifiedDetector(temp_project, "javascript")
        assert detector.detect_package_manager() == "npm"

    def test_detect_package_manager_bun(self, temp_project):
        write_file(temp_project, "bun.lockb", "binary lock file")
        detector = UnifiedDetector(temp_project, "javascript")
        assert detector.detect_package_manager() == "bun"


class TestUnifiedDetectorGo:
    """Go言語検出のテスト"""

    def test_detect_with_go_mod(self, temp_project):
        write_file(temp_project, "go.mod", "module example.com/myapp\n\ngo 1.20\n")
        detector = UnifiedDetector(temp_project, "go")
        assert detector.detect() is True
        assert detector.get_language() == "go"

    def test_detect_with_go_files(self, temp_project):
        write_file(temp_project, "main.go", "package main\n\nfunc main() {}\n")
        detector = UnifiedDetector(temp_project, "go")
        assert detector.detect() is True

    def test_detect_without_go(self, temp_project):
        detector = UnifiedDetector(temp_project, "go")
        assert detector.detect() is False

    def test_detect_package_manager_go(self, temp_project):
        write_file(temp_project, "go.mod", "module example.com/myapp\n")
        detector = UnifiedDetector(temp_project, "go")
        assert detector.detect_package_manager() == "go"


class TestUnifiedDetectorGeneric:
    """その他の言語検出のテスト"""

    def test_detect_rust(self, temp_project):
        write_file(temp_project, "src/main.rs", "fn main() {}\n")
        detector = UnifiedDetector(temp_project, "rust")
        assert detector.detect() is True
        assert detector.get_language() == "rust"

    def test_detect_java(self, temp_project):
        write_file(temp_project, "Main.java", "public class Main {}\n")
        detector = UnifiedDetector(temp_project, "java")
        assert detector.detect() is True
        assert detector.get_language() == "java"

    def test_detect_cpp(self, temp_project):
        write_file(temp_project, "main.cpp", "int main() { return 0; }\n")
        detector = UnifiedDetector(temp_project, "cpp")
        assert detector.detect() is True
        assert detector.get_language() == "cpp"

    def test_detect_ruby(self, temp_project):
        write_file(temp_project, "script.rb", "puts 'Hello'\n")
        detector = UnifiedDetector(temp_project, "ruby")
        assert detector.detect() is True
        assert detector.get_language() == "ruby"


class TestUnifiedDetectorFactory:
    """UnifiedDetectorFactoryのテスト"""

    def test_get_all_languages(self):
        languages = UnifiedDetectorFactory.get_all_languages()
        assert "python" in languages
        assert "javascript" in languages
        assert "go" in languages
        assert "typescript" in languages
        assert "rust" in languages
        assert isinstance(languages, list)
        assert len(languages) > 0

    def test_create_detector(self, temp_project):
        detector = UnifiedDetectorFactory.create_detector(temp_project, "python")
        assert isinstance(detector, UnifiedDetector)
        assert detector.get_language() == "python"

    def test_create_all_detectors(self, temp_project):
        detectors = UnifiedDetectorFactory.create_all_detectors(temp_project)
        assert len(detectors) > 0
        assert all(isinstance(d, UnifiedDetector) for d in detectors)

        # すべての主要言語がカバーされているか
        languages = [d.get_language() for d in detectors]
        assert "python" in languages
        assert "javascript" in languages
        assert "go" in languages
