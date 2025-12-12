"""
CommitMessageGeneratorのテスト
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.generators.commit_message_generator import CommitMessageGenerator


class TestCommitMessageGenerator:
    """CommitMessageGeneratorクラスのテスト"""

    def test_commit_message_generator_initialization(self, temp_project):
        """CommitMessageGeneratorの初期化テスト"""
        config = {"agents": {"llm_mode": "api"}}

        generator = CommitMessageGenerator(temp_project, config)

        assert generator.project_root == temp_project
        assert generator.config == config
        assert generator.agents_config == {"llm_mode": "api"}

    def test_generate_no_staged_changes(self, temp_project):
        """ステージングされた変更がない場合のテスト"""
        config = {"agents": {"llm_mode": "api"}}

        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(generator, "_get_staged_changes", return_value=None):
            result = generator.generate()

            assert result is None

    @patch("docgen.generators.commit_message_generator.LLMClientFactory")
    def test_generate_with_llm(self, mock_llm_factory, temp_project):
        """LLMを使用したコミットメッセージ生成テスト"""
        config = {"agents": {"llm_mode": "api", "api": {"provider": "openai"}}}

        staged_changes = """
diff --git a/src/main.py b/src/main.py
index 1234567..abcdef0 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,5 +1,7 @@
 def hello():
-    print("Hello")
+    print("Hello, World!")
+
+def goodbye():
+    print("Goodbye")
"""

        mock_client = MagicMock()
        mock_client.generate.return_value = "feat(ui): add greeting and farewell functions"
        mock_llm_factory.create_client_with_fallback.return_value = mock_client

        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(generator, "_get_staged_changes", return_value=staged_changes):
            result = generator.generate()

            assert result == "feat(ui): add greeting and farewell functions"
            mock_client.generate.assert_called_once()

    @patch("docgen.generators.commit_message_generator.LLMClientFactory")
    def test_generate_llm_client_creation_failure(self, mock_llm_factory, temp_project):
        """LLMクライアント作成失敗時のテスト"""
        config = {"agents": {"llm_mode": "api"}}
        mock_llm_factory.create_client_with_fallback.return_value = None

        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(generator, "_get_staged_changes", return_value="some changes"):
            result = generator.generate()

            assert result is None

    @patch("docgen.generators.commit_message_generator.LLMClientFactory")
    def test_generate_llm_returns_empty(self, mock_llm_factory, temp_project):
        """LLMが空文字列を返す場合のテスト"""
        config = {"agents": {"llm_mode": "api"}}

        mock_client = MagicMock()
        mock_client.generate.return_value = ""
        mock_llm_factory.create_client_with_fallback.return_value = mock_client

        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(generator, "_get_staged_changes", return_value="some changes"):
            result = generator.generate()

            assert result is None

    @patch("docgen.generators.commit_message_generator.LLMClientFactory")
    def test_generate_llm_returns_multiline(self, mock_llm_factory, temp_project):
        """LLMが複数行を返す場合のテスト"""
        config = {"agents": {"llm_mode": "api"}}

        mock_client = MagicMock()
        mock_client.generate.return_value = (
            "feat: add new feature\n\nThis is a detailed description"
        )
        mock_llm_factory.create_client_with_fallback.return_value = mock_client

        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(generator, "_get_staged_changes", return_value="some changes"):
            result = generator.generate()

            assert result == "feat: add new feature"

    def test_get_staged_changes_success(self, temp_project):
        """ステージングされた変更の取得成功テスト"""
        generator = CommitMessageGenerator(temp_project, {})

        mock_stat_result = MagicMock()
        mock_stat_result.stdout = " 1 file changed, 2 insertions(+)"
        mock_stat_result.returncode = 0

        mock_diff_result = MagicMock()
        mock_diff_result.stdout = "diff content here"
        mock_diff_result.returncode = 0

        with patch(
            "subprocess.run", side_effect=[mock_stat_result, mock_diff_result]
        ) as mock_subprocess:
            result = generator._get_staged_changes()

            assert result == " 1 file changed, 2 insertions(+)\n\ndiff content here"
            assert mock_subprocess.call_count == 2

    def test_get_staged_changes_stat_failure(self, temp_project):
        """git diff --cached --statが失敗した場合のテスト"""
        generator = CommitMessageGenerator(temp_project, {})

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "fatal: not a git repository"

        with patch("subprocess.run", return_value=mock_result):
            result = generator._get_staged_changes()

            assert result is None

    def test_get_staged_changes_no_git_repo(self, temp_project):
        """Gitリポジトリがない場合のテスト"""
        generator = CommitMessageGenerator(temp_project, {})

        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = generator._get_staged_changes()

            assert result is None

    def test_get_staged_changes_diff_failure(self, temp_project):
        """詳細diff取得失敗時のテスト（statのみ返す）"""
        generator = CommitMessageGenerator(temp_project, {})

        mock_stat_result = MagicMock()
        mock_stat_result.stdout = " 1 file changed, 2 insertions(+)"
        mock_stat_result.returncode = 0

        mock_diff_result = MagicMock()
        mock_diff_result.returncode = 1

        with patch("subprocess.run", side_effect=[mock_stat_result, mock_diff_result]):
            result = generator._get_staged_changes()

            assert result == " 1 file changed, 2 insertions(+)"

    def test_get_staged_changes_long_diff_truncated(self, temp_project):
        """長いdiffが切り詰められるテスト"""
        generator = CommitMessageGenerator(temp_project, {})

        mock_stat_result = MagicMock()
        mock_stat_result.stdout = " 1 file changed, 100 insertions(+)"
        mock_stat_result.returncode = 0

        # 長いdiffを作成
        long_diff = "a" * 6000
        mock_diff_result = MagicMock()
        mock_diff_result.stdout = long_diff
        mock_diff_result.returncode = 0

        with patch("subprocess.run", side_effect=[mock_stat_result, mock_diff_result]):
            result = generator._get_staged_changes()

            assert result is not None
            assert "... (truncated)" in result
            assert len(result) < len(long_diff) + 100

    def test_create_prompt(self, temp_project):
        """プロンプト作成テスト"""
        generator = CommitMessageGenerator(temp_project, {})

        staged_changes = "diff content here"

        prompt = generator._create_prompt(staged_changes)

        assert "以下のGitの変更内容を分析して" in prompt
        assert "Conventional Commits形式" in prompt
        assert "diff content here" in prompt

    def test_create_prompt_with_custom_changes(self, temp_project):
        """カスタム変更内容でのプロンプト作成テスト"""
        generator = CommitMessageGenerator(temp_project, {})

        staged_changes = """
diff --git a/test.py b/test.py
new file mode 100644
index 0000000..1234567
--- /dev/null
+++ b/test.py
@@ -0,0 +1,3 @@
+def test():
+    pass
"""

        prompt = generator._create_prompt(staged_changes)

        assert "test.py" in prompt
        assert "def test():" in prompt

    def test_generate_exception_handling(self, temp_project):
        """例外処理のテスト"""
        config = {"agents": {"llm_mode": "api"}}
        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(generator, "_get_staged_changes", side_effect=Exception("Test error")):
            result = generator.generate()

            assert result is None
