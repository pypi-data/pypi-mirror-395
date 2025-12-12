"""Record CRUD commands for VirtualDojo CLI."""

import json
from pathlib import Path
from typing import Optional

import typer

from ..client import SyncVirtualDojoClient
from ..utils.filters import parse_filters
from ..utils.output import console, print_error, print_record, print_records, print_success

app = typer.Typer(help="Record operations (CRUD)")


@app.command("list")
def list_records(
    object_name: str = typer.Argument(..., help="Object API name (e.g., accounts, contacts)"),
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum records to return"),
    skip: int = typer.Option(0, "--skip", "-s", help="Records to skip (pagination)"),
    filter: Optional[str] = typer.Option(
        None,
        "--filter",
        "-f",
        help="Filter expression (e.g., 'status=active,amount_gte=10000')",
    ),
    sort: Optional[str] = typer.Option(None, "--sort", help="Field to sort by"),
    desc: bool = typer.Option(False, "--desc", "-d", help="Sort descending"),
    columns: Optional[str] = typer.Option(
        None,
        "--columns",
        "-c",
        help="Columns to show (comma-separated)",
    ),
    format: str = typer.Option("table", "--format", help="Output format: table, json, yaml"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p", help="Profile to use"),
) -> None:
    """List records from an object.

    Examples:
        vdojo records list accounts
        vdojo records list opportunities --filter "stage_ne=closed,amount_gte=10000"
        vdojo records list contacts --limit 100 --sort created_at --desc
        vdojo records list accounts --format json
    """
    try:
        client = SyncVirtualDojoClient(profile)

        params: dict = {
            "limit": limit,
            "skip": skip,
        }

        if filter:
            params["filters"] = parse_filters(filter)
        if sort:
            params["sort_by"] = sort
            params["sort_order"] = "desc" if desc else "asc"

        result = client.get(f"/api/v1/objects/{object_name}/records", params=params)

        # API returns: {"object": {...}, "records": [...], "total_count": N, "pagination": {...}}
        records = result.get("records", result.get("data", [])) if isinstance(result, dict) else result
        total = result.get("total_count", result.get("total", len(records))) if isinstance(result, dict) else len(records)

        col_list = columns.split(",") if columns else None
        print_records(records, format=format, columns=col_list)

        if format == "table":
            console.print(f"\n[dim]Showing {len(records)} of {total} records[/dim]")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("get")
def get_record(
    object_name: str = typer.Argument(..., help="Object API name"),
    record_id: str = typer.Argument(..., help="Record ID"),
    format: str = typer.Option("table", "--format", help="Output format: table, json, yaml"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Get a single record by ID.

    Examples:
        vdojo records get accounts acc-123
        vdojo records get opportunities opp-456 --format json
    """
    try:
        client = SyncVirtualDojoClient(profile)
        record = client.get(f"/api/v1/objects/{object_name}/records/{record_id}")
        print_record(record, format=format)

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("create")
def create_record(
    object_name: str = typer.Argument(..., help="Object API name"),
    data: Optional[str] = typer.Option(
        None,
        "--data",
        "-d",
        help="JSON data for the record",
    ),
    file: Optional[Path] = typer.Option(
        None,
        "--file",
        "-f",
        help="JSON file containing record data",
    ),
    set_field: Optional[list[str]] = typer.Option(
        None,
        "--set",
        "-s",
        help="Field=value pairs (can be repeated)",
    ),
    format: str = typer.Option("table", "--format", help="Output format"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Create a new record.

    Examples:
        vdojo records create accounts --data '{"name": "Acme Corp"}'
        vdojo records create contacts --file contact.json
        vdojo records create tasks --set "name=Follow up" --set "status=pending"
    """
    try:
        # Build record data from various sources
        record_data: dict = {}

        if file:
            with open(file) as f:
                record_data = json.load(f)
        elif data:
            record_data = json.loads(data)

        # Apply --set field overrides
        if set_field:
            for field_value in set_field:
                if "=" in field_value:
                    key, value = field_value.split("=", 1)
                    record_data[key.strip()] = _parse_cli_value(value.strip())

        if not record_data:
            print_error("No data provided. Use --data, --file, or --set")
            raise typer.Exit(1)

        client = SyncVirtualDojoClient(profile)
        result = client.post(f"/api/v1/objects/{object_name}/records", record_data)

        print_success(f"Created {object_name} record: {result.get('id', 'unknown')}")
        print_record(result, format=format)

    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON: {e}")
        raise typer.Exit(1)
    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("update")
def update_record(
    object_name: str = typer.Argument(..., help="Object API name"),
    record_id: str = typer.Argument(..., help="Record ID"),
    data: Optional[str] = typer.Option(
        None,
        "--data",
        "-d",
        help="JSON data with fields to update",
    ),
    set_field: Optional[list[str]] = typer.Option(
        None,
        "--set",
        "-s",
        help="Field=value pairs (can be repeated)",
    ),
    format: str = typer.Option("table", "--format", help="Output format"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Update an existing record.

    Examples:
        vdojo records update accounts acc-123 --set "status=active"
        vdojo records update opportunities opp-456 --data '{"stage": "closed_won"}'
        vdojo records update contacts c-789 --set "email=new@email.com" --set "phone=555-1234"
    """
    try:
        update_data: dict = {}

        if data:
            update_data = json.loads(data)

        if set_field:
            for field_value in set_field:
                if "=" in field_value:
                    key, value = field_value.split("=", 1)
                    update_data[key.strip()] = _parse_cli_value(value.strip())

        if not update_data:
            print_error("No data provided. Use --data or --set")
            raise typer.Exit(1)

        client = SyncVirtualDojoClient(profile)
        result = client.put(
            f"/api/v1/objects/{object_name}/records/{record_id}",
            update_data,
        )

        print_success(f"Updated {object_name} record: {record_id}")
        print_record(result, format=format)

    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON: {e}")
        raise typer.Exit(1)
    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("delete")
def delete_record(
    object_name: str = typer.Argument(..., help="Object API name"),
    record_id: str = typer.Argument(..., help="Record ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Delete a record (soft delete).

    Examples:
        vdojo records delete accounts acc-123
        vdojo records delete tasks t-456 --force
    """
    if not force:
        confirm = typer.confirm(f"Delete {object_name} record {record_id}?")
        if not confirm:
            raise typer.Abort()

    try:
        client = SyncVirtualDojoClient(profile)
        client.delete(f"/api/v1/objects/{object_name}/records/{record_id}")
        print_success(f"Deleted {object_name} record: {record_id}")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("count")
def count_records(
    object_name: str = typer.Argument(..., help="Object API name"),
    filter: Optional[str] = typer.Option(
        None,
        "--filter",
        "-f",
        help="Filter expression",
    ),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Count records in an object.

    Examples:
        vdojo records count accounts
        vdojo records count opportunities --filter "status=active"
    """
    try:
        client = SyncVirtualDojoClient(profile)

        params: dict = {"limit": 1}  # Just need total count
        if filter:
            params["filters"] = parse_filters(filter)

        result = client.get(f"/api/v1/objects/{object_name}/records", params=params)

        # API returns: {"object": {...}, "records": [...], "total_count": N, "pagination": {...}}
        total = result.get("total_count", result.get("total", 0)) if isinstance(result, dict) else len(result)
        console.print(f"[bold]{total}[/bold] records")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


def _parse_cli_value(value: str):
    """Parse a CLI value string into appropriate Python type."""
    # Boolean
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    # Null
    if value.lower() in ("null", "none", ""):
        return None

    # Number
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        pass

    # JSON (for nested objects/arrays)
    if value.startswith("{") or value.startswith("["):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass

    # String (default)
    return value
