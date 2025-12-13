"""
LLM Base module
--------------

LLM連携の基底クラスを提供するモジュール
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class LLMProvider(ABC):
    """LLMプロバイダーの基底クラス"""

    @abstractmethod
    def optimize_content(
        self, content: str, options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        コンテンツをLLMを使用して最適化する

        Args:
            content: 最適化するコンテンツテキスト
            options: 最適化オプション（プロバイダーごとに異なる可能性あり）

        Returns:
            str: 最適化されたコンテンツ
        """
        pass

    @abstractmethod
    def generate_summary(self, content: str, max_length: int = 100) -> str:
        """
        コンテンツの要約を生成する

        Args:
            content: 要約するコンテンツテキスト
            max_length: 要約の最大文字数

        Returns:
            str: 生成された要約
        """
        pass
