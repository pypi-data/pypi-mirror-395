import httpx
import json
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from rich.console import Console
from rich.pretty import Pretty
from rich.table import Table
from rich.panel import Panel
from rich.box import ROUNDED

from .config import load_endpoints
from ..ui import print_error


def _make_key_value_table(data: dict) -> Table:
    """Creates a styled table for key-value data."""
    table = Table(box=ROUNDED, show_header=False, border_style="secondary")
    table.add_column("Key", style="info", no_wrap=True)
    table.add_column("Value", style="white")
    for key, value in data.items():
        table.add_row(str(key), str(value))
    return table


def parse_params(param_list, console: Console):
    """Convert ['a=1', 'b=2'] into {'a': '1', 'b': '2'}"""
    params = {}
    if not param_list:
        return params
    for item in param_list:
        if "=" not in item:
            console.print(f"[warning]Skipping invalid param:[/] {item}")
            continue
        key, value = item.split("=", 1)
        params[key] = value
    return params


def parse_headers(header_list, console: Console):
    """Convert headers list to dict"""
    headers = {}
    if not header_list:
        return headers
    for item in header_list:
        if "=" not in item:
            console.print(f"[warning]Skipping invalid header:[/] {item}")
            continue
        key, value = item.split("=", 1)
        headers[key] = value
    return headers


def parse_body(body_data, console: Console):
    """Parse JSON body from string or file"""
    if not body_data:
        return None

    if body_data.startswith("@"):
        filepath = body_data[1:]
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except Exception as e:
            print_error(f"Error reading body file: {e}")
            return None

    try:
        return json.loads(body_data)
    except json.JSONDecodeError:
        print_error(f"Invalid JSON body: {body_data}")
        return None


def merge_query_params(url, extra_params):
    """Merge base URL query params with user-provided params"""
    parsed = urlparse(url)
    base_params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
    final_params = {**base_params, **extra_params}
    new_query = urlencode(final_params)

    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )


def run_endpoint(alias: str, console: Console, params=None, headers=None, body=None):
    data = load_endpoints()
    endpoints = data.get("endpoints", {})

    if alias not in endpoints:
        print_error(f"Endpoint '{alias}' not found.")
        return

    endpoint = endpoints[alias]
    url = endpoint["url"]
    method = endpoint["method"].upper()

    # Parse inputs
    extra_params = parse_params(params, console)
    header_dict = parse_headers(headers, console)
    body_data = parse_body(body, console)

    # Merge URL params
    final_url = merge_query_params(url, extra_params)

    console.rule("[bold primary]Request[/bold primary]")
    console.print(f"[bold]→ {method} {final_url}[/bold]")

    if extra_params:
        console.print(Panel(_make_key_value_table(extra_params), title="[info]Query Parameters[/info]", border_style="secondary"))

    if header_dict:
        console.print(Panel(_make_key_value_table(header_dict), title="[info]Headers[/info]", border_style="secondary"))

    if body_data and method in ["POST", "PUT", "PATCH"]:
        console.print(Panel(Pretty(body_data, expand_all=True), title="[info]Body[/info]", border_style="secondary"))

    console.print()

    try:
        response = httpx.request(
            method, final_url, headers=header_dict, json=body_data if body_data else None
        )

        status_style = "success" if response.is_success else "error"
        console.rule(f"[bold {status_style}]Response[/bold {status_style}]")
        console.print(f"\n[bold]Status:[/bold] [{status_style}]{response.status_code}[/]")

        if response.headers:
            console.print(Panel(_make_key_value_table(response.headers), title="[info]Headers[/info]", border_style="secondary"))

        if response.content:
            try:
                json_data = response.json()
                console.print(Panel(Pretty(json_data, expand_all=True), title="[info]Body[/info]", border_style="secondary"))
            except Exception:
                console.print(Panel(response.text[:2000], title="[warning]Response (Not JSON)[/warning]", border_style="warning"))
        else:
            console.print("\n[dim]No response body[/dim]")

    except Exception as e:
        print_error(f"Error connecting to endpoint: {e}")


