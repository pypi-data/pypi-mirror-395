"""
パーサーモジュールのテスト
"""

import os
import tempfile

import pytest

from content_converter.core.parser import MarkdownParser


class TestMarkdownParser:
    """MarkdownParserクラスのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.parser = MarkdownParser()

        # テスト用の一時ファイルを作成
        self.temp_dir = tempfile.TemporaryDirectory()
        test_file = "test_markdown.md"
        self.test_file_path = os.path.join(self.temp_dir.name, test_file)

        # テスト用のマークダウンコンテンツ
        test_content = """---
title: テスト記事
description: これはテスト用の記事です
tags:
  - テスト
  - マークダウン
---

# テスト記事

これはテスト用のマークダウンコンテンツです。

## セクション1

テストテキスト1

## セクション2

テストテキスト2
"""

        # ファイルに書き込み
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            f.write(test_content)

    def teardown_method(self):
        """テスト後のクリーンアップ"""
        # 一時ディレクトリを削除
        self.temp_dir.cleanup()

    def test_parse_file_valid(self):
        """有効なマークダウンファイルの解析テスト"""
        result = self.parser.parse_file(self.test_file_path)

        # 結果の検証
        assert isinstance(result, dict)
        assert "metadata" in result
        assert "content" in result

        # メタデータの検証
        metadata = result["metadata"]
        assert metadata["title"] == "テスト記事"
        assert metadata["description"] == "これはテスト用の記事です"
        assert "tags" in metadata
        assert len(metadata["tags"]) == 2
        assert "テスト" in metadata["tags"]
        assert "マークダウン" in metadata["tags"]

        # コンテンツの検証
        content = result["content"]
        assert "# テスト記事" in content
        assert "## セクション1" in content
        assert "## セクション2" in content

    def test_parse_file_not_found(self):
        """存在しないファイルのテスト"""
        with pytest.raises(FileNotFoundError):
            self.parser.parse_file("存在しないファイル.md")

    def test_parse_file_invalid_format(self):
        """無効なフォーマットのファイルテスト"""
        # 無効なフォーマットのファイルを作成
        invalid_file_path = os.path.join(self.temp_dir.name, "invalid.md")
        with open(invalid_file_path, "w", encoding="utf-8") as f:
            f.write("---\ninvalid: yaml: format:\n---\nContent")

        # 解析を試みる（フロントマターが不正でもコンテンツは解析できる）
        result = self.parser.parse_file(invalid_file_path)
        assert "content" in result
