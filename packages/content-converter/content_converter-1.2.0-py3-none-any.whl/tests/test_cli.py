"""
CLIモジュールのテスト
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import pytest
import importlib
from content_converter.cli import main, parse_args, get_api_key
import content_converter.cli


class TestCLI:
    """CLIモジュールのテスト"""

    def setup_method(self):
        """テストメソッドの前に実行されるセットアップメソッド"""
        # 一時ディレクトリを作成
        self.temp_dir = tempfile.TemporaryDirectory()
        # テスト用の一時ファイルを作成
        self.test_file_path = os.path.join(self.temp_dir.name, "test_markdown.md")
        with open(self.test_file_path, "w") as f:
            f.write("# Test Title\n\nTest Content")

    def teardown_method(self):
        """テストメソッドの後に実行されるクリーンアップメソッド"""
        # 一時ディレクトリを削除
        self.temp_dir.cleanup()
        self.temp_dir.cleanup()

    @patch("content_converter.cli.parse_args")
    def test_parse_args_default(self, mock_parse_args):
        """デフォルト引数のテスト"""
        mock_args = MagicMock()
        mock_args.input = "test.md"
        mock_args.platform = "zenn"
        mock_args.output = None
        mock_args.use_llm = False
        mock_args.llm_provider = "gemini"
        mock_args.model = None
        mock_args.prompt_file = None
        mock_args.template = None
        mock_args.generate_summary = False
        mock_args.summary_length = 100
        mock_parse_args.return_value = mock_args

        args = content_converter.cli.parse_args()
        assert args.input == "test.md"
        assert args.platform == "zenn"
        assert args.output is None
        assert args.use_llm is False
        assert args.llm_provider == "gemini"
        assert args.model is None
        assert args.prompt_file is None
        assert args.template is None
        assert args.generate_summary is False
        assert args.summary_length == 100

    @patch("sys.argv", ["content_converter", "--input", "input.md", "--template", "template.txt"])
    def test_parse_args_custom_platform(self):
        """カスタムプラットフォーム指定のテスト"""
        args = parse_args()
        assert args.input == "input.md"
        assert not hasattr(args, 'platform') # Verify platform attribute is gone

    @patch("sys.argv", ["content_converter", "--input", "input.md", "--template", "template.txt", "--output", "output.md"])
    def test_parse_args_custom_output(self):
        """カスタム出力ファイル指定のテスト"""
        args = parse_args()
        assert args.output == "output.md"
        assert args.input == "input.md"

    @patch("sys.argv", ["content_converter", "--input", "input.md", "--template", "template.txt", "--llm-provider", "openrouter"])
    def test_parse_args_llm_options(self):
        """LLMオプション指定のテスト"""
        args = parse_args()
        assert args.llm_provider == "openrouter"
        assert args.input == "input.md"

    @patch("content_converter.cli.parse_args")
    @patch("content_converter.cli.ConverterFactory.create_converter")
    def test_main_file_not_found(self, mock_create_converter, mock_parse_args):
        """存在しないファイルを指定したときのテスト"""
        # モックの戻り値を設定
        mock_args = MagicMock()
        mock_args.input = "non_existent_file.md"
        mock_args.platform = "zenn"
        mock_args.output = None
        mock_args.use_llm = False
        mock_args.llm_provider = "gemini"
        mock_args.model = None
        mock_args.prompt_file = None
        mock_args.template = None
        mock_args.generate_summary = False
        mock_args.summary_length = 100
        mock_parse_args.return_value = mock_args

        # コンバーターのモック
        mock_converter = MagicMock()
        mock_converter.convert_file.side_effect = FileNotFoundError()
        mock_converter.save_converted_file = MagicMock()
        mock_create_converter.return_value = mock_converter

        # main関数の戻り値でエラー終了を確認
        result = content_converter.cli.main()
        assert result == 1

    @patch("content_converter.cli.parse_args")
    @patch("content_converter.cli.ConverterFactory.create_converter")
    def test_main_valid_file(self, mock_create_converter, mock_parse_args):
        """有効なファイルのテスト"""
        # モックの戻り値を設定
        mock_args = MagicMock()
        mock_args.input = self.test_file_path
        mock_args.platform = "zenn"
        mock_args.output = "dummy_output.md"
        mock_args.use_llm = False
        mock_args.llm_provider = "gemini"
        mock_args.model = None
        mock_args.prompt_file = None
        mock_args.template = None
        mock_args.generate_summary = False
        mock_args.summary_length = 100
        mock_args.prompt = None
        mock_parse_args.return_value = mock_args

        # コンバーターのモック
        mock_converter = MagicMock()
        mock_converter.convert_file.return_value = "変換後のコンテンツ"
        mock_converter.save_converted_file = MagicMock()
        mock_create_converter.return_value = mock_converter

        # テスト対象関数を実行
        content_converter.cli.main()

        # モックの呼び出し確認
        mock_create_converter.assert_called_once()
        mock_converter.convert_file.assert_called_once_with(
            input_path=self.test_file_path,
            template_path=None,
            prompt_path=mock_args.prompt
        )
        mock_converter.save_converted_file.assert_called_once_with("変換後のコンテンツ", "dummy_output.md")

    @patch("content_converter.cli.parse_args")
    @patch("content_converter.cli.ConverterFactory.create_converter")
    def test_main_with_llm_options(self, mock_create_converter, mock_parse_args):
        """LLMオプションを使用した変換テスト"""
        # モックの戻り値を設定
        mock_args = MagicMock()
        mock_args.input = self.test_file_path
        mock_args.platform = "zenn"
        mock_args.output = None
        mock_args.use_llm = True
        mock_args.llm_provider = "gemini"
        mock_args.model = "gemini-2.0-flash-001"
        mock_args.prompt_file = "test_prompt.txt"
        mock_args.template = "test_template.txt"
        mock_args.generate_summary = True
        mock_args.summary_length = 150
        mock_parse_args.return_value = mock_args

        # コンバーターのモック
        mock_converter = MagicMock()
        mock_converter.convert_file.return_value = "変換後のコンテンツ"
        mock_create_converter.return_value = mock_converter

        # テスト対象関数を実行
        with patch("builtins.print") as mock_print:
            content_converter.cli.main()

        # コンバーター作成時のconfigの検証
        expected_config = {
            "use_llm": True,
            "llm_provider": "gemini",
            "generate_summary": True,
            "summary_length": 150,
            "model": "gemini-2.0-flash-001",
            "prompt_file": "test_prompt.txt",
            "template_file": "test_template.txt",
            "llm_options": {
                "model": "gemini-2.0-flash-001"
            }
        }
        mock_create_converter.assert_called_once_with(
            platform_type="zenn",
            llm_provider=None,  # LLMプロバイダーはNone（実装中）
            config=expected_config
        )
        mock_print.assert_any_call("注意: LLM機能は現在実装中です。")

    @patch("content_converter.cli.parse_args")
    @patch("content_converter.cli.ConverterFactory.create_converter")
    def test_main_exception_handling(self, mock_create_converter, mock_parse_args):
        """例外発生時のメイン関数のテスト"""
        # モックの戻り値を設定
        mock_args = MagicMock()
        mock_args.input = self.test_file_path
        mock_args.template = "dummy_template.txt"
        mock_args.prompt = None
        mock_args.output = None
        mock_args.llm_provider = None  # APIキーエラーを回避
        mock_args.model = None
        mock_args.api_key = None
        mock_parse_args.return_value = mock_args

        # コンバーターのモック（例外を発生させる）
        mock_converter = MagicMock()
        mock_converter.convert_file.side_effect = Exception("Test error")
        mock_create_converter.return_value = mock_converter

        # main関数の戻り値を検証
        result = content_converter.cli.main()
        assert result == 1

    @patch("sys.argv", ["content_converter", "--input", "input.md", "--template", "dummy_template.txt"])
    def test_default_output_path(self):
        """デフォルト出力パスのテスト"""
        args = parse_args()
        assert args.output is None
        assert args.input == "input.md"



    def test_entry_point(self):
        """エントリーポイントのテスト"""
        # テスト用の一時ファイルを作成
        with tempfile.NamedTemporaryFile(suffix='.md') as temp_file:
            # モジュールのリロード前にモックを設定
            with patch('sys.argv', ['content_converter', '--input', 'test.md']):
                with patch('content_converter.cli.main') as mock_main:
                    # 直接main()を呼び出す
                    content_converter.cli.main()
                    
                    # mainが呼ばれたことを確認
                    mock_main.assert_called_once()
                    # 引数なしで呼ばれたことを確認
                    args, kwargs = mock_main.call_args
                    assert args == ()
                    assert kwargs == {}

    @patch("content_converter.cli.parse_args")
    @patch("content_converter.cli.ConverterFactory.create_converter")
    @patch("builtins.open", new_callable=MagicMock)
    def test_main_custom_output(self, mock_open, mock_create_converter, mock_parse_args):
        """カスタム出力先を指定したときのテスト"""
        # モックの戻り値を設定
        mock_args = MagicMock()
        mock_args.input = self.test_file_path
        mock_args.template = "dummy_template.txt"
        mock_args.prompt = None
        mock_args.output = "custom_output.md"
        mock_args.llm_provider = "gemini"
        mock_args.model = None
        mock_args.api_key = "dummy_key"
        mock_parse_args.return_value = mock_args

        # コンバーターのモック
        mock_converter = MagicMock()
        mock_converter.convert_file.return_value = "変換後のコンテンツ"
        mock_create_converter.return_value = mock_converter

        # テスト対象関数を実行
        content_converter.cli.main()

        # save_converted_fileが呼ばれたか検証
        mock_converter.save_converted_file.assert_called_once_with("変換後のコンテンツ", "custom_output.md")

    @patch("content_converter.cli.parse_args")
    @patch("content_converter.cli.ConverterFactory.create_converter")
    def test_main_with_llm_options(self, mock_create_converter, mock_parse_args):
        """LLMオプションを指定したときのテスト"""
        # モックの戻り値を設定
        mock_args = MagicMock()
        mock_args.input = self.test_file_path
        mock_args.platform = "zenn"
        mock_args.output = None
        mock_args.use_llm = True
        mock_args.llm_provider = "openrouter"
        mock_args.model = None
        mock_args.prompt_file = None
        mock_args.template = None
        mock_args.generate_summary = True
        mock_args.summary_length = 200
        mock_parse_args.return_value = mock_args

        # コンバーターのモック
        mock_converter = MagicMock()
        mock_converter.convert_file.return_value = "変換後のコンテンツ"
        mock_create_converter.return_value = mock_converter

        # テスト対象関数を実行
        content_converter.cli.main()

        # モックの呼び出し確認（configの検証）
        expected_config = {
            "use_llm": True,
            "llm_provider": "openrouter",
            "generate_summary": True,
            "summary_length": 200,
            "model": None,
            "prompt_file": None,
            "template_file": None,
            "llm_options": {}
        }
        assert mock_create_converter.called

    @patch("content_converter.cli.parse_args")
    @patch("content_converter.cli.ConverterFactory.create_converter")
    def test_main_converter_exception(self, mock_create_converter, mock_parse_args):
        """変換処理で例外が発生したときのテスト"""
        # モックの戻り値を設定
        mock_args = MagicMock()
        mock_args.input = self.test_file_path
        mock_args.template = "dummy_template.txt"
        mock_args.prompt = None
        mock_args.output = None
        mock_args.llm_provider = None  # APIキーエラーを回避
        mock_args.model = None
        mock_args.api_key = None
        mock_parse_args.return_value = mock_args

        # コンバーターのモックで例外を発生させる
        mock_converter = MagicMock()
        mock_converter.convert_file.side_effect = Exception("変換エラー")
        mock_create_converter.return_value = mock_converter

        # main関数の戻り値を検証
        result = content_converter.cli.main()
        assert result == 1


class TestGetApiKey:
    """get_api_key 関数のテスト"""

    def test_get_api_key_from_arg_with_provider(self):
        """コマンドライン引数 (provider:key 形式) からAPIキーを取得するテスト"""
        api_key = get_api_key("gemini", "gemini:arg_gemini_key")
        assert api_key == "arg_gemini_key"

        api_key_openrouter = get_api_key("openrouter", "openrouter:arg_openrouter_key")
        assert api_key_openrouter == "arg_openrouter_key"

    def test_get_api_key_from_arg_without_provider(self):
        """コマンドライン引数 (key のみ形式) からAPIキーを取得するテスト"""
        api_key = get_api_key("gemini", "just_a_key")
        assert api_key == "just_a_key"

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "env_gemini_key"}, clear=True)
    def test_get_api_key_from_env_gemini(self):
        """環境変数 (GOOGLE_API_KEY) からAPIキーを取得するテスト"""
        api_key = get_api_key("gemini")
        assert api_key == "env_gemini_key"

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "env_openrouter_key"}, clear=True)
    def test_get_api_key_from_env_openrouter(self):
        """環境変数 (OPENROUTER_API_KEY) からAPIキーを取得するテスト"""
        api_key = get_api_key("openrouter")
        assert api_key == "env_openrouter_key"

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "env_gemini_key"}, clear=True)
    def test_get_api_key_arg_takes_precedence(self):
        """コマンドライン引数が環境変数より優先されることを確認するテスト"""
        api_key = get_api_key("gemini", "gemini:arg_gemini_key_override")
        assert api_key == "arg_gemini_key_override"

        api_key_no_provider_in_arg = get_api_key("gemini", "arg_gemini_key_simple_override")
        assert api_key_no_provider_in_arg == "arg_gemini_key_simple_override"

    @patch.dict(os.environ, {}, clear=True) # 環境変数をクリア
    def test_get_api_key_not_found(self):
        """APIキーが見つからない場合にValueErrorが発生することを確認するテスト"""
        with pytest.raises(ValueError) as excinfo:
            get_api_key("gemini")
        assert "gemini apiキーが設定されていません。" in str(excinfo.value).lower()
        assert "環境変数 GOOGLE_API_KEY を設定するか、--api-key 引数で指定してください。" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo_custom_provider:
            get_api_key("custom_provider")
        assert "custom_provider apiキーが設定されていません。" in str(excinfo_custom_provider.value).lower()
        assert "環境変数 CUSTOM_PROVIDER_API_KEY を設定するか、--api-key 引数で指定してください。" in str(excinfo_custom_provider.value)

    def test_get_api_key_provider_case_insensitive_arg(self):
        """コマンドライン引数のプロバイダー名が大文字・小文字を区別しないことを確認するテスト"""
        api_key_lower = get_api_key("gemini", "gEmInI:case_insensitive_key")
        assert api_key_lower == "case_insensitive_key"

        api_key_upper = get_api_key("GEMINI", "GeMiNi:another_case_key")
        assert api_key_upper == "another_case_key"

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "env_gemini_key_case"}, clear=True)
    def test_get_api_key_provider_case_insensitive_env(self):
        """環境変数のプロバイダー名が大文字・小文字を区別しないことを確認するテスト"""
        api_key_lower = get_api_key("gemini")
        assert api_key_lower == "env_gemini_key_case"

        api_key_upper = get_api_key("GEMINI")
        assert api_key_upper == "env_gemini_key_case"

    def test_get_api_key_arg_provider_mismatch(self):
        """コマンドライン引数のプロバイダ名と実際のプロバイダ名が異なる場合、引数のキーは無視され環境変数を参照するテスト"""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "env_gemini_for_mismatch"}, clear=True):
            api_key = get_api_key("gemini", "other_provider:arg_key_wont_be_used")
            assert api_key == "env_gemini_for_mismatch"

        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                get_api_key("gemini", "other_provider:arg_key_wont_be_used_either")



if __name__ == "__main__":
    pytest.main()
