"""System health and monitoring commands for VirtualDojo CLI."""

from typing import Optional

import typer

from ..client import SyncVirtualDojoClient
from ..utils.output import console, print_error, print_success, print_warning

app = typer.Typer(help="System health and monitoring")


@app.command("health")
def health_check(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed health info"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Check system health status.

    Examples:
        vdojo system health
        vdojo system health --verbose
    """
    try:
        client = SyncVirtualDojoClient(profile)

        # Check main health endpoint
        try:
            result = client.get("/health")
            status = result.get("status", "unknown")

            if status == "healthy":
                print_success("System is healthy")
            else:
                print_warning(f"System status: {status}")

            if verbose:
                console.print("\n[bold]Health Details:[/bold]")
                for key, value in result.items():
                    console.print(f"  {key}: {value}")

        except Exception as e:
            print_error(f"Health check failed: {str(e)}")
            raise typer.Exit(1)

        # Check database health if verbose
        if verbose:
            try:
                db_result = client.get("/api/v1/sql-provisioning/health-check")
                console.print("\n[bold]Database Health:[/bold]")
                console.print(f"  Status: {db_result.get('status', 'unknown')}")
                if "database" in db_result:
                    console.print(f"  Database: {db_result.get('database')}")
                if "connection_pool" in db_result:
                    pool = db_result.get("connection_pool", {})
                    console.print(f"  Pool Size: {pool.get('size', 'N/A')}")
                    console.print(f"  Checked Out: {pool.get('checked_out', 'N/A')}")
            except Exception:
                console.print("\n[dim]Database health: Unable to check[/dim]")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("info")
def system_info(
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Show system information.

    Examples:
        vdojo system info
    """
    try:
        client = SyncVirtualDojoClient(profile)

        # Get health info
        result = client.get("/health")

        console.print("\n[bold cyan]VirtualDojo System Info[/bold cyan]")
        console.print(f"  Server: {client._profile_name or 'default'}")
        console.print(f"  Status: {result.get('status', 'unknown')}")

        if "version" in result:
            console.print(f"  Version: {result.get('version')}")
        if "environment" in result:
            console.print(f"  Environment: {result.get('environment')}")
        if "uptime" in result:
            console.print(f"  Uptime: {result.get('uptime')}")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)
