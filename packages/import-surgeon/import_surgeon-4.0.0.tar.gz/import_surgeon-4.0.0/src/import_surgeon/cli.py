#!/usr/bin/env python3
# src/import_surgeon/cli.py

"""import_surgeon.py

Elite production-standard, peace-of-mind utility to move symbols' `from ... import X` bindings
from one module to another across a Python repository.

New features:
- Rewrite dotted usages (e.g., old_module.Symbol) with --rewrite-dotted (note: does not handle aliased module imports)
- Batch mode for multiple symbols/modules via YAML config 'migrations' list (e.g., migrations: [{old_module: ..., new_module: ..., symbols: [Sym1, Sym2]}])
- Integration with isort and black formatters via --format
- Automatic detection of base_package from git repo root name if not provided
- Rollback changes using --rollback --summary-json

Design goals / guarantees:
- Dry-run by default (shows unified diffs). --apply writes changes atomically.
- Backups always (unless --no-backup), with preservation of metadata.
- Robust encoding, relative import handling with accurate directory-based resolution (auto or --base-package).
- Safety checks: Git clean requirement, max-files, post-change usage warnings for dotted accesses.
- Automation: JSON summary with detailed metadata (risk, lines, encodings) for all files, progress bar (tqdm fallback to print).
- Usability: YAML config support, granular quiet modes, optional auto-commit.
- Optional rewrite of dotted usages; warns if detected and not rewritten.

Usage examples:
  # Dry-run with config including migrations
  python import_surgeon.py --config config.yaml

  # Apply with formatting and dotted rewrite
  python import_surgeon.py --apply --format --rewrite-dotted --old-module old --new-module new --symbols Sym1,Sym2

  # Rollback
  python import_surgeon.py --rollback --summary-json summary.json

Exit codes:
 0 - success
 1 - errors/warnings (configurable)
 2 - CLI/invalid setup

"""

from __future__ import annotations

import argparse
import concurrent.futures
import functools
import json
import logging
import multiprocessing
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from .modules.config import load_config
from .modules.file_ops import find_py_files
from .modules.git_ops import find_git_root, git_commit_changes, git_is_clean
from .modules.process import process_file
from .modules.rollback import perform_rollback
from .modules.interactive import launch_interactive_mode
from .banner import print_logo

# Optional dependencies
try:
    from tqdm import tqdm  # Progress bar
except ImportError:

    class DummyTqdm:
        def __init__(self, iterable=None, **kwargs):
            self.iterable = iterable

        def __iter__(self):
            return iter(self.iterable or [])

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def update(self, n=1):
            pass

        def set_description(self, desc):
            pass

        def write(self, msg):
            print(msg)

    def tqdm(iterable=None, **kwargs):
        return DummyTqdm(iterable, **kwargs)


