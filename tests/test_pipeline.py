"""Pipeline stage tests with a stub backend."""
from pathlib import Path

import numpy as np

from headshot_studio.pipeline.stages import MattingStage, UpscaleStage


def test_matting_is_identity() -> None:
    img = np.zeros((64, 64, 3), dtype=np.float32)
    out = MattingStage().apply(img, pack=Path("x.yaml"), index=0)
    assert out.shape == img.shape


def test_upscale_returns_array() -> None:
    img = np.random.rand(32, 32, 3).astype(np.float32)
    out = UpscaleStage().apply(img, pack=Path("x.yaml"), index=1)
    assert out.dtype == np.float32
    assert out.ndim == 3