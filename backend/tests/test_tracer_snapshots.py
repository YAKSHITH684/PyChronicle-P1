import unittest
from pychronicle.tracer.execution_tracer import _snapshot_for_diff

class TracerSnapshotTests(unittest.TestCase):
    def test_list_snapshot_is_independent(self):
        values = [1]
        snapshot = _snapshot_for_diff(values)
        values.append(2)
        self.assertEqual(snapshot, [1])

if __name__ == "__main__":
    unittest.main()
