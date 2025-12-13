#!/usr/bin/env python3
# tests/test_cli_args.py

import unittest
from import_surgeon.cli import parse_args

class TestCliArgs(unittest.TestCase):
    def test_parse_args(self):
        argv = [
            "--old-module",
            "old",
            "--new-module",
            "new",
            "--symbols",
            "Sym1,Sym2",
            ".",
        ]
        args = parse_args(argv)
        self.assertEqual(args.old_module, "old")
        self.assertEqual(args.new_module, "new")
        self.assertEqual(args.symbols, "Sym1,Sym2")
        self.assertEqual(args.target, ".")

if __name__ == "__main__":
    unittest.main()
