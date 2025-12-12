"""
FileUtilsのテスト
"""

import json
from pathlib import Path
from unittest.mock import patch

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.utils.file_utils import (
    find_files_with_extensions,
    safe_read_file,
    safe_read_json,
    safe_read_toml,
    safe_read_yaml,
    safe_write_file,
    save_yaml_file,
)


class TestFileUtils:
    """FileUtils関数のテスト"""

    def test_safe_read_file_existing(self, temp_project):
        """存在するファイルの安全読み込みテスト"""
        test_file = temp_project / "test.txt"
        test_content = "Hello, World!"
        test_file.write_text(test_content)

        result = safe_read_file(test_file)
        assert result == test_content

    def test_safe_read_file_nonexistent(self, temp_project):
        """存在しないファイルの安全読み込みテスト"""
        nonexistent_file = temp_project / "nonexistent.txt"

        result = safe_read_file(nonexistent_file)
        assert result is None

    def test_safe_read_file_encoding_error(self, temp_project):
        """エンコーディングエラーのファイル読み込みテスト"""
        test_file = temp_project / "binary.dat"
        # バイナリデータを書き込む
        test_file.write_bytes(b"\x80\x81\x82")

        result = safe_read_file(test_file, encoding="utf-8")
        assert result is None

    def test_safe_read_file_permission_error(self, temp_project):
        """権限エラーのファイル読み込みテスト"""
        test_file = temp_project / "test.txt"
        test_file.write_text("content")

        with patch.object(Path, "read_text", side_effect=PermissionError):
            result = safe_read_file(test_file)
            assert result is None

    def test_safe_write_file_success(self, temp_project):
        """ファイルの安全書き込み成功テスト"""
        test_file = temp_project / "output.txt"
        content = "Test content"

        result = safe_write_file(test_file, content)
        assert result is True
        assert test_file.exists()
        assert test_file.read_text() == content

    def test_safe_write_file_permission_error(self, temp_project):
        """権限エラーのファイル書き込みテスト"""
        test_file = temp_project / "output.txt"
        content = "Test content"

        with patch.object(Path, "write_text", side_effect=PermissionError):
            result = safe_write_file(test_file, content)
            assert result is False

    def test_safe_read_json_valid(self, temp_project):
        """有効なJSONファイルの読み込みテスト"""
        test_file = temp_project / "data.json"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(json.dumps(test_data))

        result = safe_read_json(test_file)
        assert result == test_data

    def test_safe_read_json_invalid(self, temp_project):
        """無効なJSONファイルの読み込みテスト"""
        test_file = temp_project / "invalid.json"
        test_file.write_text("invalid json content")

        result = safe_read_json(test_file)
        assert result is None

    def test_safe_read_json_nonexistent(self, temp_project):
        """存在しないJSONファイルの読み込みテスト"""
        nonexistent_file = temp_project / "missing.json"

        result = safe_read_json(nonexistent_file)
        assert result is None

    def test_safe_read_yaml_valid(self, temp_project):
        """有効なYAMLファイルの読み込みテスト"""
        test_file = temp_project / "data.yaml"
        yaml_content = """
key: value
number: 42
list:
  - item1
  - item2
"""
        test_file.write_text(yaml_content)

        result = safe_read_yaml(test_file)
        expected = {"key": "value", "number": 42, "list": ["item1", "item2"]}
        assert result == expected

    def test_safe_read_yaml_no_yaml(self):
        """YAMLライブラリなしの場合のテスト"""
        # yamlがNoneの場合をモック
        with patch("docgen.utils.file_utils.yaml", None):
            result = safe_read_yaml(Path("dummy.yaml"))
            assert result is None

    def test_safe_read_toml_valid(self, temp_project):
        """有効なTOMLファイルの読み込みテスト"""
        test_file = temp_project / "data.toml"
        toml_content = """
[section]
key = "value"
number = 42
"""
        test_file.write_text(toml_content)

        result = safe_read_toml(test_file)
        assert isinstance(result, dict)

    def test_safe_read_toml_no_tomllib(self):
        """TOMLライブラリなしの場合のテスト"""
        with patch("docgen.utils.file_utils.tomllib", None):
            result = safe_read_toml(Path("dummy.toml"))
            assert result is None

    def test_save_yaml_file_success(self, temp_project):
        """YAMLファイルの保存成功テスト"""
        test_file = temp_project / "output.yaml"
        test_data = {"key": "value", "number": 42}

        result = save_yaml_file(test_file, test_data)
        assert result is True
        assert test_file.exists()

    def test_save_yaml_file_no_yaml(self):
        """YAMLライブラリなしの場合の保存テスト"""
        with patch("docgen.utils.file_utils.yaml", None):
            result = save_yaml_file(Path("dummy.yaml"), {})
            assert result is False

    def test_find_files_with_extensions(self, temp_project):
        """拡張子によるファイル検索テスト"""
        # テストファイルを作成
        (temp_project / "file1.py").write_text("python code")
        (temp_project / "file2.py").write_text("more python code")
        (temp_project / "file3.js").write_text("javascript code")
        (temp_project / "readme.txt").write_text("text file")

        # .pyファイルのみ検索
        py_files = find_files_with_extensions(temp_project, [".py"])
        # temp_project直下の.pyファイルのみを対象
        py_files = [f for f in py_files if f.parent == temp_project]
        assert len(py_files) == 2
        assert all(f.suffix == ".py" for f in py_files)

        # .jsファイル検索
        js_files = find_files_with_extensions(temp_project, [".js"])
        js_files = [f for f in js_files if f.parent == temp_project]
        assert len(js_files) == 1
        assert js_files[0].suffix == ".js"

    def test_find_files_with_extensions_recursive(self, temp_project):
        """再帰的なファイル検索テスト"""
        # サブディレクトリを作成
        subdir = temp_project / "src"
        subdir.mkdir()

        (temp_project / "main.py").write_text("main code")
        (subdir / "module.py").write_text("module code")
        (subdir / "util.js").write_text("util code")

        # 再帰検索
        py_files = find_files_with_extensions(temp_project, [".py"])
        # temp_project内のファイルのみを対象（docgenディレクトリは除外）
        py_files = [
            f for f in py_files if f.is_relative_to(temp_project) and "docgen" not in f.parts
        ]
        assert len(py_files) == 2
