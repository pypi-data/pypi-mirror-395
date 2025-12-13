#!/usr/bin/env python3
# src/import_surgeon/modules/config.py

import logging
from typing import Dict, Optional

import yaml

logger = logging.getLogger("import_surgeon")


def load_config(config_path: Optional[str]) -> Dict:
    if not config_path:
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.warning("Failed to load config %s: %s", config_path, e)
        return {}
