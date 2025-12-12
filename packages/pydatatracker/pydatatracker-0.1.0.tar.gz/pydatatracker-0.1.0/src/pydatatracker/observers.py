"""Observer utilities for collecting change log entries."""

from __future__ import annotations

import json
import logging
from collections import deque
from collections.abc import Callable, Iterable
from importlib import import_module
from pathlib import Path
from typing import Any

from .exporters import HttpExporter, JsonLinesExporter, KafkaExporter, S3Exporter
from .utils.changelog import ChangeLogEntry


class ChangeCollector:
    """Callable observer that stores incoming change log entries in memory."""

    def __init__(
        self,
        *,
        capacity: int | None = None,
        include_init_events: bool = False,
    ) -> None:
        """Initialize the collector.

        Args:
            capacity: Optional maximum number of entries to keep (FIFO).
            include_init_events: Whether to store container `init` events.
        """

        self.capacity = capacity
        self.include_init_events = include_init_events
        self._changes: deque[ChangeLogEntry] = deque(maxlen=self.capacity)

    def __call__(self, change: ChangeLogEntry) -> None:  # pragma: no cover - trivial
        if not self.include_init_events and change.extra.get("action") == "init":
            return
        self._changes.append(change)

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._changes)

    def __bool__(self) -> bool:  # pragma: no cover
        return bool(self._changes)

    def clear(self) -> None:
        """Remove all collected change log entries."""

        self._changes.clear()

    def as_list(self) -> list[ChangeLogEntry]:
        """Return collected changes as a list (in arrival order)."""

        return list(self._changes)

    def last(self) -> ChangeLogEntry | None:
        """Return the most recent collected change."""

        return self._changes[-1] if self._changes else None

    def filtered(self, action: str) -> list[ChangeLogEntry]:
        """Return collected changes matching a specific action."""

        return [entry for entry in self._changes if entry.extra.get("action") == action]

    def __iter__(self) -> Iterable[ChangeLogEntry]:  # pragma: no cover
        return iter(self._changes)


class FilteredObserver:
    """Wraps another observer, only forwarding matching changes."""

    def __init__(self, observer, *, actions=None, locations=None):
        self.observer = observer
        self.actions = set(actions or [])
        self.locations = set(locations or [])

    def __call__(self, change):
        if self.actions and change.extra.get("action") not in self.actions:
            return
        location = change.extra.get("location")
        if self.locations and location not in self.locations:
            return
        return self.observer(change)


def filtered_observer(observer, *, actions=None, locations=None):
    return FilteredObserver(observer, actions=actions, locations=locations)


def logging_observer(logger: logging.Logger | None = None) -> Callable[[ChangeLogEntry], None]:
    """Create an observer that logs changes via the provided logger."""

    logger = logger or logging.getLogger("pydatatracker")

    def _observer(change: ChangeLogEntry) -> None:
        logger.info(
            "change %s action=%s location=%s",
            change.tracked_item_uuid,
            change.extra.get("action"),
            change.extra.get("location"),
        )

    return _observer


def json_file_observer(path: str | Path) -> Callable[[ChangeLogEntry], None]:
    """Return an observer that appends serialized changes to a .jsonl file."""

    file_path = Path(path)

    def _observer(change: ChangeLogEntry) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(change.to_dict()) + "\n")

    return _observer


def async_queue_observer(queue):
    import asyncio

    async def _async_enqueue(change):
        await queue.put(change.to_dict())

    def _observer(change):
        if asyncio.iscoroutinefunction(queue.put):
            asyncio.create_task(_async_enqueue(change))
        else:
            queue.put(change.to_dict())

    return _observer


def build_observer_from_config(config: dict[str, Any]) -> Callable[[ChangeLogEntry], None]:
    """Instantiate an observer from a config dictionary."""

    config = dict(config)
    options = config.get("options", {})
    kind = config["type"]

    if kind == "change_collector":
        return ChangeCollector(**options)
    if kind == "filtered":
        base = build_observer_from_config(config["observer"])
        return FilteredObserver(base, **options)
    if kind == "logging":
        logger_name = options.get("logger")
        logger = logging.getLogger(logger_name) if logger_name else None
        return logging_observer(logger)
    if kind == "json_file":
        return json_file_observer(options["path"])
    if kind == "json_lines_exporter":
        return JsonLinesExporter(**options)
    if kind == "http_exporter":
        post_callable = _resolve_callable(options["post_callable"])
        return HttpExporter(post_callable, options["url"], **options.get("params", {}))
    if kind == "s3_exporter":
        client = _resolve_callable(options["client_callable"])()
        return S3Exporter(
            client,
            bucket=options["bucket"],
            prefix=options.get("prefix", "changes/"),
        )
    if kind == "kafka_exporter":
        producer = _resolve_callable(options["producer_callable"])()
        return KafkaExporter(producer, topic=options["topic"])
    raise ValueError(f"unknown observer type: {kind}")


def _resolve_callable(path: str) -> Callable[..., Any]:
    module, attr = path.rsplit(".", 1)
    mod = import_module(module)
    return getattr(mod, attr)


class MetricsObserver:
    """Simple metrics observer wrapping a Counter-like interface."""

    def __init__(self, counter: Any) -> None:
        self.counter = counter

    def __call__(self, change: ChangeLogEntry) -> None:
        action = change.extra.get("action", "unknown")
        self.counter.labels(action=action).inc()


def telemetry_observer(counter: Any | None = None) -> MetricsObserver:
    """Return an observer that increments a Counter per action."""

    if counter is None:
        try:
            from prometheus_client import Counter  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install prometheus_client or pass an existing counter") from exc
        counter = Counter("pydatatracker_changes", "Total changes", ["action"])
    return MetricsObserver(counter)
