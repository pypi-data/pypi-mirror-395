#!/usr/bin/env python3
# src/import_surgeon/modules/git_ops.py

import logging
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger("import_surgeon")


def git_is_clean(path: Path) -> bool:
    try:
        repo_root = find_git_root(path)
        if not repo_root:
            return False
        p = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
        return not p.stdout.strip()
    except Exception as e:
        logger.debug("Git check failed: %s", e)
        return False


def find_git_root(path: Path) -> Optional[Path]:
    current = path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return None


def git_commit_changes(repo_root: Path, message: str) -> bool:
    try:
        subprocess.run(
            ["git", "-C", str(repo_root), "add", "."], check=True, capture_output=True
        )
        subprocess.run(
            ["git", "-C", str(repo_root), "commit", "-m", message],
            check=True,
            capture_output=True,
        )
        return True
    except Exception as e:
        logger.error("Auto-commit failed: %s", e)
        return False
