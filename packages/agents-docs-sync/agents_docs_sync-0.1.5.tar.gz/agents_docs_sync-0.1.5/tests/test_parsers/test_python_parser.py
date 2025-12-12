"""
PythonParserのテスト
"""

from pathlib import Path

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.generators.parsers.python_parser import PythonParser


class TestPythonParser:
    """PythonParserクラスのテスト"""

    def test_parse_file_with_function(self, temp_project):
        """関数定義を含むPythonファイルの解析テスト"""
        python_file = temp_project / "test.py"
        python_file.write_text("""
def hello_world(name: str) -> str:
    '''Say hello to the world.

    Args:
        name: The name to greet

    Returns:
        A greeting message
    '''
    return f"Hello, {name}!"

def add_numbers(a: int, b: int) -> int:
    '''Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    '''
    return a + b
""")

        parser = PythonParser(temp_project)
        apis = parser.parse_file(python_file)

        assert len(apis) == 2

        # hello_world関数のチェック
        hello_api = next(api for api in apis if api.get("name") == "hello_world")
        assert hello_api["type"] == "function"
        assert hello_api["signature"] == "def hello_world(name: str) -> str:"
        assert "Say hello to the world" in hello_api["docstring"]
        assert hello_api["parameters"] == ["name: str"]
        assert hello_api["return_type"] == "str"

        # add_numbers関数のチェック
        add_api = next(api for api in apis if api.get("name") == "add_numbers")
        assert add_api["type"] == "function"
        assert add_api["signature"] == "def add_numbers(a: int, b: int) -> int:"
        assert "Add two numbers" in add_api["docstring"]
        assert add_api["parameters"] == ["a: int", "b: int"]
        assert add_api["return_type"] == "int"

    def test_parse_file_with_class(self, temp_project):
        """クラス定義を含むPythonファイルの解析テスト"""
        python_file = temp_project / "test.py"
        python_file.write_text("""
class Calculator:
    '''A simple calculator class.'''

    def __init__(self, initial_value: int = 0):
        '''Initialize calculator.

        Args:
            initial_value: Starting value
        '''
        self.value = initial_value

    def add(self, x: int) -> int:
        '''Add x to current value.

        Args:
            x: Value to add

        Returns:
            New value
        '''
        self.value += x
        return self.value
""")

        parser = PythonParser(temp_project)
        apis = parser.parse_file(python_file)

        # クラスとメソッドが含まれるはず
        class_api = next(api for api in apis if api.get("type") == "class")
        assert class_api["name"] == "Calculator"
        assert "A simple calculator class" in class_api["docstring"]

        # メソッドのチェック
        methods = [api for api in apis if api.get("type") == "method"]
        assert len(methods) >= 2  # __init__ と add

        init_method = next(m for m in methods if m.get("name") == "__init__")
        assert "Initialize calculator" in init_method["docstring"]

        add_method = next(m for m in methods if m.get("name") == "add")
        assert "Add x to current value" in add_method["docstring"]

    def test_parse_file_no_docstring(self, temp_project):
        """docstringのない関数の解析テスト"""
        python_file = temp_project / "test.py"
        python_file.write_text("""
def simple_function(x, y):
    return x + y

class SimpleClass:
    pass
""")

        parser = PythonParser(temp_project)
        apis = parser.parse_file(python_file)

        # docstringがない場合でも基本情報は取得される
        func_api = next(api for api in apis if api.get("name") == "simple_function")
        assert func_api["type"] == "function"
        assert func_api["docstring"] == ""

        class_api = next(api for api in apis if api.get("name") == "SimpleClass")
        assert class_api["type"] == "class"
        assert class_api["docstring"] == ""

    def test_parse_file_syntax_error(self, temp_project):
        """構文エラーのあるファイルの解析テスト"""
        python_file = temp_project / "test.py"
        python_file.write_text("""
def broken_function(
    return "broken"  # 構文エラー
""")

        parser = PythonParser(temp_project)
        apis = parser.parse_file(python_file)

        # 構文エラーの場合は空のリストが返される
        assert apis == []

    def test_parse_file_empty(self, temp_project):
        """空のファイルの解析テスト"""
        python_file = temp_project / "test.py"
        python_file.write_text("")

        parser = PythonParser(temp_project)
        apis = parser.parse_file(python_file)

        assert apis == []

    def test_parse_file_with_async_function(self, temp_project):
        """async関数の解析テスト"""
        python_file = temp_project / "test.py"
        python_file.write_text("""
async def async_function(delay: float) -> None:
    '''Async function that waits.

    Args:
        delay: Time to wait in seconds
    '''
    import asyncio
    await asyncio.sleep(delay)
""")

        parser = PythonParser(temp_project)
        apis = parser.parse_file(python_file)

        async_api = next(api for api in apis if api.get("name") == "async_function")
        assert async_api["type"] == "function"
        assert "async def async_function(delay: float) -> None:" in async_api["signature"]
        assert "Async function that waits" in async_api["docstring"]

    def test_parse_file_with_complex_types(self, temp_project):
        """複雑な型ヒントを含む関数の解析テスト"""
        python_file = temp_project / "test.py"
        python_file.write_text("""
from typing import List, Dict, Optional

def complex_function(
    items: List[str],
    mapping: Dict[str, int],
    optional_param: Optional[str] = None
) -> Dict[str, List[int]]:
    '''Function with complex type hints.

    Args:
        items: List of strings
        mapping: Dictionary mapping strings to ints
        optional_param: Optional string parameter

    Returns:
        Complex return type
    '''
    return {}
""")

        parser = PythonParser(temp_project)
        apis = parser.parse_file(python_file)

        complex_api = next(api for api in apis if api.get("name") == "complex_function")
        assert complex_api["type"] == "function"
        assert "items: List[str]" in complex_api["parameters"]
        assert "mapping: Dict[str, int]" in complex_api["parameters"]
        assert complex_api["return_type"] == "Dict[str, List[int]]"
