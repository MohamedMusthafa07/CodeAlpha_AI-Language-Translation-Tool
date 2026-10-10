"""Smoke tests: no API key or internet needed (Gemini is faked)."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


class _FakeResponse:
    text = '{"detected_language": "English", "translation": "Hola, mundo"}'


class _FakeClient:
    def __init__(self, *args, **kwargs):
        self.models = self

    def generate_content(self, **kwargs):
        return _FakeResponse()


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "GEMINI_MODEL"):
        monkeypatch.delenv(name, raising=False)


def test_app_loads_without_errors():
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception


def test_translate_without_key_shows_friendly_warning():
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.text_area(key="input_text").set_value("Hello world").run()
    at.button[1].click().run()  # index 0 is the swap button
    assert not at.exception
    assert any("API key" in w.value for w in at.warning)


def test_full_translation_flow(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    monkeypatch.setattr("google.genai.Client", _FakeClient)
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.text_area(key="input_text").set_value("Hello, world").run()
    at.button[1].click().run()
    assert not at.exception
    assert at.session_state["result"]["out"] == "Hola, mundo"
    assert at.session_state["result"]["detected_name"] == "English"
