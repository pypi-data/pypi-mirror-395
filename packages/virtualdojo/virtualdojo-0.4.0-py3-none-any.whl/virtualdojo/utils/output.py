"""Output formatting utilities for VirtualDojo CLI."""

import json
from typing import Any, Optional

from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
import yaml

console = Console()


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str, hint: Optional[str] = None) -> None:
    """Print an error message with optional hint."""
    console.print(f"[red]✗[/red] {message}")
    if hint:
        console.print(f"  [dim]{hint}[/dim]")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[yellow]![/yellow] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[blue]ℹ[/blue] {message}")


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print(JSON.from_data(data))


def print_yaml(data: Any) -> None:
    """Print data as formatted YAML."""
    yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False)
    console.print(Syntax(yaml_str, "yaml", theme="monokai"))


def print_record(record: dict[str, Any], format: str = "table") -> None:
    """Print a single record.

    Args:
        record: The record data
        format: Output format (table, json, yaml)
    """
    if format == "json":
        print_json(record)
    elif format == "yaml":
        print_yaml(record)
    else:
        # Table format - show as key-value pairs
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Field", style="bold")
        table.add_column("Value")

        for key, value in record.items():
            if value is None:
                value_str = "[dim]null[/dim]"
            elif isinstance(value, bool):
                value_str = "[green]true[/green]" if value else "[red]false[/red]"
            elif isinstance(value, dict):
                value_str = json.dumps(value, indent=2)[:100]
                if len(json.dumps(value)) > 100:
                    value_str += "..."
            elif isinstance(value, list):
                value_str = f"[{len(value)} items]"
            else:
                value_str = str(value)

            table.add_row(key, value_str)

        console.print(table)


def print_records(
    records: list[dict[str, Any]],
    format: str = "table",
    columns: Optional[list[str]] = None,
    title: Optional[str] = None,
) -> None:
    """Print multiple records.

    Args:
        records: List of record dictionaries
        format: Output format (table, json, yaml)
        columns: Specific columns to show (None = all)
        title: Optional table title
    """
    if not records:
        console.print("[dim]No records found[/dim]")
        return

    if format == "json":
        print_json(records)
        return

    if format == "yaml":
        print_yaml(records)
        return

    # Table format
    table = Table(show_header=True, header_style="bold cyan", title=title)

    # Determine columns to show
    if columns:
        show_columns = columns
    else:
        # Use keys from first record, prioritizing common fields
        priority_fields = ["id", "name", "email", "status", "created_at", "updated_at"]
        all_keys = list(records[0].keys())

        # Sort: priority fields first, then alphabetically
        show_columns = []
        for field in priority_fields:
            if field in all_keys:
                show_columns.append(field)
                all_keys.remove(field)

        # Add remaining columns (limit to prevent table overflow)
        remaining = sorted(all_keys)
        max_columns = 8
        show_columns.extend(remaining[: max_columns - len(show_columns)])

    # Add columns to table
    for col in show_columns:
        table.add_column(col)

    # Add rows
    for record in records:
        row_values = []
        for col in show_columns:
            value = record.get(col)
            if value is None:
                row_values.append("[dim]-[/dim]")
            elif isinstance(value, bool):
                row_values.append("[green]✓[/green]" if value else "[red]✗[/red]")
            elif isinstance(value, (dict, list)):
                row_values.append("[dim]...[/dim]")
            else:
                str_value = str(value)
                # Truncate long values
                if len(str_value) > 40:
                    str_value = str_value[:37] + "..."
                row_values.append(str_value)

        table.add_row(*row_values)

    console.print(table)


def print_objects(objects: list[dict[str, Any]], format: str = "table") -> None:
    """Print a list of objects/tables.

    Args:
        objects: List of object definitions
        format: Output format (table, json, yaml)
    """
    if format == "json":
        print_json(objects)
        return

    if format == "yaml":
        print_yaml(objects)
        return

    table = Table(show_header=True, header_style="bold cyan", title="Objects")
    table.add_column("Name", style="bold")
    table.add_column("Label")
    table.add_column("Type")
    table.add_column("Fields")

    for obj in objects:
        # Handle both old (api_name) and new (api_name from schema API) structures
        api_name = obj.get("api_name", obj.get("name", "-"))
        obj_type = "Custom" if obj.get("is_custom", api_name.endswith("_co")) else "Standard"
        # Handle both field_count and fields_count
        field_count = str(obj.get("fields_count", obj.get("field_count", "-")))
        table.add_row(
            api_name,
            obj.get("label", "-"),
            obj_type,
            field_count,
        )

    console.print(table)


def print_fields(fields: list[dict[str, Any]], format: str = "table") -> None:
    """Print a list of fields.

    Args:
        fields: List of field definitions
        format: Output format (table, json, yaml)
    """
    if format == "json":
        print_json(fields)
        return

    if format == "yaml":
        print_yaml(fields)
        return

    table = Table(show_header=True, header_style="bold cyan", title="Fields")
    table.add_column("Name", style="bold")
    table.add_column("Type")
    table.add_column("Required")
    table.add_column("Nullable")

    for field in fields:
        # Handle both old (api_name/field_type) and new (field_name/display_type) structures
        name = field.get("field_name", field.get("api_name", field.get("name", "-")))
        field_type = field.get("display_type", field.get("field_type", field.get("type", "-")))
        is_nullable = field.get("is_nullable", True)
        required = "[green]Yes[/green]" if not is_nullable else "[dim]No[/dim]"
        nullable = "[dim]Yes[/dim]" if is_nullable else "[green]No[/green]"

        table.add_row(name, field_type, required, nullable)

    console.print(table)


def print_panel(content: str, title: str, style: str = "blue") -> None:
    """Print content in a panel."""
    console.print(Panel(content, title=title, border_style=style))


def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def format_duration(seconds: float) -> str:
    """Format seconds as human-readable duration."""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"
