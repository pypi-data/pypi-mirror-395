#!/usr/bin/env python3
# tests/test_file_ops.py

import tempfile
import unittest
from pathlib import Path

from import_surgeon.modules.file_ops import find_py_files


class TestFileOps(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    # Test find_py_files (unchanged)
    def test_find_py_files_dir(self):
        (self.temp_path / "a.py").touch()
        (self.temp_path / "b.txt").touch()
        (self.temp_path / "sub").mkdir()
        (self.temp_path / "sub" / "c.py").touch()
        files = find_py_files(self.temp_path, [])
        self.assertEqual(len(files), 2)
        self.assertIn(self.temp_path / "a.py", files)
        self.assertIn(self.temp_path / "sub" / "c.py", files)

    def test_find_py_files_single_file(self):
        file_path = self.temp_path / "test.py"
        file_path.touch()
        files = find_py_files(file_path, [])
        self.assertEqual(files, [file_path])

    def test_find_py_files_excludes(self):
        (self.temp_path / "a.py").touch()
        (self.temp_path / "tests").mkdir(exist_ok=True)
        (self.temp_path / "tests" / "b.py").touch()
        files = find_py_files(self.temp_path, ["tests/*"])
        self.assertEqual(len(files), 1)
        self.assertIn(self.temp_path / "a.py", files)

    def test_find_py_files_max_files(self):
        for i in range(5):
            (self.temp_path / f"{i}.py").touch()
        files = find_py_files(self.temp_path, [], max_files=3)
        self.assertEqual(len(files), 3)


if __name__ == "__main__":
    unittest.main()
