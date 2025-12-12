"""ドキュメント検索モジュール

ベクトルインデックスから類似チャンクを検索・取得します。
"""

from logging import Logger
from pathlib import Path
from typing import Any

from ..utils.logger import get_logger
from .embedder import Embedder
from .indexer import VectorIndexer


class DocumentRetriever:
    """ドキュメント検索クラス"""

    def __init__(
        self,
        config: dict[str, Any],
        project_root: Path | None = None,
        logger: Logger | None = None,
    ):
        """
        初期化

        Args:
            config: 設定辞書（config.toml全体）
            project_root: プロジェクトルート（指定しない場合は現在のディレクトリ）
            logger: ロガーインスタンス（Noneの場合は新規作成）
        """
        self.config = config
        self.rag_config = config.get("rag", {})
        self.project_root = project_root or Path.cwd()
        self.logger = logger or get_logger(__name__)

        # 検索設定
        retrieval_config = self.rag_config.get("retrieval", {})
        self.default_top_k = retrieval_config.get("top_k", 6)
        self.score_threshold = retrieval_config.get("score_threshold", 0.3)

        # インデックスディレクトリ
        self.index_dir = self.project_root / "docgen" / "index"

        # コンポーネント（Lazy loading）
        self._embedder = None
        self._indexer = None

    @property
    def embedder(self) -> Embedder:
        """Embedderインスタンスを取得（Lazy loading）"""
        if self._embedder is None:
            self._embedder = Embedder(self.rag_config, logger=self.logger)
        return self._embedder

    @property
    def indexer(self) -> VectorIndexer:
        """VectorIndexerインスタンスを取得（Lazy loading）"""
        if self._indexer is None:
            # Embedderから次元数を取得
            embedding_dim = self.embedder.embedding_dim

            self._indexer = VectorIndexer(
                index_dir=self.index_dir,
                embedding_dim=embedding_dim,
                config=self.rag_config,
                logger=self.logger,
            )

            # インデックスを読み込み
            try:
                self._indexer.load()
            except FileNotFoundError:
                self.logger.warning(
                    f"Index not found at {self.index_dir}. "
                    "Please build the index first with: "
                    "uv run python -m docgen.docgen --build-index"
                )
                raise

        return self._indexer

    def retrieve(self, query: str, top_k: int | None = None) -> list[dict[str, Any]]:
        """
        クエリに類似するチャンクを検索

        Args:
            query: 検索クエリ
            top_k: 取得する件数（Noneの場合はデフォルト値）

        Returns:
            チャンクのリスト（スコア付き）
        """
        k = top_k if top_k is not None else self.default_top_k

        self.logger.info(f"Retrieving top-{k} chunks for query: {query[:50]}...")

        # クエリを埋め込み
        query_embedding = self.embedder.embed_text(query)

        # 検索実行
        results = self.indexer.search(query_embedding, k=k)

        # スコア閾値でフィルタリング
        filtered_results = [chunk for chunk, score in results if score >= self.score_threshold]

        # スコアをメタデータに追加
        for i, (_chunk, score) in enumerate(results):
            if i < len(filtered_results):
                filtered_results[i]["similarity_score"] = score

        self.logger.info(
            f"Retrieved {len(filtered_results)} chunks (threshold: {self.score_threshold})"
        )

        return filtered_results

    def format_context(self, chunks: list[dict[str, Any]]) -> str:
        """
        チャンクをコンテキスト文字列にフォーマット

        Args:
            chunks: チャンクのリスト

        Returns:
            フォーマット済みのコンテキスト文字列
        """
        if not chunks:
            return ""

        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            # 出典情報
            source = f"{chunk['file']}:{chunk['start_line']}-{chunk['end_line']}"

            # スコア情報（あれば）
            score_info = ""
            if "similarity_score" in chunk:
                score_info = f" (score: {chunk['similarity_score']:.3f})"

            # チャンク情報
            context_parts.append(
                f"[{i}] {source}{score_info}\n"
                f"Type: {chunk['type']}, Name: {chunk['name']}\n"
                f"```\n{chunk['text']}\n```\n"
            )

        return "\n".join(context_parts)

    def retrieve_with_rerank(
        self, query: str, top_k: int = 6, rerank_k: int = 20
    ) -> list[dict[str, Any]]:
        """
        再ランキング付き検索（将来の拡張用）

        Args:
            query: 検索クエリ
            top_k: 最終的に取得する件数
            rerank_k: 初期検索で取得する件数（再ランク対象）

        Returns:
            再ランク済みのチャンクのリスト
        """
        # 現時点では通常の検索と同じ（cross-encoderは将来実装）
        self.logger.info("Reranking is not yet implemented, using standard retrieval")
        return self.retrieve(query, top_k=top_k)
