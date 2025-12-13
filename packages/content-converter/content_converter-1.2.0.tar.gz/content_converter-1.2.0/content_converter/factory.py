"""
Factory module
------------

各種コンポーネントのファクトリークラスを提供するモジュール
"""

from typing import Any, Dict, Optional

from .converter import ContentConverter
from .llm.base import LLMProvider
from .llm.gemini import GeminiProvider
from .llm.openrouter import OpenRouterProvider


class LLMProviderFactory:
    """LLMプロバイダーのファクトリークラス"""

    @staticmethod
    def create(provider_type: str, api_key: Optional[str] = None, model: Optional[str] = None) -> LLMProvider:
        """
        LLMプロバイダーを作成する

        Args:
            provider_type: プロバイダータイプ ('gemini', 'openrouter')
            api_key: APIキー
            model: モデル名

        Returns:
            LLMProvider: LLMプロバイダーのインスタンス

        Raises:
            ValueError: サポートされていないプロバイダータイプの場合
        """
        if provider_type == "gemini":
            return GeminiProvider(api_key=api_key, model=model)
        elif provider_type == "openrouter":
            return OpenRouterProvider(api_key=api_key, model=model)
        else:
            raise ValueError(f"Unsupported LLM provider type: {provider_type}")


class ConverterFactory:
    """コンテンツコンバーターのファクトリークラス"""

    @staticmethod
    def create_converter(
        llm_provider: Optional[LLMProvider] = None,
        config: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
    ) -> ContentConverter:
        """
        コンテンツコンバーターを作成する

        Args:
            llm_provider: LLMプロバイダー（省略可能）
            config: コンバーター設定
            model: モデル名

        Returns:
            ContentConverter: コンテンツコンバーターのインスタンス
        """
        return ContentConverter(
            llm_provider=llm_provider, config=config or {}, model=model
        )
