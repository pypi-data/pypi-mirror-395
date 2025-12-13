#!/usr/bin/env python3
# src/import_surgeon/modules/encoding.py

import logging
import tokenize as py_tokenize
from pathlib import Path

# Optional dependencies
HAS_CHARDET = True
try:
    from chardet.universaldetector import UniversalDetector
except ImportError:
    HAS_CHARDET = False
    UniversalDetector = None

logger = logging.getLogger("import_surgeon")


def detect_encoding(file_path: Path) -> str:
    try:
        with file_path.open("rb") as f:
            encoding, _ = py_tokenize.detect_encoding(f.readline)
            if encoding:
                return encoding.lower()
    except Exception:
        pass

    if HAS_CHARDET:
        detector = UniversalDetector()
        try:
            with file_path.open("rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    detector.feed(chunk)
                    if detector.done:
                        break
            detector.close()
            enc = detector.result.get("encoding")
            if enc:
                return enc.lower()
        except Exception:
            pass
    else:
        logger.debug("chardet unavailable; defaulting to utf-8 for %s", file_path)

    return "utf-8"
