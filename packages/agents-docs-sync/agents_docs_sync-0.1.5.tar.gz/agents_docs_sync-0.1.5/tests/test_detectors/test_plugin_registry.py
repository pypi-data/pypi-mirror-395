"""
PluginRegistryのテスト
"""

from pathlib import Path
import tempfile

from docgen.detectors.base_detector import BaseDetector
from docgen.detectors.plugin_registry import PluginRegistry


class TestPluginRegistry:
    """PluginRegistryクラスのテスト"""

    def test_discover_plugins_no_directory(self):
        """プラグインディレクトリが存在しない場合のテスト"""
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = PluginRegistry()
            registry.discover_plugins(Path(tmpdir))
            assert registry.get_all_languages() == []

    def test_discover_plugins_with_custom_detector(self):
        """カスタムdetectorの発見テスト"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            plugin_dir = tmppath / ".agent" / "detectors"
            plugin_dir.mkdir(parents=True)

            # カスタムdetectorを作成
            plugin_file = plugin_dir / "test_detector.py"
            plugin_file.write_text(
                """
from docgen.detectors.base_detector import BaseDetector

class TestDetector(BaseDetector):
    language = "test_lang"

    def detect(self):
        return True

    def get_language(self):
        return "test_lang"

    def detect_package_manager(self):
        return None
"""
            )

            registry = PluginRegistry()
            registry.discover_plugins(tmppath)

            assert "test_lang" in registry.get_all_languages()

    def test_discover_plugins_skips_private_files(self):
        """アンダースコアで始まるファイルをスキップするテスト"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            plugin_dir = tmppath / ".agent" / "detectors"
            plugin_dir.mkdir(parents=True)

            # プライベートファイルを作成
            plugin_file = plugin_dir / "_private_detector.py"
            plugin_file.write_text(
                """
from docgen.detectors.base_detector import BaseDetector

class PrivateDetector(BaseDetector):
    language = "private"

    def detect(self):
        return True

    def get_language(self):
        return "private"

    def detect_package_manager(self):
        return None
"""
            )

            registry = PluginRegistry()
            registry.discover_plugins(tmppath)

            assert "private" not in registry.get_all_languages()

    def test_get_detector(self):
        """Detectorインスタンスの取得テスト"""

        class MockDetector(BaseDetector):
            language = "mock"

            def detect(self):
                return True

            def get_language(self):
                return "mock"

            def detect_package_manager(self):
                return None

        registry = PluginRegistry()
        registry.register(MockDetector)

        with tempfile.TemporaryDirectory() as tmpdir:
            detector = registry.get_detector("mock", Path(tmpdir))
            assert detector is not None
            assert isinstance(detector, MockDetector)
            assert detector.get_language() == "mock"

    def test_get_detector_not_found(self):
        """存在しない言語のdetector取得テスト"""
        registry = PluginRegistry()

        with tempfile.TemporaryDirectory() as tmpdir:
            detector = registry.get_detector("nonexistent", Path(tmpdir))
            assert detector is None

    def test_register_without_language_attribute(self):
        """language属性のないdetectorの登録テスト"""

        class InvalidDetector(BaseDetector):
            def detect(self):
                return True

            def get_language(self):
                return "invalid"

            def detect_package_manager(self):
                return None

        registry = PluginRegistry()
        registry.register(InvalidDetector)

        # language属性がないため登録されない
        assert registry.get_all_languages() == []
