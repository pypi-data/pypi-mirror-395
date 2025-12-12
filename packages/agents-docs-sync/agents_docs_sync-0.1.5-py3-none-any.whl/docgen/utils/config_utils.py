"""
設定アクセスユーティリティ
"""

from typing import Any


def get_nested_config(config: dict[str, Any], *keys: str, default: Any = None) -> Any:
    """
    ネストされた設定値を安全に取得

    Args:
        config: 設定辞書
        *keys: 取得するキーのパス
        default: デフォルト値

    Returns:
        設定値。存在しない場合はdefault

    Examples:
        >>> config = {"a": {"b": {"c": "value"}}}
        >>> get_nested_config(config, "a", "b", "c")
        'value'
        >>> get_nested_config(config, "a", "x", "y", default="default")
        'default'
    """
    current = config
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def get_config_bool(config: dict[str, Any], *keys: str, default: bool = False) -> bool:
    """
    設定値をブール値として取得

    Args:
        config: 設定辞書
        *keys: 取得するキーのパス
        default: デフォルト値

    Returns:
        ブール値
    """
    value = get_nested_config(config, *keys, default=default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    return bool(value)


def get_config_list(config: dict[str, Any], *keys: str, default: list | None = None) -> list:
    """
    設定値をリストとして取得

    Args:
        config: 設定辞書
        *keys: 取得するキーのパス
        default: デフォルト値

    Returns:
        リスト
    """
    if default is None:
        default = []
    value = get_nested_config(config, *keys, default=default)
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        # カンマ区切りをサポート
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, (int, float)):
        return [value]
    return default


def get_config_str(config: dict[str, Any], *keys: str, default: str = "") -> str:
    """
    設定値を文字列として取得

    Args:
        config: 設定辞書
        *keys: 取得するキーのパス
        default: デフォルト値

    Returns:
        文字列
    """
    value = get_nested_config(config, *keys, default=default)
    if value is None:
        return default
    if isinstance(value, str):
        return value
    return str(value)
