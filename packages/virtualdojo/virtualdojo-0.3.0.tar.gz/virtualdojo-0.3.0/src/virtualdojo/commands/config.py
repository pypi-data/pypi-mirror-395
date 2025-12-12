"""Configuration commands for VirtualDojo CLI."""

from typing import Optional

import typer
from rich.table import Table

from ..config import config_manager, get_config_dir, get_config_file
from ..utils.output import console, print_error, print_success, print_warning

app = typer.Typer(help="Configuration management")


@app.command("show")
def show_config() -> None:
    """Show current configuration.

    Examples:
        vdojo config show
    """
    config = config_manager.config

    console.print("\n[bold cyan]Configuration[/bold cyan]")
    console.print(f"[dim]Config file:[/dim] {get_config_file()}")
    console.print(f"[dim]Config dir:[/dim] {get_config_dir()}")
    console.print()
    console.print(f"[dim]Default profile:[/dim] {config.default_profile or '[not set]'}")
    console.print(f"[dim]Output format:[/dim] {config.output_format}")
    console.print(f"[dim]Default limit:[/dim] {config.default_limit}")
    console.print()

    if config.profiles:
        console.print("[bold]Profiles:[/bold]")
        for name, profile in config.profiles.items():
            is_default = " [green](default)[/green]" if name == config.default_profile else ""
            has_creds = " [dim]●[/dim]" if config_manager.has_credentials(name) else " [dim]○[/dim]"
            console.print(f"  {has_creds} {name}{is_default}")
            console.print(f"      [dim]Server:[/dim] {profile.server}")
            console.print(f"      [dim]Tenant:[/dim] {profile.tenant}")
    else:
        console.print("[dim]No profiles configured[/dim]")


@app.command("get")
def get_setting(
    key: str = typer.Argument(..., help="Setting key to get"),
) -> None:
    """Get a configuration setting.

    Examples:
        vdojo config get default_limit
        vdojo config get output_format
    """
    config = config_manager.config

    if key == "default_profile":
        console.print(config.default_profile or "[not set]")
    elif key == "output_format":
        console.print(config.output_format)
    elif key == "default_limit":
        console.print(str(config.default_limit))
    else:
        print_error(f"Unknown setting: {key}")
        console.print("[dim]Available settings: default_profile, output_format, default_limit[/dim]")
        raise typer.Exit(1)


@app.command("set")
def set_setting(
    key: str = typer.Argument(..., help="Setting key"),
    value: str = typer.Argument(..., help="Setting value"),
) -> None:
    """Set a configuration setting.

    Examples:
        vdojo config set default_limit 100
        vdojo config set output_format json
    """
    config = config_manager.config

    if key == "default_profile":
        if value not in config.profiles:
            print_error(f"Profile '{value}' does not exist")
            raise typer.Exit(1)
        config.default_profile = value
    elif key == "output_format":
        if value not in ("table", "json", "yaml"):
            print_error("output_format must be: table, json, or yaml")
            raise typer.Exit(1)
        config.output_format = value
    elif key == "default_limit":
        try:
            config.default_limit = int(value)
        except ValueError:
            print_error("default_limit must be a number")
            raise typer.Exit(1)
    else:
        print_error(f"Unknown setting: {key}")
        console.print("[dim]Available settings: default_profile, output_format, default_limit[/dim]")
        raise typer.Exit(1)

    config_manager.save_config()
    print_success(f"Set {key} = {value}")


# Profile subcommands
profile_app = typer.Typer(help="Profile management")


@profile_app.command("list")
def list_profiles() -> None:
    """List all configured profiles.

    Examples:
        vdojo config profile list
    """
    profiles = config_manager.list_profiles()

    if not profiles:
        console.print("[dim]No profiles configured[/dim]")
        console.print("[dim]Run 'vdojo auth login' to create a profile[/dim]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Name")
    table.add_column("Server")
    table.add_column("Tenant")
    table.add_column("Default")
    table.add_column("Logged In")

    default_profile = config_manager.config.default_profile

    for profile in profiles:
        is_default = "[green]✓[/green]" if profile.name == default_profile else ""
        has_creds = "[green]✓[/green]" if config_manager.has_credentials(profile.name) else "[dim]-[/dim]"

        table.add_row(
            profile.name,
            profile.server,
            profile.tenant,
            is_default,
            has_creds,
        )

    console.print(table)


@profile_app.command("add")
def add_profile(
    name: str = typer.Argument(..., help="Profile name"),
    server: str = typer.Option(..., "--server", "-s", help="Server URL"),
    tenant: str = typer.Option(..., "--tenant", "-t", help="Tenant ID or subdomain"),
    set_default: bool = typer.Option(False, "--default", "-d", help="Set as default profile"),
) -> None:
    """Add a new profile.

    Examples:
        vdojo config profile add production --server https://api.virtualdojo.com --tenant my-company
        vdojo config profile add local --server http://localhost:8000 --tenant test --default
    """
    from ..config import Profile

    if name in config_manager.config.profiles:
        print_warning(f"Profile '{name}' already exists, updating...")

    profile = Profile(
        name=name,
        server=server.rstrip("/"),
        tenant=tenant,
    )

    config_manager.add_profile(profile, set_default=set_default)
    print_success(f"Profile '{name}' added")

    if set_default:
        console.print(f"[dim]Set as default profile[/dim]")


@profile_app.command("remove")
def remove_profile(
    name: str = typer.Argument(..., help="Profile name to remove"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
) -> None:
    """Remove a profile.

    Examples:
        vdojo config profile remove staging
        vdojo config profile remove old-profile --force
    """
    if name not in config_manager.config.profiles:
        print_error(f"Profile '{name}' does not exist")
        raise typer.Exit(1)

    if not force:
        confirm = typer.confirm(f"Remove profile '{name}'?")
        if not confirm:
            raise typer.Abort()

    config_manager.remove_profile(name)
    print_success(f"Profile '{name}' removed")


@profile_app.command("use")
def use_profile(
    name: str = typer.Argument(..., help="Profile name to use as default"),
) -> None:
    """Set the default profile.

    Examples:
        vdojo config profile use production
    """
    if name not in config_manager.config.profiles:
        print_error(f"Profile '{name}' does not exist")
        raise typer.Exit(1)

    config_manager.set_default_profile(name)
    print_success(f"Default profile set to '{name}'")


# Add profile subcommands to config app
app.add_typer(profile_app, name="profile")
