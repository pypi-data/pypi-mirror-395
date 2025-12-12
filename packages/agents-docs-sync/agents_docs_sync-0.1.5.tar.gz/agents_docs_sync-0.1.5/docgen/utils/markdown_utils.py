"""Markdown generation utilities for document generators."""

from pathlib import Path
import re

# Manual section markers
MANUAL_START_PREFIX = "<!-- MANUAL_START:"
MANUAL_END_PREFIX = "<!-- MANUAL_END:"
MANUAL_MARKER_PATTERN = r"<!--\s*MANUAL_START:(\w+)\s*-->(.*?)<!--\s*MANUAL_END:\1\s*-->"
MANUAL_MARKER_REGEX = re.compile(MANUAL_MARKER_PATTERN, re.DOTALL)

# Specific manual markers
DESCRIPTION_START = "<!-- MANUAL_START:description -->"
DESCRIPTION_END = "<!-- MANUAL_END:description -->"
SETUP_START = "<!-- MANUAL_START:setup -->"
SETUP_END = "<!-- MANUAL_END:setup -->"
USAGE_START = "<!-- MANUAL_START:usage -->"
USAGE_END = "<!-- MANUAL_END:usage -->"
OTHER_START = "<!-- MANUAL_START:other -->"
OTHER_END = "<!-- MANUAL_END:other -->"

# Common strings
UNKNOWN = "不明"
GENERATION_TIMESTAMP_LABEL = "自動生成日時:"
SECTION_SEPARATOR = "---"

# Timestamp format
CURRENT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_current_timestamp() -> str:
    """Get current timestamp in standard format."""
    from datetime import datetime

    return datetime.now().strftime(CURRENT_TIMESTAMP_FORMAT)


def extract_project_description(
    project_root: Path,
    project_info_description: str | None,
    exclude_readme_path: Path | None = None,
) -> str:
    """
    Extract project description from README.md or project info.

    Args:
        project_root: Project root directory
        project_info_description: Description from project info (fallback)
        exclude_readme_path: README path to exclude (to prevent circular reference)

    Returns:
        Project description text
    """
    readme_path = project_root / "README.md"

    # Try to extract from README first (if not excluded)
    if readme_path.exists() and readme_path != exclude_readme_path:
        readme_content = readme_path.read_text(encoding="utf-8")
        # Extract first meaningful paragraph
        for line in readme_content.split("\n"):
            line_stripped = line.strip()
            if (
                line_stripped
                and not line_stripped.startswith("#")
                and not line_stripped.startswith("<!--")
            ):
                # Skip generic template text
                if "このプロジェクトの説明をここに記述してください" not in line_stripped:
                    return line_stripped

    # Fallback to project info
    if project_info_description:
        return project_info_description

    # Default message
    return "このプロジェクトの説明をここに記述してください。"


def clean_llm_output_advanced(text: str) -> str:
    """
    Advanced LLM output cleaning with thinking process removal and code block handling.

    Args:
        text: LLM generated text to clean

    Returns:
        Cleaned text with thinking processes removed
    """
    if not text:
        return text

    lines = text.split("\n")
    cleaned_lines = []
    in_code_block = False
    code_block_lang = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # コードブロックの開始/終了を検出
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_lang = line.strip()[3:].strip().lower()
                # マークダウンコードブロック内の思考過程をスキップ
                if "markdown" in code_block_lang:
                    i += 1
                    # 次の```までスキップ
                    while i < len(lines) and not lines[i].strip().startswith("```"):
                        i += 1
                    if i < len(lines):
                        i += 1  # ```をスキップ
                    in_code_block = False
                    continue
                else:
                    cleaned_lines.append(line)
                    i += 1
                    continue
            else:
                in_code_block = False
                code_block_lang = None
                cleaned_lines.append(line)
                i += 1
                continue

        # コードブロック内はそのまま保持
        if in_code_block:
            cleaned_lines.append(line)
            i += 1
            continue

        # 思考過程のパターンを検出
        line_lower = line.lower().strip()

        # 特殊なマーカーパターン（最初にチェック）
        if "<|channel|>" in line or "<|message|>" in line or "commentary/analysis" in line_lower:
            i += 1
            # 次の空行または通常のコンテンツまでスキップ
            while (
                i < len(lines)
                and not lines[i].strip().startswith("##")
                and not lines[i].strip().startswith("<!--")
            ):
                if lines[i].strip() and not any(
                    pattern in lines[i].lower()
                    for pattern in ["let's", "we need", "but we", "thus final"]
                ):
                    break
                i += 1
            continue

        # 思考過程の開始パターン
        thinking_patterns = [
            "we need to",
            "thus final answer",
            "let's generate",
            "let's do",
            "but we need",
            "hence final answer",
            "thus final output",
            "i will produce",
            "i think",
            "ok i'll",
            "let's finalize",
            "but i think",
            "but we need to",
            "thus final answer will",
            "we should produce",
            "we will output",
            "we must produce",
            "thus the final",
            "but the actual",
            "so i will",
            "i'm going to",
            "i'm still not sure",
            "but it's enough",
            "let's output",
            "let's produce",
            "let's final answer",
            "but we need the final",
            "thus final answer is",
            "we now produce",
            "this content includes",
            "but we also mention",
            "ok, i will",
            "thus we must",
            "but we need to ensure",
            "let's generate:",
            "we should produce final",
            "thus final answer will be",
            "but i'm still not sure",
            "but i think it's",
            "let's finalize:",
            "we need the final answer",
            "thus final answer:",
            "ok i'll produce",
            "以下が、",
            "改訂版です",
            "手動セクションは保持",
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

        # 思考過程の行をスキップ
        if any(pattern in line_lower for pattern in thinking_patterns):
            i += 1
            continue

        # プレースホルダーや不完全な記述を検出
        placeholder_patterns = [
            "???",
            "(??)",
            "... ...",
            "|  | |",
            "---‐‐‐",
            "continue",
            "we should now",
            "this content, while present",
            "# ... (continue)",
        ]

        if any(pattern in line_lower for pattern in placeholder_patterns):
            i += 1
            continue

        # 空行の連続を制限（3行以上は2行に）
        if not line.strip():
            if cleaned_lines and not cleaned_lines[-1].strip():
                if len(cleaned_lines) >= 2 and not cleaned_lines[-2].strip():
                    i += 1
                    continue

        cleaned_lines.append(line)
        i += 1

    # 結果を結合
    result = "\n".join(cleaned_lines)

    # 手動マーカーを除去
    result = re.sub(
        r"<!--\s*MANUAL_START:\w+\s*-->|<!--\s*MANUAL_END:\w+\s*-->", "", result
    ).strip()

    # 先頭と末尾の空行を削除
    result = result.strip()

    # 重複した説明を削除（同じ行が3回以上続く場合）
    lines_result = result.split("\n")
    deduplicated = []
    prev_line = None
    repeat_count = 0

    for line in lines_result:
        if line == prev_line:
            repeat_count += 1
            if repeat_count < 3:
                deduplicated.append(line)
        else:
            repeat_count = 0
            deduplicated.append(line)
        prev_line = line

    return "\n".join(deduplicated)
