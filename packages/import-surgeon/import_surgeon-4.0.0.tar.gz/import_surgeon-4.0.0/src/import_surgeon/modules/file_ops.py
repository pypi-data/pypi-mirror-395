#!/usr/bin/env python3
# src/import_surgeon/modules/file_ops.py

import logging
import os
import stat
import tempfile
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path
from typing import List, Optional

from .encoding import detect_encoding

logger = logging.getLogger("import_surgeon")


def safe_backup(file_path: Path, backup_suffix: Optional[str] = None) -> Path:
    if backup_suffix is None:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        pid = os.getpid()
        backup_suffix = f".bak.{ts}.{pid}"
    backup_path = file_path.with_name(file_path.name + backup_suffix)
    if backup_path.exists():
        counter = 1
        while backup_path.exists():
            backup_path = file_path.with_name(
                file_path.name + backup_suffix + f".{counter}"
            )
            counter += 1
    encoding = detect_encoding(file_path)
    text = file_path.read_text(encoding=encoding)
    backup_path.write_text(text, encoding=encoding)
    try:
        st = file_path.stat()
        os.chmod(backup_path, st.st_mode)
        os.chown(backup_path, st.st_uid, st.st_gid)
    except Exception:
        logger.debug("Could not preserve metadata for backup: %s", backup_path)
    return backup_path


def atomic_write(file_path: Path, content: str, encoding: str = "utf-8") -> None:
    dirpath = file_path.parent
    tmpname = None
    try:
        st = file_path.stat() if file_path.exists() else None
        with tempfile.NamedTemporaryFile(
            "w", delete=False, dir=str(dirpath), encoding=encoding
        ) as tf:
            tf.write(content)
            tmpname = tf.name
        if st:
            os.chmod(tmpname, stat.S_IMODE(st.st_mode))
            try:
                os.chown(tmpname, st.st_uid, st.st_gid)
            except Exception:
                pass
        os.replace(tmpname, str(file_path))
    finally:
        if tmpname and os.path.exists(tmpname):
            try:
                os.remove(tmpname)
            except Exception:
                pass


def find_py_files(
    target: Path, excludes: List[str], max_files: int = 10000
) -> List[Path]:
    matches: List[Path] = []
    count = 0
    if (
        target.is_file()
        and target.suffix == ".py"
        and not any(fnmatch(str(target), exc) for exc in excludes)
    ):
        matches.append(target)
        return matches

    if target.is_dir():
        for p in target.rglob("*.py"):
            if count >= max_files:
                logger.warning(
                    "Reached max_files limit (%d); stopping scan.", max_files
                )
                break
            rel = str(p.relative_to(target))
            if any(fnmatch(rel, exc) or fnmatch(str(p), exc) for exc in excludes):
                continue
            matches.append(p)
            count += 1
    return matches
