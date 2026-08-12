import unittest
from pathlib import Path

class ProjectLayoutTests(unittest.TestCase):
    def test_core_package_files_exist(self):
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "pychronicle" / "database.py").exists())
        self.assertTrue((root / "pychronicle" / "tracer" / "execution_tracer.py").exists())

if __name__ == "__main__":
    unittest.main()
