"""
Outlines統合ユーティリティモジュール
共通のOutlines関連機能をまとめる
"""

try:
    import outlines

    OUTLINES_AVAILABLE = True
except ImportError:
    OUTLINES_AVAILABLE = False
    outlines = None

from typing import Any

from ..utils.llm import LLMClientFactory


def should_use_outlines(config: dict[str, Any]) -> bool:
    """
    Outlinesを使用するかどうかを判定

    Args:
        config: 設定辞書

    Returns:
        Outlinesを使用するかどうか
    """
    # Outlinesライブラリが利用可能かチェック
    if not OUTLINES_AVAILABLE:
        return False

    # 設定でOutlinesが有効になっているかチェック
    return config.get("use_outlines", False)


def create_outlines_model(client, provider: str = "openai"):
    """
    Outlinesモデルを作成

    Args:
        client: LLMクライアント
        provider: プロバイダー名 ('openai', 'anthropic', 'local')

    Returns:
        Outlinesモデルインスタンス（作成できない場合はNone）
    """
    if not OUTLINES_AVAILABLE:
        return None

    try:
        # クライアントの種類に応じてOutlinesモデルを作成
        if hasattr(client, "client") and hasattr(client.client, "api_key"):
            # OpenAIクライアント
            if outlines is not None:
                return outlines.from_openai(client.client, client.model)  # type: ignore
        elif hasattr(client, "base_url"):
            # ローカルLLMクライアント
            provider = getattr(client, "provider", "ollama")

            if provider == "ollama":
                # Ollamaの場合
                if outlines is not None:
                    return outlines.from_ollama(client.model, client.base_url)  # type: ignore
            else:
                # その他のローカルLLMはOpenAI互換APIとして扱う
                import openai

                openai_client = openai.OpenAI(
                    base_url=f"{client.base_url}"
                    if client.base_url.rstrip("/").endswith("/v1")
                    else f"{client.base_url}/v1",
                    api_key="dummy",  # ローカルでは不要
                )
                if outlines is not None:
                    return outlines.from_openai(openai_client, client.model)  # type: ignore
        else:
            raise ValueError("サポートされていないクライアントタイプ")
    except Exception:
        # エラーログは呼び出し元で処理
        return None


def get_llm_client_with_fallback(config: dict[str, Any], agents_config: dict[str, Any]):
    """
    LLMクライアントを取得（フォールバック付き）

    Args:
        config: メイン設定
        agents_config: AGENTS設定

    Returns:
        LLMクライアントインスタンス
    """
    llm_mode = agents_config.get("llm_mode", "api")
    preferred_mode = "api" if llm_mode in "api" else "local"

    return LLMClientFactory.create_client_with_fallback(
        agents_config, preferred_mode=preferred_mode
    )


def validate_output(text: str) -> bool:
    """
    LLMの出力を検証して、不適切な内容が含まれていないかチェック

    Args:
        text: 検証するテキスト

    Returns:
        検証に合格したかどうか
    """
    if not text or not text.strip():
        return False

    text_lower = text.lower()

    # 特殊なマーカーパターンをチェック
    if "<|channel|>" in text or "<|message|>" in text or "commentary/analysis" in text_lower:
        return False

    # 思考過程のパターンが含まれていないかチェック
    thinking_patterns = [
        "thus final answer",
        "let's generate",
        "but we need",
        "i will produce",
        "i think",
        "let's finalize",
        "we should produce",
        "we will output",
        "thus the final",
        "i'm going to",
        "let's output",
        "let's produce",
        "but i think it's",
        "thus final answer will be",
        "以下が、",
        "改訂版です",
        "we should now",
        "we will not include",
        "should we keep",
        "possibly they want",
        "but we must keep",
        "but we might need",
        "however, user wrote",
        "also note",
        "but the user",
        "ok final output",
        "ok. i'll generate",
        "let's create final output",
        "check that it doesn't",
        "now i will provide",
        "the user wants",
        "they gave",
        "so we should",
        "so we can",
        "also keep",
        "we must not include",
        "so final output",
        "but we must also keep",
        "we must only output",
        "but we must",
    ]

    for pattern in thinking_patterns:
        if pattern in text_lower:
            return False

    # プレースホルダーが含まれていないかチェック
    placeholder_patterns = [
        "???",
        "(??)",
        "... ...",
        "|  | |",
        "---‐‐‐",
        "# ... (continue)",
    ]

    for pattern in placeholder_patterns:
        if pattern in text:
            return False

    # マークダウンコードブロック内に思考過程が含まれていないかチェック
    lines = text.split("\n")
    in_markdown_block = False
    for line in lines:
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip().lower()
            if "markdown" in lang:
                in_markdown_block = True
            elif in_markdown_block:
                in_markdown_block = False
        elif in_markdown_block:
            if any(pattern in line.lower() for pattern in thinking_patterns):
                return False

    return True
