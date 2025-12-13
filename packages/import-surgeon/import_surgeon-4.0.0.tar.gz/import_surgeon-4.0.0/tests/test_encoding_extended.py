#!/usr/bin/env python3
# tests/test_encoding_extended.py

import unittest
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock
from import_surgeon.modules import encoding as encoding_module
from import_surgeon.modules.encoding import detect_encoding

class TestEncodingExtended(unittest.TestCase):
    def test_import_error_chardet(self):
        """Test behavior when chardet is missing (ImportError)."""
        with patch.dict(sys.modules, {'chardet.universaldetector': None}):
            # Reload the module to trigger ImportError handling
            import importlib
            importlib.reload(encoding_module)
            self.assertFalse(encoding_module.HAS_CHARDET)
            self.assertIsNone(encoding_module.UniversalDetector)

        # Restore
        importlib.reload(encoding_module)

    @patch("import_surgeon.modules.encoding.py_tokenize.detect_encoding")
    def test_detect_encoding_exception_in_tokenize(self, mock_tokenize):
        """Test exception handling in py_tokenize.detect_encoding."""
        mock_tokenize.side_effect = Exception("Tokenize error")

        # Create a dummy file
        file_path = Path("dummy.py")
        with patch("pathlib.Path.open", MagicMock()) as mock_open:
             # Ensure fallback logic is triggered or it returns default "utf-8"
             # We need to ensure chardet also fails or is mocked to not return anything to test full path
             with patch("import_surgeon.modules.encoding.HAS_CHARDET", False):
                 enc = detect_encoding(file_path)
                 self.assertEqual(enc, "utf-8")

    @patch("import_surgeon.modules.encoding.HAS_CHARDET", True)
    @patch("import_surgeon.modules.encoding.py_tokenize.detect_encoding")
    @patch("import_surgeon.modules.encoding.UniversalDetector")
    def test_detect_encoding_exception_in_chardet(self, mock_detector_cls, mock_tokenize):
        """Test exception handling in chardet block."""
        # py_tokenize fails
        mock_tokenize.side_effect = Exception("Tokenize error")

        # chardet detector throws exception during feed/read
        mock_detector = mock_detector_cls.return_value
        mock_detector.feed.side_effect = Exception("Chardet error")

        file_path = Path("dummy.py")
        with patch("pathlib.Path.open", MagicMock()) as mock_open:
            # Mock file read to return something so loop runs
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.read.side_effect = [b"some data", b""]

            enc = detect_encoding(file_path)
            self.assertEqual(enc, "utf-8")

    @patch("import_surgeon.modules.encoding.HAS_CHARDET", True)
    @patch("import_surgeon.modules.encoding.py_tokenize.detect_encoding")
    @patch("import_surgeon.modules.encoding.UniversalDetector")
    def test_detect_encoding_chardet_done_early(self, mock_detector_cls, mock_tokenize):
        """Test chardet loop break when detector.done is True."""
        mock_tokenize.side_effect = Exception("Tokenize error")

        mock_detector = mock_detector_cls.return_value
        mock_detector.done = True # Done immediately
        mock_detector.result = {"encoding": "windows-1252"}

        file_path = Path("dummy.py")
        with patch("pathlib.Path.open", MagicMock()) as mock_open:
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.read.return_value = b"data"

            enc = detect_encoding(file_path)
            self.assertEqual(enc, "windows-1252")

    @patch("import_surgeon.modules.encoding.HAS_CHARDET", False)
    @patch("import_surgeon.modules.encoding.py_tokenize.detect_encoding")
    def test_detect_encoding_no_chardet_log(self, mock_tokenize):
        """Test logging when chardet is unavailable."""
        mock_tokenize.side_effect = Exception("Tokenize error")

        file_path = Path("dummy.py")
        with patch("pathlib.Path.open", MagicMock()):
            with self.assertLogs("import_surgeon", level="DEBUG") as cm:
                enc = detect_encoding(file_path)
                self.assertEqual(enc, "utf-8")
                self.assertTrue(any("chardet unavailable" in output for output in cm.output))

if __name__ == "__main__":
    unittest.main()
