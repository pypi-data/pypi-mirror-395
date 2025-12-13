import pytest
from unittest.mock import patch, MagicMock
from import_surgeon.modules.interactive import launch_interactive_mode

def test_launch_interactive_mode_returns_config():
    """
    Test that interactive mode prompts for old_module, new_module, and symbols,
    and returns a correct configuration dictionary.
    """
    # Since imports are local now, we need to patch rich.prompt.Prompt.ask directly
    # BUT we need to make sure the function imports it.
    # We can mock sys.modules to ensure 'rich' is present or just let it use the real one if present.
    # The environment has rich installed.
    # We need to patch where it is used. But since it's imported locally inside the function,
    # 'import_surgeon.modules.interactive.Prompt' does not exist at module level.

    # We should patch 'rich.prompt.Prompt.ask' globally.
    with patch("rich.prompt.Prompt.ask") as mock_ask:
        # Sequence of inputs: old_module, new_module, symbols, confirm
        mock_ask.side_effect = [
            "old.pkg",
            "new.pkg",
            "SymbolA, SymbolB",
            "y"
        ]

        config = launch_interactive_mode()

        assert config["old_module"] == "old.pkg"
        assert config["new_module"] == "new.pkg"
        assert config["symbols"] == ["SymbolA", "SymbolB"]

        assert mock_ask.call_count == 4
