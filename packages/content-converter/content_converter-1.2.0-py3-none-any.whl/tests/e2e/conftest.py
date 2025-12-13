import pytest
from unittest.mock import patch

class DummyLLMProvider:
    def __init__(self, *args, **kwargs):
        pass
    def generate(self, prompt, **kwargs):
        # prompt内容をそのまま返す（テスト用）
        return prompt

@pytest.fixture(autouse=True)
def patch_llm_provider_factory(monkeypatch):
    from content_converter import factory
    monkeypatch.setattr(factory.LLMProviderFactory, "create", lambda *a, **kw: DummyLLMProvider())
