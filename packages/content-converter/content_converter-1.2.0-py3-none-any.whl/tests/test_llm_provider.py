"""
LLM Provider Tests
----------------

LLMプロバイダーのテスト
"""

import pytest
from unittest.mock import Mock, patch

from content_converter.llm import LLMProvider


class TestLLMProvider:
    """LLMProviderのテスト"""

    def test_optimize_content_abstract(self):
        """optimize_contentが抽象メソッドであることを確認"""
        with pytest.raises(TypeError):
            LLMProvider().optimize_content("test content")

    def test_generate_summary_abstract(self):
        """generate_summaryが抽象メソッドであることを確認"""
        with pytest.raises(TypeError):
            LLMProvider().generate_summary("test content")

    def test_optimize_content_options_default(self):
        """optimize_contentのデフォルトオプションを確認"""
        mock_provider = Mock(spec=LLMProvider)
        mock_provider.optimize_content.return_value = "optimized content"

        result = mock_provider.optimize_content("test content")
        mock_provider.optimize_content.assert_called_once_with("test content")
        assert result == "optimized content"

    def test_generate_summary_max_length_default(self):
        """generate_summaryのデフォルトmax_lengthを確認"""
        mock_provider = Mock(spec=LLMProvider)
        mock_provider.generate_summary.return_value = "summary"

        result = mock_provider.generate_summary("test content")
        mock_provider.generate_summary.assert_called_once_with("test content")
        assert result == "summary" 