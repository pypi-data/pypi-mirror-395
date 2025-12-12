"""
Exceptionsのテスト
"""

# docgenモジュールをインポート可能にする
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.utils.exceptions import (
    CacheError,
    ConfigError,
    DocGenError,
    FileOperationError,
    LLMError,
    ParseError,
)


class TestExceptions:
    """例外クラスのテスト"""

    def test_docgen_error_basic(self):
        """DocGenErrorの基本テスト"""
        error = DocGenError("Test error")

        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details is None

    def test_docgen_error_with_details(self):
        """詳細付きDocGenErrorのテスト"""
        error = DocGenError("Test error", "Additional details")

        assert str(error) == "Test error: Additional details"
        assert error.message == "Test error"
        assert error.details == "Additional details"

    def test_config_error(self):
        """ConfigErrorのテスト"""
        error = ConfigError("Config error", "Invalid configuration")

        assert isinstance(error, DocGenError)
        assert isinstance(error, ConfigError)
        assert str(error) == "Config error: Invalid configuration"

    def test_llm_error(self):
        """LLMErrorのテスト"""
        error = LLMError("LLM error", "API call failed")

        assert isinstance(error, DocGenError)
        assert isinstance(error, LLMError)
        assert str(error) == "LLM error: API call failed"

    def test_parse_error(self):
        """ParseErrorのテスト"""
        error = ParseError("Parse error", "Syntax error in file")

        assert isinstance(error, DocGenError)
        assert isinstance(error, ParseError)
        assert str(error) == "Parse error: Syntax error in file"

    def test_cache_error(self):
        """CacheErrorのテスト"""
        error = CacheError("Cache error", "Cache file corrupted")

        assert isinstance(error, DocGenError)
        assert isinstance(error, CacheError)
        assert str(error) == "Cache error: Cache file corrupted"

    def test_file_operation_error(self):
        """FileOperationErrorのテスト"""
        error = FileOperationError("File error", "Permission denied")

        assert isinstance(error, DocGenError)
        assert isinstance(error, FileOperationError)
        assert str(error) == "File error: Permission denied"

    def test_exception_inheritance(self):
        """例外クラスの継承関係テスト"""
        # すべての例外がDocGenErrorを継承していることを確認
        exceptions = [
            ConfigError("test"),
            LLMError("test"),
            ParseError("test"),
            CacheError("test"),
            FileOperationError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, DocGenError)
            assert isinstance(exc, Exception)

    def test_exception_without_details(self):
        """詳細なしの例外テスト"""
        error = DocGenError("Simple error")

        assert str(error) == "Simple error"
        assert error.details is None

    def test_exception_with_empty_details(self):
        """空の詳細付き例外テスト"""
        error = DocGenError("Error", "")

        assert str(error) == "Error"
        assert error.details == ""

    def test_exception_chaining(self):
        """例外チェーン機能のテスト"""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise ConfigError("Config failed", "Caused by ValueError") from e
        except ConfigError as e:
            assert "Config failed" in str(e)
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, ValueError)

    def test_exception_attributes(self):
        """例外の属性アクセステスト"""
        error = DocGenError("Test message", "Test details")

        # 属性が正しく設定されていることを確認
        assert hasattr(error, "message")
        assert hasattr(error, "details")
        assert error.message == "Test message"
        assert error.details == "Test details"

    def test_exception_repr(self):
        """例外のreprテスト"""
        error = DocGenError("Test")

        # reprがExceptionのデフォルト動作に従うことを確認
        assert "DocGenError" in repr(error)
        assert "Test" in repr(error)
