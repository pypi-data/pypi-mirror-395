"""
CacheManagerのテスト
"""

import json
from pathlib import Path

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.utils.cache import CacheManager


class TestCacheManager:
    """CacheManagerクラスのテスト"""

    def test_cache_manager_initialization_enabled(self, temp_project):
        """キャッシュ有効時の初期化テスト"""
        cache_manager = CacheManager(temp_project, enabled=True)

        assert cache_manager.project_root == temp_project.resolve()
        assert cache_manager.enabled is True
        assert cache_manager.cache_dir == temp_project / "docgen" / ".cache"
        assert cache_manager.cache_file == cache_manager.cache_dir / "parser_cache.json"
        assert cache_manager._cache_data is not None

        # キャッシュディレクトリが作成されているはず
        assert cache_manager.cache_dir.exists()

    def test_cache_manager_initialization_disabled(self, temp_project):
        """キャッシュ無効時の初期化テスト"""
        cache_manager = CacheManager(temp_project, enabled=False)

        assert cache_manager.enabled is False
        assert cache_manager._cache_data is None

    def test_cache_manager_custom_cache_dir(self, temp_project):
        """カスタムキャッシュディレクトリのテスト"""
        custom_cache_dir = temp_project / "custom_cache"
        cache_manager = CacheManager(temp_project, cache_dir=custom_cache_dir, enabled=True)

        assert cache_manager.cache_dir == custom_cache_dir
        assert cache_manager.cache_file == custom_cache_dir / "parser_cache.json"
        assert custom_cache_dir.exists()

    def test_load_cache_existing_file(self, temp_project):
        """既存のキャッシュファイル読み込みテスト"""
        cache_dir = temp_project / "docgen" / ".cache"
        cache_dir.mkdir(parents=True)
        cache_file = cache_dir / "parser_cache.json"

        test_data = {
            "file_hash_1": {"apis": [{"name": "func1"}], "timestamp": "2023-01-01T00:00:00"},
            "file_hash_2": {"apis": [{"name": "func2"}], "timestamp": "2023-01-02T00:00:00"},
        }

        cache_file.write_text(json.dumps(test_data))

        cache_manager = CacheManager(temp_project, enabled=True)

        assert cache_manager._cache_data == test_data

    def test_load_cache_invalid_json(self, temp_project):
        """無効なJSONのキャッシュファイル読み込みテスト"""
        cache_dir = temp_project / "docgen" / ".cache"
        cache_dir.mkdir(parents=True)
        cache_file = cache_dir / "parser_cache.json"

        # 無効なJSON
        cache_file.write_text("invalid json content")

        cache_manager = CacheManager(temp_project, enabled=True)

        # 無効なJSONの場合は空のキャッシュが作成される
        assert cache_manager._cache_data == {}

    def test_load_cache_nonexistent_file(self, temp_project):
        """存在しないキャッシュファイルのテスト"""
        cache_manager = CacheManager(temp_project, enabled=True)

        # ファイルが存在しない場合は空のキャッシュが作成される
        assert cache_manager._cache_data == {}

    def test_save_cache(self, temp_project):
        """キャッシュ保存テスト"""
        cache_manager = CacheManager(temp_project, enabled=True)

        test_data = {
            "file_hash_1": {"apis": [{"name": "func1"}], "timestamp": "2023-01-01T00:00:00"}
        }
        cache_manager._cache_data = test_data

        cache_manager._save_cache()

        # ファイルが保存されているはず
        assert cache_manager.cache_file.exists()

        # 内容が正しいか確認
        saved_data = json.loads(cache_manager.cache_file.read_text())
        assert saved_data == test_data

    def test_save_cache_disabled(self, temp_project):
        """キャッシュ無効時の保存テスト"""
        cache_manager = CacheManager(temp_project, enabled=False)

        # 無効時は保存されない
        cache_manager._save_cache()

        # ファイルが存在しないはず
        assert not cache_manager.cache_file.exists()

    def test_get_file_hash(self, temp_project):
        """ファイルハッシュの生成テスト"""
        cache_manager = CacheManager(temp_project, enabled=True)

        file_path = temp_project / "src" / "main.py"
        file_path.parent.mkdir(parents=True)
        file_path.write_text("print('hello')")

        hash_value = cache_manager.get_file_hash(file_path)

        # ファイルの内容に基づくハッシュが生成されるはず
        assert isinstance(hash_value, str)
        assert len(hash_value) > 0

        # 同じ内容の場合は同じハッシュが生成される
        hash_value2 = cache_manager.get_file_hash(file_path)
        assert hash_value == hash_value2

    def test_get_file_hash_nonexistent_file(self, temp_project):
        """存在しないファイルのハッシュ生成テスト"""
        cache_manager = CacheManager(temp_project, enabled=True)

        nonexistent_file = temp_project / "nonexistent.py"

        hash_value = cache_manager.get_file_hash(nonexistent_file)
        assert hash_value == ""

    def test_get_cached_result(self, temp_project):
        """キャッシュ結果取得テスト"""
        cache_manager = CacheManager(temp_project, enabled=True)

        file_path = temp_project / "src" / "main.py"
        file_path.parent.mkdir(parents=True)
        file_path.write_text("print('hello')")

        # キャッシュが存在しない場合
        result = cache_manager.get_cached_result(file_path, "python")
        assert result is None

    def test_get_cached_result_disabled(self, temp_project):
        """キャッシュ無効時の結果取得テスト"""
        cache_manager = CacheManager(temp_project, enabled=False)

        file_path = temp_project / "src" / "main.py"
        file_path.parent.mkdir(parents=True)
        file_path.write_text("print('hello')")

        # 無効時は常にNoneが返される
        result = cache_manager.get_cached_result(file_path, "python")
        assert result is None

    def test_set_cached_result(self, temp_project):
        """キャッシュ結果設定テスト"""
        cache_manager = CacheManager(temp_project, enabled=True)

        file_path = temp_project / "src" / "main.py"
        file_path.parent.mkdir(parents=True)
        file_path.write_text("print('hello')")

        apis = [{"name": "func1"}, {"name": "func2"}]

        cache_manager.set_cached_result(file_path, "python", apis)

        # キャッシュが設定されているはず
        cache_key = cache_manager.get_cache_key(file_path, "python")
        if cache_manager._cache_data is not None:
            assert cache_key in cache_manager._cache_data
            assert cache_manager._cache_data[cache_key]["result"] == apis

    def test_set_cached_result_disabled(self, temp_project):
        """キャッシュ無効時の結果設定テスト"""
        cache_manager = CacheManager(temp_project, enabled=False)

        file_path = temp_project / "src" / "main.py"
        file_path.parent.mkdir(parents=True)
        file_path.write_text("print('hello')")

        apis = [{"name": "func1"}]

        # 無効時は何も起こらない
        cache_manager.set_cached_result(file_path, "python", apis)

        # キャッシュデータはNoneのまま
        assert cache_manager._cache_data is None

    def test_clear_cache(self, temp_project):
        """キャッシュクリアテスト"""
        cache_manager = CacheManager(temp_project, enabled=True)

        # キャッシュデータを設定
        cache_manager._cache_data = {"key1": "value1", "key2": "value2"}

        cache_manager.clear_cache()

        # キャッシュが空になる
        assert cache_manager._cache_data == {}

        # ファイルは空の状態で保存されているはず
        assert cache_manager.cache_file.exists()

    def test_clear_cache_disabled(self, temp_project):
        """キャッシュ無効時のクリアテスト"""
        cache_manager = CacheManager(temp_project, enabled=False)

        # 無効時は何も起こらない
        cache_manager.clear_cache()

        # エラーが発生しない
        assert cache_manager._cache_data is None
