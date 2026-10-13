"""Project storage for `.ahsproj` files (JSON inside a zip)."""
from __future__ import annotations

import json
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Project:
    name: str
    refs: list[str]
    style: str
    created: str


class ProjectStorage:
    """Reads/writes `.ahsproj` project bundles."""

    def save(self, project: Project, target: Path) -> Path:
        target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("project.json", json.dumps(asdict(project), indent=2))
            for ref in project.refs:
                p = Path(ref)
                if p.exists():
                    zf.write(p, arcname=f"refs/{p.name}")
        return target

    def load(self, source: Path) -> Project:
        with zipfile.ZipFile(source, "r") as zf:
            data = json.loads(zf.read("project.json"))
        return Project(**data)