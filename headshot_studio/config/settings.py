"""Typed settings loaded from YAML + environment overrides."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "headshot_studio" / "config"


class RenderConfig(BaseModel):
    width: int = 1024
    height: int = 1024
    steps: int = 28
    guidance: float = 5.5
    sampler: str = "dpmpp_2m"
    seed: int = -1


class Settings(BaseModel):
    backend: str = Field(default="onnx", description="onnx | torch | cloud")
    device: str = "cuda"
    models_dir: Path = ROOT / "models" / "weights"
    outputs_dir: Path = ROOT / "outputs"
    render: RenderConfig = RenderConfig()
    style_packs: dict[str, Path] = Field(default_factory=dict)
    cloud_endpoint: str | None = None


def _load_style_packs() -> dict[str, Path]:
    packs_dir = CONFIG_DIR / "style_packs"
    if not packs_dir.exists():
        return {}
    return {p.stem: p for p in packs_dir.glob("*.yaml")}


@lru_cache(maxsize=1)
def load_settings(path: Path | None = None) -> Settings:
    """Load settings from `config/settings.yaml`, with env overrides."""
    cfg_path = path or (CONFIG_DIR / "settings.yaml")
    raw: dict = {}
    if cfg_path.exists():
        raw = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}

    if env_backend := os.getenv("AHS_BACKEND"):
        raw["backend"] = env_backend
    if env_device := os.getenv("AHS_DEVICE"):
        raw["device"] = env_device

    settings = Settings(**raw)
    settings.style_packs = _load_style_packs()
    return settings