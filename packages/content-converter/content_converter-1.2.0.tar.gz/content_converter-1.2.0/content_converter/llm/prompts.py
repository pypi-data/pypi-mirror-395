"""
Prompt Templates module
---------------------

LLMプロバイダーで使用するプロンプトテンプレートを管理するモジュール
"""

from typing import Dict, Any


class PromptTemplate:
    """プロンプトテンプレートの基底クラス"""

    def __init__(self, template: str):
        """
        プロンプトテンプレートの初期化

        Args:
            template: プロンプトテンプレート文字列
        """
        self.template = template

    def format(self, **kwargs: Any) -> str:
        """
        テンプレートに値を埋め込む

        Args:
            **kwargs: テンプレートに埋め込む値

        Returns:
            str: フォーマットされたプロンプト
        """
        return self.template.format(**kwargs)


class OptimizeContentTemplate(PromptTemplate):
    """コンテンツ最適化用のプロンプトテンプレート"""

    def __init__(self):
        super().__init__("""
        以下のコンテンツを最適化してください。文章の流れを改善し、読みやすさを向上させてください。
        ただし、元の内容や意図は保持してください。

        コンテンツ:
        {content}
        """)


class GenerateSummaryTemplate(PromptTemplate):
    """要約生成用のプロンプトテンプレート"""

    def __init__(self):
        super().__init__("""
        以下のコンテンツを{max_length}文字以内で要約してください。
        重要なポイントを簡潔にまとめてください。

        コンテンツ:
        {content}
        """)


# プロンプトテンプレートのインスタンス
OPTIMIZE_CONTENT_TEMPLATE = OptimizeContentTemplate()
GENERATE_SUMMARY_TEMPLATE = GenerateSummaryTemplate() 