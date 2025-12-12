"""
Coverage tests for MarkdownUtils.
"""

from docgen.utils.markdown_utils import clean_llm_output_advanced


class TestMarkdownUtilsCoverage:
    def test_clean_llm_output_advanced_empty(self):
        assert clean_llm_output_advanced("") == ""
        assert clean_llm_output_advanced(None) is None

    def test_clean_llm_output_advanced_code_block(self):
        text = """
Here is code:
```python
def foo():
    pass
```
End.
"""
        cleaned = clean_llm_output_advanced(text)
        assert "def foo():" in cleaned
        assert "```python" in cleaned

    def test_clean_llm_output_advanced_markdown_thinking(self):
        text = """
```markdown
Thinking...
```
Real content
"""
        cleaned = clean_llm_output_advanced(text)
        assert "Thinking..." not in cleaned
        assert "Real content" in cleaned

    def test_clean_llm_output_advanced_thinking_patterns(self):
        text = """
We need to generate code.
Thus final answer is:
Actual content.
"""
        cleaned = clean_llm_output_advanced(text)
        assert "We need to" not in cleaned
        assert "Thus final answer is" not in cleaned
        assert "Actual content" in cleaned

    def test_clean_llm_output_advanced_special_markers(self):
        text = """
<|channel|>
Let's think...
## Header
Content
"""
        cleaned = clean_llm_output_advanced(text)
        assert "<|channel|>" not in cleaned
        assert "Let's think..." not in cleaned
        assert "## Header" in cleaned

    def test_clean_llm_output_advanced_placeholders(self):
        text = """
Content
???
More content
"""
        cleaned = clean_llm_output_advanced(text)
        assert "???" not in cleaned
        assert "Content" in cleaned
        assert "More content" in cleaned

    def test_clean_llm_output_advanced_deduplication(self):
        text = """
Line 1
Line 1
Line 1
Line 1
"""
        cleaned = clean_llm_output_advanced(text)
        lines = cleaned.split("\n")
        assert len(lines) == 3  # Should keep first 3 (implementation allows 2 repetitions)
        assert lines[0] == "Line 1"
        assert lines[1] == "Line 1"
        assert lines[2] == "Line 1"

    def test_clean_llm_output_advanced_manual_markers(self):
        text = """
<!-- MANUAL_START:foo -->
Content
<!-- MANUAL_END:foo -->
"""
        cleaned = clean_llm_output_advanced(text)
        assert "MANUAL_START" not in cleaned
        assert "Content" in cleaned
