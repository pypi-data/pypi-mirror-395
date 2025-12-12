"""
GenericParserのテスト
"""

from pathlib import Path

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.generators.parsers.generic_parser import GenericParser


class TestGenericParser:
    """GenericParserクラスのテスト"""

    def test_parse_file_rust(self, temp_project):
        """Rustファイルの解析テスト"""
        rs_file = temp_project / "lib.rs"
        rs_file.write_text("""//! This is a Rust library

/// Add two numbers
/// # Arguments
/// * `a` - First number
/// * `b` - Second number
/// # Returns
/// The sum of a and b
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// A simple struct
pub struct Point {
    pub x: f64,
    pub y: f64,
}
""")

        parser = GenericParser(temp_project, "rust")
        apis = parser.parse_file(rs_file)

        assert len(apis) >= 1

        add_api = next((api for api in apis if api.get("name") == "add"), None)
        if add_api:
            assert add_api["type"] == "function"
            assert "Add two numbers" in add_api["docstring"]

    def test_parse_file_java(self, temp_project):
        """Javaファイルの解析テスト"""
        java_file = temp_project / "Main.java"
        java_file.write_text("""
/**
 * Main class for the application
 */
public class Main {
    /**
     * Main method
     * @param args command line arguments
     */
    public static void main(String[] args) {
        System.out.println("Hello World");
    }

    /**
     * Calculate sum
     * @param a first number
     * @param b second number
     * @return sum of a and b
     */
    public int add(int a, int b) {
        return a + b;
    }
}
""")

        parser = GenericParser(temp_project, "java")
        apis = parser.parse_file(java_file)

        assert len(apis) >= 1

        main_api = next((api for api in apis if api.get("name") == "main"), None)
        if main_api:
            assert main_api["type"] == "function"
            assert "Main class for the application" in main_api["docstring"]

    def test_parse_file_go(self, temp_project):
        """Goファイルの解析テスト"""
        go_file = temp_project / "main.go"
        go_file.write_text("""package main

// Add adds two numbers
// Parameters:
//   a: first number
//   b: second number
// Returns: sum of a and b
func Add(a, b int) int {
    return a + b
}

// Person represents a person
type Person struct {
    Name string
    Age  int
}
""")

        parser = GenericParser(temp_project, "go")
        apis = parser.parse_file(go_file)

        assert len(apis) >= 1

        add_api = next((api for api in apis if api.get("name") == "Add"), None)
        if add_api:
            assert add_api["type"] == "function"
            assert "Add adds two numbers" in add_api["docstring"]

    def test_parse_file_ruby(self, temp_project):
        """Rubyファイルの解析テスト"""
        rb_file = temp_project / "main.rb"
        rb_file.write_text("""# Main module

# Calculate sum of two numbers
# @param a [Integer] first number
# @param b [Integer] second number
# @return [Integer] sum of a and b
def add(a, b)
  a + b
end

# Person class
class Person
  attr_accessor :name, :age
end
""")

        parser = GenericParser(temp_project, "ruby")
        apis = parser.parse_file(rb_file)

        assert len(apis) >= 1

        add_api = next((api for api in apis if api.get("name") == "add"), None)
        if add_api:
            assert add_api["type"] == "function"
            assert "Calculate sum of two numbers" in add_api["docstring"]

    def test_parse_file_php(self, temp_project):
        """PHPファイルの解析テスト"""
        php_file = temp_project / "functions.php"
        php_file.write_text("""<?php
/**
 * Add two numbers
 * @param int $a First number
 * @param int $b Second number
 * @return int Sum of a and b
 */
function add($a, $b) {
    return $a + $b;
}

/**
 * User class
 */
class User {
    /**
     * Get user name
     * @return string User name
     */
    public function getName() {
        return $this->name;
    }
}
""")

        parser = GenericParser(temp_project, "php")
        apis = parser.parse_file(php_file)

        assert len(apis) >= 1

        add_api = next((api for api in apis if api.get("name") == "add"), None)
        if add_api:
            assert add_api["type"] == "function"
            assert "Add two numbers" in add_api["docstring"]

    def test_parse_file_c(self, temp_project):
        """Cファイルの解析テスト"""
        c_file = temp_project / "main.c"
        c_file.write_text("""
/**
 * Add two integers
 * @param a first integer
 * @param b second integer
 * @return sum of a and b
 */
int add(int a, int b) {
    return a + b;
}

/**
 * Point structure
 */
struct Point {
    int x;
    int y;
};
""")

        parser = GenericParser(temp_project, "c")
        apis = parser.parse_file(c_file)

        assert len(apis) >= 1

        add_api = next((api for api in apis if api.get("name") == "add"), None)
        if add_api:
            assert add_api["type"] == "function"
            assert "Add two integers" in add_api["docstring"]

    def test_parse_file_cpp(self, temp_project):
        """C++ファイルの解析テスト"""
        cpp_file = temp_project / "main.cpp"
        cpp_file.write_text("""
/**
 * Calculator class
 */
class Calculator {
public:
    /**
     * Add two numbers
     * @param a first number
     * @param b second number
     * @return sum of a and b
     */
    int add(int a, int b) {
        return a + b;
    }
};
""")

        parser = GenericParser(temp_project, "cpp")
        apis = parser.parse_file(cpp_file)

        assert len(apis) >= 1

        add_api = next((api for api in apis if api.get("name") == "add"), None)
        if add_api:
            assert add_api["type"] == "function"
            assert "Calculator class" in add_api["docstring"]

    def test_parse_file_unsupported_language(self, temp_project):
        """サポートされていない言語のテスト"""
        unknown_file = temp_project / "unknown.xyz"
        unknown_file.write_text("""
# Some unknown language
def func():
    pass
""")

        parser = GenericParser(temp_project, "unknown")
        apis = parser.parse_file(unknown_file)

        # サポートされていない言語の場合は空のリストが返される
        assert apis == []

    def test_parse_file_empty(self, temp_project):
        """空のファイルの解析テスト"""
        empty_file = temp_project / "empty.rs"
        empty_file.write_text("")

        parser = GenericParser(temp_project, "rust")
        apis = parser.parse_file(empty_file)

        assert apis == []

    def test_parse_file_no_comments(self, temp_project):
        """コメントなしのファイルの解析テスト"""
        no_comment_file = temp_project / "no_comment.java"
        no_comment_file.write_text("""
public class Test {
    public void method() {
        // do something
    }
}
""")

        parser = GenericParser(temp_project, "java")
        apis = parser.parse_file(no_comment_file)

        # コメントがない場合は基本情報のみ取得されるはず
        assert len(apis) >= 1

    def test_parser_initialization(self, temp_project):
        """パーサーの初期化テスト"""
        parser = GenericParser(temp_project, "rust")
        assert parser.project_root == temp_project
        assert parser.language == "rust"

        # デフォルト言語
        parser_default = GenericParser(temp_project)
        assert parser_default.language == "generic"
