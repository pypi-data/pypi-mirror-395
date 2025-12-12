"""
ハイブリッド検出システムの統合テスト
"""

from pathlib import Path
import tempfile

from docgen.language_detector import LanguageDetector


class TestHybridDetection:
    """ハイブリッド検出システムの統合テスト"""

    def test_default_detection(self):
        """デフォルト設定での検出テスト"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Pythonプロジェクトを作成
            (tmppath / "requirements.txt").write_text("pytest>=7.0.0")
            (tmppath / "main.py").write_text("print('hello')")

            detector = LanguageDetector(tmppath)
            languages = detector.detect_languages(use_parallel=False)

            assert "python" in languages

    def test_user_config_override(self, tmp_path):
        """Test user config override detection"""
        # Create config.toml with custom language config
        user_config = tmp_path / "config.toml"
        user_config.write_text(
            """
[detectors.elixir]
extensions = [".ex", ".exs"]
"""
        )

        # Elixirファイルを作成
        (tmp_path / "mix.exs").write_text("# mix config")
        lib_dir = tmp_path / "lib"
        lib_dir.mkdir(parents=True, exist_ok=True)
        (lib_dir / "app.ex").write_text("defmodule App do\\nend")

        detector = LanguageDetector(tmp_path)

        # ユーザ設定が読み込まれていることを確認
        assert "elixir" in detector.configs

    def test_plugin_detection(self):
        """プラグインdetectorの検出テスト"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            plugin_dir = tmppath / ".agent" / "detectors"
            plugin_dir.mkdir(parents=True)

            # カスタムdetectorプラグインを作成
            plugin_file = plugin_dir / "custom_detector.py"
            plugin_file.write_text(
                """
from docgen.detectors.base_detector import BaseDetector

class CustomDetector(BaseDetector):
    language = "custom_lang"

    def detect(self):
        return self._file_exists("CUSTOM.txt")

    def get_language(self):
        return "custom_lang"

    def detect_package_manager(self):
        if self._file_exists("custom.lock"):
            return "custom-pm"
        return None
"""
            )

            # カスタムファイルを作成
            (tmppath / "CUSTOM.txt").write_text("custom file")
            (tmppath / "custom.lock").write_text("lock file")

            detector = LanguageDetector(tmppath)
            languages = detector.detect_languages(use_parallel=False)

            assert "custom_lang" in languages

            # パッケージマネージャも検出されるか
            pm = detector.get_detected_package_managers()
            assert pm.get("custom_lang") == "custom-pm"

    def test_mixed_detection(self):
        """組み込みdetectorとプラグインdetectorの混合検出テスト"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Pythonファイル（組み込みdetector）
            (tmppath / "script.py").write_text("print('python')")
            (tmppath / "requirements.txt").write_text("pytest")

            # JavaScriptファイル（組み込みdetector）
            (tmppath / "package.json").write_text('{"name": "test"}')
            (tmppath / "index.js").write_text("console.log('js')")

            # カスタムプラグイン
            plugin_dir = tmppath / ".agent" / "detectors"
            plugin_dir.mkdir(parents=True)
            plugin_file = plugin_dir / "test_detector.py"
            plugin_file.write_text(
                """
from docgen.detectors.base_detector import BaseDetector

class TestDetector(BaseDetector):
    language = "test_lang"

    def detect(self):
        return self._file_exists("TEST.md")

    def get_language(self):
        return "test_lang"

    def detect_package_manager(self):
        return None
"""
            )
            (tmppath / "TEST.md").write_text("test")

            detector = LanguageDetector(tmppath)
            languages = detector.detect_languages(use_parallel=False)

            # 全ての言語が検出される
            assert "python" in languages
            assert "javascript" in languages
            assert "test_lang" in languages
