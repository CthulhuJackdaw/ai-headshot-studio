"""Individual pipeline stages."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from headshot_studio.models.backends import Backend


class Stage:
    name = "stage"

    def apply(self, image: np.ndarray, *, pack: Path, index: int) -> np.ndarray:
        raise NotImplementedError


@dataclass
class RenderStage(Stage):
    name = "render"
    backend: Backend
    render_cfg: object

    def apply(self, image: np.ndarray, *, pack: Path, index: int) -> np.ndarray:
        seed = self.render_cfg.seed if self.render_cfg.seed >= 0 else index
        return self.backend.render(
            prompt=str(pack), negative="", seed=seed, steps=self.render_cfg.steps
        )


@dataclass
class FaceRestoreStage(Stage):
    name = "face_restore"
    backend: Backend

    def apply(self, image: np.ndarray, *, pack: Path, index: int) -> np.ndarray:
        return self.backend.face_restore(image)


@dataclass
class MattingStage(Stage):
    name = "matting"

    def apply(self, image: np.ndarray, *, pack: Path, index: int) -> np.ndarray:
        return image


@dataclass
class UpscaleStage(Stage):
    name = "upscale"

    def apply(self, image: np.ndarray, *, pack: Path, index: int) -> np.ndarray:
        return image