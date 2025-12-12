#!/usr/bin/env python3
"""Simple CLI to tail/dump serialized changes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pydatatracker import TrackedDict
from pydatatracker.observers import ChangeCollector


def cmd_demo(_: argparse.Namespace) -> None:
    tracked = TrackedDict(tracking_capture_snapshots=False)
    collector = ChangeCollector()
    tracked.tracking_add_observer(collector)
    tracked['status'] = 'ready'
    for entry in collector.as_list():
        print(json.dumps(entry.to_dict()))


def cmd_show(args: argparse.Namespace) -> None:
    path = Path(args.file)
    for line in path.read_text().splitlines():
        print(json.loads(line))


def main() -> None:
    parser = argparse.ArgumentParser(prog='pydatatracker-cli')
    sub = parser.add_subparsers(dest='cmd', required=True)

    demo = sub.add_parser('demo')
    demo.set_defaults(func=cmd_demo)

    show = sub.add_parser('show')
    show.add_argument('file')
    show.set_defaults(func=cmd_show)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
