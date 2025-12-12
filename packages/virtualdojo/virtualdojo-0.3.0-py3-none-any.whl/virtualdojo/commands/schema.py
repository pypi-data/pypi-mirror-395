"""Schema discovery commands for VirtualDojo CLI."""

from typing import Optional

import typer

from ..client import SyncVirtualDojoClient
from ..utils.output import (
    console,
    print_error,
    print_fields,
    print_json,
    print_objects,
    print_yaml,
)

app = typer.Typer(help="Schema discovery and object management")


@app.command("objects")
def list_objects(
    type_filter: Optional[str] = typer.Option(
        None,
        "--type",
        "-t",
        help="Filter by type: standard, custom, all",
    ),
    format: str = typer.Option("table", "--format", help="Output format: table, json, yaml"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """List all available objects.

    Examples:
        vdojo schema objects
        vdojo schema objects --type custom
        vdojo schema objects --format json
    """
    try:
        client = SyncVirtualDojoClient(profile)
        result = client.get("/api/v1/schema/objects")

        # API returns a list of objects directly
        objects = result if isinstance(result, list) else result.get("objects", result.get("data", []))

        # Apply type filter
        if type_filter == "standard":
            objects = [o for o in objects if not o.get("api_name", "").endswith("_co")]
        elif type_filter == "custom":
            objects = [o for o in objects if o.get("api_name", "").endswith("_co")]

        print_objects(objects, format=format)

        if format == "table":
            console.print(f"\n[dim]{len(objects)} objects[/dim]")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("describe")
def describe_object(
    object_name: str = typer.Argument(..., help="Object API name to describe"),
    format: str = typer.Option("table", "--format", help="Output format: table, json, yaml"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Describe an object and its fields.

    Examples:
        vdojo schema describe accounts
        vdojo schema describe opportunities --format json
    """
    try:
        client = SyncVirtualDojoClient(profile)

        # Get schema with fields
        schema_result = client.get(f"/api/v1/schema/objects/{object_name}/schema")

        if format == "json":
            print_json(schema_result)
            return

        if format == "yaml":
            print_yaml(schema_result)
            return

        # Table format - show object info then fields
        console.print(f"\n[bold cyan]{object_name}[/bold cyan]")

        is_custom = object_name.endswith("_co")
        console.print(f"[dim]Type:[/dim] {'Custom' if is_custom else 'Standard'}")

        console.print()

        # Print fields - API returns dict keyed by field name
        fields_dict = schema_result.get("fields", {})
        fields = list(fields_dict.values()) if isinstance(fields_dict, dict) else fields_dict
        print_fields(fields, format="table")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("fields")
def list_fields(
    object_name: str = typer.Argument(..., help="Object API name"),
    required_only: bool = typer.Option(
        False,
        "--required",
        "-r",
        help="Show only required fields",
    ),
    field_type: Optional[str] = typer.Option(
        None,
        "--type",
        "-t",
        help="Filter by field type (string, number, boolean, etc.)",
    ),
    format: str = typer.Option("table", "--format", help="Output format"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """List fields for an object.

    Examples:
        vdojo schema fields accounts
        vdojo schema fields opportunities --required
        vdojo schema fields contacts --type lookup
    """
    try:
        client = SyncVirtualDojoClient(profile)
        schema_result = client.get(f"/api/v1/schema/objects/{object_name}/schema")

        # API returns dict keyed by field name
        fields_dict = schema_result.get("fields", {})
        fields = list(fields_dict.values()) if isinstance(fields_dict, dict) else fields_dict

        # Apply filters
        if required_only:
            fields = [f for f in fields if not f.get("is_nullable", True)]

        if field_type:
            fields = [
                f
                for f in fields
                if f.get("display_type", f.get("field_type", "")).lower() == field_type.lower()
            ]

        print_fields(fields, format=format)

        if format == "table":
            console.print(f"\n[dim]{len(fields)} fields[/dim]")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("picklists")
def list_picklists(
    object_name: str = typer.Argument(..., help="Object API name"),
    field_name: Optional[str] = typer.Option(
        None,
        "--field",
        "-f",
        help="Specific picklist field name",
    ),
    format: str = typer.Option("table", "--format", help="Output format"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """List picklist values for an object's fields.

    Examples:
        vdojo schema picklists accounts
        vdojo schema picklists opportunities --field stage
    """
    try:
        client = SyncVirtualDojoClient(profile)

        # Get schema to find picklist fields
        schema_result = client.get(f"/api/v1/schema/objects/{object_name}/schema")

        # API returns dict keyed by field name
        fields_dict = schema_result.get("fields", {})
        fields = list(fields_dict.values()) if isinstance(fields_dict, dict) else fields_dict

        # Filter to picklist fields
        picklist_fields = [
            f for f in fields
            if f.get("display_type", f.get("field_type", "")) in ("picklist", "multipicklist")
        ]

        if field_name:
            picklist_fields = [
                f for f in picklist_fields
                if f.get("field_name", f.get("api_name")) == field_name
            ]

        if not picklist_fields:
            console.print("[dim]No picklist fields found[/dim]")
            return

        if format == "json":
            print_json(picklist_fields)
            return

        if format == "yaml":
            print_yaml(picklist_fields)
            return

        # Table format
        for field in picklist_fields:
            field_name = field.get('field_name', field.get('api_name', '-'))
            console.print(f"\n[bold]{field_name}[/bold]")

            # API returns choices array instead of picklist_values
            values = field.get("choices", field.get("picklist_values", []))
            if values:
                from rich.table import Table

                table = Table(show_header=True, header_style="bold")
                table.add_column("Value")
                table.add_column("Label")
                table.add_column("Active")

                for v in values:
                    if isinstance(v, dict):
                        active = "[green]Yes[/green]" if v.get("is_active", True) else "[red]No[/red]"
                        table.add_row(
                            v.get("value", "-"),
                            v.get("label", v.get("value", "-")),
                            active,
                        )
                    else:
                        table.add_row(str(v), str(v), "[green]Yes[/green]")

                console.print(table)
            else:
                console.print("[dim]  No values defined[/dim]")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)
