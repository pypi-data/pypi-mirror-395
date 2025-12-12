# Architecture Notes

## Goals

- Provide light-weight tracking primitives that higher-level data pipelines can compose.
- Emit consistent change log entries across dict/list/attribute tracking layers.
- Keep side effects observable through the observer hooks in `TrackBase`.

## Key modules

- `pydatatracker.types._trackbase.TrackBase`: shared behaviors for locking,
  observer coordination, and change log orchestration.
- `pydatatracker.types.trackedlist.TrackedList` / `trackedict.TrackedDict`:
  public containers surfaced to client code.
- `pydatatracker.utils.changelog.ChangeLogEntry`: serializable audit records that tie
  into future persistence layers.

## Data flow

1. Client code mutates a tracked container.
2. Decorators defined in `_trackbase` note the mutation and populate the tracking
   context.
3. When the mutation finishes, a `ChangeLogEntry` is created and dispatched to all
   observers.
4. Observers can persist, aggregate, or further inspect these records to build the
   wrapper-specific workflows.

## Future work

- Define concrete observer interfaces for persistence targets (files, HTTP sinks,
  telemetry services).
- Document additional examples that demonstrate how tracked containers simplify
  multi-stage data workflows.
- Provide CLI helpers for inspecting change logs or exporting history snapshots.

## Observability controls

- `tracking_capture_snapshots`: opt-in repr snapshots per container
- `tracking_capture_stack`: opt-in stack/actor inference for debugging
- `tracking_actor` context manager: sets the actor stored on each ChangeLogEntry without stack inspection
- Shallow frame inspection only runs when both snapshot and stack capture are disabled
- Consumers should rely on `last_change()` and `changes_since()` when inspecting history.
