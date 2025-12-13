from typing import Optional, List, Dict, Any
from pathlib import Path
import json
import sys

from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table
from rich.panel import Panel
from rich.theme import Theme

class DisplayManager:
    """Manages all display output with rich formatting."""

    def __init__(self, verbose: bool = False, debug: bool = False):
        self.verbose = verbose
        self.debug = debug
        self.console = Console(theme=Theme({
            "info": "blue",
            "success": "green",
            "warning": "yellow",
            "error": "red bold",
            "highlight": "cyan"
        }))

    def info(self, message: str) -> None:
        """Display info message."""
        self.console.print(f"[info]ℹ️[/info] {message}")

    def success(self, message: str) -> None:
        """Display success message."""
        self.console.print(f"[success]✅[/success] {message}")

    def warning(self, message: str) -> None:
        """Display warning message."""
        self.console.print(f"[warning]⚠️[/warning] {message}")

    def error(self, message: str) -> None:
        """Display error message."""
        self.console.print(f"[error]❌[/error] {message}")

    def display_code(self, code: str, title: str = "Code", language: str = "python") -> None:
        """Display code with syntax highlighting."""
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        panel = Panel(syntax, title=title, border_style="blue")
        self.console.print(panel)

    def display_table(self, data: List[List[str]], headers: List[str], title: Optional[str] = None) -> None:
        """Display data in a table."""
        table = Table(title=title)
        for header in headers:
            table.add_column(header, style="cyan")

        for row in data:
            table.add_row(*[str(item) for item in row])

        self.console.print(table)

    def display_progress_info(self, completed: int, total: int, best_fitness: Optional[float]) -> None:
        """Display progress information."""
        if self.verbose:
            pct = (completed / total * 100) if total > 0 else 0
            best_str = f"{best_fitness:.6f}" if best_fitness is not None else "—"
            self.info(f"Progress: {completed}/{total} ({pct:.1f}%) | Best: {best_str}")

    def save_output(self, data: dict, filepath: Path) -> None:
        """Save data to JSON file."""
        filepath.write_text(json.dumps(data, indent=2))
        self.success(f"Data saved to {filepath}")
