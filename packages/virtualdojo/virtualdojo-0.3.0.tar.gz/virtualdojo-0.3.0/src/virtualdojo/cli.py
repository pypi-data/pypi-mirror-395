"""Main CLI application for VirtualDojo."""

from typing import Optional

import typer
from rich.console import Console

from . import __version__, DEFAULT_SERVER_URL
from .commands import ai, auth, config, files, logs, records, schema, system
from .exceptions import VirtualDojoError

console = Console()

# Create main app
app = typer.Typer(
    name="vdojo",
    help="VirtualDojo CLI - Command-line interface for VirtualDojo CRM",
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=False,
)


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        console.print(f"VirtualDojo CLI version [bold]{__version__}[/bold]")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        is_eager=True,
    ),
) -> None:
    """VirtualDojo CLI - Interact with VirtualDojo CRM from the command line.

    Use 'vdojo login' to get started.

    Examples:
        vdojo login                              # Login to default server
        vdojo login --local                      # Login to localhost:8000
        vdojo login -s myserver.com -t tenant    # Login to custom server
        vdojo records list accounts              # List records
        vdojo schema describe opportunities      # Describe object
    """
    if version:
        console.print(f"VirtualDojo CLI version [bold]{__version__}[/bold]")
        raise typer.Exit()


# =============================================================================
# Top-level shortcuts for common commands
# =============================================================================


@app.command("login")
def login_shortcut(
    server: Optional[str] = typer.Option(
        None,
        "--server",
        "-s",
        help=f"Server URL or shortcut. Env: VIRTUALDOJO_SERVER. Default: {DEFAULT_SERVER_URL}",
    ),
    tenant: Optional[str] = typer.Option(
        None,
        "--tenant",
        "-t",
        help="Tenant ID or subdomain. Env: VIRTUALDOJO_TENANT. Auto-detected if not provided.",
    ),
    email: Optional[str] = typer.Option(
        None,
        "--email",
        "-e",
        help="Email address. Env: VIRTUALDOJO_EMAIL. Prompts if not provided.",
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        "-k",
        help="API key. Env: VIRTUALDOJO_API_KEY (preferred for security).",
    ),
    profile_name: str = typer.Option(
        "default",
        "--profile",
        help="Profile name to save credentials under",
    ),
    local: bool = typer.Option(
        False,
        "--local",
        "-l",
        help="Shortcut for --server localhost:8000",
    ),
) -> None:
    """Login to VirtualDojo (shortcut for 'vdojo auth login').

    Just enter your email and password - tenant is auto-detected!
    If you belong to multiple tenants, you'll be prompted to choose.

    SECURITY: For CI/CD and scripts, use environment variables:

        export VIRTUALDOJO_API_KEY=sk-abc123
        export VIRTUALDOJO_TENANT=my-company
        vdojo login

    Server shortcuts:
      --local, -l     → http://localhost:8000
      --server local  → http://localhost:8000
      --server staging → staging server

    Examples:
        vdojo login                              # Interactive login
        vdojo login --local                      # Connect to localhost:8000
        vdojo login -t my-company                # Specify tenant explicitly
    """
    auth.login(
        server=server,
        tenant=tenant,
        email=email,
        api_key=api_key,
        profile_name=profile_name,
        local=local,
    )


@app.command("logout")
def logout_shortcut(
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        "-p",
        help="Profile to logout from",
    ),
    all_profiles: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Logout from all profiles",
    ),
) -> None:
    """Logout from VirtualDojo (shortcut for 'vdojo auth logout')."""
    auth.logout(profile=profile, all_profiles=all_profiles)


@app.command("whoami")
def whoami_shortcut(
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        "-p",
        help="Profile to check",
    ),
) -> None:
    """Show current user info (shortcut for 'vdojo auth whoami')."""
    auth.whoami(profile=profile)


# =============================================================================
# Register command groups
# =============================================================================

app.add_typer(auth.app, name="auth", help="Authentication and API key management")
app.add_typer(records.app, name="records", help="Record CRUD operations")
app.add_typer(schema.app, name="schema", help="Schema discovery and object management")
app.add_typer(files.app, name="files", help="File upload, download, and management")
app.add_typer(config.app, name="config", help="CLI configuration management")
app.add_typer(ai.app, name="ai", help="AI chat and conversations")
app.add_typer(logs.app, name="logs", help="Log viewing and management")
app.add_typer(system.app, name="system", help="System health and monitoring")




def run() -> None:
    """Run the CLI application."""
    try:
        app()
    except VirtualDojoError as e:
        console.print(f"[red]Error:[/red] {e.message}")
        if e.hint:
            console.print(f"[dim]Hint: {e.hint}[/dim]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted[/dim]")
        raise typer.Exit(130)


if __name__ == "__main__":
    run()
