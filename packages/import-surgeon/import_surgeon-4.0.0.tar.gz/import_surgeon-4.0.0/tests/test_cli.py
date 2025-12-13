#!/usr/bin/env python3
# tests/test_cli.py

import json
import logging
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import libcst as cst
import libcst.metadata as md
import yaml

import import_surgeon
# Import the script modules
from import_surgeon.cli import main, parse_args
from import_surgeon.modules.analysis import check_remaining_usages
from import_surgeon.modules.config import load_config
from import_surgeon.modules.cst_utils import (
    DottedReplacer,
    ImportReplacer,
    _attr_to_dotted,
    _import_alias_name,
    _module_to_str,
    _str_to_expr,
)
from import_surgeon.modules.encoding import detect_encoding
from import_surgeon.modules.file_ops import find_py_files
from import_surgeon.modules.git_ops import (
    find_git_root,
    git_commit_changes,
    git_is_clean,
)
from import_surgeon.modules.process import process_file

class TestSafeReplaceImports(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        logging.disable(logging.CRITICAL)  # Suppress logs during tests

    def tearDown(self):
        self.temp_dir.cleanup()
        logging.disable(logging.NOTSET)

    def test_main_missing_args(self):
        argv = ["."]
        with patch("logging.Logger.error") as mock_err:
            exit_code = main(argv)
            self.assertEqual(exit_code, 2)
            mock_err.assert_called()

    @patch("import_surgeon.cli.find_py_files", return_value=[])
    @patch(
        "import_surgeon.cli.process_file",
        return_value=(False, "UNCHANGED", {"warnings": []}),
    )
    @patch("builtins.print")
    def test_main_dry_run(self, mock_print, mock_process, mock_find):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            str(self.temp_path),
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    @patch("import_surgeon.cli.find_py_files", return_value=[Path("test.py")])
    @patch(
        "import_surgeon.cli.process_file",
        return_value=(True, "MODIFIED", {"warnings": []}),
    )
    @patch("import_surgeon.cli.git_is_clean", return_value=True)
    @patch("import_surgeon.cli.git_commit_changes", return_value=True)
    @patch("builtins.print")
    def test_main_apply_auto_commit(
        self, mock_print, mock_commit, mock_clean, mock_process, mock_find
    ):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            "--apply",
            "--auto-commit",
            "msg",
            "--require-clean-git",
            str(self.temp_path),
        ]
        with patch(
            "import_surgeon.cli.find_git_root", return_value=self.temp_path
        ):
            exit_code = main(argv)
            self.assertEqual(exit_code, 0)
            mock_commit.assert_called()

    @patch("import_surgeon.cli.find_py_files", return_value=[Path("test.py")])
    @patch(
        "import_surgeon.cli.process_file",
        return_value=(False, "ERROR", {"warnings": []}),
    )
    @patch("builtins.print")
    def test_main_errors(self, mock_print, mock_process, mock_find):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            str(self.temp_path),
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    @patch("import_surgeon.cli.find_py_files", return_value=[Path("test.py")])
    @patch(
        "import_surgeon.cli.process_file",
        return_value=(False, "SKIPPED", {"warnings": ["warn"]}),
    )
    @patch("builtins.print")
    def test_main_strict_warnings(self, mock_print, mock_process, mock_find):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            "--strict-warnings",
            str(self.temp_path),
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    @patch("import_surgeon.cli.find_py_files", return_value=[Path("test.py")])
    @patch(
        "import_surgeon.cli.process_file",
        return_value=(True, "CHANGED", {"warnings": []}),
    )
    @patch("json.dump")
    def test_main_summary_json(self, mock_json, mock_process, mock_find):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            "--summary-json",
            "out.json",
            str(self.temp_path),
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        mock_json.assert_called()

    @patch("import_surgeon.cli.git_is_clean", return_value=False)
    @patch("logging.Logger.error")
    def test_main_git_not_clean(self, mock_err, mock_clean):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            "--apply",
            "--require-clean-git",
            str(self.temp_path),
        ]
        with patch(
            "import_surgeon.cli.find_git_root", return_value=self.temp_path
        ):
            exit_code = main(argv)
            self.assertEqual(exit_code, 1)
            mock_err.assert_called_with(
                "Git not clean; commit/stash or remove --require-clean-git"
            )

    @patch("import_surgeon.cli.load_config", return_value={"old-module": "old"})
    def test_main_config_override(self, mock_load):
        argv = [
            "--config",
            "config.yaml",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            str(self.temp_path),
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    @patch(
        "import_surgeon.cli.load_config",
        return_value={"old-module": "old", "new-module": "newer"},
    )
    def test_main_config_override_selective(self, mock_load):
        argv = [
            "--config",
            "config.yaml",
            "--old-module",
            "myold",
            "--symbols",
            "Sym",
            str(self.temp_path),
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    # New test: Quiet mode not printing
    @patch("builtins.print")
    def test_process_file_quiet(self, mock_print):
        file_path = self.temp_path / "test.py"
        file_path.write_text("from old.mod import Symbol\n")
        migrations = [
            {"old_module": "old.mod", "new_module": "new.mod", "symbols": ["Symbol"]}
        ]
        changed, msg, detail = process_file(
            file_path, migrations, dry_run=True, quiet="all"
        )
        mock_print.assert_not_called()

    # New test: Summary JSON content
    @patch("import_surgeon.cli.find_py_files", return_value=[Path("test.py")])
    @patch(
        "import_surgeon.cli.process_file",
        return_value=(True, "CHANGED", {"warnings": [], "risk_level": "low"}),
    )
    @patch("json.dump")
    @patch("builtins.open", mock_open())
    def test_main_summary_json_content(self, mock_json, mock_process, mock_find):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            "--summary-json",
            "out.json",
            str(self.temp_path),
        ]
        main(argv)
        mock_json.assert_called_once()
        args, _ = mock_json.call_args
        summary = args[0]
        self.assertIn("summary", summary)
        self.assertIn("timestamp", summary)
        self.assertEqual(len(summary["summary"]), 1)
        entry = summary["summary"][0]
        self.assertTrue(entry["changed"])
        self.assertEqual(entry["risk_level"], "low")

    # New test: Auto-commit failure
    @patch("import_surgeon.cli.find_py_files", return_value=[Path("test.py")])
    @patch(
        "import_surgeon.cli.process_file",
        return_value=(True, "MODIFIED", {"warnings": []}),
    )
    @patch("import_surgeon.cli.git_is_clean", return_value=True)
    @patch("import_surgeon.cli.git_commit_changes", return_value=False)
    @patch("builtins.print")
    @patch("logging.Logger.info")
    def test_main_auto_commit_failure(
        self, mock_info, mock_print, mock_commit, mock_clean, mock_process, mock_find
    ):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            "--apply",
            "--auto-commit",
            "msg",
            str(self.temp_path),
        ]
        with patch(
            "import_surgeon.cli.find_git_root", return_value=self.temp_path
        ):
            exit_code = main(argv)
            self.assertEqual(exit_code, 0)
            mock_commit.assert_called()
            calls = mock_info.call_args_list
            self.assertFalse(
                any(call[0][0].startswith("Auto-committed") for call in calls)
            )  # No success message

    # New test: Main with migrations in config
    @patch(
        "import_surgeon.cli.load_config",
        return_value={
            "migrations": [
                {"old_module": "old", "new_module": "new", "symbols": ["Sym"]}
            ]
        },
    )
    @patch("import_surgeon.cli.find_py_files", return_value=[])
    @patch("import_surgeon.cli.process_file")
    def test_main_with_migrations_config(self, mock_process, mock_find, mock_load):
        argv = ["--config", "config.yaml", str(self.temp_path)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    # New test: Rollback success
    def test_main_rollback(self):
        summary_path = self.temp_path / "summary.json"
        file_path = self.temp_path / "test.py"
        backup_path = self.temp_path / "test.py.bak"
        file_path.write_text("modified")
        backup_path.write_text("original")
        summary_data = {
            "summary": [
                {"file": str(file_path), "changed": True, "backup": str(backup_path)}
            ]
        }
        with open(summary_path, "w") as f:
            json.dump(summary_data, f)
        argv = ["--rollback", "--summary-json", str(summary_path)]
        with patch("logging.Logger.info") as mock_info:
            exit_code = main(argv)
            self.assertEqual(exit_code, 0)
            self.assertEqual(file_path.read_text(), "original")
            self.assertFalse(backup_path.exists())

    # New test: Rollback missing backup
    def test_main_rollback_missing_backup(self):
        summary_path = self.temp_path / "summary.json"
        file_path = self.temp_path / "test.py"
        backup_path = self.temp_path / "missing.bak"
        summary_data = {
            "summary": [
                {"file": str(file_path), "changed": True, "backup": str(backup_path)}
            ]
        }
        with open(summary_path, "w") as f:
            json.dump(summary_data, f)
        argv = ["--rollback", "--summary-json", str(summary_path)]
        with patch("logging.Logger.warning") as mock_warn:
            exit_code = main(argv)
            self.assertEqual(exit_code, 0)
            mock_warn.assert_called_with("Backup missing for %s", file_path)

    # New test: Auto base_package detection
    @patch("import_surgeon.cli.find_py_files", return_value=[])
    @patch("import_surgeon.cli.process_file")
    @patch(
        "import_surgeon.cli.find_git_root", return_value=Path("/repo/myproject")
    )
    @patch("logging.Logger.info")
    def test_main_auto_base_package(
        self, mock_info, mock_root, mock_process, mock_find
    ):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            str(self.temp_path),
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        mock_info.assert_any_call("Auto-detected base_package: %s", "myproject")

    # New test: Main with --rewrite-dotted
    @patch("import_surgeon.cli.find_py_files", return_value=[Path("test.py")])
    @patch(
        "import_surgeon.cli.process_file",
        return_value=(True, "MODIFIED", {"warnings": []}),
    )
    def test_main_rewrite_dotted(self, mock_process, mock_find):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            "--rewrite-dotted",
            str(self.temp_path),
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        mock_process.assert_called_once()
        # With partial used in cli.py, arguments might be positional or kwargs depending on how partial was created
        # But we pass rewrite_dotted as kwarg to partial.
        # Check call_args.kwargs
        call_kwargs = mock_process.call_args.kwargs
        if "rewrite_dotted" in call_kwargs:
            self.assertTrue(call_kwargs["rewrite_dotted"])
        else:
             # Fallback if somehow passed positionally (though partial passes kwargs as kwargs usually)
             # signature: process_file(file_path, migrations, dry_run, no_backup, force_relative, base_package, rewrite_dotted, ...)
             # rewrite_dotted is index 6
             call_args = mock_process.call_args[0]
             self.assertTrue(call_args[6])

    # New test: Main with --format
    @patch("import_surgeon.cli.find_py_files", return_value=[Path("test.py")])
    @patch(
        "import_surgeon.cli.process_file",
        return_value=(True, "MODIFIED", {"warnings": []}),
    )
    def test_main_format(self, mock_process, mock_find):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            "--format",
            str(self.temp_path),
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        mock_process.assert_called_once()
        call_kwargs = mock_process.call_args.kwargs
        if "do_format" in call_kwargs:
            self.assertTrue(call_kwargs["do_format"])
        else:
             call_args = mock_process.call_args[0]
             self.assertTrue(call_args[7])  # do_format=True

    # New test: Rollback with non-UTF8 encoding
    def test_main_rollback_non_utf8(self):
        summary_path = self.temp_path / "summary.json"
        file_path = self.temp_path / "test.py"
        backup_path = self.temp_path / "test.py.bak"
        latin_content = b"# -*- coding: latin-1 -*-\nprint('\xe9')\n"
        file_path.write_bytes(latin_content + b"# modified")
        backup_path.write_bytes(latin_content)
        summary_data = {
            "summary": [
                {"file": str(file_path), "changed": True, "backup": str(backup_path)}
            ]
        }
        with open(summary_path, "w") as f:
            json.dump(summary_data, f)
        argv = ["--rollback", "--summary-json", str(summary_path)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        enc = detect_encoding(file_path)
        self.assertIn(enc, ["latin-1", "iso-8859-1", "latin1"])
        self.assertEqual(file_path.read_bytes(), latin_content)
        self.assertFalse(backup_path.exists())

    # New test: Interrupted apply (partial failure during multi-file processing)
    @patch(
        "import_surgeon.cli.find_py_files",
        return_value=[Path("good.py"), Path("bad.py")],
    )
    @patch("import_surgeon.cli.process_file")
    @patch("builtins.print")
    def test_main_partial_failure(self, mock_print, mock_process, mock_find):
        mock_process.side_effect = [
            (True, "MODIFIED: good.py", {"warnings": []}),
            (False, "ERROR: bad.py: fail", {"warnings": ["Error: fail"]}),
        ]
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym",
            "--apply",
            str(self.temp_path),
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)  # Exits with error due to failure
        self.assertEqual(mock_process.call_count, 2)  # Processes all files


if __name__ == "__main__":
    unittest.main()
