from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from .encoding import detect_encoding
from .file_ops import atomic_write

logger = logging.getLogger("import_surgeon")


def perform_rollback(summary_json_path: str) -> bool:
    """
    Performs rollback based on the provided summary JSON file.

    Args:
        summary_json_path: Path to the summary JSON file generated during a previous run.

    Returns:
        True if rollback was successful, False otherwise.
    """
    if not summary_json_path:
        logger.error("Missing --summary-json for rollback")
        return False

    try:
        with open(summary_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for entry in data["summary"]:
            if entry.get("changed") and entry.get("backup"):
                bkp = Path(entry["backup"])
                file = Path(entry["file"])
                if bkp.exists():
                    encoding = (
                        detect_encoding(file)
                        if file.exists()
                        else detect_encoding(bkp)
                    )
                    atomic_write(file, bkp.read_text(encoding), encoding)
                    os.remove(bkp)
                    logger.info("Restored %s from %s", file, bkp)
                else:
                    logger.warning("Backup missing for %s", file)
        logger.info("Rollback completed")
        return True
    except Exception as e:
        logger.error("Rollback failed: %s", e)
        return False
