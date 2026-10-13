"""Backend adapters: onnx, torch, cloud."""
from __future__ import annotations

from typing import Protocol

import numpy as np


class Backend(Protocol):
    name: str

    def render(self, prompt: str, negative: str, seed: int, steps: int) -> np.ndarray: ...

    def face_restore(self, image: np.ndarray) -> np.ndarray: ...


class OnnxBackend:
    name = "onnx"

    def __init__(self, models_dir) -> None:  # noqa: ANN001
        self.models_dir = models_dir
        self._session = None  # lazy

    def _ensure_session(self) -> None:
        if self._session is not None:
            return
        import onnxruntime as ort  # type: ignore[import-not-found]

        self._session = ort.InferenceSession(
            str(self.models_dir / "sdxl_headshot_base.onnx"),
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
        )

    def render(self, prompt: str, negative: str, seed: int, steps: int) -> np.ndarray:
        self._ensure_session()
        raise NotImplementedError("wire up prompt embedding in models/backends.py")

    def face_restore(self, image: np.ndarray) -> np.ndarray:
        return image


class TorchBackend:
    name = "torch"

    def __init__(self, models_dir) -> None:  # noqa: ANN001
        self.models_dir = models_dir

    def render(self, prompt: str, negative: str, seed: int, steps: int) -> np.ndarray:
        raise NotImplementedError("torch backend stubbed in 0.6.x")

    def face_restore(self, image: np.ndarray) -> np.ndarray:
        return image


class CloudBackend:
    name = "cloud"

    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def render(self, prompt: str, negative: str, seed: int, steps: int) -> np.ndarray:
        raise NotImplementedError("cloud renderer requires AHS_CLOUD_TOKEN")

    def face_restore(self, image: np.ndarray) -> np.ndarray:
        return image


def get_backend(name: str, models_dir, endpoint: str | None = None) -> Backend:  # noqa: ANN001
    if name == "onnx":
        return OnnxBackend(models_dir)
    if name == "torch":
        return TorchBackend(models_dir)
    if name == "cloud":
        if not endpoint:
            raise ValueError("cloud backend requires cloud_endpoint in settings")
        return CloudBackend(endpoint)
    raise ValueError(f"unknown backend: {name}")