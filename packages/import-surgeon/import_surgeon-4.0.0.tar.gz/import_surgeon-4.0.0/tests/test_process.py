
import pytest
import shutil
import tempfile
import subprocess
from unittest.mock import patch, MagicMock
from pathlib import Path
from import_surgeon.modules.process import process_file
import libcst as cst

class TestProcess:
    @pytest.fixture
    def temp_path(self, temp_workspace):
        # We can use the conftest fixture or create one here if needed.
        # But `temp_workspace` is already available from conftest if I defined it there.
        # Since I defined `temp_workspace` in conftest.py, I can use it directly.
        return temp_workspace

    def test_process_file_change(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("from old.mod import Symbol\n")
        migrations = [
            {"old_module": "old.mod", "new_module": "new.mod", "symbols": ["Symbol"]}
        ]
        changed, msg, detail = process_file(file_path, migrations, dry_run=True)
        assert changed
        assert "CHANGES IN" in msg
        assert "diff" in detail
        assert detail["risk_level"] == "low"

    def test_process_file_no_change(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("from new.mod import Symbol\n")
        migrations = [
            {"old_module": "old.mod", "new_module": "new.mod", "symbols": ["Symbol"]}
        ]
        changed, msg, detail = process_file(file_path, migrations, dry_run=True)
        assert not changed
        assert "UNCHANGED" in msg

    def test_process_file_apply_backup(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("from old.mod import Symbol\n")
        migrations = [
            {"old_module": "old.mod", "new_module": "new.mod", "symbols": ["Symbol"]}
        ]
        changed, msg, detail = process_file(
            file_path, migrations, dry_run=False, no_backup=False
        )
        assert changed
        assert "MODIFIED" in msg
        assert "backup" in detail
        assert file_path.read_text() == "from new.mod import Symbol\n"

    def test_process_file_star_warning(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("from old.mod import *\n")
        migrations = [
            {"old_module": "old.mod", "new_module": "new.mod", "symbols": ["Symbol"]}
        ]
        changed, msg, detail = process_file(file_path, migrations, dry_run=True)
        assert changed
        assert detail["risk_level"] == "medium"
        assert "Handled wildcard import" in detail["warnings"]

    def test_process_file_relative_skip(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("from .old import Symbol\n")
        migrations = [{"old_module": "old", "new_module": "new", "symbols": ["Symbol"]}]
        changed, msg, detail = process_file(file_path, migrations, dry_run=True)
        assert not changed
        assert "SKIPPED (relative)" in msg
        assert detail["risk_level"] == "high"

    def test_process_file_dotted_warning(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("from old.mod import Symbol\nold.mod.Symbol\n")
        migrations = [
            {"old_module": "old.mod", "new_module": "new.mod", "symbols": ["Symbol"]}
        ]
        changed, msg, detail = process_file(file_path, migrations, dry_run=True)
        assert changed
        assert detail["risk_level"] == "high"
        assert "Potential remaining dotted usages for Symbol: 1 instances" in detail["warnings"]

    def test_process_file_error(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("invalid syntax")
        migrations = [{"old_module": "old", "new_module": "new", "symbols": ["Symbol"]}]
        # Mocking libcst.parse_module to raise SyntaxError is tricky because it might raise ParserSyntaxError
        # or just fail if we don't mock it and let it run on invalid syntax.
        # But libcst.parse_module raises ParserSyntaxError on invalid syntax.
        # The code catches ParserSyntaxError.

        # Let's rely on actual libcst behavior for syntax error
        changed, msg, detail = process_file(file_path, migrations)
        assert not changed
        assert "ERROR" in msg
        # ParserSyntaxError message usually contains "Syntax Error"
        assert any("Syntax Error" in w for w in detail["warnings"])

    def test_process_file_rewrite_dotted(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("a = old.mod.Symbol\n")
        migrations = [
            {"old_module": "old.mod", "new_module": "new.mod", "symbols": ["Symbol"]}
        ]
        changed, msg, detail = process_file(
            file_path, migrations, dry_run=False, rewrite_dotted=True
        )
        assert changed
        assert "MODIFIED" in msg
        assert file_path.read_text() == "a = new.mod.Symbol\n"
        assert "Rewrote 1 dotted usages" in detail["warnings"][0]
        assert detail["risk_level"] == "medium"

    def test_process_file_multiple_migrations(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("from mod1 import Sym1\nfrom mod2 import Sym2\n")
        migrations = [
            {"old_module": "mod1", "new_module": "new1", "symbols": ["Sym1"]},
            {"old_module": "mod2", "new_module": "new2", "symbols": ["Sym2"]},
        ]
        changed, msg, detail = process_file(file_path, migrations, dry_run=False)
        assert changed
        content = file_path.read_text()
        assert "from new1 import Sym1" in content
        assert "from new2 import Sym2" in content

    def test_process_file_format(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("from old.mod import Symbol\n")
        migrations = [
            {"old_module": "old.mod", "new_module": "new.mod", "symbols": ["Symbol"]}
        ]
        with patch("subprocess.run") as mock_run:
            changed, msg, detail = process_file(
                file_path, migrations, dry_run=False, do_format=True
            )
            assert changed
            # Verify calls
            # We can check if isort and black were called
            cmds = [call.args[0][0] for call in mock_run.call_args_list]
            assert "isort" in cmds
            assert "black" in cmds

    def test_process_file_format_fail(self, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("from old.mod import Symbol\n")
        migrations = [
            {"old_module": "old.mod", "new_module": "new.mod", "symbols": ["Symbol"]}
        ]
        with patch("subprocess.run", side_effect=Exception("fail")):
            changed, msg, detail = process_file(
                file_path, migrations, dry_run=False, do_format=True
            )
            assert changed
            assert "Formatting failed" in detail["warnings"][0]

    @patch("builtins.print")
    def test_process_file_quiet(self, mock_print, temp_path):
        file_path = temp_path / "test.py"
        file_path.write_text("from old.mod import Symbol\n")
        migrations = [
            {"old_module": "old.mod", "new_module": "new.mod", "symbols": ["Symbol"]}
        ]
        changed, msg, detail = process_file(
            file_path, migrations, dry_run=True, quiet="all"
        )
        mock_print.assert_not_called()
