"""User-facing handlers: CLI, local IPC, and HTTP bridge."""
from .cli import app as cli_app

__all__ = ["cli_app"]