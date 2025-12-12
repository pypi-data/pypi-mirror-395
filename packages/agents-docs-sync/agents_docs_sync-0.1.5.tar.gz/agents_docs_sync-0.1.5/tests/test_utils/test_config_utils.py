"""
ConfigUtilsのテスト
"""

# docgenモジュールをインポート可能にする
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.utils.config_utils import (
    get_config_bool,
    get_config_list,
    get_config_str,
    get_nested_config,
)


class TestConfigUtils:
    """ConfigUtils関数のテスト"""

    def test_get_nested_config_simple(self):
        """単純なネストされた設定取得テスト"""
        config = {"a": {"b": "value"}}

        result = get_nested_config(config, "a", "b")
        assert result == "value"

    def test_get_nested_config_deep(self):
        """深いネストされた設定取得テスト"""
        config = {"a": {"b": {"c": {"d": "deep_value"}}}}

        result = get_nested_config(config, "a", "b", "c", "d")
        assert result == "deep_value"

    def test_get_nested_config_default(self):
        """存在しないキーのデフォルト値テスト"""
        config = {"a": {"b": "value"}}

        result = get_nested_config(config, "a", "x", default="default")
        assert result == "default"

    def test_get_nested_config_none_default(self):
        """デフォルト値なしの存在しないキーテスト"""
        config = {"a": {"b": "value"}}

        result = get_nested_config(config, "a", "x")
        assert result is None

    def test_get_nested_config_non_dict(self):
        """非辞書値の中間でのテスト"""
        config = {"a": {"b": "not_dict"}}

        result = get_nested_config(config, "a", "b", "c", default="default")
        assert result == "default"

    def test_get_nested_config_empty_keys(self):
        """空のキーシーケンステスト"""
        config = {"a": "value"}

        result = get_nested_config(config)
        assert result == config

    def test_get_config_bool_true(self):
        """ブール値Trueの取得テスト"""
        config = {"flag": True}

        result = get_config_bool(config, "flag")
        assert result is True

    def test_get_config_bool_false(self):
        """ブール値Falseの取得テスト"""
        config = {"flag": False}

        result = get_config_bool(config, "flag")
        assert result is False

    def test_get_config_bool_string_true(self):
        """文字列"true"のブール変換テスト"""
        config = {"flag": "true"}

        result = get_config_bool(config, "flag")
        assert result is True

    def test_get_config_bool_string_false(self):
        """文字列"false"のブール変換テスト"""
        config = {"flag": "false"}

        result = get_config_bool(config, "flag")
        assert result is False

    def test_get_config_bool_string_yes(self):
        """文字列"yes"のブール変換テスト"""
        config = {"flag": "yes"}

        result = get_config_bool(config, "flag")
        assert result is True

    def test_get_config_bool_string_no(self):
        """文字列"no"のブール変換テスト"""
        config = {"flag": "no"}

        result = get_config_bool(config, "flag")
        assert result is False

    def test_get_config_bool_string_one(self):
        """文字列"1"のブール変換テスト"""
        config = {"flag": "1"}

        result = get_config_bool(config, "flag")
        assert result is True

    def test_get_config_bool_string_zero(self):
        """文字列"0"のブール変換テスト"""
        config = {"flag": "0"}

        result = get_config_bool(config, "flag")
        assert result is False

    def test_get_config_bool_invalid_string(self):
        """無効な文字列のブール変換テスト"""
        config = {"flag": "invalid"}

        result = get_config_bool(config, "flag")
        assert result is False  # デフォルト値

    def test_get_config_bool_default(self):
        """デフォルト値付きブール取得テスト"""
        config = {"other": "value"}

        result = get_config_bool(config, "missing", default=True)
        assert result is True

    def test_get_config_list_valid(self):
        """有効なリストの取得テスト"""
        config = {"items": ["a", "b", "c"]}

        result = get_config_list(config, "items")
        assert result == ["a", "b", "c"]

    def test_get_config_list_string(self):
        """文字列からのリスト変換テスト（カンマ区切り）"""
        config = {"items": "a,b,c"}

        result = get_config_list(config, "items")
        assert result == ["a", "b", "c"]

    def test_get_config_list_invalid(self):
        """無効な値のリスト変換テスト"""
        config = {"items": 123}

        result = get_config_list(config, "items", default=["default"])
        assert result == [123]

    def test_get_config_str_valid(self):
        """有効な文字列の取得テスト"""
        config = {"name": "test"}

        result = get_config_str(config, "name")
        assert result == "test"

    def test_get_config_str_non_string(self):
        """非文字列の文字列変換テスト"""
        config = {"number": 42}

        result = get_config_str(config, "number")
        assert result == "42"

    def test_get_config_str_none(self):
        """None値の文字列変換テスト"""
        config = {"value": None}

        result = get_config_str(config, "value", default="default")
        assert result == "default"
