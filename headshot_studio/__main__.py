"""Entry point for the `headshot-studio` CLI."""
from __future__ import annotations

import sys

from headshot_studio.handlers.cli import app


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    try:
        app(args=argv, standalone_mode=False)
    except KeyboardInterrupt:
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())