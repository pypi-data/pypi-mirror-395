"""Tests for exporter utilities."""

from __future__ import annotations

import json
from pathlib import Path

from pydatatracker import TrackedDict
from pydatatracker.exporters import HttpExporter, JsonLinesExporter, KafkaExporter, S3Exporter


def _make_change():
    tracked = TrackedDict()
    tracked["foo"] = "bar"
    return tracked.last_change()


def test_json_lines_exporter(tmp_path: Path) -> None:
    change = _make_change()
    exporter = JsonLinesExporter(tmp_path / "changes.jsonl")
    exporter(change)
    data = (tmp_path / "changes.jsonl").read_text().strip().splitlines()
    assert len(data) == 1
    assert json.loads(data[0])["extra"]["location"] == "foo"


def test_http_exporter_invokes_post(monkeypatch) -> None:
    captured = {}

    def fake_post(url, json=None, **kwargs):
        captured["url"] = url
        captured["json"] = json

    exporter = HttpExporter(fake_post, "https://api.example.com/")
    exporter(_make_change())
    assert captured["url"].startswith("https://api.example.com")
    assert captured["json"]["extra"]["location"] == "foo"


def test_s3_exporter(monkeypatch, tmp_path: Path) -> None:
    class Client:
        def __init__(self):
            self.calls = []

        def put_object(self, **kwargs):
            self.calls.append(kwargs)

    client = Client()
    exporter = S3Exporter(client, bucket="test", prefix="logs")
    exporter(_make_change())
    assert client.calls
    assert client.calls[0]["Bucket"] == "test"


def test_kafka_exporter() -> None:
    class Producer:
        def __init__(self):
            self.messages = []

        def send(self, topic, payload):
            self.messages.append((topic, payload))

    producer = Producer()
    exporter = KafkaExporter(producer, topic="changes")
    exporter(_make_change())
    assert producer.messages
