#!/usr/bin/env python3
# src/import_surgeon/modules/cst_utils.py

import logging
from pathlib import Path
from typing import Dict, List, Optional

import libcst as cst
import libcst.metadata as md

logger = logging.getLogger("import_surgeon")


def _attr_to_dotted(name: cst.BaseExpression) -> Optional[str]:
    if isinstance(name, cst.Name):
        return name.value
    parts: List[str] = []
    node = name
    while isinstance(node, cst.Attribute):
        attr = node.attr
        if not isinstance(attr, cst.Name):
            return None
        parts.append(attr.value)
        node = node.value
    if isinstance(node, cst.Name):
        parts.append(node.value)
        return ".".join(reversed(parts))
    return None


def _module_to_str(module_expr: Optional[cst.BaseExpression], level: int = 0) -> str:
    if module_expr is None:
        base = ""
    else:
        dotted = _attr_to_dotted(module_expr)
        base = dotted if dotted is not None else module_expr.code.strip()
    return ("." * level) + base


def _import_alias_name(alias: cst.ImportAlias) -> Optional[str]:
    return _attr_to_dotted(alias.name) or alias.name.code.strip()


def _str_to_expr(mod_str: str) -> cst.BaseExpression:
    parts = mod_str.split(".")
    expr: cst.BaseExpression = cst.Name(parts[0])
    for p in parts[1:]:
        expr = cst.Attribute(value=expr, attr=cst.Name(p))
    return expr


class BaseReplacer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (md.PositionProvider,)

    def __init__(
        self,
        old_module: str,
        new_module: str,
        symbols: List[str],
        force_relative: bool = False,
        base_package: Optional[str] = None,
        file_path: Optional[Path] = None,
    ):
        self.old_module = old_module
        self.new_module = new_module
        self.symbols = symbols
        self.force_relative = force_relative
        self.base_package = base_package
        self.file_path = file_path

        self.warnings: List[str] = []
        self.changed_lines: List[int] = []

    def _resolve_relative(self, mod_str: str) -> Optional[str]:
        if not self.file_path or not self.base_package or not mod_str.startswith("."):
            return None
        level = len(mod_str) - len(mod_str.lstrip("."))
        clean_mod = mod_str.lstrip(".")
        base_dir = None
        for parent in [self.file_path.parent] + list(self.file_path.parent.parents):
            if parent.name == self.base_package:
                base_dir = parent
                break
        if not base_dir:
            return None
        try:
            rel_path = self.file_path.parent.relative_to(base_dir)
            rel_parts = list(rel_path.parts)
        except ValueError:
            return None
        up = level - 1
        if up > len(rel_parts):
            return None
        abs_parts = rel_parts[:-up] if up > 0 else rel_parts
        clean_parts = clean_mod.split(".") if clean_mod else []
        full_parts = abs_parts + clean_parts
        return self.base_package + ("." + ".".join(full_parts) if full_parts else "")

    def _match_module(self, mod_str: str) -> bool:
        clean = mod_str.lstrip(".")
        if clean == self.old_module or mod_str == self.old_module:
            return True
        if not self.force_relative:
            return False
        resolved = self._resolve_relative(mod_str) if self.base_package else None
        if resolved and (
            resolved == self.old_module or resolved.endswith("." + self.old_module)
        ):
            return True
        if resolved is None and mod_str.startswith("."):
            return False
        if (
            self.force_relative
            and self.base_package
            and self.old_module.endswith("." + clean)
        ):
            return True
        if (
            clean.endswith("." + self.old_module)
            or clean == self.old_module.split(".")[-1]
        ):
            return True
        return False


