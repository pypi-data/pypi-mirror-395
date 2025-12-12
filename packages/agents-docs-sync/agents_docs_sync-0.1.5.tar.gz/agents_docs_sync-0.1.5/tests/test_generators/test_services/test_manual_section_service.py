"""
ManualSectionService のテスト
"""

import pytest

from docgen.generators.services.manual_section_service import ManualSectionService


class TestManualSectionService:
    """ManualSectionService のテストクラス"""

    @pytest.fixture
    def service(self):
        """ManualSectionService インスタンス"""
        return ManualSectionService()

    def test_extract_empty_content(self, service):
        """空コンテンツからの抽出"""
        result = service.extract("")
        assert result == {}

    def test_extract_no_manual_sections(self, service):
        """手動セクションがないコンテンツ"""
        content = "# Title\n\nSome content without manual sections."
        result = service.extract(content)
        assert result == {}

    def test_extract_single_section(self, service):
        """単一の手動セクション抽出"""
        content = """# Title

<!-- MANUAL_START: custom -->
This is custom content.
<!-- MANUAL_END: custom -->

Footer
"""
        result = service.extract(content)
        assert "custom" in result
        assert "This is custom content." in result["custom"]

    def test_extract_multiple_sections(self, service):
        """複数の手動セクション抽出"""
        content = """
<!-- MANUAL_START: section1 -->
Content 1
<!-- MANUAL_END: section1 -->

Some other text

<!-- MANUAL_START: section2 -->
Content 2
<!-- MANUAL_END: section2 -->
"""
        result = service.extract(content)
        assert len(result) == 2
        assert "section1" in result
        assert "section2" in result
        assert "Content 1" in result["section1"]
        assert "Content 2" in result["section2"]

    def test_merge_empty_sections(self, service):
        """空の手動セクションでのマージ"""
        content = "# Title\n\nContent"
        result = service.merge(content, {})
        assert result == content

    def test_merge_with_sections(self, service):
        """手動セクションのマージ"""
        generated = """# Title

<!-- MANUAL_START: custom -->
<!-- MANUAL_END: custom -->

Footer
"""
        manual_sections = {"custom": "Preserved content here"}
        result = service.merge(generated, manual_sections)
        assert "Preserved content here" in result

    def test_merge_section_not_in_template(self, service):
        """テンプレートにないセクションは無視される"""
        generated = "# Title\n\nContent without markers"
        manual_sections = {"nonexistent": "This should not appear"}
        result = service.merge(generated, manual_sections)
        assert "This should not appear" not in result
