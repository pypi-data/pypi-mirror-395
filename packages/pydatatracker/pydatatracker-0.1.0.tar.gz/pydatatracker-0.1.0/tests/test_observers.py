from pydatatracker import TrackedDict
from pydatatracker.observers import telemetry_observer


class DummyCounter:
    def __init__(self):
        self.counts = {}

    def labels(self, **labels):
        key = tuple(sorted(labels.items()))
        if key not in self.counts:
            self.counts[key] = 0

        class Inc:
            def __init__(self, parent, key):
                self.parent = parent
                self.key = key

            def inc(self):
                self.parent.counts[self.key] += 1

        return Inc(self, key)


def test_telemetry_observer_counts():
    tracked = TrackedDict()
    counter = DummyCounter()
    tracked.tracking_add_observer(telemetry_observer(counter))
    tracked["foo"] = "bar"
    assert counter.counts
