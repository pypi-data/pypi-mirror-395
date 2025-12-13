"""
LLM module
---------

LLMプロバイダーとプロンプトテンプレートを提供するモジュール
"""

from .base import LLMProvider
from .gemini import GeminiProvider
from .openrouter import OpenRouterProvider
from .prompts import (
    PromptTemplate,
    OptimizeContentTemplate,
    GenerateSummaryTemplate,
    OPTIMIZE_CONTENT_TEMPLATE,
    GENERATE_SUMMARY_TEMPLATE,
)

__all__ = [
    "LLMProvider",
    "GeminiProvider",
    "OpenRouterProvider",
    "PromptTemplate",
    "OptimizeContentTemplate",
    "GenerateSummaryTemplate",
    "OPTIMIZE_CONTENT_TEMPLATE",
    "GENERATE_SUMMARY_TEMPLATE",
]
