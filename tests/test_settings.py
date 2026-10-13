"""Smoke tests for the settings loader."""
from pathlib import Path

from headshot_studio.config.settings import Settings, load_settings


def test_defaults() -> None:
    s = Settings()
    assert s.backend in {"onnx", "torch", "cloud"}
    assert s.render.width == 1024


def test_style_packs_discovered() -> None:
    load_settings.cache_clear()
    s = load_settings()
    assert "corporate_neutral" in s.style_packs
    assert s.style_packs["corporate_neutral"].suffix == ".yaml"


def test_env_override(monkeypatch) -> None:
    monkeypatch.setenv("AHS_BACKEND", "torch")
    load_settings.cache_clear()
    assert load_settings().backend == "torch"