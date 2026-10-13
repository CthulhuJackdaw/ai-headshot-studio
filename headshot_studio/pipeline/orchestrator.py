"""Orchestrates the headshot generation stages."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from headshot_studio.config.settings import Settings
from headshot_studio.models.backends import get_backend
from headshot_studio.pipeline.stages import (
    FaceRestoreStage,
    MattingStage,
    RenderStage,
    UpscaleStage,
)
from headshot_studio.utils.image import load_image, save_image

log = logging.getLogger(__name__)


@dataclass
class Job:
    id: str
    refs: list[Path]
    style: str
    count: int
    out: Path


class Orchestrator:
    """Runs the full render pipeline for one job."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.backend = get_backend(settings.backend, settings.models_dir, settings.cloud_endpoint)
        self.stages = [
            RenderStage(self.backend, settings.render),
            FaceRestoreStage(self.backend),
            MattingStage(),
            UpscaleStage(),
        ]

    def run(self, job: Job) -> list[Path]:
        pack = self.settings.style_packs.get(job.style)
        if pack is None:
            raise ValueError(f"unknown style: {job.style}")
        job.out.mkdir(parents=True, exist_ok=True)

        written: list[Path] = []
        for i in range(job.count):
            image = load_image(job.refs[i % len(job.refs)])
            for stage in self.stages:
                image = stage.apply(image, pack=pack, index=i)
            target = job.out / f"{job.id}_{i:03d}.png"
            save_image(image, target)
            written.append(target)
            log.info("wrote %s", target)
        return written