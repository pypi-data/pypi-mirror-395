
import pytest
from import_surgeon.modules.analysis import check_remaining_usages

class TestAnalysis:
    @pytest.mark.parametrize("content,old_mod,symbols,expected_warnings_count,expected_symbol", [
        ("old.mod.Sym1 used\nold.mod.Sym2 here", "old.mod", ["Sym1", "Sym2"], 2, "Sym1"),
        ("new.mod.Sym1 used", "old.mod", ["Sym1"], 0, None),
        ("some content", "old.mod", ["*"], 0, None),
    ])
    def test_check_remaining_usages(self, content, old_mod, symbols, expected_warnings_count, expected_symbol):
        warnings = check_remaining_usages(content, old_mod, symbols)
        assert len(warnings) == expected_warnings_count
        if expected_symbol:
            assert any(expected_symbol in w for w in warnings)
