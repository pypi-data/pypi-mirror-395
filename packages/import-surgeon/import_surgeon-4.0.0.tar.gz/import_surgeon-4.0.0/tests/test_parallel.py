
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from concurrent.futures import Future
import pytest
from import_surgeon.cli import main

@pytest.fixture
def mock_executor():
    with patch("concurrent.futures.ProcessPoolExecutor") as mock_executor:
        mock_instance = mock_executor.return_value
        mock_instance.__enter__.return_value = mock_instance
        yield mock_executor

def test_parallel_execution_trigger(mock_executor, temp_workspace):
    """
    Test that --jobs > 1 triggers parallel execution path.
    We mock ProcessPoolExecutor to verify it's used.
    """
    (temp_workspace / "a.py").write_text("import old.pkg", encoding="utf-8")
    (temp_workspace / "b.py").write_text("import old.pkg", encoding="utf-8")

    argv = [
        str(temp_workspace),
        "--old-module", "old.pkg",
        "--new-module", "new.pkg",
        "--symbol", "Sym",
        "--jobs", "2",
    ]

    # Create a real Future that is already done
    f = Future()
    f.set_result((False, "UNCHANGED", {"warnings": []}))

    # Return this future for every submit call
    mock_instance = mock_executor.return_value
    mock_instance.submit.return_value = f

    ret = main(argv)
    assert ret == 0, "Main exited with non-zero code"

    mock_executor.assert_called()
    assert mock_instance.submit.call_count >= 2

def test_parallel_argument_parsing(temp_workspace):
    """
    Simple test to check if --jobs argument is accepted.
    """
    (temp_workspace / "a.py").write_text("import old", encoding="utf-8")
    argv = [
        str(temp_workspace),
        "--old-module", "old",
        "--new-module", "new",
        "--symbol", "S",
        "--jobs", "4"
    ]

    ret = main(argv)
    assert ret == 0
