# content_converter/converter.py
"""
Converter module
--------------

コンテンツ変換の中核機能を提供するモジュール
"""

from typing import Any, Dict, Optional

from .llm.base import LLMProvider


class ContentConverter:
    """コンテンツ変換を行うメインクラス"""

    def save_converted_file(self, text: str, output_path: str) -> None:
        """
        変換結果を指定ファイルに保存する
        Args:
            text: 保存するテキスト
            output_path: 出力ファイルパス
        """
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

    def __init__(
        self,
        llm_provider: LLMProvider,
        config: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
    ):
        """
        初期化メソッド

        Args:
            llm_provider: LLMプロバイダー
            config: コンバーター設定
        """
        self.llm_provider = llm_provider
        self.config = config or {}
        self.model = model

    def convert(
        self,
        input_text: str,
        template: str,
        prompt: Optional[str] = None,
    ) -> str:
        """
        コンテンツを変換する

        Args:
            input_text: 入力テキスト
            template: テンプレートテキスト
            prompt: カスタムプロンプト（省略可）

        Returns:
            str: 変換されたテキスト
        """
        use_llm = self.config.get("use_llm", True)
        if not use_llm:
            # テンプレートの{{content}}または{{input}}にinput_textを埋め込むだけ
            # どちらもなければinput_textをそのまま返す
            if "{{content}}" in template:
                return template.replace("{{content}}", input_text)
            elif "{{input}}" in template:
                return template.replace("{{input}}", input_text)
            else:
                return input_text
        # LLM使用時
        default_prompt = """
        以下の入力テキストを指定されたテンプレートの形式に変換してください。

        # 入力テキスト
        {{input}}

        # 使用するテンプレート
        {{template}}

        # 出力要件
        - テンプレート内のプレースホルダーを適切に置き換えてください
        - フォーマットを維持してください
        - 構造を保持してください
        """
        final_prompt = (prompt or default_prompt).replace(
            "{{input}}", input_text
        ).replace(
            "{{template}}", template
        )
        options = {}
        if self.model:
            options["model"] = self.model
        return self.llm_provider.optimize_content(final_prompt, options=options)

    def convert_file(
        self,
        input_path: str,
        template_path: str,
        prompt_path: Optional[str] = None,
    ) -> str:
        """
        ファイルからコンテンツを読み込んで変換する

        Args:
            input_path: 入力ファイルのパス
            template_path: テンプレートファイルのパス
            prompt_path: プロンプトファイルのパス（省略可）

        Returns:
            str: 変換されたテキスト
        """
        # ファイルの読み込み
        with open(input_path, "r", encoding="utf-8") as f:
            input_text = f.read()

        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        prompt = None
        if prompt_path:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()

        # 変換を実行
        return self.convert(input_text, template, prompt)
