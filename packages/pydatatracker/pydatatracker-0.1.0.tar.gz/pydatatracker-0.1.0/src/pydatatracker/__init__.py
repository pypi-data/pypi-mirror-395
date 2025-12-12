# Project: bastproxy
# Filename: pydatatracker/__init__.py
#
# File Description: a "package" to manage records
#
# By: Bast
"""Module for monitoring and managing attributes with tracking capabilities.

This module provides the `TrackedAttr` class, which allows for the tracking
of changes to attributes and the management of relationships between tracked
attributes and their children. It includes methods for locking and unlocking
attributes, notifying observers of changes, and maintaining a history of
original values, making it a valuable tool for monitoring state changes in
an application.

Key Components:
    - TrackedAttr: A class that extends TrackBase to monitor attribute changes.
    - Methods for adding, locking, unlocking, and notifying changes to attributes.
    - Utility methods for handling attribute changes, conversions, and tracking.

Features:
    - Automatic conversion of tracked attribute values.
    - Management of parent-child relationships for tracked attributes.
    - Notification system for observers when attribute changes occur.
    - Locking mechanism to prevent modifications to specific attributes.
    - Comprehensive logging of attribute changes and original values.

Usage:
    - Instantiate TrackedAttr to create an object that tracks attribute changes.
    - Use `tracking_add_attribute_to_monitor` to start monitoring specific attributes.
    - Lock and unlock attributes using `lock` and `unlock` methods.
    - Access original values and change logs through provided methods.

Classes:
    - `TrackedAttr`: Represents a class that can track attribute changes.
"""

# imported to prevent circular references
from ._version import __version__
from .types._trackbase import TrackBase  # noqa: F401

__all__ = [
    "TrackedDict",
    "TrackedList",
    "TrackedAttr",
    "ChangeLogEntry",
    "add_to_ignore_in_stack",
    "ChangeCollector",
    "tracking_actor",
    "__version__",
]

from .observers import ChangeCollector
from .types.actor import tracking_actor
from .types.trackedattributes import TrackedAttr
from .types.trackeddict import TrackedDict
from .types.trackedlist import TrackedList
from .utils.changelog import ChangeLogEntry, add_to_ignore_in_stack
