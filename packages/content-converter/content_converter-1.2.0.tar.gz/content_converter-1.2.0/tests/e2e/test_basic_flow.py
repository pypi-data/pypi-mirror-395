import subprocess
import tempfile
import os

import pytest

def test_basic_conversion_flow():
    """
    入力ファイル・テンプレート・プロンプトを指定してCLIを実行し、
    想定通りの出力ファイルが生成されることを検証するE2Eテスト
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # テスト用入力ファイル・テンプレート・プロンプトを準備
        input_path = os.path.join(tmpdir, "input.md")
        template_path = os.path.join(tmpdir, "template.md")
        prompt_path = os.path.join(tmpdir, "prompt.txt")
        output_path = os.path.join(tmpdir, "output.md")

        with open(input_path, "w", encoding="utf-8") as f:
            f.write("テスト入力")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write("{{input}}を変換しました")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write("{{input}}を変換しました")

        # APIキーのダミー設定（必要なら）
        os.environ["GOOGLE_API_KEY"] = "dummy-key"

        # CLIコマンド実行
        cmd = [
            "python", "-m", "content_converter.cli",
            "--input", input_path,
            "--template", template_path,
            "--prompt-file", prompt_path,
            "--output", output_path,
            "--model", "gemini-2.0-flash-001"
        ]
        env = os.environ.copy()
        env["MOCK_LLM_PROVIDER"] = "1"
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)

        # 正常終了を期待
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        # 出力ファイルの内容検証
        assert os.path.exists(output_path), "出力ファイルが生成されていません"
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
        # 仮の期待値（現状は失敗するはず）
        assert "テスト入力を変換しました" in content
