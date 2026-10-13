# Contributing to ai-headshot-studio

Thanks for wanting to help build the studio. This is a Windows-first desktop
tool for generating professional AI headshots and portrait variants from a
handful of reference photos.

## Ground rules

- Python 3.11+ is the target runtime. 3.12 works; 3.10 is best-effort.
- Every PR must pass `pytest` and `ruff check .` locally before opening.
- One feature per PR. If it touches the pipeline, include a smoke test.
- No new heavyweight dependency without a discussion issue first.

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q
```

## Layout

- `headshot_studio/` — main package (pipeline, services, handlers)
- `headshot_studio/models/` — model registry + backend adapters
- `headshot_studio/pipeline/` — staged generation stages
- `headshot_studio/services/` — long-lived services (queue, storage, GPU)
- `headshot_studio/handlers/` — CLI + IPC + HTTP handlers
- `headshot_studio/config/` — typed settings, presets, style packs
- `headshot_studio/utils/` — image, io, logging helpers
- `native/` — optional C++/CUDA acceleration
- `dotnet/` — optional C# tray/installer shell
- `java/` — optional Java batch client for enterprise batches

## Style packs

New style packs go in `headshot_studio/config/style_packs/`. Each pack is a
YAML file with `name`, `prompt_template`, `negative_prompt`, `lora`, and
`strength`. Ship a sample render in the PR description.

## Commit style

`<area>: <short imperative>` — e.g. `pipeline: add face restore stage`.