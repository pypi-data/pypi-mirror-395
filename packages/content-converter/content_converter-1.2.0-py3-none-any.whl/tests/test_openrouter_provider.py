"""
OpenRouter Provider Tests
----------------------

OpenRouter APIを使用したLLMプロバイダーのテスト
"""

import os
import pytest
from unittest.mock import Mock, patch

from content_converter.llm import OpenRouterProvider


class TestOpenRouterProvider:
    """OpenRouterProviderのテスト"""

    @pytest.fixture
    def mock_requests(self):
        """requestsのモック"""
        with patch("content_converter.llm.openrouter.requests") as mock:
            mock_response = Mock()
            mock_response.json.return_value = {
                "choices": [{"message": {"content": "test response"}}]
            }
            mock.post.return_value = mock_response
            yield mock

    @pytest.fixture
    def provider(self, mock_requests):
        """OpenRouterProviderのインスタンス"""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_key"}):
            return OpenRouterProvider()

    def test_init_with_env_var(self, mock_requests):
        """環境変数からAPIキーを取得するテスト"""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_key"}):
            provider = OpenRouterProvider()
            assert provider.api_key == "test_key"
            assert provider.headers["Authorization"] == "Bearer test_key"

    def test_init_with_api_key(self, mock_requests):
        """APIキーを直接指定するテスト"""
        provider = OpenRouterProvider(api_key="direct_key")
        assert provider.api_key == "direct_key"
        assert provider.headers["Authorization"] == "Bearer direct_key"

    def test_init_without_api_key(self):
        """APIキーが設定されていない場合のテスト"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OpenRouter APIキーが設定されていません"):
                OpenRouterProvider()

    def test_init_with_custom_model(self, mock_requests):
        """カスタムモデルを指定するテスト"""
        provider = OpenRouterProvider(api_key="test_key", model="custom/model")
        assert provider.model == "custom/model"

    def test_optimize_content(self, provider, mock_requests):
        """optimize_contentのテスト"""
        result = provider.optimize_content("test content")
        assert result == "test response"
        mock_requests.post.assert_called_once()

    def test_optimize_content_with_options(self, provider, mock_requests):
        """optimize_contentのオプション指定テスト"""
        options = {"temperature": 0.5, "max_tokens": 1024}
        result = provider.optimize_content("test content", options)
        assert result == "test response"
        mock_requests.post.assert_called_once()

    def test_generate_summary(self, provider, mock_requests):
        """generate_summaryのテスト"""
        result = provider.generate_summary("test content", max_length=50)
        assert result == "test response"
        mock_requests.post.assert_called_once()

    def test_api_error_handling(self, provider, mock_requests):
        """APIエラーのハンドリングテスト"""
        mock_requests.post.side_effect = Exception("API Error")
        with pytest.raises(Exception, match="API Error"):
            provider.optimize_content("test content")

    def test_headers(self, provider):
        """ヘッダーの設定テスト"""
        expected_headers = {
            "Authorization": "Bearer test_key",
            "HTTP-Referer": "https://github.com/centervil/Content-Converter",
            "X-Title": "Content Converter",
        }
        assert provider.headers == expected_headers 