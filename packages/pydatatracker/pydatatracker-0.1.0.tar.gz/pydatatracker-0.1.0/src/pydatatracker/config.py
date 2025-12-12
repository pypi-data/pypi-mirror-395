"""Helpers for loading observer configurations."""

from __future__ import annotations

import json
from pathlib import Path

from .observers import build_observer_from_config


def load_observers_from_json(path: str | Path) -> list:
    """Load observer configs from a JSON file."""

    data = json.loads(Path(path).read_text())
    if not isinstance(data, list):
        raise ValueError("config file must contain a list of observers")
    return [build_observer_from_config(item) for item in data]
