"""
Gemini Provider Tests
------------------

Google Gemini APIを使用したLLMプロバイダーのテスト
"""

import os
import pytest
from unittest.mock import Mock, patch

import google.generativeai as genai
from content_converter.llm import GeminiProvider


class TestGeminiProvider:
    """GeminiProviderのテスト"""

    @pytest.fixture
    def mock_genai(self):
        """google.generativeaiのモック"""
        with patch("content_converter.llm.gemini.genai") as mock:
            mock.GenerativeModel.return_value = Mock()
            yield mock

    @pytest.fixture
    def provider(self, mock_genai):
        """GeminiProviderのインスタンス"""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"}):
            return GeminiProvider()

    def test_init_with_env_var(self, mock_genai):
        """環境変数からAPIキーを取得するテスト"""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"}):
            provider = GeminiProvider()
            assert provider.api_key == "test_key"
            mock_genai.configure.assert_called_once_with(api_key="test_key")

    def test_init_with_model(self, mock_genai):
        """モデル指定のテスト"""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"}):
            provider = GeminiProvider(model="gemini-2.0-flash-001")
            assert provider.model_name == "gemini-2.0-flash-001"
            mock_genai.GenerativeModel.assert_called_once_with("gemini-2.0-flash-001")

    def test_init_with_api_key(self, mock_genai):
        """APIキーを直接指定するテスト"""
        provider = GeminiProvider(api_key="direct_key")
        assert provider.api_key == "direct_key"
        mock_genai.configure.assert_called_once_with(api_key="direct_key")

    def test_init_without_api_key(self):
        """APIキーが設定されていない場合のテスト"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Gemini APIキーが設定されていません"):
                GeminiProvider()

    def test_optimize_content(self, provider, mock_genai):
        """optimize_contentのテスト"""
        mock_response = Mock()
        mock_response.text = "optimized content"
        provider.model.generate_content.return_value = mock_response

        result = provider.optimize_content("test content")
        assert result == "optimized content"
        provider.model.generate_content.assert_called_once()
        args, kwargs = provider.model.generate_content.call_args
        generation_config = kwargs["generation_config"]
        generation_config.configure_mock(
            temperature=0.7,
            max_output_tokens=2048,
            top_p=None,
            top_k=None
        )

    def test_optimize_content_with_options(self, provider, mock_genai):
        """optimize_contentのオプション指定テスト"""
        mock_response = Mock()
        mock_response.text = "optimized content"
        provider.model.generate_content.return_value = mock_response

        options = {"temperature": 0.5, "max_tokens": 1024}
        result = provider.optimize_content("test content", options)
        assert result == "optimized content"
        provider.model.generate_content.assert_called_once()
        args, kwargs = provider.model.generate_content.call_args
        generation_config = kwargs["generation_config"]
        generation_config.configure_mock(
            temperature=0.5,
            max_output_tokens=1024,
            top_p=None,
            top_k=None
        )

    def test_generate_summary(self, provider, mock_genai):
        """generate_summaryのテスト"""
        mock_response = Mock()
        mock_response.text = "summary"
        provider.model.generate_content.return_value = mock_response

        result = provider.generate_summary("test content", max_length=50)
        assert result == "summary"
        provider.model.generate_content.assert_called_once()

    def test_safety_settings(self, provider):
        """セーフティ設定のテスト"""
        from google.generativeai.types import HarmCategory, HarmBlockThreshold

        expected_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
        assert provider.safety_settings == expected_settings 