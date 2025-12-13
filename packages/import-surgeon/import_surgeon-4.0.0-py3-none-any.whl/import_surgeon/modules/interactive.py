from typing import Dict, List, Any
import sys

def launch_interactive_mode() -> Dict[str, Any]:
    """
    Launches an interactive TUI to collect migration configuration.
    Returns a dictionary suitable for processing.
    """
    try:
        from rich.prompt import Prompt
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
    except ImportError:
        print("Error: 'rich' library is required for interactive mode.")
        print("Please install it via 'pip install rich'")
        sys.exit(1)

    console = Console()

    console.print(Panel.fit("[bold blue]Import Surgeon Interactive Mode[/bold blue]", border_style="blue"))
    console.print("[dim]Use this wizard to configure your symbol migration.[/dim]\n")

    old_module = Prompt.ask("[bold green]Old Module[/bold green] (e.g. 'old.pkg')")
    new_module = Prompt.ask("[bold green]New Module[/bold green] (e.g. 'new.pkg')")

    symbols_input = Prompt.ask("[bold green]Symbols[/bold green] (comma-separated, e.g. 'Sym1, Sym2')")
    symbols = [s.strip() for s in symbols_input.split(",") if s.strip()]

    # Preview
    console.print("\n[bold yellow]Preview of Configuration:[/bold yellow]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Parameter")
    table.add_column("Value")

    table.add_row("Old Module", old_module)
    table.add_row("New Module", new_module)
    table.add_row("Symbols", ", ".join(symbols))

    console.print(table)

    if not Prompt.ask("\n[bold]Proceed with this configuration?[/bold]", choices=["y", "n"], default="y") == "y":
        console.print("[red]Aborted.[/red]")
        sys.exit(0)

    return {
        "old_module": old_module,
        "new_module": new_module,
        "symbols": symbols
    }
