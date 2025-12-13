import pytest
from import_surgeon.modules.analysis import check_internal_dependencies

def test_check_internal_dependencies_no_issues():
    """Test that no warning is returned if moved symbol is not used by remaining code."""
    content = """
class MovedSymbol:
    pass

class RemainingSymbol:
    pass
"""
    warnings = check_internal_dependencies(content, ["MovedSymbol"])
    assert len(warnings) == 0

def test_check_internal_dependencies_usage_in_remaining_code():
    """Test that a warning is returned if a moved symbol is used by remaining code."""
    content = """
class MovedSymbol:
    pass

class RemainingSymbol:
    def method(self):
        return MovedSymbol()
"""
    warnings = check_internal_dependencies(content, ["MovedSymbol"])
    assert len(warnings) == 1
    assert "MovedSymbol" in warnings[0]
    assert "may break internal dependencies" in warnings[0]

def test_check_internal_dependencies_multiple_usages():
    """Test multiple moved symbols used in the file."""
    content = """
class A: pass
class B: pass

def func():
    a = A()
    b = B()
"""
    warnings = check_internal_dependencies(content, ["A", "B"])
    assert len(warnings) == 2
    assert any("A" in w for w in warnings)
    assert any("B" in w for w in warnings)
