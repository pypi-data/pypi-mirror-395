#!/usr/bin/env python3
# tests/test_cli_extended.py

import unittest
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import io

from import_surgeon.cli import main, parse_args

class TestCliExtended(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_version_flag(self):
        """Test --version flag."""
        # argparse exits on --version, so we need to catch SystemExit
        with patch("sys.stdout", new=MagicMock()) as mock_stdout:
            with self.assertRaises(SystemExit):
                parse_args(["--version"])
            # We can't easily check output because argparse prints to stdout/stderr directly
            # but confirming it raises SystemExit is good enough

    @patch("import_surgeon.cli.tqdm")
    def test_tqdm_fallback(self, mock_tqdm):
        """Test tqdm fallback when import fails."""
        # We need to reload the module to trigger the fallback logic
        # But that's tricky with 'from ... import ...' style imports in tests
        # Instead, we can test the fallback function directly if we can access it

        # However, the fallback is defined inside the try/except block at module level.
        # Let's simulate ImportError by mocking sys.modules for a fresh import
        with patch.dict(sys.modules, {'tqdm': None}):
             # Reload cli
             import importlib
             import import_surgeon.cli
             importlib.reload(import_surgeon.cli)

             # Check if tqdm is the dummy function
             # The dummy function is a class instance that iterates over the iterable
             iterable = [1, 2, 3]
             dummy_tqdm = import_surgeon.cli.tqdm(iterable)
             self.assertEqual(list(dummy_tqdm), iterable)

             # Also verify it works as context manager
             with dummy_tqdm as pbar:
                 self.assertEqual(pbar, dummy_tqdm)

             # Restore
             importlib.reload(import_surgeon.cli)

    def test_rollback_no_summary_json(self):
        """Test rollback without summary-json argument."""
        with patch("logging.Logger.error") as mock_err:
            exit_code = main(["--rollback"])
            self.assertEqual(exit_code, 2)
            mock_err.assert_called_with("Missing --summary-json for rollback")

    def test_rollback_invalid_json(self):
        """Test rollback with invalid summary json file."""
        json_path = self.temp_path / "bad.json"
        json_path.write_text("{invalid json")

        with patch("logging.Logger.error") as mock_err:
            exit_code = main(["--rollback", "--summary-json", str(json_path)])
            self.assertEqual(exit_code, 1)
            self.assertTrue(any("Rollback failed" in str(call) for call in mock_err.mock_calls))

    @patch("import_surgeon.cli.process_file")
    @patch("import_surgeon.cli.find_py_files")
    def test_process_file_errors_counting(self, mock_find, mock_process):
        """Test error counting in main loop."""
        mock_find.return_value = [Path("file1.py"), Path("file2.py")]
        mock_process.side_effect = [
             (False, "ERROR: file1", {"warnings": []}),
             (False, "OK: file2", {"warnings": ["warn"]}),
             (True, "OK: file3", {"warnings": []})
        ]

        argv = ["--old-module", "old", "--new-module", "new", "--symbols", "S", str(self.temp_path)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)



    def test_main_missing_old_module_no_config(self):
        """Test main when --old-module is missing and no config migrations."""
        with patch("logging.Logger.error") as mock_err:
            argv = ["--new-module", "new", "--symbols", "S"]
            exit_code = main(argv)
            self.assertEqual(exit_code, 2)
            mock_err.assert_called_with("Missing required: --old-module or migrations in config")

    def test_main_missing_new_module_no_config(self):
        """Test main when --new-module is missing and no config migrations."""
        with patch("logging.Logger.error") as mock_err:
            argv = ["--old-module", "old", "--symbols", "S"]
            exit_code = main(argv)
            self.assertEqual(exit_code, 2)
            mock_err.assert_called_with("Missing required: --new-module or migrations in config")

    @patch("import_surgeon.modules.rollback.detect_encoding")
    @patch("import_surgeon.modules.rollback.atomic_write")
    @patch("os.remove")
    def test_main_rollback_original_file_missing(self, mock_os_remove, mock_atomic_write, mock_detect_encoding):
        """Test rollback when original file is missing but backup exists."""
        # Setup: Create a dummy backup file and a summary JSON
        original_file = self.temp_path / "test_file.py"
        backup_file = self.temp_path / "test_file.py.bak"
        summary_json_path = self.temp_path / "summary.json"

        backup_file.write_text("backup content")
        # Ensure original_file does NOT exist to trigger the missing file branch
        if original_file.exists():
            original_file.unlink()

        summary_data = {
            "summary": [
                {
                    "file": str(original_file),
                    "changed": True,
                    "backup": str(backup_file),
                    "message": "changed"
                }
            ],
            "timestamp": "2023-01-01T00:00:00Z"
        }
        summary_json_path.write_text(json.dumps(summary_data))

        # Mock detect_encoding to return a specific encoding
        mock_detect_encoding.return_value = "utf-8"

        exit_code = main(["--rollback", "--summary-json", str(summary_json_path)])

        self.assertEqual(exit_code, 0)
        mock_detect_encoding.assert_called_with(backup_file) # Should be called with backup file
        mock_atomic_write.assert_called_with(original_file, "backup content", "utf-8")
        mock_os_remove.assert_called_with(backup_file)

    @patch("import_surgeon.cli.process_file")
    @patch("import_surgeon.cli.find_py_files")
    @patch("import_surgeon.cli.print_logo") # Mock print_logo
    def test_main_summary_without_dry_run(self, mock_print_logo, mock_find, mock_process):
        """Test summary output when not in dry-run mode (--apply)."""
        mock_find.return_value = [Path("file1.py")]
        mock_process.return_value = (True, "OK: file1", {"warnings": []})

        argv = ["--old-module", "old", "--new-module", "new", "--symbols", "S", "--apply", str(self.temp_path)]

        with patch('builtins.print') as mock_print:
            main(argv)
            output_str = "".join([call.args[0] for call in mock_print.call_args_list if call.args])

        mock_print_logo.assert_called_once() # Ensure logo was supposed to be printed but got mocked

        self.assertIn("OK: file1", output_str)
        self.assertIn("Summary:", output_str)
        self.assertNotIn("Dry-run", output_str)
        self.assertIn("Changed: 1", output_str)
        self.assertIn("Errors: 0", output_str)
        self.assertIn("Warnings: 0", output_str)
        self.assertIn("Scanned: 1", output_str)

if __name__ == "__main__":
    unittest.main()
