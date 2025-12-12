"""Unit tests for PyDataTracker public APIs."""

from __future__ import annotations

import datetime
import logging
import time

import pytest

from pydatatracker import ChangeCollector, TrackedDict
from pydatatracker.observers import (
    FilteredObserver,
    async_queue_observer,
    json_file_observer,
    logging_observer,
)


def test_tracked_dict_logs_updates() -> None:
    """`TrackedDict` should record mutations as change log entries."""
    tracked = TrackedDict()

    tracked["status"] = "pending"
    tracked["status"] = "complete"

    last_entry = tracked.tracking_changes()[-1]

    assert last_entry.extra["action"] == "update"
    assert last_entry.extra["location"] == "status"
    assert "complete" in last_entry.extra["value"]


def test_tracked_dict_lock_prevents_mutation() -> None:
    """When locked, tracked containers should reject write operations."""
    tracked = TrackedDict({"status": "pending"})

    tracked.lock()

    with pytest.raises(RuntimeError):
        tracked["status"] = "complete"


def test_tracking_changes_can_be_limited() -> None:
    """`tracking_changes` returns only the requested number of entries."""
    tracked = TrackedDict()
    tracked["a"] = 1
    tracked["b"] = 2

    history = tracked.tracking_changes(most_recent=1)

    assert len(history) == 1
    assert history[0].extra["location"] == "b"


def _measure_assignment_time(snapshot: bool, iterations: int = 2000) -> float:
    tracked = TrackedDict(tracking_capture_snapshots=snapshot)
    start = time.perf_counter()
    for index in range(iterations):
        tracked[str(index)] = index
    end = time.perf_counter()
    return end - start


def test_snapshot_mode_relative_timing() -> None:
    """Report timing difference between snapshot modes for manual inspection."""
    baseline = _measure_assignment_time(snapshot=False)
    snapshot = _measure_assignment_time(snapshot=True)
    percent = ((snapshot - baseline) / baseline * 100) if baseline else float("inf")

    print(
        f"tracking_capture_snapshots timing: off={baseline:.6f}s "
        f"on={snapshot:.6f}s ({snapshot - baseline:.6f}s delta, "
        f"{percent:.2f}% slower)"
    )

    assert snapshot >= baseline


def test_capture_stack_is_opt_in() -> None:
    tracked = TrackedDict()
    tracked["foo"] = "bar"

    change = tracked.tracking_changes()[-1]
    assert change.stack == []
    assert change.actor == ""

    tracked_verbose = TrackedDict(tracking_capture_stack=True)
    tracked_verbose["foo"] = "bar"
    verbose_change = tracked_verbose.tracking_changes()[-1]
    assert verbose_change.stack, "stack should be populated when capture is enabled"


def test_tracking_changes_preserve_insertion_order() -> None:
    tracked = TrackedDict()
    tracked["first"] = 1
    tracked["second"] = 2

    last_two = tracked.tracking_changes()[-2:]
    assert [entry.extra["location"] for entry in last_two] == ["first", "second"]
    assert last_two[0].created_time <= last_two[1].created_time


def test_last_change_and_changes_since() -> None:
    tracked = TrackedDict()
    initial = tracked.last_change()
    assert initial is not None
    assert initial.extra["action"] == "init"

    tracked["alpha"] = 1
    first_entry = tracked.last_change()
    assert first_entry is not None
    assert first_entry.extra["location"] == "alpha"

    tracked["beta"] = 2
    all_changes = tracked.changes_since(first_entry)
    assert [entry.extra["location"] for entry in all_changes] == ["alpha", "beta"]

    cutoff = first_entry.created_time + datetime.timedelta(microseconds=1)
    recent_changes = tracked.changes_since(cutoff)
    assert [entry.extra["location"] for entry in recent_changes] == ["beta"]


def test_change_collector_observer_records_events() -> None:
    tracked = TrackedDict()
    collector = ChangeCollector()
    tracked.tracking_add_observer(collector)

    tracked["evt"] = 1
    tracked["evt"] = 2

    collected_locations = [entry.extra["location"] for entry in collector.as_list()]
    assert "evt" in collected_locations


def test_filtered_observer_filters_events() -> None:
    tracked = TrackedDict()
    collected = []

    def observer(change):
        collected.append(change.extra.get("location"))

    filtered = FilteredObserver(observer, actions={"update"}, locations={"foo"})
    tracked.tracking_add_observer(filtered)

    tracked["foo"] = 1
    tracked["bar"] = 2
    tracked["foo"] = 3

    assert collected == ["foo"]


def test_change_log_entry_to_dict() -> None:
    tracked = TrackedDict()
    tracked["count"] = 1
    entry = tracked.last_change()
    assert entry is not None
    serialized = entry.to_dict()
    assert serialized["extra"]["location"] == "count"
    assert "actor" in serialized
    assert serialized["created_time"].endswith("Z") or serialized["created_time"].count(":") >= 2


def test_json_file_observer_writes_changes(tmp_path) -> None:
    tracked = TrackedDict()
    file_path = tmp_path / "log.jsonl"

    observer = json_file_observer(file_path)
    tracked.tracking_add_observer(observer)
    tracked["foo"] = "bar"

    lines = file_path.read_text().strip().splitlines()
    assert len(lines) == 1
    assert "foo" in lines[0]


def test_logging_observer_uses_logger(caplog) -> None:
    tracked = TrackedDict()
    logger = logging.getLogger("pydatatracker.tests")
    observer = logging_observer(logger)
    tracked.tracking_add_observer(observer)

    with caplog.at_level(logging.INFO):
        tracked["foo"] = "bar"

    assert any("foo" in record.message for record in caplog.records)


def test_async_queue_observer_handles_coroutines():
    tracked = TrackedDict()

    class DummyQueue:
        def __init__(self):
            self.items = []

        def put(self, value):
            self.items.append(value)

    queue = DummyQueue()
    observer = async_queue_observer(queue)
    tracked.tracking_add_observer(observer)

    tracked["foo"] = "bar"
    assert queue.items


def test_async_queue_observer_synchronous_queue():
    tracked = TrackedDict()

    class SyncQueue:
        def __init__(self):
            self.items = []

        def put(self, value):
            self.items.append(value)

    queue = SyncQueue()
    observer = async_queue_observer(queue)
    tracked.tracking_add_observer(observer)
    tracked["foo"] = "bar"
    assert queue.items
