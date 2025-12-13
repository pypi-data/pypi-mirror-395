#!/usr/bin/env python3
# tests/test_error_handling.py

import tempfile
import unittest
from pathlib import Path

from import_surgeon.modules.process import process_file


class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_syntax_error_suggestion(self):
        """Test that syntax errors return a helpful suggestion."""
        file_path = self.temp_path / "bad_syntax.py"
        # Write invalid Python syntax
        file_path.write_text("def invalid_syntax(:\n    pass\n")

        migrations = [
            {"old_module": "old", "new_module": "new", "symbols": ["Symbol"]}
        ]

        changed, msg, detail = process_file(file_path, migrations, dry_run=True)

        self.assertFalse(changed)
        self.assertIn("ERROR", msg)
        # Check for specific suggestion
        self.assertIn("Suggestion: The file contains invalid Python syntax", msg)

    def test_encoding_error_suggestion(self):
        """Test that encoding errors return a helpful suggestion."""
        file_path = self.temp_path / "bad_encoding.py"
        # Write invalid UTF-8 bytes
        with open(file_path, "wb") as f:
            f.write(b"\x80\x81\x82")

        migrations = [
            {"old_module": "old", "new_module": "new", "symbols": ["Symbol"]}
        ]

        changed, msg, detail = process_file(file_path, migrations, dry_run=True)

        self.assertFalse(changed)
        self.assertIn("ERROR", msg)
        # Check for specific suggestion
        self.assertIn("Suggestion: The file encoding could not be detected or is invalid", msg)

if __name__ == "__main__":
    unittest.main()
