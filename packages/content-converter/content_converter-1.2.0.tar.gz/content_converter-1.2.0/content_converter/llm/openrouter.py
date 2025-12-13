"""
OpenRouter Provider module
------------------------

OpenRouter APIを使用したLLMプロバイダーの実装
"""

import os
from typing import Any, Dict, Optional

import requests

from .base import LLMProvider


class OpenRouterProvider(LLMProvider):
    """OpenRouter APIを使用したLLMプロバイダー"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        OpenRouterProviderの初期化

        Args:
            api_key: OpenRouter APIキー。指定がない場合は環境変数OPENROUTER_API_KEYから取得
            model: 使用するモデル名（デフォルト: anthropic/claude-3-opus-20240229）
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter APIキーが設定されていません。環境変数OPENROUTER_API_KEYを設定するか、api_key引数を指定してください。")

        self.model = model or "anthropic/claude-3-opus-20240229"
        self.api_base = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/centervil/Content-Converter",
            "X-Title": "Content Converter",
        }

    def optimize_content(
        self, content: str, options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        コンテンツをOpenRouterを使用して最適化する

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
        model = options.get("model") or self.model
        temperature = options.get("temperature", 0.7)
        max_tokens = options.get("max_tokens", 2048)

        prompt = f"""
        以下のコンテンツを最適化してください。文章の流れを改善し、読みやすさを向上させてください。
        ただし、元の内容や意図は保持してください。

        コンテンツ:
        {content}
        """

        response = requests.post(
            f"{self.api_base}/chat/completions",
            headers=self.headers,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    def generate_summary(self, content: str, max_length: int = 100) -> str:
        """
        コンテンツの要約をOpenRouterを使用して生成する

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

        response = requests.post(
            f"{self.api_base}/chat/completions",
            headers=self.headers,
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 100,
            },
        )
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"] 