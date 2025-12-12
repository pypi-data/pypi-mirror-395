"""Tests for `TrackedList` steady-state behavior."""

from __future__ import annotations

from pydatatracker import TrackedList


def _latest_change(tracked: TrackedList):
    return tracked.tracking_changes()[-1]


def test_tracked_list_append_records_index() -> None:
    """Appending should log the index where the new item landed."""
    tracked = TrackedList([1, 2])

    tracked.append(3)

    change = _latest_change(tracked)
    assert change.extra["action"] == "add"
    assert change.extra["location"] == 2
    assert "3" in change.extra["value"]


def test_tracked_list_pop_stores_passed_and_actual_index() -> None:
    """Popping should retain both logical and actual index information."""
    tracked = TrackedList(["a", "b"])

    removed = tracked.pop(-1)

    change = _latest_change(tracked)
    assert removed == "b"
    assert change.extra["action"] == "remove"
    assert change.extra["location"] == 1  # actual index after normalization
    assert change.extra["passed_index"] == "-1"
    assert "b" in change.extra["removed_items"]


def test_tracked_list_extend_logs_location_range() -> None:
    """Extending logs comma-separated locations for appended items."""
    tracked = TrackedList([1, 2])

    tracked.extend([3, 4])

    change = _latest_change(tracked)
    assert change.extra["action"] == "add"
    assert change.extra["location"] == "2,3"
    assert "[3, 4]" in change.extra["value"]


def test_tracked_list_remove_reports_removed_items() -> None:
    """Removing an item should capture location and removed payload."""
    tracked = TrackedList(["a", "b", "c"])

    tracked.remove("b")

    change = _latest_change(tracked)
    assert change.extra["action"] == "remove"
    assert change.extra["location"] == 1
    assert "['b']" in change.extra["removed_items"]


def test_tracked_list_clear_records_all_removed_items() -> None:
    """Clearing the list records all removed values."""
    tracked = TrackedList([1, 2])

    tracked.clear()

    change = _latest_change(tracked)
    assert change.extra["action"] == "remove"
    assert "[1, 2]" in change.extra["removed_items"]
