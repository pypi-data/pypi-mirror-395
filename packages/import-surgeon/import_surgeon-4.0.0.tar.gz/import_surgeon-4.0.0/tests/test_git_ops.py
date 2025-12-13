#!/usr/bin/env python3
# tests/test_git_ops.py

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from import_surgeon.modules.git_ops import (
    find_git_root,
    git_commit_changes,
    git_is_clean,
)


class TestGitOps(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    # Test safety checks
    @patch("import_surgeon.modules.git_ops.find_git_root", return_value=Path("/tmp"))
    @patch("subprocess.run")
    def test_git_is_clean(self, mock_run, mock_find):
        mock_run.return_value = MagicMock(stdout="")
        self.assertTrue(git_is_clean(self.temp_path))

    @patch("import_surgeon.modules.git_ops.find_git_root", return_value=Path("/tmp"))
    @patch("subprocess.run")
    def test_git_is_clean_dirty(self, mock_run, mock_find):
        mock_run.return_value = MagicMock(stdout="M file.py")
        self.assertFalse(git_is_clean(self.temp_path))

    @patch("import_surgeon.modules.git_ops.find_git_root", return_value=None)
    def test_git_is_clean_no_repo(self, mock_find):
        self.assertFalse(git_is_clean(self.temp_path))

    @patch("import_surgeon.modules.git_ops.find_git_root", return_value=Path("/tmp"))
    @patch("subprocess.run", side_effect=Exception("Git command failed"))
    def test_git_is_clean_exception(self, mock_run, mock_find):
        with self.assertLogs('import_surgeon', level='DEBUG') as cm:
            self.assertFalse(git_is_clean(self.temp_path))
            self.assertIn("Git check failed: Git command failed", cm.output[0])

    def test_find_git_root(self):
        git_dir = self.temp_path / ".git"
        git_dir.mkdir()
        self.assertEqual(find_git_root(self.temp_path), self.temp_path)

    def test_find_git_root_in_parent(self):
        git_dir = self.temp_path / ".git"
        git_dir.mkdir()
        sub_dir = self.temp_path / "sub"
        sub_dir.mkdir()
        self.assertEqual(find_git_root(sub_dir), self.temp_path)

    def test_find_git_root_none(self):
        self.assertIsNone(find_git_root(self.temp_path))

    @patch("subprocess.run")
    def test_git_commit_changes_success(self, mock_run):
        mock_run.return_value = MagicMock()
        self.assertTrue(git_commit_changes(self.temp_path, "msg"))

    @patch("subprocess.run", side_effect=Exception("fail"))
    def test_git_commit_changes_fail(self, mock_run):
        with patch("logging.Logger.error") as mock_err:
            self.assertFalse(git_commit_changes(self.temp_path, "msg"))
            mock_err.assert_called()


if __name__ == "__main__":
    unittest.main()
