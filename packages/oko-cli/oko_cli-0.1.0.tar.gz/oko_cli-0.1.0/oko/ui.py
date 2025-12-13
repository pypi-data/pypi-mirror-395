from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from rich.table import Table
from rich.box import ROUNDED

LOGO_CAT = """[bold blue]
      /\\_/\\
     ( o.o )
      > ^ <
[/bold blue]"""

LOGO_OKO = """[bold bright_cyan]
  ___  _  __  ___
 / _ \| |/ / / _ \\
| | | | ' / | | | |
| |_| | . \\ | |_| |
 \\___/|_|\\_\\ \\___/
[/bold bright_cyan]"""


# Custom theme for consistent styling
custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "primary": "blue",
        "secondary": "bright_cyan",
    }
)

# Global console object
console = Console(theme=custom_theme)


def print_logo():
    """Prints the OKO logo."""
    console.print(LOGO_CAT, justify="center")
    console.print(LOGO_OKO, justify="center")


def print_success(message: str, title: str = "✅ Success"):
    """Prints a success message in a panel."""
    console.print(
        Panel(
            f"[success]{message}[/success]",
            title=title,
            border_style="success",
            expand=False,
        )
    )


def print_error(message: str, title: str = "❌ Error"):
    """Prints an error message in a panel."""
    console.print(
        Panel(
            f"[error]{message}[/error]", title=title, border_style="error", expand=False
        )
    )


def print_warning(message: str, title: str = "⚠️ Warning"):
    """Prints a warning message in a panel."""
    console.print(
        Panel(
            f"[warning]{message}[/warning]",
            title=title,
            border_style="warning",
            expand=False,
        )
    )


def print_info_panel(message: str, title: str = "📋 Info"):
    """Prints an info message in a panel."""
    console.print(Panel(message, title=title, border_style="info", expand=False))


def get_table() -> Table:
    """Returns a nicely styled table."""
    return Table(
        show_header=True, header_style="bold bright_cyan", box=ROUNDED, padding=(0, 2)
    )
