"""Logging configuration for CLI and services."""
from __future__ import annotations

import logging
import os
import sys


def configure_logging(level: str | None = None) -> None:
    lvl = (level or os.getenv("AHS_LOG", "INFO")).upper()
    logging.basicConfig(
        level=getattr(logging, lvl, logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        stream=sys.stderr,
    )