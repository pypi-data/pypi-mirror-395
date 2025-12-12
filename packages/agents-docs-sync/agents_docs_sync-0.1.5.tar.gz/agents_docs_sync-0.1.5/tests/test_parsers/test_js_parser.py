"""
JSParserのテスト
"""

from pathlib import Path

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.generators.parsers.js_parser import JSParser


class TestJSParser:
    """JSParserクラスのテスト"""

    def test_parse_file_with_jsdoc_function(self, temp_project):
        """JSDoc付き関数の解析テスト"""
        js_file = temp_project / "test.js"
        js_file.write_text("""
/**
 * Say hello to the world
 * @param {string} name - The name to greet
 * @returns {string} A greeting message
 */
function helloWorld(name) {
    return `Hello, ${name}!`;
}

/**
 * Add two numbers
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} The sum of a and b
 */
function addNumbers(a, b) {
    return a + b;
}
""")

        parser = JSParser(temp_project)
        apis = parser.parse_file(js_file)

        assert len(apis) == 2

        # helloWorld関数のチェック
        hello_api = next(api for api in apis if api.get("name") == "helloWorld")
        assert hello_api["type"] == "function"
        assert "Say hello to the world" in hello_api["docstring"]
        assert hello_api["parameters"] == ["name"]

        # addNumbers関数のチェック
        add_api = next(api for api in apis if api.get("name") == "addNumbers")
        assert add_api["type"] == "function"
        assert "Add two numbers" in add_api["docstring"]
        assert add_api["parameters"] == ["a", "b"]

    def test_parse_file_with_class(self, temp_project):
        """クラスの解析テスト"""
        js_file = temp_project / "test.js"
        js_file.write_text("""
/**
 * Calculator class
 */
class Calculator {
    /**
     * Add two numbers
     * @param {number} a - First number
     * @param {number} b - Second number
     * @returns {number} The sum
     */
    add(a, b) {
        return a + b;
    }
}
""")

        parser = JSParser(temp_project)
        apis = parser.parse_file(js_file)

        # クラスとメソッドが含まれるはず
        class_api = next(api for api in apis if api.get("type") == "class")
        assert class_api["name"] == "Calculator"
        assert "Calculator class" in class_api["docstring"]

        method_api = next(api for api in apis if api.get("name") == "add")
        assert method_api["type"] == "method"
        assert "Add two numbers" in method_api["docstring"]

    def test_parse_file_with_arrow_function(self, temp_project):
        """アロー関数の解析テスト"""
        js_file = temp_project / "test.js"
        js_file.write_text("""
/**
 * Arrow function example
 * @param {string} text - Input text
 * @returns {string} Processed text
 */
const processText = (text) => {
    return text.toUpperCase();
};

/**
 * Async arrow function
 * @param {string} url - URL to fetch
 * @returns {Promise<Object>} Fetch result
 */
const fetchData = async (url) => {
    const response = await fetch(url);
    return response.json();
};
""")

        parser = JSParser(temp_project)
        apis = parser.parse_file(js_file)

        assert len(apis) >= 2

        process_api = next(api for api in apis if api.get("name") == "processText")
        assert process_api["type"] == "function"
        assert "Arrow function example" in process_api["docstring"]

        fetch_api = next(api for api in apis if api.get("name") == "fetchData")
        assert fetch_api["type"] == "function"
        assert "Async arrow function" in fetch_api["docstring"]

    def test_parse_file_with_export(self, temp_project):
        """export付き関数の解析テスト"""
        js_file = temp_project / "test.js"
        js_file.write_text("""
/**
 * Exported function
 * @param {number} x - Input value
 * @returns {number} Doubled value
 */
export function double(x) {
    return x * 2;
}

/**
 * Exported class
 */
export class MathUtils {
    /**
     * Square a number
     * @param {number} n - Number to square
     * @returns {number} Squared value
     */
    static square(n) {
        return n * n;
    }
}
""")

        parser = JSParser(temp_project)
        apis = parser.parse_file(js_file)

        assert len(apis) >= 2

        double_api = next(api for api in apis if api.get("name") == "double")
        assert double_api["type"] == "function"

        square_api = next(api for api in apis if api.get("name") == "square")
        assert square_api["type"] == "method"

    def test_parse_file_no_jsdoc(self, temp_project):
        """JSDocなしの関数の解析テスト"""
        js_file = temp_project / "test.js"
        js_file.write_text("""
function simpleFunction(x, y) {
    return x + y;
}

class SimpleClass {
    method() {
        return "hello";
    }
}
""")

        parser = JSParser(temp_project)
        apis = parser.parse_file(js_file)

        # JSDocがない場合は基本情報のみ取得
        func_api = next(api for api in apis if api.get("name") == "simpleFunction")
        assert func_api["type"] == "function"
        assert func_api["docstring"] == ""

        class_api = next(api for api in apis if api.get("name") == "SimpleClass")
        assert class_api["type"] == "class"
        assert class_api["docstring"] == ""

    def test_parse_file_typescript(self, temp_project):
        """TypeScriptファイルの解析テスト"""
        ts_file = temp_project / "test.ts"
        ts_file.write_text("""
/**
 * TypeScript function
 * @param name - The name to greet
 * @returns A greeting message
 */
function greet(name: string): string {
    return `Hello, ${name}!`;
}

/**
 * TypeScript interface
 */
interface User {
    name: string;
    age: number;
}
""")

        parser = JSParser(temp_project)
        apis = parser.parse_file(ts_file)

        greet_api = next(api for api in apis if api.get("name") == "greet")
        assert greet_api["type"] == "function"
        assert "TypeScript function" in greet_api["docstring"]

    def test_parse_file_empty(self, temp_project):
        """空のファイルの解析テスト"""
        js_file = temp_project / "empty.js"
        js_file.write_text("")

        parser = JSParser(temp_project)
        apis = parser.parse_file(js_file)

        assert apis == []

    def test_parse_file_complex_jsdoc(self, temp_project):
        """複雑なJSDocの解析テスト"""
        js_file = temp_project / "complex.js"
        js_file.write_text("""
/**
 * Complex function with multiple parameters
 * @param {string} name - User's name
 * @param {number} age - User's age
 * @param {Object} options - Additional options
 * @param {boolean} options.active - Whether user is active
 * @param {string[]} options.tags - User tags
 * @returns {Object} User object
 * @throws {Error} If name is empty
 */
function createUser(name, age, options = {}) {
    if (!name) {
        throw new Error("Name is required");
    }
    return { name, age, ...options };
}
""")

        parser = JSParser(temp_project)
        apis = parser.parse_file(js_file)

        create_api = next(api for api in apis if api.get("name") == "createUser")
        assert create_api["type"] == "function"
        assert "Complex function with multiple parameters" in create_api["docstring"]
        # パラメータ名の一部が含まれていればOK
        assert "name" in create_api["parameters"]
        assert "age" in create_api["parameters"]
        assert "options" in create_api["parameters"]

    def test_parse_file_mixed_content(self, temp_project):
        """JSDoc付きとJSDocなしが混在するファイルのテスト"""
        js_file = temp_project / "mixed.js"
        js_file.write_text("""
/**
 * Documented function
 * @param {string} input - Input string
 * @returns {string} Processed string
 */
function documented(input) {
    return input.toUpperCase();
}

function undocumented(output) {
    return output.toLowerCase();
}

/**
 * Another documented function
 */
function anotherDocumented() {
    return "hello";
}
""")

        parser = JSParser(temp_project)
        apis = parser.parse_file(js_file)

        # JSDoc付きの関数のみがAPIとして抽出されるはず
        documented_apis = [api for api in apis if api.get("docstring")]
        assert len(documented_apis) == 2

        names = [api["name"] for api in documented_apis]
        assert "documented" in names
        assert "anotherDocumented" in names
        assert "undocumented" not in names
