"""Utilities for setting the current tracking actor."""

from __future__ import annotations

import contextlib
import contextvars

current_actor: contextvars.ContextVar[str | None]
current_actor = contextvars.ContextVar("tracking_actor", default=None)


@contextlib.contextmanager
def tracking_actor(name: str):
    """Context manager that temporarily sets the tracking actor."""
    token = current_actor.set(name)
    try:
        yield
    finally:
        current_actor.reset(token)
