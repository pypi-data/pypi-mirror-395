"""
Tests for the ContentConverter class.
"""
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from content_converter.converter import ContentConverter


class TestContentConverter:
    """Test suite for ContentConverter class."""

    @pytest.fixture
    def mock_llm_provider(self):
        """Create a mock LLM provider."""
        llm = MagicMock()
        llm.optimize_content.return_value = "optimized content"
        llm.generate_summary.return_value = "test summary"
        return llm

    @pytest.fixture
    def test_data_dir(self):
        """Return the path to the test data directory."""
        return os.path.join(os.path.dirname(__file__), "fixtures")

    def test_convert_file_with_template(self, mock_llm_provider, test_data_dir, tmp_path):
        """Test convert_file with a template file."""
        # Arrange
        template_file = os.path.join(test_data_dir, "templates", "test_template.md")
        input_file = tmp_path / "test_input.md"
        input_text = "# Test\n\nThis is a test document."
        input_file.write_text(input_text)
        
        converter = ContentConverter(llm_provider=mock_llm_provider,
            config={
                "use_llm": False,
                "template_file": template_file,
            }
        )
        
        # Act
        result = converter.convert_file(str(input_file), template_file)
        
        # Assert
        expected_output = (
            "# {{title}}\n\n"
            "## 概要\n{{summary}}\n\n"
            "## 詳細\n" + input_text + "\n"
        )
        assert result == expected_output

    def test_convert_file_with_prompt_and_template(self, mock_llm_provider, test_data_dir, tmp_path):
        """Test convert_file with both prompt and template files."""
        # Arrange
        template_file = os.path.join(test_data_dir, "templates", "test_template.md")
        prompt_file = os.path.join(test_data_dir, "prompts", "test_prompt.txt")
        input_file = tmp_path / "test_input.md"
        input_file.write_text("# Test\n\nThis is a test document.")
        
        converter = ContentConverter(llm_provider=mock_llm_provider,
            config={
                "use_llm": True,
                "template_file": template_file,
                "prompt_file": prompt_file,
            }
        )
        
        # Act
        result = converter.convert_file(str(input_file), template_file, prompt_file)
        
        # Assert
        mock_llm_provider.optimize_content.assert_called_once()
        
        # Check if the prompt and template were used in the LLM call
        prompt_text = mock_llm_provider.optimize_content.call_args[0][0]
        assert "以下の入力文を指定されたテンプレートに基づいて整形してください" in prompt_text
        assert "# {{title}}\n\n## 概要\n{{summary}}\n\n## 詳細\n{{content}}" in prompt_text
        
        # Check if the optimized content is in the result
        assert result == "optimized content"

    def test_convert_file_with_invalid_template(self, mock_llm_provider, tmp_path):
        """テンプレートファイルが存在しない場合はFileNotFoundErrorになることを確認"""
        # Arrange
        input_file = tmp_path / "test_input.md"
        input_file.write_text("# Test\n\nThis is a test document.")
        
        converter = ContentConverter(llm_provider=mock_llm_provider,
            config={
                "use_llm": False,
                "template_file": "/path/to/nonexistent/template.md",
            }
        )
        
        # Act & Assert
        with pytest.raises(FileNotFoundError):
            converter.convert_file(str(input_file), "/path/to/nonexistent/template.md")
            
    def test_convert_file_with_custom_model(self, mock_llm_provider, tmp_path):
        """Test convert_file with a custom model specified."""
        # Arrange
        input_file = tmp_path / "test_input.md"
        input_file.write_text("# Test\n\nThis is a test document.")
        
        # Configure the mock LLM provider to return a specific response
        mock_llm_provider.optimize_content.return_value = "optimized with custom model"
        
        converter = ContentConverter(llm_provider=mock_llm_provider,
            config={
                "use_llm": True,
                "model": "custom-model-1.0",
                "llm_options": {
                    "model": "custom-model-1.0"
                }
            }
        )
        
        # Act
        template_file = os.path.join(os.path.dirname(__file__), "fixtures", "templates", "test_template.md")
        result = converter.convert_file(str(input_file), template_file)
        
        # Assert
        mock_llm_provider.optimize_content.assert_called_once()
        # 最低限、mockの戻り値が返ることのみ検証
        assert result == "optimized with custom model"
        
    def test_save_converted_file_success(self, mock_llm_provider, tmp_path):
        """Test successful save of converted content to a file."""
        # Arrange
        converter = ContentConverter(llm_provider=mock_llm_provider)
        output_file = tmp_path / "output.md"
        content = {
            "content": "Test content",
            "metadata": {"title": "Test Title", "tags": ["test", "example"]}
        }
        
        # Act
        converter.save_converted_file(content["content"], str(output_file))
        
        # Assert
        assert output_file.exists()
        with open(output_file, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        assert "Test content" in saved_content

    def test_save_converted_file_invalid_path(self, mock_llm_provider):
        """Test save with invalid output path raises IOError."""
        # Arrange
        converter = ContentConverter(llm_provider=mock_llm_provider)
        content = {
            "content": "Test content",
            "metadata": {"title": "Test"}
        }
        
        # Act & Assert
        with pytest.raises(IOError):
            converter.save_converted_file(content, "/invalid/path/output.md")
    
