"""Tests for observer configuration loading."""

from __future__ import annotations

import json
from pathlib import Path

from pydatatracker import TrackedDict
from pydatatracker.config import load_observers_from_json


def test_load_observers_from_json(tmp_path: Path) -> None:
    config = [
        {"type": "change_collector", "options": {"capacity": 5}},
        {
            "type": "filtered",
            "observer": {"type": "json_file", "options": {"path": str(tmp_path / "log.jsonl")}},
            "options": {"actions": ["add"]},
        },
    ]
    cfg_path = tmp_path / "observers.json"
    cfg_path.write_text(json.dumps(config))

    observers = load_observers_from_json(cfg_path)
    tracked = TrackedDict()
    for observer in observers:
        tracked.tracking_add_observer(observer)

    tracked["foo"] = "bar"
    assert (tmp_path / "log.jsonl").read_text()
