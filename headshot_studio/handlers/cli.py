"""Typer CLI for ai-headshot-studio."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from headshot_studio.config.settings import load_settings
from headshot_studio.pipeline.orchestrator import Orchestrator
from headshot_studio.services.job_queue import JobQueue

app = typer.Typer(add_completion=False, help="AI headshot / portrait generation studio.")
console = Console()


@app.command()
def generate(
    refs: list[Path] = typer.Option(..., "--ref", "-r", help="Reference photo(s)."),
    style: str = typer.Option("corporate_neutral", "--style", "-s"),
    count: int = typer.Option(8, "--count", "-n", min=1, max=64),
    out: Path = typer.Option(Path("outputs"), "--out", "-o"),
) -> None:
    """Generate `count` headshots from reference photos using `style`."""
    settings = load_settings()
    queue = JobQueue(settings)
    job = queue.submit(refs=refs, style=style, count=count, out=out)
    console.print(f"[bold green]queued[/] job {job.id} -> {out}")


@app.command()
def styles() -> None:
    """List available style packs."""
    settings = load_settings()
    for name in sorted(settings.style_packs):
        console.print(f"- {name}")


if __name__ == "__main__":
    app()