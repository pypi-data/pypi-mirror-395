"""
Gemini Provider module
--------------------

Google Gemini APIを使用したLLMプロバイダーの実装
"""

import os
from typing import Any, Dict, Optional

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from .base import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini APIを使用したLLMプロバイダー"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        GeminiProviderの初期化

        Args:
            api_key: Gemini APIキー。指定がない場合は環境変数GOOGLE_API_KEYから取得
            model: 使用するモデル名（デフォルト: gemini-2.0-flash-001）
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini APIキーが設定されていません。環境変数 GOOGLE_API_KEY を設定するか、--api-key 引数で指定してください。詳細は [Gemini API ドキュメント](https://ai.google.dev/docs/api_key) を参照してください。")

        genai.configure(api_key=self.api_key)
        self.model_name = model or 'gemini-2.0-flash-001'
        self.model = genai.GenerativeModel(self.model_name)
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

    def optimize_content(
        self, content: str, options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        コンテンツをGeminiを使用して最適化する

        Args:
            content: 最適化するコンテンツテキスト
            options: 最適化オプション
                - model: 使用するモデル名
                - temperature: 生成の多様性（0.0-1.0）
                - max_tokens: 生成する最大トークン数

        Returns:
            str: 最適化されたコンテンツ
        """
        options = options or {}
        model_name = options.get("model") or self.model_name
        temperature = options.get("temperature", 0.7)
        max_tokens = options.get("max_tokens", 2048)

        # モデルが変更された場合は新しいモデルをロード
        if model_name != self.model_name:
            self.model_name = model_name
            self.model = genai.GenerativeModel(self.model_name)

        prompt = f"""
        以下のコンテンツを最適化してください。文章の流れを改善し、読みやすさを向上させてください。
        ただし、元の内容や意図は保持してください。

        コンテンツ:
        {content}
        """

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
            safety_settings=self.safety_settings,
        )

        return response.text

    def generate_summary(self, content: str, max_length: int = 100) -> str:
        """
        コンテンツの要約をGeminiを使用して生成する

        Args:
            content: 要約するコンテンツテキスト
            max_length: 要約の最大文字数

        Returns:
            str: 生成された要約
        """
        prompt = f"""
        以下のコンテンツを{max_length}文字以内で要約してください。
        重要なポイントを簡潔にまとめてください。

        コンテンツ:
        {content}
        """

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=100,
            ),
            safety_settings=self.safety_settings,
        )

        return response.text 