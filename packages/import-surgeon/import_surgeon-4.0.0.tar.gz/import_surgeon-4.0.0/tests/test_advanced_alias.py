
import pytest
import libcst as cst
from import_surgeon.modules.cst_utils import DottedReplacer, ImportReplacer

def test_alias_dotted_access_replacement():
    """
    Test that 'import old.pkg as o; o.Symbol()' is correctly rewritten.
    Should become 'import old.pkg as o; import new.pkg; new.pkg.Symbol()'.
    """
    code = """
import old.pkg as o

def foo():
    return o.Symbol()
"""
    old_mod = "old.pkg"
    new_mod = "new.pkg"
    symbols = ["Symbol"]

    wrapper = cst.MetadataWrapper(cst.parse_module(code))

    # We run DottedReplacer first as it handles usage replacement
    dotted_replacer = DottedReplacer(old_mod, new_mod, symbols)
    new_wrapper = wrapper.visit(dotted_replacer)

    result_code = new_wrapper.code

    # Expectation: o.Symbol() should be replaced by new.pkg.Symbol()
    assert "new.pkg.Symbol()" in result_code
    # DottedReplacer doesn't currently remove the old import or add the new one,
    # but it *must* rewrite the usage.
    assert "o.Symbol()" not in result_code

def test_alias_dotted_access_replacement_multiple_aliases():
    """
    Test with multiple aliases and mixed imports.
    """
    code = """
import old.pkg as o
import old.pkg

def foo():
    x = o.Symbol()
    y = old.pkg.Symbol()
"""
    old_mod = "old.pkg"
    new_mod = "new.pkg"
    symbols = ["Symbol"]

    wrapper = cst.MetadataWrapper(cst.parse_module(code))
    dotted_replacer = DottedReplacer(old_mod, new_mod, symbols)
    new_wrapper = wrapper.visit(dotted_replacer)

    result_code = new_wrapper.code

    assert "new.pkg.Symbol()" in result_code
    assert "o.Symbol()" not in result_code
    assert "old.pkg.Symbol()" not in result_code
