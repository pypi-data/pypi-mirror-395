#!/usr/bin/env python3
# src/import_surgeon/modules/analysis.py

import re
from typing import List


def check_remaining_usages(
    content: str, old_module: str, symbols: List[str]
) -> List[str]:
    res = []
    for symbol in symbols:
        try:
            pattern = re.compile(rf"\b{re.escape(old_module)}\.{re.escape(symbol)}\b")
            matches = pattern.findall(content)
            if matches:
                res.append(
                    f"Potential remaining dotted usages for {symbol}: {len(matches)} instances"
                )
        except Exception:
            pass
    return res


def check_internal_dependencies(content: str, moving_symbols: List[str]) -> List[str]:
    """
    Analyzes the content to see if any of the moving_symbols are used
    within the file (which represents the old module). If they are used,
    moving them might break the module unless they are imported back.
    """
    warnings = []

    for symbol in moving_symbols:
        # We assume one match is the definition itself.
        # If there are 2+, potentially used.

        pattern = re.compile(rf"\b{re.escape(symbol)}\b")
        matches = pattern.findall(content)

        if len(matches) > 1:
             warnings.append(f"Moving '{symbol}' may break internal dependencies in the source file.")

    return warnings
