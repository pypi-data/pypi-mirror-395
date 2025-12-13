
import pytest
import libcst as cst
import libcst.metadata as md
from pathlib import Path
from import_surgeon.modules.cst_utils import (
    DottedReplacer,
    ImportReplacer,
    _attr_to_dotted,
    _import_alias_name,
    _module_to_str,
    _str_to_expr,
)

class TestCstUtils:
    @pytest.mark.parametrize("expr,expected", [
        (cst.Name("foo"), "foo"),
        (cst.Attribute(value=cst.Name("mod"), attr=cst.Name("sub")), "mod.sub"),
        (cst.Attribute(value=cst.Attribute(value=cst.Name("a"), attr=cst.Name("b")), attr=cst.Name("c")), "a.b.c"),
        (cst.SimpleString('"foo"'), None),
    ])
    def test_attr_to_dotted(self, expr, expected):
        assert _attr_to_dotted(expr) == expected

    @pytest.mark.parametrize("node,expected", [
        (cst.Name("mod"), "mod"),
        (None, ".."), # relative import with 2 dots
        (cst.Attribute(value=cst.Name("pkg"), attr=cst.Name("mod")), "pkg.mod"),
    ])
    def test_module_to_str(self, node, expected):
        # Special handling for relative import test case
        if node is None:
             assert _module_to_str(None, 2) == expected
        else:
             assert _module_to_str(node) == expected

    @pytest.mark.parametrize("alias,expected", [
        (cst.ImportAlias(name=cst.Name("Symbol")), "Symbol"),
        (cst.ImportAlias(name=cst.Attribute(value=cst.Name("mod"), attr=cst.Name("Symbol"))), "mod.Symbol"),
    ])
    def test_import_alias_name(self, alias, expected):
        assert _import_alias_name(alias) == expected

    def test_str_to_expr(self):
        expr = _str_to_expr("pkg.mod")
        assert _attr_to_dotted(expr) == "pkg.mod"

