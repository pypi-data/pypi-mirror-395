#!/usr/bin/env python3
# tests/test_file_ops_extended.py

import unittest
import os
import stat
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, call

from import_surgeon.modules.file_ops import safe_backup, atomic_write, find_py_files

class TestFileOpsExtended(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_safe_backup_collision(self):
        """Test backup name collision resolution."""
        f = self.temp_path / "test.py"
        f.write_text("original")

        # Create existing backups
        # First one is suffix based on time/pid, so we mock that
        with patch("import_surgeon.modules.file_ops.datetime") as mock_dt, \
             patch("import_surgeon.modules.file_ops.os.getpid") as mock_pid:
            mock_dt.now.return_value.strftime.return_value = "20230101"
            mock_pid.return_value = 1234
            suffix = ".bak.20230101.1234"

            # Create the primary backup
            (self.temp_path / f"test.py{suffix}").touch()
            # Create the first indexed backup
            (self.temp_path / f"test.py{suffix}.1").touch()

            backup_path = safe_backup(f)

            expected = self.temp_path / f"test.py{suffix}.2"
            self.assertEqual(backup_path, expected)
            self.assertTrue(backup_path.exists())

    @patch("os.chmod")
    @patch("os.chown")
    def test_safe_backup_metadata_fail(self, mock_chown, mock_chmod):
        """Test failure to preserve metadata during backup."""
        f = self.temp_path / "test.py"
        f.write_text("content")

        # Raise exception during chmod
        mock_chmod.side_effect = OSError("Chmod failed")

        with self.assertLogs("import_surgeon", level="DEBUG") as cm:
            backup_path = safe_backup(f)
            self.assertTrue(backup_path.exists())
            self.assertTrue(any("Could not preserve metadata" in msg for msg in cm.output))

    def test_atomic_write_metadata_success(self):
        """Test atomic write with metadata preservation."""
        f = self.temp_path / "test.py"
        f.write_text("old")

        # We can't easily test chown as non-root, but we can test chmod
        # Change permission to something distinctive if possible, or just ensure code runs
        try:
            f.chmod(0o700)
        except OSError:
            pass # Skip if not allowed

        original_stat = f.stat()
        atomic_write(f, "new content")

        self.assertEqual(f.read_text(), "new content")
        # Check permission bits match if possible on this platform
        self.assertEqual(stat.S_IMODE(f.stat().st_mode), stat.S_IMODE(original_stat.st_mode) if os.name != 'nt' else stat.S_IMODE(f.stat().st_mode))

    @patch("os.chown")
    def test_atomic_write_chown_fail(self, mock_chown):
        """Test atomic write ignoring chown errors."""
        f = self.temp_path / "test.py"
        f.write_text("old")
        mock_chown.side_effect = OSError("Chown fail")

        atomic_write(f, "new content")
        self.assertEqual(f.read_text(), "new content")

    @patch("os.remove")
    def test_atomic_write_cleanup_fail(self, mock_remove):
        """Test atomic write ignoring temp file cleanup errors."""
        f = self.temp_path / "test.py"
        f.write_text("old")

        # Simulate remove failure
        mock_remove.side_effect = OSError("Remove fail")

        # To verify cleanup was attempted, we can inspect mock calls?
        # But os.remove is called in finally block.
        # atomic_write uses NamedTemporaryFile(delete=False), so it definitely tries to remove it.
        # We need to ensure it raises exception on remove BUT the function catches it.

        # We need to make sure the temp file exists so the `if tmpname and os.path.exists(tmpname):` check passes
        # However, NamedTemporaryFile creates it. os.replace moves it.
        # Wait, if os.replace succeeds, tmpname no longer exists at the old path!
        # So cleanup only happens if os.replace FAILS.

        with patch("os.replace") as mock_replace:
            mock_replace.side_effect = OSError("Replace fail")
            try:
                atomic_write(f, "new")
            except OSError:
                pass # Expected

            # Now verify os.remove was called and exception suppressed
            self.assertTrue(mock_remove.called)

    def test_find_py_files_non_py_target(self):
        """Test find_py_files with a single non-python file target."""
        f = self.temp_path / "test.txt"
        f.touch()
        files = find_py_files(f, [])
        self.assertEqual(files, [])

    def test_find_py_files_exclude_relative(self):
        """Test find_py_files excluding relative path."""
        d = self.temp_path / "subdir"
        d.mkdir()
        f1 = d / "keep.py"
        f2 = d / "skip.py"
        f1.touch()
        f2.touch()

        # Exclude by filename relative to target
        files = find_py_files(d, ["skip.py"])
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], f1)

    def test_find_py_files_exclude_absolute(self):
        """Test find_py_files excluding absolute path glob."""
        d = self.temp_path / "subdir"
        d.mkdir()
        f1 = d / "keep.py"
        f2 = d / "skip.py"
        f1.touch()
        f2.touch()

        # Exclude by full path glob
        files = find_py_files(d, [str(f2)])
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], f1)

if __name__ == "__main__":
    unittest.main()
