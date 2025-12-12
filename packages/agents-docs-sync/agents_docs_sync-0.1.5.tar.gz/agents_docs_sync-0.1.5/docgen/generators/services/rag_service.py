"""
RAG Service

RAG (Retrieval-Augmented Generation) コンテキスト取得サービス。
MixinパターンからDIへの移行に対応。
"""

from logging import Logger
from pathlib import Path
from typing import Any

from docgen.utils.logger import get_logger


class RAGService:
    """RAGコンテキスト取得サービス"""

    def __init__(
        self,
        project_root: Path,
        config: dict[str, Any],
        logger: Logger | None = None,
    ):
        """
        初期化

        Args:
            project_root: プロジェクトルートディレクトリ
            config: 設定辞書
            logger: ロガー
        """
        self._project_root = project_root
        self._config = config
        self._logger = logger or get_logger("rag_service")

    @property
    def is_enabled(self) -> bool:
        """RAGが有効かどうか"""
        return self._config.get("rag", {}).get("enabled", False)

    def get_context(self, query: str, top_k: int | None = None) -> str:
        """
        RAGコンテキストを取得してフォーマット

        Args:
            query: 検索クエリ
            top_k: 取得するチャンク数（Noneの場合は設定ファイルから読み取る）

        Returns:
            フォーマット済みのコンテキスト文字列（RAG無効時は空文字列）
        """
        if not self.is_enabled:
            return ""

        try:
            from docgen.rag.retriever import DocumentRetriever

            self._logger.info(f"Retrieving RAG context for query: {query[:50]}...")

            if top_k is None:
                top_k = self._config.get("rag", {}).get("retrieval", {}).get("top_k", 6)

            retriever = DocumentRetriever(self._config, self._project_root, logger=self._logger)
            chunks = retriever.retrieve(query, top_k=top_k)

            if not chunks:
                self._logger.warning("No relevant chunks found for query")
                return ""

            formatted_context = retriever.format_context(chunks)
            self._logger.info(f"Retrieved {len(chunks)} relevant chunks")
            return formatted_context

        except ImportError:
            self._logger.warning(
                "RAGモジュールが利用できません。"
                "RAG依存関係をインストールしてください: uv sync --extra rag"
            )
            return ""
        except FileNotFoundError as e:
            self._logger.warning(
                f"RAGインデックスが見つかりません: {e}。"
                "インデックスをビルドしてください: uv run python -m docgen.docgen --build-index"
            )
            return ""
        except Exception as e:
            self._logger.error(f"RAGコンテキスト取得中にエラー: {e}", exc_info=True)
            return ""
