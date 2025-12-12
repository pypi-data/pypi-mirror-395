"""
APIGeneratorのテスト
"""

from pathlib import Path

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.generators.api_generator import APIGenerator


class TestAPIGenerator:
    """APIGeneratorクラスのテスト"""

    def test_api_generator_initialization(self, temp_project):
        """APIGeneratorの初期化テスト"""
        config = {"output": {"api_doc": "docs/api.md"}, "cache": {"enabled": True}}
        generator = APIGenerator(temp_project, ["python"], config)

        assert generator.project_root == temp_project
        assert generator.languages == ["python"]
        assert str(generator.output_path) == str(temp_project / "docs" / "api.md")
        assert generator.cache_manager is not None

    def test_api_generator_initialization_cache_disabled(self, temp_project):
        """キャッシュ無効時の初期化テスト"""
        config = {"output": {"api_doc": "api.md"}, "cache": {"enabled": False}}
        generator = APIGenerator(temp_project, ["python"], config)

        assert generator.cache_manager is None

    def test_generate_api_doc_python(self, temp_project):
        """PythonファイルのAPIドキュメント生成テスト"""
        # Pythonファイルを作成
        (temp_project / "src").mkdir()
        (temp_project / "src" / "__init__.py").write_text("")
        (temp_project / "src" / "main.py").write_text("""
def hello_world(name: str) -> str:
    '''Say hello to the world.

    Args:
        name: The name to greet

    Returns:
        A greeting message
    '''
    return f"Hello, {name}!"

class Calculator:
    '''A simple calculator class.'''

    def add(self, a: int, b: int) -> int:
        '''Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            The sum of a and b
        '''
        return a + b
""")

        config = {"output": {"api_doc": "api.md"}, "cache": {"enabled": False}}

        generator = APIGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "api.md").exists()

        content = (temp_project / "api.md").read_text(encoding="utf-8")
        assert "# API ドキュメント" in content
        assert "hello_world" in content
        assert "Calculator" in content
        assert "add" in content

    def test_generate_api_doc_javascript(self, temp_project):
        """JavaScriptファイルのAPIドキュメント生成テスト"""
        # JavaScriptファイルを作成
        (temp_project / "src").mkdir()
        (temp_project / "src" / "main.js").write_text("""
/**
 * Say hello to the world
 * @param {string} name - The name to greet
 * @returns {string} A greeting message
 */
function helloWorld(name) {
    return `Hello, ${name}!`;
}

/**
 * Calculator class
 */
class Calculator {
    /**
     * Add two numbers
     * @param {number} a - First number
     * @param {number} b - Second number
     * @returns {number} The sum of a and b
     */
    add(a, b) {
        return a + b;
    }
}
""")

        config = {"output": {"api_doc": "api.md"}, "cache": {"enabled": False}}

        generator = APIGenerator(temp_project, ["javascript"], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "api.md").exists()

        content = (temp_project / "api.md").read_text(encoding="utf-8")
        assert "# API ドキュメント" in content
        assert "helloWorld" in content
        assert "Calculator" in content

    def test_generate_api_doc_multiple_languages(self, temp_project):
        """複数言語のAPIドキュメント生成テスト"""
        # Pythonファイル
        (temp_project / "src").mkdir()
        (temp_project / "src" / "main.py").write_text("""
def hello_python(name: str) -> str:
    '''Say hello from Python'''
    return f"Hello from Python, {name}!"
""")

        # JavaScriptファイル
        (temp_project / "src" / "main.js").write_text("""
/**
 * Say hello from JavaScript
 * @param {string} name - The name to greet
 * @returns {string} A greeting message
 */
function helloJavaScript(name) {
    return `Hello from JavaScript, ${name}!`;
}
""")

        config = {"output": {"api_doc": "api.md"}, "cache": {"enabled": False}}

        generator = APIGenerator(temp_project, ["python", "javascript"], config)
        result = generator.generate()

        assert result is True
        content = (temp_project / "api.md").read_text(encoding="utf-8")
        assert "hello_python" in content
        assert "helloJavaScript" in content

    def test_generate_api_doc_empty_project(self, temp_project):
        """空のプロジェクトでのAPIドキュメント生成テスト"""
        config = {"output": {"api_doc": "api.md"}, "cache": {"enabled": False}}

        generator = APIGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "api.md").exists()

        content = (temp_project / "api.md").read_text(encoding="utf-8")
        assert "# API ドキュメント" in content
        # 空のプロジェクトなのでAPIが見つからない旨のメッセージがあるはず
        assert "API" in content

    def test_generate_api_doc_output_directory_creation(self, temp_project):
        """出力ディレクトリが存在しない場合のテスト"""
        config = {"output": {"api_doc": "docs/api/custom.md"}, "cache": {"enabled": False}}

        generator = APIGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "docs" / "api" / "custom.md").exists()

    def test_generate_api_doc_with_cache(self, temp_project):
        """キャッシュ有効時のテスト"""
        # Pythonファイルを作成
        (temp_project / "src").mkdir()
        (temp_project / "src" / "main.py").write_text("""
def cached_function(x: int) -> int:
    '''A cached function'''
    return x * 2
""")

        config = {"output": {"api_doc": "api.md"}, "cache": {"enabled": True}}

        generator = APIGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        assert generator.cache_manager is not None
