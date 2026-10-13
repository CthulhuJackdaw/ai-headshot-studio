"""Image IO helpers built on Pillow + numpy."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

MAX_DIM = 4096


def load_image(path: Path) -> np.ndarray:
    """Load an image as an RGB float32 array in [0, 1]."""
    with Image.open(path) as im:
        im = im.convert("RGB")
        if max(im.size) > MAX_DIM:
            im.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
        return np.asarray(im, dtype=np.float32) / 255.0


def to_pil(arr: np.ndarray) -> Image.Image:
    if arr.dtype != np.uint8:
        arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGB")


def save_image(arr: np.ndarray, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    to_pil(arr).save(path, format="PNG", optimize=True)
    return path