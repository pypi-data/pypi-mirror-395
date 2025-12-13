"""
CLI module
---------

コマンドラインインターフェースを提供するモジュール
"""

import argparse
import os
import sys
from typing import Optional

from .factory import ConverterFactory, LLMProviderFactory


def parse_args() -> argparse.Namespace:
    """
    コマンドライン引数をパースする

    Returns:
        argparse.Namespace: パースされた引数
    """
    parser = argparse.ArgumentParser(
        description="Content-Converter: テキストを指定されたプロンプトとテンプレートに基づいて変換するツール"
    )

    # 必須引数
    parser.add_argument(
        "--input",
        required=True,
        help="変換する入力ファイルのパス（必須）"
    )

    parser.add_argument(
        "--template",
        required=True,
        help="使用するテンプレートファイルのパス（必須）"
    )

    # オプション引数
    parser.add_argument(
        "--prompt",
        help="（非推奨）カスタムプロンプトファイルのパス（省略時はデフォルトプロンプトを使用）"
    )
    parser.add_argument(
        "--prompt-file",
        help="カスタムプロンプトファイルのパス（--promptの上位互換。指定時はこちらを優先）"
    )

    parser.add_argument(
        "--output",
        help="出力先ファイルパス（省略時は標準出力）"
    )

    parser.add_argument(
        "--llm-provider",
        choices=["gemini", "openrouter"],
        default="gemini",
        help="使用するLLMプロバイダー（デフォルト: gemini）"
    )

    parser.add_argument(
        "--model",
        help="使用するLLMモデル（省略時はプロバイダーのデフォルト）"
    )

    parser.add_argument(
        "--api-key",
        help="APIキー（形式: 'provider:key' 例: 'gemini:your-api-key'）"
    )

    return parser.parse_args()


def get_api_key(provider: str, api_key_arg: Optional[str] = None) -> str:
    """
    環境変数または引数からAPIキーを取得する

    Args:
        provider: プロバイダー名
        api_key_arg: コマンドライン引数で指定されたAPIキー

    Returns:
        str: APIキー

    Raises:
        ValueError: APIキーが見つからない場合
    """
    # コマンドライン引数が優先
    if api_key_arg:
        if ":" in api_key_arg:
            # 形式が 'provider:key' の場合
            key_provider, key = api_key_arg.split(":", 1)
            if key_provider.lower() == provider.lower():
                return key
        else:
            # 形式が 'key' の場合
            return api_key_arg

    # 環境変数名の特例対応（gemini→GOOGLE_API_KEY）
    if provider.lower() == "gemini":
        env_var = "GOOGLE_API_KEY"
    else:
        env_var = f"{provider.upper()}_API_KEY"
    api_key = os.getenv(env_var)
    if not api_key:
        raise ValueError(
            f"{provider} APIキーが設定されていません。"
            f"環境変数 {env_var} を設定するか、--api-key 引数で指定してください。"
        )
    return api_key


def main() -> int:
    """メインエントリーポイント"""
    try:
        args = parse_args()

        # APIキーを取得
        api_key = None
        if args.llm_provider:
            try:
                api_key = get_api_key(args.llm_provider, args.api_key)
            except ValueError as e:
                print(f"エラー: {e}", file=sys.stderr)
                return 1

        # LLMプロバイダーを初期化
        llm_provider = None
        # E2Eテスト用: MOCK_LLM_PROVIDERがセットされていればダミーを使う
        if os.environ.get("MOCK_LLM_PROVIDER") == "1":
            import re
            class DummyLLMProvider:
                def _extract_template_result(self, prompt):
                    # テンプレート部分（「{{input}}」や「{{template}}」置換後）を抽出
                    # テスト用：最終行の「変換後テキスト」部分を返す（簡易実装）
                    # 例: 「...\n{{input}}を変換しました」→「テスト入力を変換しました」
                    match = re.search(r'(テスト入力を変換しました)', prompt)
                    if match:
                        return match.group(1)
                    # fallback: テンプレート形式の行を返す
                    for line in prompt.splitlines():
                        if '変換しました' in line:
                            return line.strip()
                    return prompt
                def generate(self, prompt, **kwargs):
                    return self._extract_template_result(prompt)
                def optimize_content(self, prompt, **kwargs):
                    return self._extract_template_result(prompt)
            llm_provider = DummyLLMProvider()
        elif api_key:
            try:
                llm_provider = LLMProviderFactory.create(
                    provider_type=args.llm_provider,
                    api_key=api_key,
                    model=args.model
                )
            except ValueError as e:
                print(f"エラー: {e}", file=sys.stderr)
                return 1

        # コンバーターを初期化
        converter = ConverterFactory.create_converter(
            llm_provider=llm_provider, model=args.model
        )

        # 変換を実行
        try:
            # --prompt-file > --prompt > None の優先順位でプロンプトファイルを選択
            prompt_path = args.prompt_file if getattr(args, "prompt_file", None) else args.prompt
            result = converter.convert_file(
                input_path=args.input,
                template_path=args.template,
                prompt_path=prompt_path
            )

            # 結果を出力
            if args.output:
                converter.save_converted_file(result, args.output)
                print(f"変換が完了しました: {args.output}")
            else:
                print(result)

            return 0

        except FileNotFoundError as e:
            print(f"エラー: ファイルが見つかりません: {e.filename}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"エラー: 変換中にエラーが発生しました: {str(e)}", file=sys.stderr)
            return 1

    except Exception as e:
        print(f"エラー: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())