"""
言語検出モジュール
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .detectors.plugin_registry import PluginRegistry
from .utils.logger import get_logger

logger = get_logger("language_detector")


class LanguageDetector:
    """言語検出クラス"""

    def __init__(self, project_root: Path, config_manager=None):
        """
        初期化

        Args:
            project_root: プロジェクトルートパス
            config_manager: 設定マネージャー（Noneの場合は新規作成）
        """
        self.project_root = project_root
        self.detected_languages = []
        self.detected_package_managers = {}

        # 設定マネージャーの初期化
        if config_manager:
            self.config_manager = config_manager
        else:
            from .config_manager import ConfigManager

            # docgenディレクトリはプロジェクトルート内のdocgenディレクトリと仮定
            docgen_dir = project_root / "docgen"
            self.config_manager = ConfigManager(project_root, docgen_dir)

        self.plugin_registry = PluginRegistry()

        # 設定の読み込み
        self.configs = self.config_manager.load_detector_defaults()
        user_configs = self.config_manager.load_detector_user_overrides()
        self.configs = self.config_manager.merge_detector_configs(self.configs, user_configs)

        # プラグインの発見
        self.plugin_registry.discover_plugins(project_root)

        logger.debug(
            f"Config system enabled: {len(self.configs)} configs, "
            f"{len(self.plugin_registry.get_all_languages())} plugins"
        )

    def detect_languages(self, use_parallel: bool = True) -> list[str]:
        """
        プロジェクトの使用言語を自動検出

        Args:
            use_parallel: 並列処理を使用するかどうか（デフォルト: True）

        Returns:
            検出された言語のリスト
        """
        from .detectors.unified_detector import UnifiedDetectorFactory

        # 統一 detector を使用
        detectors = UnifiedDetectorFactory.create_all_detectors(self.project_root)

        # プラグインdetectorを追加（優先度が高い）
        for lang in self.plugin_registry.get_all_languages():
            plugin_detector = self.plugin_registry.get_detector(lang, self.project_root)
            if plugin_detector:
                detectors.insert(0, plugin_detector)

        detected = []
        package_managers = {}

        if use_parallel:
            # 並列処理で検出
            with ThreadPoolExecutor(max_workers=len(detectors)) as executor:
                future_to_detector = {
                    executor.submit(detector.detect): detector for detector in detectors
                }

                for future in as_completed(future_to_detector):
                    detector = future_to_detector[future]
                    try:
                        if future.result():
                            lang = detector.get_language()
                            if lang not in detected:
                                detected.append(lang)
                                logger.info(f"✓ 検出: {lang}")

                                # パッケージマネージャも同時に取得
                                pm = detector.detect_package_manager()
                                if pm:
                                    package_managers[lang] = pm
                                    logger.info(f"✓ パッケージマネージャ検出: {lang} -> {pm}")
                    except Exception as e:
                        logger.warning(
                            f"言語検出中にエラーが発生しました ({detector.__class__.__name__}): {e}"
                        )
        else:
            # 逐次処理で検出
            for detector in detectors:
                try:
                    if detector.detect():
                        lang = detector.get_language()
                        if lang not in detected:
                            detected.append(lang)
                            logger.info(f"✓ 検出: {lang}")

                            # パッケージマネージャも同時に取得
                            pm = detector.detect_package_manager()
                            if pm:
                                package_managers[lang] = pm
                                logger.info(f"✓ パッケージマネージャ検出: {lang} -> {pm}")
                except Exception as e:
                    logger.warning(
                        f"言語検出中にエラーが発生しました ({detector.__class__.__name__}): {e}"
                    )

        self.detected_languages = detected
        self.detected_package_managers = package_managers
        return detected

    def get_detected_languages(self) -> list[str]:
        """検出された言語を取得"""
        return self.detected_languages

    def get_detected_package_managers(self) -> dict[str, str]:
        """検出されたパッケージマネージャを取得"""
        return self.detected_package_managers