class ImportReplacer(BaseReplacer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bound_names: Dict[str, str] = {}  # bound -> orig
        self.existing_new_bindings: Dict[str, str] = {}
        self.has_star_old = False
        self.has_star_new = False
        self.skipped_relative = False
        self.insert_line_approx: int = 1

    def visit_Module(self, node: cst.Module) -> Optional[bool]:
        self.bound_names = {}
        self.existing_new_bindings = {}
        self.has_star_old = False
        self.has_star_new = False
        self.skipped_relative = False
        self.changed_lines = []
        if node.body:
            pos = self.get_metadata(md.PositionProvider, node.body[0])
            self.insert_line_approx = pos.start.line
        else:
            self.insert_line_approx = 1
        return True

    def _get_bound_name(self, alias: cst.ImportAlias) -> Optional[str]:
        if alias.asname and isinstance(alias.asname.name, cst.Name):
            return alias.asname.name.value
        imported = _import_alias_name(alias)
        return imported if imported in self.symbols else None

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> cst.CSTNode:
        level = len(original_node.relative)
        mod_str = _module_to_str(original_node.module, level)

        # Record existing from new_module
        if mod_str.lstrip(".") == self.new_module or mod_str == self.new_module:
            if isinstance(original_node.names, cst.ImportStar):
                self.has_star_new = True
                return updated_node
            if original_node.names:
                for alias in original_node.names:
                    if isinstance(alias, cst.ImportAlias):
                        orig = _import_alias_name(alias)
                        bound = self._get_bound_name(alias) or orig
                        self.existing_new_bindings[bound] = orig or bound
            return updated_node

        # Handle from old_module
        if self._match_module(mod_str):
            if mod_str.startswith(".") and not self.force_relative:
                logger.warning("Skipping relative import %s", mod_str)
                self.skipped_relative = True
                self.warnings.append(f"Skipped relative import {mod_str}")
                return updated_node

            if isinstance(original_node.names, cst.ImportStar):
                self.has_star_old = True
                for s in self.symbols:
                    self.bound_names[s] = s
                return updated_node

            if original_node.names:
                new_names: List[cst.ImportAlias] = []
                removed = False
                for alias in original_node.names:
                    if not isinstance(alias, cst.ImportAlias):
                        new_names.append(alias)
                        continue
                    orig = _import_alias_name(alias)
                    if orig in self.symbols:
                        bound = self._get_bound_name(alias) or orig
                        self.bound_names[bound] = orig
                        removed = True
                        pos = self.get_metadata(md.PositionProvider, original_node)
                        self.changed_lines.append(pos.start.line)
                    else:
                        new_names.append(alias)
                if removed:
                    if new_names:
                        # Reset commas to avoid trailing comma
                        new_names = [
                            new_names[i].with_changes(
                                comma=cst.Comma(
                                    whitespace_after=cst.SimpleWhitespace(" ")
                                )
                                if i < len(new_names) - 1
                                else cst.MaybeSentinel.DEFAULT
                            )
                            for i in range(len(new_names))
                        ]
                        return updated_node.with_changes(names=new_names)
                    else:
                        return cst.RemoveFromParent()
        return updated_node

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        if self.skipped_relative or not self.bound_names:
            return updated_node

        if self.has_star_old:
            self.warnings.append("Handled wildcard import")

        # Collect aliases for new import
        aliases: List[cst.ImportAlias] = []
        sorted_items = sorted(self.bound_names.items(), key=lambda x: x[1])
        for bound_name, orig_symbol in sorted_items:
            covered = bound_name in self.existing_new_bindings or (
                self.has_star_new and bound_name == orig_symbol
            )
            if covered:
                continue
            name = cst.Name(orig_symbol)
            asname = (
                cst.AsName(name=cst.Name(bound_name))
                if bound_name != orig_symbol
                else None
            )
            alias = cst.ImportAlias(name=name, asname=asname)
            aliases.append(alias)

        to_insert: List[cst.SimpleStatementLine] = []
        if aliases:
            # Add commas
            aliases_with_comma = [
                aliases[i].with_changes(
                    comma=cst.Comma(whitespace_after=cst.SimpleWhitespace(" "))
                    if i < len(aliases) - 1
                    else cst.MaybeSentinel.DEFAULT
                )
                for i in range(len(aliases))
            ]
            import_from = cst.ImportFrom(
                module=_str_to_expr(self.new_module),
                names=aliases_with_comma,
            )
            stmt = cst.SimpleStatementLine(body=[import_from])
            to_insert.append(stmt)
            self.changed_lines.append(self.insert_line_approx)

        if not to_insert:
            return updated_node

        body = list(updated_node.body)
        insert_at = 0
        if (
            body
            and isinstance(body[0], cst.SimpleStatementLine)
            and body[0].body
            and isinstance(body[0].body[0], cst.Expr)
            and isinstance(body[0].body[0].value, cst.SimpleString)
        ):
            insert_at = 1

        while insert_at < len(body) and self._is_import_or_future_stmt(body[insert_at]):
            insert_at += 1

        new_body = body[:insert_at] + to_insert + body[insert_at:]
        return updated_node.with_changes(body=new_body)

    def _is_import_or_future_stmt(self, stmt: cst.CSTNode) -> bool:
        if not isinstance(stmt, cst.SimpleStatementLine) or not stmt.body:
            return False
        return isinstance(stmt.body[0], (cst.Import, cst.ImportFrom))


class DottedReplacer(BaseReplacer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rewrote_count = 0
        self.aliases: Dict[str, str] = {}  # alias -> original_module_name

    def visit_Import(self, node: cst.Import) -> Optional[bool]:
        for alias in node.names:
            mod_name = _module_to_str(alias.name)
            if self._match_module(mod_name):
                # Found an import of the old module
                if alias.asname and isinstance(alias.asname.name, cst.Name):
                    # import old.pkg as o
                    alias_name = alias.asname.name.value
                    self.aliases[alias_name] = mod_name
                else:
                    # import old.pkg
                    # alias is old.pkg
                    self.aliases[mod_name] = mod_name
        return True

    def leave_Attribute(
        self, original_node: cst.Attribute, updated_node: cst.Attribute
    ) -> cst.Attribute:
        if (
            isinstance(updated_node.attr, cst.Name)
            and updated_node.attr.value in self.symbols
        ):
            mod_str = _attr_to_dotted(updated_node.value)

            matched = False
            if mod_str:
                if self._match_module(mod_str):
                    matched = True
                elif mod_str in self.aliases:
                    matched = True

            if matched:
                new_value = _str_to_expr(self.new_module)
                self.rewrote_count += 1
                pos = self.get_metadata(md.PositionProvider, original_node)
                self.changed_lines.append(pos.start.line)
                return updated_node.with_changes(value=new_value)
        return updated_node

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        if self.rewrote_count > 0:
            self.warnings.append(
                f"Rewrote {self.rewrote_count} dotted usages for symbols {self.symbols}"
            )
        return updated_node
