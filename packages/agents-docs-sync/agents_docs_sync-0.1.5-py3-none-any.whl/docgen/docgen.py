#!/usr/bin/env python3
"""
汎用ドキュメント自動生成システム
コミット時にAPIドキュメントとREADME.mdを自動更新します。
"""

from pathlib import Path
import sys
from typing import Any

# プロジェクトルートのパスを取得
DOCGEN_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = DOCGEN_DIR.parent

# sys.pathにプロジェクトルートを追加（パッケージとして実行する場合）
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# パッケージとしてインストールされた場合は相対インポートを使用
from .cli_handlers import BuildIndexHandler, HooksHandler, InitHandler
from .config_manager import ConfigManager
from .document_generator import DocumentGenerator
from .language_detector import LanguageDetector
from .utils.logger import get_logger

# ロガーの初期化
logger = get_logger("docgen")


class DocGen:
    """ドキュメント自動生成メインクラス"""

    def __init__(self, project_root: Path | None = None, config_path: Path | None = None):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ（Noneの場合は現在の作業ディレクトリ）
            config_path: 設定ファイルのパス（Noneの場合はデフォルト）
        """
        # プロジェクトルートの決定
        # パッケージとしてインストールされた場合、実行時のカレントディレクトリを使用
        if project_root is None:
            self.project_root = Path.cwd().resolve()
        else:
            if not project_root or str(project_root) == ".":
                raise ValueError("プロジェクトルートが無効です")
            resolved_root = Path(project_root).resolve()
            self.project_root = resolved_root

        # docgenディレクトリはプロジェクトルート内のdocgenディレクトリ
        self.docgen_dir = self.project_root / "docgen"

        # パッケージ内のconfig.toml.sampleを参照するためのパス
        package_config_sample = DOCGEN_DIR / "config.toml.sample"

        self.config_path = config_path or self.docgen_dir / "config.toml"

        self.config_manager = ConfigManager(
            self.project_root, self.docgen_dir, self.config_path, package_config_sample
        )
        self.config = self.config_manager.get_config()
        self.language_detector = LanguageDetector(self.project_root, self.config_manager)
        self.detected_languages = []
        self.detected_package_managers = {}

    def detect_languages(self, use_parallel: bool = True) -> list[str]:
        """
        プロジェクトの使用言語を自動検出

        Args:
            use_parallel: 並列処理を使用するかどうか（デフォルト: True）

        Returns:
            検出された言語のリスト
        """
        self.detected_languages = self.language_detector.detect_languages(use_parallel)
        self.detected_package_managers = self.language_detector.detected_package_managers
        return self.detected_languages

    def update_config(self, updates: dict[str, Any]) -> None:
        """
        設定を動的に更新

        Args:
            updates: 更新する設定辞書（ドット記法対応、例: {'generation.update_readme': False}）
        """
        self.config_manager.update_config(updates)
        self.config = self.config_manager.get_config()

    def generate_documents(self) -> bool:
        """
        ドキュメントを生成

        Returns:
            成功したかどうか
        """
        self.detect_languages()
        logger.info(f"Detected languages: {self.detected_languages}")

        if not self.detected_languages:
            logger.warning("サポートされている言語が検出されませんでした")
            return False

        document_generator = DocumentGenerator(
            self.project_root, self.detected_languages, self.config, self.detected_package_managers
        )
        return document_generator.generate_documents()


class CommandLineInterface:
    """コマンドラインインターフェースクラス"""

    def __init__(self):
        self.docgen = None
        self.init_handler = InitHandler()
        self.build_index_handler = BuildIndexHandler()
        self.hooks_handler = HooksHandler()

    def run(self) -> int:
        """メイン実行メソッド"""
        import argparse

        try:
            from . import __version__
        except (ImportError, ValueError, SystemError):
            __version__ = "0.0.1"

        parser = argparse.ArgumentParser(description="汎用ドキュメント自動生成システム")
        parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
        parser.add_argument("--config", type=Path, help="設定ファイルのパス")
        parser.add_argument("--detect-only", action="store_true", help="言語検出のみ実行")
        parser.add_argument("--no-api-doc", action="store_true", help="APIドキュメントを生成しない")
        parser.add_argument("--no-readme", action="store_true", help="READMEを更新しない")

        # RAG関連オプション
        parser.add_argument("--build-index", action="store_true", help="RAGインデックスをビルド")
        parser.add_argument("--use-rag", action="store_true", help="RAGを使用してドキュメント生成")

        # アーキテクチャ生成オプション
        parser.add_argument(
            "--generate-arch", action="store_true", help="アーキテクチャ図を生成（Mermaid形式）"
        )

        subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")

        # commit-msg サブコマンド
        subparsers.add_parser("commit-msg", help="コミットメッセージ生成")

        # hooks サブコマンド
        hooks_parser = subparsers.add_parser("hooks", help="Git hooksの管理")
        hooks_subparsers = hooks_parser.add_subparsers(dest="hooks_action", help="アクション")

        # hooks list
        hooks_subparsers.add_parser("list", help="利用可能なフックを表示")

        # hooks enable
        enable_parser = hooks_subparsers.add_parser("enable", help="フックを有効化")
        enable_parser.add_argument("hook_name", nargs="?", help="フック名（指定しない場合は全て）")

        # hooks disable
        disable_parser = hooks_subparsers.add_parser("disable", help="フックを無効化")
        disable_parser.add_argument("hook_name", nargs="?", help="フック名（指定しない場合は全て）")

        # hooks run
        run_parser = hooks_subparsers.add_parser("run", help="フックを手動実行")
        run_parser.add_argument("hook_name", help="実行するフック名")
        run_parser.add_argument("hook_args", nargs="*", help="フック引数")

        # hooks validate
        hooks_subparsers.add_parser("validate", help="フック設定を検証")

        # init サブコマンド
        init_parser = subparsers.add_parser(
            "init", help="プロジェクトの初期化（必須ファイルを作成）"
        )
        init_parser.add_argument("--force", action="store_true", help="既存ファイルを強制上書き")

        args = parser.parse_args()

        # 実行時のカレントディレクトリをプロジェクトルートとして使用
        project_root = Path.cwd().resolve()

        # init コマンド（DocGen初期化前に処理）
        if args.command == "init":
            return self.init_handler.handle(args.force, project_root)

        # build-index コマンド（DocGen初期化後に処理）
        if args.build_index:
            # 必須ファイルがない場合は自動初期化
            auto_init_result = self._check_and_auto_init(project_root)
            if auto_init_result != 0:
                return auto_init_result

            self.docgen = DocGen(project_root=project_root, config_path=args.config)
            return self.build_index_handler.handle(project_root, self.docgen.config)

        # DocGenの初期化（config.tomlが必要）
        # 必須ファイルがない場合は自動初期化
        if args.command not in ["init"]:
            auto_init_result = self._check_and_auto_init(project_root)
            if auto_init_result != 0:
                return auto_init_result

        self.docgen = DocGen(project_root=project_root, config_path=args.config)

        # コミットメッセージ生成コマンド
        if args.command == "commit-msg":
            try:
                from .generators.commit_message_generator import CommitMessageGenerator
            except (ImportError, ValueError, SystemError):
                from generators.commit_message_generator import CommitMessageGenerator

            generator = CommitMessageGenerator(project_root, self.docgen.config)
            message = generator.generate()
            if message:
                print(message)
                return 0
            else:
                return 1

        # hooks コマンド
        if args.command == "hooks":
            return self.hooks_handler.handle(args, project_root)

        # アーキテクチャ生成コマンド
        if args.generate_arch:
            from .archgen.cli import generate_architecture

            output_dir = project_root / "docs" / "architecture"
            success = generate_architecture(project_root, output_dir)
            return 0 if success else 1

        if args.detect_only:
            languages = self.docgen.detect_languages()
            logger.info(f"\n検出された言語: {', '.join(languages) if languages else 'なし'}")
            return 0

        # 設定を一時的に上書き
        if args.no_api_doc:
            self.docgen.config_manager.update_config({"generation.generate_api_doc": False})
        if args.no_readme:
            self.docgen.config_manager.update_config({"generation.update_readme": False})

        # RAG有効化
        if args.use_rag:
            self.docgen.config_manager.update_config({"rag.enabled": True})

        if self.docgen.generate_documents():
            return 0
        else:
            return 1

    def _check_and_auto_init(self, project_root: Path) -> int:
        """必須ファイルがない場合に自動初期化"""
        config_path = project_root / "docgen" / "config.toml"

        if not config_path.exists():
            logger.info("必須ファイルが見つかりません。初期化を実行します...")
            result = self.init_handler.handle(force=True, project_root=project_root, quiet=True)
            if result == 0:
                logger.info("✓ 初期化が完了しました")
            return result

        return 0


def main():
    """メインエントリーポイント"""
    try:
        cli = CommandLineInterface()
        sys.exit(cli.run())
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
