#!/usr/bin/env python3
# src/import_surgeon/modules/process.py

import difflib
import logging
import os
import subprocess
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import libcst as cst
import libcst.metadata as md
from libcst import ParserSyntaxError

from .analysis import check_remaining_usages, check_internal_dependencies
from .cst_utils import DottedReplacer, ImportReplacer
from .encoding import detect_encoding
from .file_ops import atomic_write, safe_backup

logger = logging.getLogger("import_surgeon")


def process_file(
    file_path: Path,
    migrations: List[Dict],
    dry_run: bool = True,
    no_backup: bool = False,
    force_relative: bool = False,
    base_package: Optional[str] = None,
    rewrite_dotted: bool = False,
    do_format: bool = False,
    quiet: str = "none",
) -> Tuple[bool, str, Dict]:
    detail: Dict = {
        "diff": None,
        "backup": None,
        "encoding": None,
        "risk_level": "low",
        "changed_lines": [],
        "warnings": [],
    }
    try:
        encoding = detect_encoding(file_path)
        detail["encoding"] = encoding
        original_content = file_path.read_text(encoding=encoding)
        wrapper = md.MetadataWrapper(cst.parse_module(original_content))
        current = wrapper.module
        all_warnings: List[str] = []
        all_changed_lines: List[int] = []
        risk_levels = {"low": 0, "medium": 1, "high": 2}
        current_risk = 0
        skipped_relative = False
        for mig in migrations:
            old_module = mig["old_module"]
            new_module = mig["new_module"]
            symbols = (
                mig["symbols"] if isinstance(mig["symbols"], list) else [mig["symbols"]]
            )
            replacer = ImportReplacer(
                old_module, new_module, symbols, force_relative, base_package, file_path
            )
            wrapper = md.MetadataWrapper(current)
            current = wrapper.visit(replacer)
            all_warnings.extend(replacer.warnings)
            all_changed_lines.extend(replacer.changed_lines)
            if replacer.has_star_old or "wildcard" in " ".join(replacer.warnings):
                current_risk = max(current_risk, 1)
            if replacer.skipped_relative:
                skipped_relative = True
                current_risk = max(current_risk, 2)
            if rewrite_dotted:
                dotted_replacer = DottedReplacer(
                    old_module,
                    new_module,
                    symbols,
                    force_relative,
                    base_package,
                    file_path,
                )
                wrapper = md.MetadataWrapper(current)
                current = wrapper.visit(dotted_replacer)
                all_warnings.extend(dotted_replacer.warnings)
                all_changed_lines.extend(dotted_replacer.changed_lines)
                if dotted_replacer.rewrote_count > 0:
                    current_risk = max(current_risk, 1)
        new_content = current.code
        changed_flag = new_content != original_content
        detail["changed_lines"] = sorted(set(all_changed_lines))
        dotted_warnings = []
        internal_dep_warnings = []
        content_to_check = original_content if dry_run else new_content

        for mig in migrations:
            symbols = (
                mig["symbols"] if isinstance(mig["symbols"], list) else [mig["symbols"]]
            )
            dotted_warnings.extend(
                check_remaining_usages(content_to_check, mig["old_module"], symbols)
            )

            # Internal dependency check: verify if moving a symbol breaks usage in the source module
            # We verify if file path matches old_module converted to path.
            old_mod_path_suffix = mig["old_module"].replace(".", os.sep)

            is_match = False
            # Possible file paths for the module: module.py or module/__init__.py
            candidates = [f"{old_mod_path_suffix}.py", f"{old_mod_path_suffix}{os.sep}__init__.py"]

            path_str = str(file_path)
            for cand in candidates:
                # Check for exact match or suffix match with separator (e.g. /path/to/module.py)
                if path_str == cand or path_str.endswith(os.sep + cand):
                    is_match = True
                    break

            if is_match:
                 dep_warnings = check_internal_dependencies(content_to_check, symbols)
                 internal_dep_warnings.extend(dep_warnings)

        if dotted_warnings or internal_dep_warnings:
            current_risk = max(current_risk, 2)
        detail["warnings"] = all_warnings + dotted_warnings + internal_dep_warnings
        detail["risk_level"] = list(risk_levels.keys())[current_risk]
        if changed_flag:
            diff = "\n".join(
                difflib.unified_diff(
                    original_content.splitlines(),
                    new_content.splitlines(),
                    fromfile=str(file_path),
                    tofile=str(file_path) + " (modified)",
                    lineterm="",
                )
            )
            detail["diff"] = diff
            if dry_run:
                return True, f"CHANGES IN {file_path}:\n{diff}", detail
            else:
                backup_path = None
                if not no_backup:
                    bkp = safe_backup(file_path)
                    backup_path = str(bkp)
                    detail["backup"] = backup_path
                atomic_write(file_path, new_content, encoding)
                if do_format:
                    try:
                        subprocess.run(
                            ["isort", "--quiet", "--atomic", str(file_path)],
                            check=True,
                            capture_output=True,
                        )
                        subprocess.run(
                            ["black", "--quiet", str(file_path)],
                            check=True,
                            capture_output=True,
                        )
                    except Exception as e:
                        detail["warnings"].append(f"Formatting failed: {str(e)}")
                backup_str = f" (backup: {backup_path})" if backup_path else ""
                return True, f"MODIFIED: {file_path}{backup_str}", detail
        else:
            if skipped_relative:
                return False, f"SKIPPED (relative): {file_path}", detail
        return False, f"UNCHANGED: {file_path}", detail
    except ParserSyntaxError as e:
        detail["warnings"].append(f"Syntax Error: {e}")
        msg = (
            f"ERROR: {file_path}: {e}\n"
            "Suggestion: The file contains invalid Python syntax. Please fix the syntax errors before processing."
        )
        return False, msg, detail
    except UnicodeDecodeError as e:
        detail["warnings"].append(f"Encoding Error: {e}")
        msg = (
            f"ERROR: {file_path}: {e}\n"
            "Suggestion: The file encoding could not be detected or is invalid. Please check the file encoding."
        )
        return False, msg, detail
    except Exception as e:
        tb = traceback.format_exc()
        logger.error("Error in %s: %s\n%s", file_path, e, tb)
        detail["warnings"].append(f"Error: {e}")
        return False, f"ERROR: {file_path}: {e}", detail
