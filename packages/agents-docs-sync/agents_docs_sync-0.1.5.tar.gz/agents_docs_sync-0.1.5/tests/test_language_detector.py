"""
言語検出モジュールのテスト
"""

from docgen.language_detector import LanguageDetector


class TestLanguageDetector:
    """LanguageDetectorクラスのテスト"""

    def test_init(self, tmp_path):
        """初期化テスト"""
        detector = LanguageDetector(tmp_path)
        assert detector.project_root == tmp_path
        assert detector.detected_languages == []
        assert detector.detected_package_managers == {}

    def test_detect_languages_python(self, tmp_path):
        """Python言語検出テスト"""
        # Pythonファイルを作成
        (tmp_path / "main.py").write_text("print('hello')")

        detector = LanguageDetector(tmp_path)
        languages = detector.detect_languages(use_parallel=False)

        assert "python" in languages
        assert detector.get_detected_languages() == languages

    def test_get_detected_package_managers(self, tmp_path):
        """パッケージマネージャ取得テスト"""
        detector = LanguageDetector(tmp_path)
        assert detector.get_detected_package_managers() == {}
