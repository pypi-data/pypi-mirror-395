from typing import List, Optional
import typer
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from datetime import datetime
from pathlib import Path

from .core.config import config, ConfigType, load_endpoints
from .core.endpoints import add_endpoint
from .core.runner import run_endpoint
from .ui import (
    console,
    print_logo,
    print_success,
    print_error,
    print_warning,
    print_info_panel,
    get_table,
)

app = typer.Typer(
    help="OKO CLI - API Testing made simple",
    rich_markup_mode="rich",
    no_args_is_help=True,
)
endpoint_app = typer.Typer(help="Manage API endpoints")
app.add_typer(endpoint_app, name="endpoint")


@app.command("init")
def init():
    """Initialize OKO configuration."""
    print_logo()
    console.print("[bold primary]🚀 Welcome to OKO CLI![/bold primary]")
    console.print("Let's set up your configuration.\n")

    if config.find_config():
        current_config = config.load_config()
        warning_message = (
            f"Configuration already exists at: [info]{config.config_dir}[/info]\n"
            f"Type: [info]{current_config.get('type', 'unknown')}[/info]"
        )
        print_warning(warning_message, title="Configuration Found")

        if not Confirm.ask("\nDo you want to reinitialize?"):
            console.print("[dim]Initialization cancelled.[/dim]")
            return

    console.print("\n[bold primary]Where would you like to store endpoints?[/bold primary]")
    options = [
        ("project", "In this project (.oko/) - For team collaboration"),
        ("global", "Global (~/.oko/) - For personal use"),
        ("custom", "Custom location - Specify a path"),
    ]

    for i, (_, desc) in enumerate(options, 1):
        console.print(f"  [secondary]{i}[/secondary]. {desc}")

    choice = Prompt.ask("\nSelect option (1-3)", choices=["1", "2", "3"], default="1")

    config_type: ConfigType
    config_dir: Path

    if choice == "1":
        config_type = "project"
        config_dir = Path.cwd() / ".oko"
    elif choice == "2":
        config_type = "global"
        config_dir = Path.home() / ".oko"
    else:
        config_type = "custom"
        custom_path = Prompt.ask("\nEnter custom path")
        config_dir = Path(custom_path).expanduser().resolve()

    project_name = None
    if config_type == "project":
        project_name = Prompt.ask("\nProject name", default=Path.cwd().name)

    summary = (
        f"  [bold]Type:[/bold] [info]{config_type}[/info]\n"
        f"  [bold]Location:[/bold] [info]{config_dir}[/info]\n"
    )
    if project_name:
        summary += f"  [bold]Project:[/bold] [info]{project_name}[/info]"

    print_info_panel(summary, title="Summary")

    if not Confirm.ask("\nCreate configuration?"):
        console.print("[dim]Cancelled.[/dim]")
        return

    config_data = {
        "created_at": datetime.now().isoformat(),
        "project_name": project_name,
    }
    config.save_config(config_type, config_dir, config_data)

    success_message = (
        f"Configuration saved at: [info]{config.config_dir}[/info]\n\n"
        "[bold]Next steps:[/bold]\n"
        "  • Add an endpoint: [secondary]oko endpoint add <alias> <url>[/secondary]\n"
        "  • Run an endpoint: [secondary]oko run <alias>[/secondary]"
    )
    print_success(success_message, title="✅ OKO initialized successfully!")


@app.command("info")
def info():
    """Show current OKO configuration."""
    if not config.find_config():
        print_warning("No OKO configuration found. Run [secondary]oko init[/secondary] to get started.")
        return

    print_logo()
    current_config = config.load_config()

    config_details = (
        f"  [bold]Type:[/bold] [info]{current_config.get('type', 'unknown')}[/info]\n"
        f"  [bold]Location:[/bold] [info]{config.config_dir}[/info]\n"
        f"  [bold]Version:[/bold] [info]{current_config.get('version', '1.0')}[/info]\n"
    )
    if current_config.get("project_name"):
        config_details += f"  [bold]Project:[/bold] [info]{current_config.get('project_name')}[/info]\n"
    if current_config.get("created_at"):
        config_details += f"  [bold]Created:[/bold] [info]{current_config.get('created_at')}[/info]"

    print_info_panel(config_details, title="OKO Configuration")

    endpoints_data = load_endpoints()
    endpoints = endpoints_data.get("endpoints", {})
    console.print(f"\n[bold primary]📊 Endpoints found:[/bold primary] [bold secondary]{len(endpoints)}[/bold secondary]")

    if endpoints:
        table = get_table()
        table.add_column("Alias", style="blue", no_wrap=True)
        table.add_column("Method", style="cyan")
        table.add_column("URL", style="white")

        for alias, endpoint in endpoints.items():
            method = endpoint.get("method", "GET")
            url = endpoint.get("url", "")
            table.add_row(alias, method, url[:70] + ("..." if len(url) > 70 else ""))
        
        console.print(table)


@endpoint_app.command("add")
def endpoint_add(
    alias: str = typer.Argument(..., help="Alias to identify the endpoint"),
    url: str = typer.Argument(..., help="Full URL of the endpoint"),
    method: str = typer.Option(
        "GET", "--method", "-M", help="HTTP method"
    ),
):
    """Register a new endpoint."""
    if not config.find_config():
        print_warning("No OKO configuration found. Run [secondary]oko init[/secondary] first.")
        raise typer.Exit(1)

    method = method.upper()
    SUPPORTED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

    if method not in SUPPORTED_METHODS:
        print_error(f"Method '{method}' not supported. Choose from: [info]{', '.join(SUPPORTED_METHODS)}[/info]")
        raise typer.Exit(1)

    add_endpoint(alias, url, method)
    
    message = (
        f"Alias: [primary]{alias}[/primary]\n"
        f"URL: [info]{method} {url}[/info]\n"
        f"Saved in: [dim]{config.config_dir}[/dim]"
    )
    print_success(message, title=f"Endpoint '{alias}' saved!")


@app.command("run")
def run(
    alias: str,
    param: List[str] = typer.Option(
        None, "--param", "-p", help="Query params (key=value). Use multiple times."
    ),
    header: List[str] = typer.Option(
        None, "--header", "-H", help="HTTP headers (key=value). Use multiple times."
    ),
    body: Optional[str] = typer.Option(
        None, "--body", "-B", help="JSON body or use '@file.json' to load from a file."
    ),
):
    """
    Run a saved endpoint.
    
    Examples:
      - [cyan]oko run my_api -p id=123[/cyan]
      - [cyan]oko run create_user -B '{"name":"Test"}'[/cyan]
      - [cyan]oko run upload -B @data.json[/cyan]
    """
    if not config.find_config():
        print_warning("No OKO configuration found. Run [secondary]oko init[/secondary] first.")
        raise typer.Exit(1)

    with console.status(f"[bold green]Running [primary]'{alias}'[/primary]...[/bold green]", spinner="dots"):
        run_endpoint(alias, console, param, header, body)


if __name__ == "__main__":
    app()
