#!/usr/bin/env python3
# tests/test_config.py

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml
from import_surgeon.modules.config import load_config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    # Test config helpers
    def test_load_config_valid(self):
        config_path = self.temp_path / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump({"old-module": "old"}, f)
        config = load_config(str(config_path))
        self.assertEqual(config, {"old-module": "old"})

    def test_load_config_invalid(self):
        config_path = self.temp_path / "invalid.yaml"
        with open(config_path, "w") as f:
            f.write("invalid: yaml: here")
        with patch("logging.Logger.warning") as mock_warn:
            config = load_config(str(config_path))
            self.assertEqual(config, {})
            mock_warn.assert_called()

    def test_load_config_missing(self):
        config = load_config(None)
        self.assertEqual(config, {})


if __name__ == "__main__":
    unittest.main()
