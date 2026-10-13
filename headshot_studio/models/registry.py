"""Registry mapping logical model roles to on-disk weights."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelEntry:
    role: str
    filename: str
    sha256: str
    size_mb: int


_BUILTIN: tuple[ModelEntry, ...] = (
    ModelEntry("base", "sdxl_headshot_base.safetensors", "a1b2c3d4", 5120),
    ModelEntry("face_restore", "gfpgan_v14.onnx", "e5f6a7b8", 340),
    ModelEntry("matting", "rmbg_v2.onnx", "c9d0e1f2", 176),
    ModelEntry("upscale", "realesrgan_x2.onnx", "3a4b5c6d", 64),
)


class ModelRegistry:
    """Resolves model roles to files under `models_dir`."""

    def __init__(self, models_dir: Path) -> None:
        self.models_dir = models_dir
        self._entries = {e.role: e for e in _BUILTIN}

    def path_for(self, role: str) -> Path:
        entry = self._entries.get(role)
        if entry is None:
            raise KeyError(f"unknown model role: {role}")
        return self.models_dir / entry.filename

    def missing(self) -> list[str]:
        return [r for r, e in self._entries.items() if not (self.models_dir / e.filename).exists()]