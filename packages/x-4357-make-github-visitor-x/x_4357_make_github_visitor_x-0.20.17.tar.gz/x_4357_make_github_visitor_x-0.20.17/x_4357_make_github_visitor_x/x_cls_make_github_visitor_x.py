"""Compatibility wrapper re-exporting the GitHub visitor implementation."""

from __future__ import annotations

import sys

from .runner import *  # noqa: F403
from .runner import _run_json_cli

if __name__ == "__main__":
    _run_json_cli(sys.argv[1:])
