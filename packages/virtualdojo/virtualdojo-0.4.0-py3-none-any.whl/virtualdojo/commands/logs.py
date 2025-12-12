"""Log viewing and management commands for VirtualDojo CLI."""

import time
from typing import Optional

import typer

from ..client import SyncVirtualDojoClient
from ..utils.output import console, print_error, print_json, print_warning

app = typer.Typer(help="Log viewing and management")


@app.command("list")
def list_logs(
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum logs to return"),
    offset: int = typer.Option(0, "--skip", "-s", help="Logs to skip"),
    level: Optional[str] = typer.Option(
        None,
        "--level",
        help="Filter by level: debug, info, warning, error",
    ),
    component: Optional[str] = typer.Option(
        None,
        "--component",
        "-c",
        help="Filter by component name",
    ),
    source: Optional[str] = typer.Option(
        None,
        "--source",
        help="Filter by source: frontend, backend, system",
    ),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """List debug logs with filtering.

    Examples:
        vdojo logs list
        vdojo logs list --level error
        vdojo logs list --component RecordList --limit 20
        vdojo logs list --source backend --format json
    """
    try:
        client = SyncVirtualDojoClient(profile)

        params = {"limit": limit, "offset": offset}
        if level:
            params["log_level"] = level
        if component:
            params["component"] = component
        if source:
            params["source"] = source

        result = client.get("/api/v1/debug-logs", params=params)

        logs = result.get("logs", [])
        total = result.get("total", 0)

        if format == "json":
            print_json(logs)
            return

        if not logs:
            console.print("[dim]No logs found[/dim]")
            return

        from rich.table import Table

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Time", style="dim", width=19)
        table.add_column("Level", width=8)
        table.add_column("Component", width=20)
        table.add_column("Message", width=50)

        for log in logs:
            level_str = log.get("log_level", "info").upper()
            level_style = {
                "ERROR": "[red]ERROR[/red]",
                "WARNING": "[yellow]WARN[/yellow]",
                "INFO": "[green]INFO[/green]",
                "DEBUG": "[dim]DEBUG[/dim]",
            }.get(level_str, level_str)

            created_at = str(log.get("created_at", ""))[:19]
            message = log.get("message", "")[:50]
            if len(log.get("message", "")) > 50:
                message += "..."

            table.add_row(
                created_at,
                level_style,
                log.get("component", "-")[:20],
                message,
            )

        console.print(table)
        console.print(f"\n[dim]Showing {len(logs)} of {total} logs[/dim]")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("search")
def search_logs(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum results"),
    level: Optional[str] = typer.Option(None, "--level", help="Filter by level"),
    component: Optional[str] = typer.Option(None, "--component", "-c", help="Filter by component"),
    start_date: Optional[str] = typer.Option(None, "--start", help="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, "--end", help="End date (YYYY-MM-DD)"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Search logs with full-text search.

    Examples:
        vdojo logs search "error"
        vdojo logs search "failed to load" --level error
        vdojo logs search "RecordList" --component RecordList
        vdojo logs search "authentication" --start 2024-01-01
    """
    try:
        client = SyncVirtualDojoClient(profile)

        params = {"query": query, "limit": limit}
        if level:
            params["log_level"] = level
        if component:
            params["component"] = component
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        result = client.get("/api/v1/logs/search", params=params)

        logs = result.get("logs", result) if isinstance(result, dict) else result

        if format == "json":
            print_json(logs)
            return

        if not logs:
            console.print("[dim]No logs found matching your search[/dim]")
            return

        from rich.table import Table

        table = Table(show_header=True, header_style="bold cyan", title=f"Search: {query}")
        table.add_column("Time", style="dim", width=19)
        table.add_column("Level", width=8)
        table.add_column("Component", width=20)
        table.add_column("Message", width=50)

        for log in logs:
            level_str = log.get("log_level", "info").upper()
            level_style = {
                "ERROR": "[red]ERROR[/red]",
                "WARNING": "[yellow]WARN[/yellow]",
                "INFO": "[green]INFO[/green]",
                "DEBUG": "[dim]DEBUG[/dim]",
            }.get(level_str, level_str)

            created_at = str(log.get("created_at", ""))[:19]
            message = log.get("message", "")[:50]
            if len(log.get("message", "")) > 50:
                message += "..."

            table.add_row(
                created_at,
                level_style,
                log.get("component", "-")[:20],
                message,
            )

        console.print(table)
        console.print(f"\n[dim]{len(logs)} results[/dim]")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("stats")
def log_stats(
    hours: int = typer.Option(24, "--hours", "-h", help="Time range in hours"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Show log statistics and analytics.

    Examples:
        vdojo logs stats
        vdojo logs stats --hours 48
        vdojo logs stats --format json
    """
    try:
        client = SyncVirtualDojoClient(profile)

        result = client.get("/api/v1/debug-logs/stats", params={"hours": hours})

        if format == "json":
            print_json(result)
            return

        console.print(f"\n[bold cyan]Log Statistics (last {hours} hours)[/bold cyan]\n")

        total = result.get("total_logs", 0)
        console.print(f"[bold]Total Logs:[/bold] {total:,}")

        # Logs by level
        by_level = result.get("logs_by_level", {})
        if by_level:
            console.print("\n[bold]By Level:[/bold]")
            for level, count in sorted(by_level.items(), key=lambda x: -x[1]):
                level_style = {
                    "error": "[red]",
                    "warning": "[yellow]",
                    "info": "[green]",
                    "debug": "[dim]",
                }.get(level.lower(), "")
                console.print(f"  {level_style}{level.upper()}[/]: {count:,}")

        # Logs by component
        by_component = result.get("logs_by_component", {})
        if by_component:
            console.print("\n[bold]Top Components:[/bold]")
            sorted_components = sorted(by_component.items(), key=lambda x: -x[1])[:10]
            for component, count in sorted_components:
                console.print(f"  {component}: {count:,}")

        # Logs by source
        by_source = result.get("logs_by_source", {})
        if by_source:
            console.print("\n[bold]By Source:[/bold]")
            for source, count in by_source.items():
                console.print(f"  {source}: {count:,}")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("tail")
def tail_logs(
    follow: bool = typer.Option(True, "--follow", "-f", help="Follow logs in real-time"),
    level: Optional[str] = typer.Option(None, "--level", help="Filter by level"),
    component: Optional[str] = typer.Option(None, "--component", "-c", help="Filter by component"),
    interval: int = typer.Option(2, "--interval", "-i", help="Polling interval in seconds"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Stream logs in real-time (like tail -f).

    Examples:
        vdojo logs tail
        vdojo logs tail --level error
        vdojo logs tail --component RecordList --interval 5
    """
    try:
        client = SyncVirtualDojoClient(profile)

        console.print("[bold cyan]Streaming logs...[/bold cyan] (Ctrl+C to stop)\n")

        seen_ids = set()
        last_timestamp = None

        while True:
            try:
                params = {"limit": 20}
                if level:
                    params["log_level"] = level
                if component:
                    params["component"] = component

                result = client.get("/api/v1/debug-logs", params=params)
                logs = result.get("logs", [])

                # Process new logs (reverse to show oldest first)
                for log in reversed(logs):
                    log_id = log.get("id")
                    if log_id and log_id not in seen_ids:
                        seen_ids.add(log_id)

                        level_str = log.get("log_level", "info").upper()
                        level_style = {
                            "ERROR": "[red]ERROR[/red]",
                            "WARNING": "[yellow]WARN[/yellow]",
                            "INFO": "[green]INFO[/green]",
                            "DEBUG": "[dim]DEBUG[/dim]",
                        }.get(level_str, level_str)

                        created_at = str(log.get("created_at", ""))[:19]
                        component_name = log.get("component", "-")
                        message = log.get("message", "")

                        console.print(
                            f"[dim]{created_at}[/dim] {level_style} "
                            f"[cyan]{component_name}[/cyan]: {message}"
                        )

                if not follow:
                    break

                time.sleep(interval)

            except KeyboardInterrupt:
                console.print("\n[dim]Stopped streaming[/dim]")
                break

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("components")
def list_components(
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """List all components with debug logging.

    Examples:
        vdojo logs components
    """
    try:
        client = SyncVirtualDojoClient(profile)

        result = client.get("/api/v1/debug-logs/components")

        components = result if isinstance(result, list) else result.get("data", [])

        if not components:
            console.print("[dim]No components found[/dim]")
            return

        from rich.table import Table

        table = Table(show_header=True, header_style="bold cyan", title="Debug Components")
        table.add_column("Component")
        table.add_column("Enabled")
        table.add_column("Logs (24h)", justify="right")

        for comp in components:
            enabled = "[green]Yes[/green]" if comp.get("is_enabled") else "[dim]No[/dim]"
            table.add_row(
                comp.get("component", "-"),
                enabled,
                str(comp.get("log_count_24h", 0)),
            )

        console.print(table)

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("analytics")
def log_analytics(
    hours: int = typer.Option(24, "--hours", "-h", help="Time range in hours"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Get comprehensive log analytics.

    Examples:
        vdojo logs analytics
        vdojo logs analytics --hours 48
    """
    try:
        client = SyncVirtualDojoClient(profile)

        result = client.get("/api/v1/logs/analytics", params={"hours": hours})

        if format == "json":
            print_json(result)
            return

        console.print(f"\n[bold cyan]Log Analytics (last {hours} hours)[/bold cyan]\n")

        console.print(f"[bold]Total Logs:[/bold] {result.get('total_logs', 0):,}")

        # Error patterns
        error_patterns = result.get("error_patterns", [])
        if error_patterns:
            console.print("\n[bold red]Common Error Patterns:[/bold red]")
            for pattern in error_patterns[:5]:
                count = pattern.get("count", 0)
                message = pattern.get("message", "")[:60]
                console.print(f"  ({count}x) {message}")

        # Top users
        top_users = result.get("top_users", [])
        if top_users:
            console.print("\n[bold]Top Users by Log Volume:[/bold]")
            for user in top_users[:5]:
                console.print(f"  {user.get('user_email', 'Unknown')}: {user.get('log_count', 0):,}")

        # Hourly trends
        trends = result.get("hourly_trends", [])
        if trends:
            console.print("\n[bold]Hourly Trend (last 6 hours):[/bold]")
            for trend in trends[-6:]:
                hour = trend.get("hour", "")
                count = trend.get("count", 0)
                bar = "#" * min(count // 10, 30)
                console.print(f"  {hour}: {bar} {count}")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)