logger = logging.getLogger("import_surgeon")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Elite safe import replacer")
    parser.add_argument("target", nargs="?", default=".", help="file/dir to scan")
    parser.add_argument("--old-module", help="old module")
    parser.add_argument("--new-module", help="new module")
    parser.add_argument("--symbol", help="symbol to move (deprecated, use --symbols)")
    parser.add_argument("--symbols", help="comma-separated symbols to move")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    parser.add_argument("--exclude", help="comma-separated globs")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument("--quiet", default="none", choices=["none", "errors", "all"])
    parser.add_argument("--force-relative", action="store_true")
    parser.add_argument("--base-package", help="base package for relative resolution")
    parser.add_argument("--max-files", type=int, default=10000)
    parser.add_argument("--require-clean-git", action="store_true")
    parser.add_argument("--auto-commit", help="commit message for auto-commit")
    parser.add_argument("--summary-json", help="JSON summary path")
    parser.add_argument("--strict-warnings", action="store_true")
    parser.add_argument("--config", help="YAML config path")
    parser.add_argument(
        "--rewrite-dotted", action="store_true", help="rewrite dotted usages"
    )
    parser.add_argument(
        "--format",
        action="store_true",
        help="format with isort and black after changes",
    )
    parser.add_argument(
        "--rollback", action="store_true", help="rollback changes using summary-json"
    )
    parser.add_argument(
        "--jobs",
        "-j",
        type=int,
        default=1,
        help="number of parallel jobs (default: 1)",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s 3.0.2", help="Show program's version number and exit"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="launch interactive mode"
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    print_logo()
    args = parse_args(argv)

    if args.interactive:
        config_data = launch_interactive_mode()
        args.old_module = config_data.get("old_module")
        args.new_module = config_data.get("new_module")
        args.symbols = ",".join(config_data.get("symbols", []))

    config = load_config(args.config)
    for k, v in config.items():
        key = k.replace("-", "_")
        if not hasattr(args, key) or getattr(args, key) is None:
            setattr(args, key, v)
        # If interactive mode set these, don't overwrite with empty config values
        # (Though load_config shouldn't have them if not in config file)

    if args.rollback:
        if perform_rollback(args.summary_json):
            return 0
        else:
            return 2 if not args.summary_json else 1

    if not (hasattr(args, "old_module") and args.old_module) and not config.get(
        "migrations"
    ):
        logger.error("Missing required: --old-module or migrations in config")
        return 2

    if not (hasattr(args, "new_module") and args.new_module) and not config.get(
        "migrations"
    ):
        logger.error("Missing required: --new-module or migrations in config")
        return 2

    if not (hasattr(args, "symbol") or hasattr(args, "symbols")) and not config.get(
        "migrations"
    ):
        logger.error("Missing required: --symbol / --symbols or migrations in config")
        return 2

    lvl = max(logging.DEBUG, logging.WARNING - (10 * args.verbose))
    logging.basicConfig(level=lvl, format="%(levelname)s: %(message)s")

    target_path = Path(args.target)
    if not target_path.exists():
        logger.error("Target not found: %s", target_path)
        return 2

    excludes = [s.strip() for s in (args.exclude or "").split(",") if s.strip()]
    py_files = find_py_files(target_path, excludes, args.max_files)
    logger.info("Found %d files", len(py_files))

    repo_root = find_git_root(target_path)
    if not args.base_package and repo_root:
        args.base_package = repo_root.name
        logger.info("Auto-detected base_package: %s", args.base_package)

    if (
        args.apply
        and args.require_clean_git
        and repo_root
        and not git_is_clean(target_path)
    ):
        logger.error("Git not clean; commit/stash or remove --require-clean-git")
        return 1

    # Prepare migrations
    if config.get("migrations"):
        migrations = config["migrations"]
    else:
        symbols = (
            args.symbols.split(",")
            if hasattr(args, "symbols") and args.symbols
            else [args.symbol]
            if hasattr(args, "symbol") and args.symbol
            else []
        )
        migrations = [
            {
                "old_module": args.old_module,
                "new_module": args.new_module,
                "symbols": symbols,
            }
        ]

    changed = 0
    errors = 0
    warnings = 0
    summary: List[Dict] = []
    dry_run = not args.apply

    worker_func = functools.partial(
        process_file,
        migrations=migrations,
        dry_run=dry_run,
        no_backup=args.no_backup,
        force_relative=args.force_relative,
        base_package=args.base_package,
        rewrite_dotted=args.rewrite_dotted if hasattr(args, "rewrite_dotted") else False,
        do_format=args.format if hasattr(args, "format") else False,
        quiet=args.quiet,
    )

    if args.jobs > 1:
        cpu_count = multiprocessing.cpu_count()
        max_workers = min(args.jobs, cpu_count * 2)  # Cap reasonable max
        logger.info("Starting parallel processing with %d workers", max_workers)

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            # We map futures to file paths to track progress
            futures = {executor.submit(worker_func, p): p for p in py_files}

            with tqdm(total=len(py_files), disable=(args.quiet != "none")) as pbar:
                for future in concurrent.futures.as_completed(futures):
                    p = futures[future]
                    pbar.set_description(f"Processing {p.name}")
                    try:
                        changed_flag, msg, detail = future.result()

                        should_print = args.quiet == "none" or (
                            args.quiet == "errors" and "ERROR" in msg
                        )
                        if should_print:
                            # Using tqdm.write to avoid interfering with progress bar
                            pbar.write(msg)

                        if "SKIPPED" in msg or detail["warnings"]:
                            warnings += 1
                        if changed_flag and not dry_run:
                            changed += 1
                        if "ERROR" in msg:
                            errors += 1
                        entry = {"file": str(p), "changed": changed_flag, "message": msg, **detail}
                        summary.append(entry)
                    except Exception as exc:
                        logger.error("Generated an exception: %s", exc)
                        errors += 1
                    pbar.update(1)

    else:
        progress_iter = tqdm(py_files, disable=(args.quiet != "none"))
        for p in progress_iter:
            progress_iter.set_description(f"Processing {p.name}")
            # Note: worker_func needs keyword arg 'file_path' which corresponds to the first arg of process_file
            # process_file(file_path, ...)
            # worker_func is partial(process_file, ...) so we just pass p
            changed_flag, msg, detail = worker_func(p)

            should_print = args.quiet == "none" or (
                args.quiet == "errors" and "ERROR" in msg
            )
            if should_print:
                print(msg)
            if "SKIPPED" in msg or detail["warnings"]:
                warnings += 1
            if changed_flag and not dry_run:
                changed += 1
            if "ERROR" in msg:
                errors += 1
            entry = {"file": str(p), "changed": changed_flag, "message": msg, **detail}
            summary.append(entry)

    if args.summary_json:
        with open(args.summary_json, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "summary": summary,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
                f,
                indent=2,
            )
        logger.info("JSON summary written to %s", args.summary_json)

    if args.apply and args.auto_commit and repo_root:
        if git_commit_changes(repo_root, args.auto_commit):
            logger.info("Auto-committed with message: %s", args.auto_commit)

    if args.quiet != "all":
        print("\nSummary:")
        if dry_run:
            print("  Dry-run; use --apply to write.")
        print(f"  Changed: {changed}")
        print(f"  Errors: {errors}")
        print(f"  Warnings: {warnings}")
        print(f"  Scanned: {len(py_files)}")

    if errors:
        return 1
    if args.strict_warnings and warnings:
        return 1
    return 0


if __name__ == "__main__":
    main()
