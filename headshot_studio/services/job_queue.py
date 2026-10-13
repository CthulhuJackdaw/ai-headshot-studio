"""In-process job queue with a single worker thread."""
from __future__ import annotations

import queue
import threading
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from headshot_studio.config.settings import Settings
from headshot_studio.pipeline.orchestrator import Job, Orchestrator


@dataclass
class QueuedJob:
    id: str
    refs: list[Path]
    style: str
    count: int
    out: Path
    status: str = "queued"
    result: list[Path] = field(default_factory=list)
    error: str | None = None


class JobQueue:
    """Threaded queue; one worker to keep VRAM usage serialized."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._q: queue.Queue[QueuedJob] = queue.Queue()
        self._jobs: dict[str, QueuedJob] = {}
        self._orchestrator: Orchestrator | None = None
        self._worker = threading.Thread(target=self._run, daemon=True)
        self._worker.start()

    def submit(self, *, refs: list[Path], style: str, count: int, out: Path) -> QueuedJob:
        job = QueuedJob(id=uuid.uuid4().hex[:12], refs=refs, style=style, count=count, out=out)
        self._jobs[job.id] = job
        self._q.put(job)
        return job

    def get(self, job_id: str) -> QueuedJob | None:
        return self._jobs.get(job_id)

    def _run(self) -> None:
        while True:
            job = self._q.get()
            try:
                if self._orchestrator is None:
                    self._orchestrator = Orchestrator(self.settings)
                job.status = "running"
                job.result = self._orchestrator.run(
                    Job(id=job.id, refs=job.refs, style=job.style, count=job.count, out=job.out)
                )
                job.status = "done"
            except Exception as exc:  # noqa: BLE001
                job.status = "failed"
                job.error = str(exc)
            finally:
                self._q.task_done()