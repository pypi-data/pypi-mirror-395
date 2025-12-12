# Debugging & Observability Cookbook

## Capture actors without stack traces
```python
from pydatatracker import TrackedDict, tracking_actor

payload = TrackedDict()
with tracking_actor("importer"):
    payload["status"] = "ready"

print(payload.last_change().actor)  # importer
```

## Enable snapshots and stack traces when needed
```python
payload = TrackedDict(
    tracking_capture_snapshots=True,
    tracking_capture_stack=True,
)
payload["status"] = "ready"
change = payload.last_change()
print(change.extra["data_pre_change"], change.stack)
```

## Collect change events via observers
```python
from pydatatracker import ChangeCollector

collector = ChangeCollector()
payload.tracking_add_observer(collector)

payload["status"] = "ready"
print(collector.as_list())
```

### Telemetry observer
```python
from pydatatracker.observers import telemetry_observer

payload.tracking_add_observer(telemetry_observer())
payload["status"] = "ready"
```

### Log observer
```python
import logging
logger = logging.getLogger("changes")

def log_observer(change):
    logger.info("Change: %s -> %s", change.extra.get("location"), change.extra.get("action"))

payload.tracking_add_observer(log_observer)
payload["status"] = "ready"
```

### JSON observer
```python
import json
from pathlib import Path

def json_observer(change):
    Path("changes.jsonl").write_text(json.dumps(change.extra) + "\n", append=True)

payload.tracking_add_observer(json_observer)
payload["status"] = "ready"
```

## Export change history per request
```python
changes = payload.tracking_changes()
latest = payload.last_change()
recent = payload.changes_since(latest.created_time)
```

## Debug workflow example
1. Wrap the code path in `tracking_actor("job-123")`.
2. Enable snapshots/stacks temporarily via `TrackedDict(tracking_capture_snapshots=True, tracking_capture_stack=True)`.
3. Attach a `ChangeCollector` or custom observer.
4. Re-run the workflow and inspect `collector.as_list()` or `changes_since(...)`.
5. Disable the flags when you’re satisfied with the diagnosis.

## Benchmarking observability costs

Run `just benchmark` to quantify how actors, snapshots, and stack capture affect throughput. Compare modes before enabling diagnostic knobs in production.

## Async observers
Use `async_queue_observer` to forward change dictionaries into an `asyncio.Queue` while continuing to operate in synchronous contexts.

## CLI utilities
Use `scripts/cli.py` (or `just cli`) to emit serialized changes from a demo session or show JSONL logs via `show`.

## Export pipelines
Combine observers with exporters (e.g., `JsonLinesExporter`, `HttpExporter`) to persist changes outside of your process.

### Config examples
```json
[
  {"type": "change_collector"},
  {"type": "json_file", "options": {"path": "tmp/change.jsonl"}}
]
```
Load via `load_observers_from_json` and attach to tracked objects.
