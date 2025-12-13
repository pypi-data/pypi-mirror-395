#!/usr/bin/env python3
# tests/test_encoding.py

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from import_surgeon.modules.encoding import detect_encoding


class TestEncoding(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    # Test encoding helpers
    def test_detect_encoding_utf8(self):
        file_path = self.temp_path / "test.py"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# coding: utf-8\nprint('hello')")
        enc = detect_encoding(file_path)
        self.assertEqual(enc, "utf-8")

    def test_detect_encoding_no_declaration(self):
        file_path = self.temp_path / "test.py"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("print('hello')")
        enc = detect_encoding(file_path)
        self.assertEqual(enc, "utf-8")  # Default fallback

    @patch("import_surgeon.modules.encoding.HAS_CHARDET", True)
    @patch(
        "import_surgeon.modules.encoding.py_tokenize.detect_encoding",
        return_value=(None, []),
    )
    @patch("import_surgeon.modules.encoding.UniversalDetector")
    def test_detect_encoding_chardet(self, mock_detector, mock_tokenize):
        mock_inst = mock_detector.return_value
        mock_inst.result = {"encoding": "ascii"}
        file_path = self.temp_path / "test.py"
        file_path.write_bytes(b"print('hello')")
        enc = detect_encoding(file_path)
        self.assertEqual(enc, "ascii")

    # New test: Non-UTF8 encoding
    def test_detect_encoding_latin1(self):
        file_path = self.temp_path / "test.py"
        with open(file_path, "wb") as f:
            f.write(b"# -*- coding: latin-1 -*-\nprint('\xe9')")
        enc = detect_encoding(file_path)
        self.assertIn(enc, ["latin-1", "iso-8859-1", "latin1"])
        content = file_path.read_text(encoding=enc)
        self.assertIn("\xe9", content)


if __name__ == "__main__":
    unittest.main()
