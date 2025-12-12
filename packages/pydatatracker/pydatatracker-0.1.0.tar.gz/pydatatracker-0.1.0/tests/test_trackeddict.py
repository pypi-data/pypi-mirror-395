"""Tests for `TrackedDict` steady-state behavior."""

from __future__ import annotations

from pydatatracker import TrackedDict


def _latest_change(tracked: TrackedDict):
    return tracked.tracking_changes()[-1]


def test_tracked_dict_pop_logs_removed_items() -> None:
    """Popping keys should record removal metadata."""
    tracked = TrackedDict({"status": "pending"})

    result = tracked.pop("status")

    change = _latest_change(tracked)
    assert result == "pending"
    assert change.extra["action"] == "update"
    assert change.extra["location"] == "status"
    assert "pending" in change.extra["removed_items"]


def test_tracked_dict_child_updates_do_not_touch_parent_log() -> None:
    """Changing a nested trackable currently leaves the parent log untouched."""
    parent = TrackedDict(tracking_auto_convert=True)
    parent["child"] = {"state": "draft"}

    child = parent["child"]
    child["state"] = "final"

    change = _latest_change(parent)
    assert change.extra["location"] == "child"
    assert "state" in change.extra["value"]
    assert "draft" in change.extra["value"]
    assert len(parent.tracking_changes()) == 2  # no additional entry added


def test_tracked_dict_child_tracks_its_own_updates() -> None:
    """Child tracked dicts still emit their own change log entries."""
    parent = TrackedDict(tracking_auto_convert=True)
    parent["child"] = {"state": "draft"}
    child = parent["child"]

    child["state"] = "final"

    change = _latest_change(child)
    assert change.extra["action"] == "update"
    assert change.extra["location"] == "state"
    assert change.extra["value"] == "final"


def test_tracked_dict_setdefault_records_default_and_return() -> None:
    """`setdefault` tracks the provided default and the return value."""
    tracked = TrackedDict({"a": 1})

    returned = tracked.setdefault("b", 2)

    change = _latest_change(tracked)
    assert returned == 2
    assert change.extra["action"] == "update"
    assert change.extra["location"] == "b"
    assert change.extra["default"] == "2"
    assert change.extra["return_value"] == "2"


def test_tracked_dict_update_logs_replacements() -> None:
    """`update` notes removed values when keys are overwritten."""
    tracked = TrackedDict({"a": 1})

    tracked.update({"a": 3, "b": 2})

    change = _latest_change(tracked)
    assert change.extra["action"] == "update"
    assert "1" in change.extra["removed_items"]
    assert "{'a': 3" in change.extra["value"]
    assert "'b': 2" in change.extra["value"]


def test_tracked_dict_clear_records_removed_items() -> None:
    """`clear` stores all removed values."""
    tracked = TrackedDict({"a": 1, "b": 2})

    tracked.clear()

    change = _latest_change(tracked)
    assert change.extra["action"] == "remove"
    assert "[1, 2]" in change.extra["removed_items"]


def test_tracked_dict_copy_untracked_returns_plain_dict() -> None:
    """`copy(untracked=True)` returns regular dictionaries."""
    tracked = TrackedDict({"a": {"nested": 1}}, tracking_auto_convert=True)

    clone = tracked.copy(untracked=True)

    change = _latest_change(tracked)
    assert isinstance(clone, dict)
    assert isinstance(clone["a"], dict)
    assert change.extra["action"] == "copy"
    assert change.extra["untracked"] == "True"


def test_tracked_dict_snapshot_opt_in_records_repr() -> None:
    """`tracking_capture_snapshots` controls repr logging."""
    tracked = TrackedDict(tracking_capture_snapshots=True)

    tracked["a"] = 1
    change = tracked.tracking_changes()[-1]
    assert "data_pre_change" in change.extra
    assert change.extra["data_post_change"].endswith("1}")

    tracked2 = TrackedDict()
    tracked2["a"] = 1
    change2 = tracked2.tracking_changes()[-1]
    assert "data_pre_change" not in change2.extra
