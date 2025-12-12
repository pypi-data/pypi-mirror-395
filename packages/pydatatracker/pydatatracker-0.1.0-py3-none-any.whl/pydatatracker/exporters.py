"""Structured export helpers for change log entries."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable
from pathlib import Path

from .utils.changelog import ChangeLogEntry


class BaseExporter:
    """Base class for exporters that also act as observers."""

    def __call__(self, change: ChangeLogEntry) -> None:
        self.export(change.to_dict())

    def export(self, change_dict: dict[str, object]) -> None:  # pragma: no cover
        raise NotImplementedError


class JsonLinesExporter(BaseExporter):
    """Append serialized change dicts to a JSONL file."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def export(self, change_dict: dict[str, object]) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(change_dict) + "\n")


class HttpExporter(BaseExporter):
    """Send serialized change dicts via an injected HTTP client."""

    def __init__(self, post: Callable[..., object], url: str, **kwargs: object) -> None:
        self.post = post
        self.url = url
        self.kwargs = kwargs

    def export(self, change_dict: dict[str, object]) -> None:
        self.post(self.url, json=change_dict, **self.kwargs)


class S3Exporter(BaseExporter):
    """Upload serialized change dicts to S3-compatible storage."""

    def __init__(self, client: object, bucket: str, prefix: str = "changes/") -> None:
        self.client = client
        self.bucket = bucket
        self.prefix = prefix.rstrip("/") + "/"

    def export(self, change_dict: dict[str, object]) -> None:
        body = json.dumps(change_dict).encode("utf-8")
        key = f"{self.prefix}{change_dict['uuid'] or uuid.uuid4().hex}.json"
        self.client.put_object(Bucket=self.bucket, Key=key, Body=body)


class KafkaExporter(BaseExporter):
    """Send serialized change dicts to a Kafka-like producer."""

    def __init__(self, producer: object, topic: str) -> None:
        self.producer = producer
        self.topic = topic

    def export(self, change_dict: dict[str, object]) -> None:
        payload = json.dumps(change_dict).encode("utf-8")
        self.producer.send(self.topic, payload)
