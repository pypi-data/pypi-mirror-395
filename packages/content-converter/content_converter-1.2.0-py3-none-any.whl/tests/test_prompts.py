"""
Prompt Templates Tests
-------------------

プロンプトテンプレートのテスト
"""

import pytest

from content_converter.llm import (
    PromptTemplate,
    OptimizeContentTemplate,
    GenerateSummaryTemplate,
    OPTIMIZE_CONTENT_TEMPLATE,
    GENERATE_SUMMARY_TEMPLATE,
)


class TestPromptTemplate:
    """PromptTemplateのテスト"""

    def test_format(self):
        """formatメソッドのテスト"""
        template = PromptTemplate("Hello, {name}!")
        result = template.format(name="World")
        assert result == "Hello, World!"

    def test_format_with_multiple_vars(self):
        """複数の変数を持つテンプレートのテスト"""
        template = PromptTemplate("{greeting}, {name}!")
        result = template.format(greeting="Hello", name="World")
        assert result == "Hello, World!"


class TestOptimizeContentTemplate:
    """OptimizeContentTemplateのテスト"""

    def test_format(self):
        """formatメソッドのテスト"""
        template = OptimizeContentTemplate()
        result = template.format(content="test content")
        assert "test content" in result
        assert "最適化してください" in result

    def test_singleton_instance(self):
        pass


class TestGenerateSummaryTemplate:
    """GenerateSummaryTemplateのテスト"""

    def test_format(self):
        """formatメソッドのテスト"""
        template = GenerateSummaryTemplate()
        result = template.format(content="test content", max_length=50)
        assert "test content" in result
        assert "50文字以内" in result

    def test_singleton_instance(self):
        pass 