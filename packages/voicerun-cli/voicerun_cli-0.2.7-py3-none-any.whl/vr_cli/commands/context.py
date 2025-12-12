import typer
from rich.table import Table

from ..utils.config import (
    CONTEXTS,
    get_current_context,
    set_current_context,
    get_context_urls,
    get_all_contexts,
    create_context,
    delete_context,
    SUCCESS_STYLE,
    ERROR_STYLE,
    TITLE_STYLE,
    INFO_STYLE,
)
from ..utils.utils import console

app = typer.Typer(help="Manage API context for different environments.")


@app.command("list")
def list_contexts():
    """List all available contexts and show the current one."""
    current = get_current_context()
    all_contexts = get_all_contexts()
    
    table = Table(title="Available Contexts")
    table.add_column("Context", style=TITLE_STYLE)
    table.add_column("API URL", style=INFO_STYLE)
    table.add_column("Frontend URL", style=INFO_STYLE)
    table.add_column("Type", style=INFO_STYLE)
    table.add_column("Current", style=SUCCESS_STYLE)
    
    for name, urls in all_contexts.items():
        is_current = "✓" if name == current else ""
        context_type = "predefined" if name in CONTEXTS else "user-defined"
        table.add_row(name, urls["api_url"], urls["frontend_url"], context_type, is_current)
    
    # Check if using custom URL
    api_url, frontend_url = get_context_urls()
    if current not in all_contexts or api_url not in [ctx["api_url"] for ctx in all_contexts.values()]:
        table.add_row("custom", api_url, frontend_url, "custom", "✓" if current == "custom" else "")
    
    console.print(table)


@app.command("current") 
def show_current():
    """Show the current context and URLs."""
    current = get_current_context()
    api_url, frontend_url = get_context_urls()
    
    console.print(f"[{SUCCESS_STYLE}]Current context:[/{SUCCESS_STYLE}] {current}")
    console.print(f"[{INFO_STYLE}]API URL:[/{INFO_STYLE}] {api_url}")
    console.print(f"[{INFO_STYLE}]Frontend URL:[/{INFO_STYLE}] {frontend_url}")


@app.command("switch")
def switch_context(
    context_name: str = typer.Argument(help="Context name to switch to")
):
    """Switch to a different context."""
    all_contexts = get_all_contexts()
    if context_name in all_contexts:
        set_current_context(context_name)
        api_url, frontend_url = get_context_urls()
        console.print(f"[{SUCCESS_STYLE}]Switched to {context_name} context[/{SUCCESS_STYLE}]")
        console.print(f"[{INFO_STYLE}]API URL:[/{INFO_STYLE}] {api_url}")
        console.print(f"[{INFO_STYLE}]Frontend URL:[/{INFO_STYLE}] {frontend_url}")
    else:
        console.print(f"[{ERROR_STYLE}]Unknown context: {context_name}[/{ERROR_STYLE}]")
        console.print(f"[{INFO_STYLE}]Available contexts: {', '.join(all_contexts.keys())}[/{INFO_STYLE}]")
        raise typer.Exit(1)


@app.command("create")
def create_new_context(
    name: str = typer.Argument(help="Name for the new context"),
    api_url: str = typer.Argument(help="API URL for the context"),
    frontend_url: str = typer.Argument(help="Frontend URL for the context")
):
    """Create a new context."""
    if not api_url.startswith(('http://', 'https://')):
        console.print(f"[{ERROR_STYLE}]API URL must start with http:// or https://[/{ERROR_STYLE}]")
        raise typer.Exit(1)
    
    if not frontend_url.startswith(('http://', 'https://')):
        console.print(f"[{ERROR_STYLE}]Frontend URL must start with http:// or https://[/{ERROR_STYLE}]")
        raise typer.Exit(1)
    
    all_contexts = get_all_contexts()
    if name in all_contexts:
        console.print(f"[{ERROR_STYLE}]Context '{name}' already exists[/{ERROR_STYLE}]")
        raise typer.Exit(1)
    
    create_context(name, api_url, frontend_url)
    console.print(f"[{SUCCESS_STYLE}]Created context '{name}'[/{SUCCESS_STYLE}]")
    console.print(f"[{INFO_STYLE}]API URL:[/{INFO_STYLE}] {api_url}")
    console.print(f"[{INFO_STYLE}]Frontend URL:[/{INFO_STYLE}] {frontend_url}")


@app.command("delete")
def delete_existing_context(
    name: str = typer.Argument(help="Name of the context to delete")
):
    """Delete a user-defined context."""
    success, message = delete_context(name)
    if success:
        console.print(f"[{SUCCESS_STYLE}]{message}[/{SUCCESS_STYLE}]")
    else:
        console.print(f"[{ERROR_STYLE}]{message}[/{ERROR_STYLE}]")
        raise typer.Exit(1)


@app.command("set-url")
def set_custom_url(
    api_url: str = typer.Argument(help="Custom API URL to use")
):
    """Set a custom API URL."""
    if not api_url.startswith(('http://', 'https://')):
        console.print(f"[{ERROR_STYLE}]API URL must start with http:// or https://[/{ERROR_STYLE}]")
        raise typer.Exit(1)
    
    set_current_context("custom", api_url)
    _, frontend_url = get_context_urls()
    console.print(f"[{SUCCESS_STYLE}]Set custom API URL[/{SUCCESS_STYLE}]")
    console.print(f"[{INFO_STYLE}]API URL:[/{INFO_STYLE}] {api_url}")
    console.print(f"[{INFO_STYLE}]Frontend URL:[/{INFO_STYLE}] {frontend_url}")


if __name__ == "__main__":
    app()