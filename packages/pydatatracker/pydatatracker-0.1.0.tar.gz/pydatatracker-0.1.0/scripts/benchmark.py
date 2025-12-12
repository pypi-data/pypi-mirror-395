"""Benchmark snapshot/stack/actor combinations for PyDataTracker."""

from __future__ import annotations

import statistics
import time
from contextlib import nullcontext
from enum import Enum

from pydatatracker import TrackedDict, tracking_actor

ITERATIONS = 5000
WARMUP = 200
RUNS = 5


class Mode(Enum):
    BASE = "base"
    ACTOR = "actor"
    SNAPSHOT = "snapshot"
    FULL = "full"


def run(mode: Mode) -> float:
    payload = TrackedDict(
        tracking_capture_snapshots=mode in {Mode.SNAPSHOT, Mode.FULL},
        tracking_capture_stack=mode is Mode.FULL,
    )
    ctx = tracking_actor("bench") if mode in {Mode.ACTOR, Mode.FULL} else nullcontext()
    with ctx:
        start = time.perf_counter()
        for i in range(ITERATIONS + WARMUP):
            payload[str(i)] = i
        end = time.perf_counter()
    return end - start


def main() -> None:
    results: dict[Mode, list[float]] = {mode: [] for mode in Mode}
    for mode in Mode:
        for _ in range(RUNS):
            results[mode].append(run(mode))
    print(f"Benchmark results ({ITERATIONS} mutations, {RUNS} runs)")
    for mode, samples in results.items():
        mean = statistics.mean(samples)
        stdev = statistics.pstdev(samples)
        print(f"  {mode.value:<8} mean={mean:.4f}s stdev={stdev:.4f}s")


if __name__ == "__main__":
    main()
