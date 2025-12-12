"""Tests for `TrackedAttr` steady-state behavior."""

from __future__ import annotations

import pytest

from pydatatracker import TrackedAttr, TrackedDict


class SampleTrackedAttr(TrackedAttr):
    """Helper object exposing a couple monitored attributes."""

    def __init__(self) -> None:
        super().__init__(tracking_auto_convert=True)
        self.name = "alpha"
        self.profile = {"score": 1}
        self.tracking_add_attribute_to_monitor("name")
        self.tracking_add_attribute_to_monitor("profile")


def _latest_change(tracked: TrackedAttr):
    return tracked.tracking_changes()[-1]


def test_tracked_attr_records_attribute_update() -> None:
    sample = SampleTrackedAttr()

    sample.name = "beta"

    change = _latest_change(sample)
    assert change.extra["action"] == "update"
    assert change.extra["location"] == "name"
    assert change.extra["data_pre_change"] == "alpha"
    assert change.extra["data_post_change"] == "beta"


def test_tracked_attr_lock_blocks_mutation() -> None:
    sample = SampleTrackedAttr()

    sample.lock("name")

    change = _latest_change(sample)
    assert change.extra["action"] == "lock"
    assert change.extra["attribute_name"] == "name"
    assert change.extra["attribute_locked"] == "True"

    with pytest.raises(RuntimeError):
        sample.name = "gamma"


def test_tracked_attr_child_updates_include_parent_location() -> None:
    sample = SampleTrackedAttr()
    assert isinstance(sample.profile, TrackedDict)

    sample.profile["score"] = 5

    change = _latest_change(sample)
    assert change.extra["location"] == "profile:score"
    assert "5" in change.extra["value"]


def test_tracked_attr_unlock_attribute_logs_change() -> None:
    sample = SampleTrackedAttr()

    sample.lock("name")
    sample.unlock("name")

    change = _latest_change(sample)
    assert change.extra["action"] == "unlock"
    assert change.extra["attribute_name"] == "name"
    assert change.extra["attribute_locked"] == "False"


def test_tracked_attr_unlock_all_clears_global_lock() -> None:
    sample = SampleTrackedAttr()

    sample.lock()
    sample.unlock()

    change = _latest_change(sample)
    assert change.extra["action"] == "unlock"
    assert sample._tracking_locked is False
