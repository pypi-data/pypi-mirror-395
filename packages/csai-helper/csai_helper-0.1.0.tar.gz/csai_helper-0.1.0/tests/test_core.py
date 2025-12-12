from ai_helper import format_response, get_response, summarize_text
from ai_helper.providers.local import LocalProvider


class DummyProvider(LocalProvider):
    def __init__(self):
        super().__init__(prefix="")
        self.seen_prompts = []

    def get_response(self, prompt: str, *, system_prompt=None, **kwargs) -> str:  # type: ignore[override]
        if system_prompt:
            self.seen_prompts.append(system_prompt)
        self.seen_prompts.append(prompt)
        return "dummy response"


def test_get_response_uses_provider_and_formats():
    provider = DummyProvider()
    result = get_response("hello", provider=provider, system_prompt="system")
    assert result == "dummy response"
    assert provider.seen_prompts == ["system", "hello"]


def test_summarize_text_limits_words():
    provider = LocalProvider(prefix="")
    text = "Python is great. It is used widely for data science and automation."
    summary = summarize_text(text, provider=provider, max_words=5)
    assert len(summary.split()) <= 5


def test_format_response_collapses_whitespace():
    messy = "  Hello\n\n\nWorld  \t nice  "
    assert format_response(messy) == "Hello\nWorld nice"