class TestImportReplacer:
    @pytest.mark.parametrize("code,old_mod,new_mod,symbols,expected", [
        ("from old.mod import Symbol", "old.mod", "new.mod", ["Symbol"], "from new.mod import Symbol"),
        ("from old.mod import Symbol as Alias", "old.mod", "new.mod", ["Symbol"], "from new.mod import Symbol as Alias"),
        ("from new.mod import Symbol", "old.mod", "new.mod", ["Symbol"], "from new.mod import Symbol"),
        ("from .old_sub import Symbol", "old_sub", "new_sub", ["Symbol"], "from .old_sub import Symbol"),
        ("from old.mod import Symbol\nfrom old.mod import Symbol", "old.mod", "new.mod", ["Symbol"], "from new.mod import Symbol"), # Duplicate avoid
        ("from old.mod import Symbol", "old.mod", "new.mod", ["Symbol"], "from new.mod import Symbol"), # Empty removal
        ("import old.mod\nold.mod.Symbol", "old.mod", "new.mod", ["Symbol"], "import old.mod\nold.mod.Symbol"), # No change dotted
        ("from old.mod import Sym1, Sym2", "old.mod", "new.mod", ["Sym1", "Sym2"], "from new.mod import Sym1, Sym2"),
        ("def f():\n    from old.mod import Symbol", "old.mod", "new.mod", ["Symbol"], "from new.mod import Symbol\ndef f():\n    pass"),
        ("if cond:\n    from old.mod import Symbol", "old.mod", "new.mod", ["Symbol"], "from new.mod import Symbol\nif cond:\n    pass"),
        ("try:\n    from old.mod import Symbol\nexcept ImportError:\n    pass", "old.mod", "new.mod", ["Symbol"], "from new.mod import Symbol\ntry:\n    pass\nexcept ImportError:\n    pass"),
    ])
    def test_import_replacer_simple_cases(self, code, old_mod, new_mod, symbols, expected):
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer(old_mod, new_mod, symbols)
        new_code = wrapper.visit(replacer).code
        assert new_code.strip() == expected.strip()

    def test_import_replacer_star(self):
        code = "from old.mod import *"
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Symbol"])
        new_code = wrapper.visit(replacer).code
        assert "from new.mod import Symbol" in new_code
        assert "from old.mod import *" in new_code

    def test_import_replacer_multi_mixed(self):
        code = "from old.mod import A, Symbol, B"
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Symbol"])
        new_code = wrapper.visit(replacer).code
        assert "from old.mod import A, B" in new_code
        assert "from new.mod import Symbol" in new_code

    def test_import_replacer_relative_force(self):
        code = "from .old.mod import Symbol"
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Symbol"], force_relative=True)
        new_code = wrapper.visit(replacer).code
        assert new_code.strip() == "from new.mod import Symbol"

    def test_import_replacer_resolve_relative(self):
        code = "from ..old.mod import Symbol"
        file_path = Path("/fake/pkg/sub/file.py")
        replacer = ImportReplacer(
            "pkg.old.mod",
            "pkg.new.mod",
            ["Symbol"],
            force_relative=True,
            base_package="pkg",
            file_path=file_path,
        )
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        new_code = wrapper.visit(replacer).code
        assert new_code.strip() == "from pkg.new.mod import Symbol"

    def test_import_replacer_multi_level_relative(self):
        code = "from ...old.mod import Symbol"
        file_path = Path("/fake/pkg/sub/dir/file.py")
        replacer = ImportReplacer(
            "pkg.old.mod",
            "pkg.new.mod",
            ["Symbol"],
            force_relative=True,
            base_package="pkg",
            file_path=file_path,
        )
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        new_code = wrapper.visit(replacer).code
        assert new_code.strip() == "from pkg.new.mod import Symbol"

    def test_import_replacer_relative_too_deep(self):
        code = "from ....old.mod import Symbol"
        file_path = Path("/fake/pkg/sub/file.py")
        replacer = ImportReplacer(
            "pkg.old.mod",
            "pkg.new.mod",
            ["Symbol"],
            force_relative=True,
            base_package="pkg",
            file_path=file_path,
        )
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        new_code = wrapper.visit(replacer).code
        assert new_code.strip() == code

    def test_import_replacer_relative_force_no_base_no_match(self):
        code = "from ..old.mod import Symbol"
        file_path = Path("/fake/pkg/sub/file.py")
        replacer = ImportReplacer(
            "pkg.old.mod",
            "pkg.new.mod",
            ["Symbol"],
            force_relative=True,
            base_package=None,
            file_path=file_path,
        )
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        new_code = wrapper.visit(replacer).code
        assert new_code.strip() == code

    def test_import_replacer_insert_position(self):
        code = '''"""Docstring"""
from __future__ import annotations
import os
from old.mod import Symbol'''
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Symbol"])
        new_code = wrapper.visit(replacer).code
        lines = new_code.splitlines()
        assert "from new.mod import Symbol" in lines
        assert lines.index("from new.mod import Symbol") == 3

    def test_import_replacer_with_comments(self):
        code = "# Comment above\nfrom old.mod import Symbol  # inline comment"
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Symbol"])
        new_code = wrapper.visit(replacer).code
        assert "from new.mod import Symbol" in new_code
        assert "# Comment above" in new_code

    def test_import_replacer_multi_line(self):
        code = "from old.mod import (\n    A,\n    Symbol,\n    B,\n)"
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Symbol"])
        new_code = wrapper.visit(replacer).code
        assert "from old.mod import (\n    A, B)" in new_code
        assert "from new.mod import Symbol" in new_code

    def test_import_replacer_no_body(self):
        code = ""
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Symbol"])
        new_code = wrapper.visit(replacer).code
        assert new_code == ""

    def test_import_replacer_star_new_with_alias_old(self):
        code = """from new.mod import *
from old.mod import Symbol as Alias"""
        expected = """from new.mod import *
from new.mod import Symbol as Alias"""
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Symbol"])
        new_code = wrapper.visit(replacer).code
        assert new_code.strip() == expected.strip()

    def test_import_replacer_existing_alias_in_new(self):
        code = """from new.mod import Symbol as Alias
from old.mod import Symbol as Alias"""
        expected = """from new.mod import Symbol as Alias"""
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Symbol"])
        new_code = wrapper.visit(replacer).code
        assert new_code.strip() == expected.strip()

    def test_import_replacer_multiple_symbols_mixed(self):
        code = "from old.mod import Sym1, Other, Sym2"
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Sym1", "Sym2"])
        new_code = wrapper.visit(replacer).code
        assert "from old.mod import Other" in new_code
        assert "from new.mod import Sym1, Sym2" in new_code

    def test_import_replacer_multiple_symbols_aliases(self):
        code = "from old.mod import Sym1 as A, Sym2 as B"
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Sym1", "Sym2"])
        new_code = wrapper.visit(replacer).code
        assert "from new.mod import Sym1 as A, Sym2 as B" in new_code

    def test_import_replacer_star_multiple_symbols(self):
        code = "from old.mod import *"
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = ImportReplacer("old.mod", "new.mod", ["Sym1", "Sym2"])
        new_code = wrapper.visit(replacer).code
        assert "from old.mod import *" in new_code
        assert "from new.mod import Sym1, Sym2" in new_code

class TestDottedReplacer:
    @pytest.mark.parametrize("code,old_mod,new_mod,symbols,expected", [
        ("a = old.mod.Symbol", "old.mod", "new.mod", ["Symbol"], "a = new.mod.Symbol"),
        ("a = old.mod.Sym1\nb = old.mod.Sym2", "old.mod", "new.mod", ["Sym1", "Sym2"], "a = new.mod.Sym1\nb = new.mod.Sym2"),
        ("a = other.mod.Symbol", "old.mod", "new.mod", ["Symbol"], "a = other.mod.Symbol"),
    ])
    def test_dotted_replacer_simple_cases(self, code, old_mod, new_mod, symbols, expected):
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        replacer = DottedReplacer(old_mod, new_mod, symbols)
        new_code = wrapper.visit(replacer).code
        assert new_code.strip() == expected.strip()

    def test_dotted_replacer_relative(self):
        code = "a = old.mod.Symbol"
        file_path = Path("/fake/pkg/sub/file.py")
        replacer = DottedReplacer(
            "pkg.old.mod",
            "pkg.new.mod",
            ["Symbol"],
            force_relative=True,
            base_package="pkg",
            file_path=file_path,
        )
        wrapper = md.MetadataWrapper(cst.parse_module(code))
        new_code = wrapper.visit(replacer).code
        assert new_code.strip() == "a = pkg.new.mod.Symbol"
