"""File management commands for VirtualDojo CLI."""

import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TransferSpeedColumn,
)
from rich.table import Table

from ..client import SyncVirtualDojoClient
from ..utils.output import (
    console,
    format_size,
    print_error,
    print_info,
    print_json,
    print_success,
    print_warning,
    print_yaml,
)

app = typer.Typer(help="File management operations")


def _get_client(profile: Optional[str] = None) -> SyncVirtualDojoClient:
    """Get a configured API client."""
    return SyncVirtualDojoClient(profile)


def _get_file_icon(item: dict) -> str:
    """Get an icon for a file/folder based on its type."""
    if item.get("is_folder"):
        return "📁"

    mime_type = item.get("mime_type", "")
    if mime_type.startswith("image/"):
        return "🖼️"
    elif mime_type.startswith("video/"):
        return "🎬"
    elif mime_type.startswith("audio/"):
        return "🎵"
    elif mime_type.startswith("text/"):
        return "📝"
    elif "pdf" in mime_type:
        return "📕"
    elif "spreadsheet" in mime_type or "excel" in mime_type:
        return "📊"
    elif "document" in mime_type or "word" in mime_type:
        return "📄"
    elif "zip" in mime_type or "archive" in mime_type or "compressed" in mime_type:
        return "📦"
    else:
        return "📄"


@app.command("list")
def list_files(
    folder: Optional[str] = typer.Option(
        None, "--folder", "-f", help="Folder ID or path to list"
    ),
    file_type: Optional[str] = typer.Option(
        None,
        "--type",
        "-t",
        help="Filter by type (document, image, video, audio, archive)",
    ),
    format: str = typer.Option(
        "table", "--format", help="Output format: table, json, yaml"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """List files and folders.

    Examples:
        vdojo files list                          # List root files
        vdojo files list -f folder-123            # List folder contents
        vdojo files list --type image             # List only images
        vdojo files list --format json            # Output as JSON
    """
    client = _get_client(profile)

    params: dict = {}
    if folder:
        params["folder_id"] = folder
    if file_type:
        params["file_type"] = file_type

    try:
        result = client.get("/api/v1/files/", params=params)
    except Exception as e:
        print_error(f"Failed to list files: {e}")
        raise typer.Exit(1)

    items = result.get("items", result.get("data", []))

    if format == "json":
        print_json(items)
        return
    if format == "yaml":
        print_yaml(items)
        return

    if not items:
        print_info("No files found")
        return

    table = Table(show_header=True, header_style="bold cyan", title="Files")
    table.add_column("", width=2)  # Icon
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Size", justify="right")
    table.add_column("Embed", justify="center")  # Embeddings indicator
    table.add_column("Modified")
    table.add_column("ID", style="dim")

    for item in items:
        icon = _get_file_icon(item)
        # Handle both 'name' and 'title' field names
        name = item.get("name", item.get("title", item.get("filename", "-")))
        mime_type = item.get("mime_type", item.get("file_type", "folder" if item.get("is_folder") else "-"))
        # Handle both 'size' and 'content_size' field names
        file_size = item.get("size", item.get("content_size", 0))
        size = format_size(file_size) if not item.get("is_folder") else "-"
        # Show embeddings status
        has_embeddings = item.get("has_embeddings", False)
        embed = "[green]✓[/green]" if has_embeddings else "[dim]-[/dim]"
        modified = str(item.get("updated_at", item.get("created_at", "-")))[:10]
        file_id = item.get("id", "-")
        # Truncate ID for display
        if len(file_id) > 12:
            file_id = file_id[:8] + "..."

        table.add_row(icon, name, mime_type, size, embed, modified, file_id)

    console.print(table)
    console.print(f"\n[dim]{len(items)} items[/dim]")


@app.command("info")
def file_info(
    file_id: str = typer.Argument(..., help="File ID to get info for"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table, json, yaml"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Get detailed information about a file.

    Examples:
        vdojo files info file-123
        vdojo files info file-123 --format json
    """
    client = _get_client(profile)

    try:
        result = client.get(f"/api/v1/files/{file_id}")
    except Exception as e:
        print_error(f"Failed to get file info: {e}")
        raise typer.Exit(1)

    if format == "json":
        print_json(result)
        return
    if format == "yaml":
        print_yaml(result)
        return

    table = Table(show_header=True, header_style="bold cyan", title="File Details")
    table.add_column("Property", style="bold")
    table.add_column("Value")

    # Handle both API field name variations
    fields = [
        ("ID", ["id"]),
        ("Name", ["name", "title", "filename"]),
        ("Type", ["mime_type", "file_type"]),
        ("Extension", ["file_extension"]),
        ("Size", ["size", "content_size"]),
        ("Folder ID", ["folder_id", "parent_folder_id"]),
        ("Created At", ["created_at"]),
        ("Updated At", ["updated_at"]),
        ("Owner ID", ["owner_id"]),
        ("Is Public", ["is_public"]),
        ("Has Embeddings", ["has_embeddings"]),
    ]

    for label, keys in fields:
        value = None
        for key in keys:
            if key in result and result[key] is not None:
                value = result[key]
                break

        if value is None:
            value_str = "[dim]-[/dim]"
        elif "size" in keys[0].lower():
            value_str = format_size(value)
        elif isinstance(value, bool):
            value_str = "[green]Yes[/green]" if value else "[red]No[/red]"
        else:
            value_str = str(value)
        table.add_row(label, value_str)

    console.print(table)


@app.command("upload")
def upload_file(
    path: Path = typer.Argument(..., help="Local file or directory to upload"),
    folder: Optional[str] = typer.Option(
        None, "--folder", "-f", help="Target folder ID or path"
    ),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Upload directory recursively"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Upload a file or directory to VirtualDojo.

    Examples:
        vdojo files upload ./report.pdf                    # Upload to root
        vdojo files upload ./report.pdf -f folder-123      # Upload to folder
        vdojo files upload ./images/*.png -f /Images       # Upload multiple
        vdojo files upload ./data/ --recursive             # Upload directory
    """
    if not path.exists():
        print_error(f"File not found: {path}")
        raise typer.Exit(1)

    client = _get_client(profile)

    if path.is_dir():
        if not recursive:
            print_error("Use --recursive to upload directories")
            raise typer.Exit(1)

        files_to_upload = [f for f in path.rglob("*") if f.is_file()]

        if not files_to_upload:
            print_warning("No files found in directory")
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"Uploading {len(files_to_upload)} files...", total=len(files_to_upload)
            )

            uploaded = 0
            failed = 0
            for file in files_to_upload:
                try:
                    client.upload(
                        "/api/v1/files/upload",
                        str(file),
                        folder_id=folder,
                    )
                    uploaded += 1
                except Exception as e:
                    console.print(f"[red]Failed to upload {file.name}: {e}[/red]")
                    failed += 1
                progress.advance(task)

        print_success(f"Uploaded {uploaded} files")
        if failed:
            print_warning(f"Failed to upload {failed} files")
    else:
        # Single file upload
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(f"Uploading {path.name}...", total=None)

            try:
                result = client.upload(
                    "/api/v1/files/upload",
                    str(path),
                    folder_id=folder,
                )
            except Exception as e:
                print_error(f"Failed to upload: {e}")
                raise typer.Exit(1)

        file_id = result.get("id", "unknown")
        print_success(f"Uploaded {path.name} (ID: {file_id})")


@app.command("download")
def download_file(
    file_id: str = typer.Argument(..., help="File ID to download"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output path (file or directory)"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Download a file from VirtualDojo.

    Examples:
        vdojo files download file-123                      # Download to current dir
        vdojo files download file-123 -o ./downloads/      # Download to directory
        vdojo files download file-123 -o ./report.pdf      # Download with name
    """
    client = _get_client(profile)

    # Get file info first to get the filename
    try:
        info = client.get(f"/api/v1/files/{file_id}")
    except Exception as e:
        print_error(f"Failed to get file info: {e}")
        raise typer.Exit(1)

    # Handle both 'name' and 'title' field names
    filename = info.get("name", info.get("title", info.get("filename", f"file-{file_id}")))
    file_size = info.get("size", info.get("content_size", 0))

    # Determine output path
    if output is None:
        output_path = Path(filename)
    elif output.is_dir() or str(output).endswith("/"):
        output.mkdir(parents=True, exist_ok=True)
        output_path = output / filename
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output_path = output

    # Download via /stream endpoint (secure, authenticated streaming)
    downloaded = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"Downloading {filename}...", total=file_size or None)

        def progress_callback(bytes_downloaded: int, total_bytes: int) -> None:
            nonlocal downloaded
            downloaded = bytes_downloaded
            if total_bytes > 0:
                progress.update(task, total=total_bytes, completed=bytes_downloaded)
            else:
                progress.update(task, completed=bytes_downloaded)

        try:
            downloaded = client.download(
                f"/api/v1/files/{file_id}/stream",
                str(output_path),
                progress_callback=progress_callback,
            )
        except Exception as e:
            print_error(f"Failed to download: {e}")
            raise typer.Exit(1)

    print_success(f"Downloaded to {output_path} ({format_size(downloaded)})")


@app.command("delete")
def delete_file(
    file_id: str = typer.Argument(..., help="File or folder ID to delete"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Skip confirmation prompt"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Delete a file or folder.

    Examples:
        vdojo files delete file-123
        vdojo files delete folder-456 --force
    """
    client = _get_client(profile)

    # Get file info for confirmation
    try:
        info = client.get(f"/api/v1/files/{file_id}")
    except Exception as e:
        print_error(f"Failed to get file info: {e}")
        raise typer.Exit(1)

    name = info.get("name", info.get("filename", file_id))
    is_folder = info.get("is_folder", False)
    item_type = "folder" if is_folder else "file"

    if not force:
        confirm = typer.confirm(f"Delete {item_type} '{name}'?")
        if not confirm:
            print_info("Cancelled")
            raise typer.Abort()

    try:
        client.delete(f"/api/v1/files/{file_id}")
    except Exception as e:
        print_error(f"Failed to delete: {e}")
        raise typer.Exit(1)

    print_success(f"Deleted {item_type} '{name}'")


@app.command("mkdir")
def make_directory(
    name: str = typer.Argument(..., help="Folder name to create"),
    parent: Optional[str] = typer.Option(
        None, "--parent", "-p", help="Parent folder ID"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", help="Profile to use"
    ),
) -> None:
    """Create a new folder.

    Examples:
        vdojo files mkdir "New Folder"                     # Create in root
        vdojo files mkdir "Reports" -p folder-123          # Create in parent
    """
    client = _get_client(profile)

    data: dict = {"name": name}
    if parent:
        data["parent_id"] = parent

    try:
        result = client.post("/api/v1/files/folders", data)
    except Exception as e:
        print_error(f"Failed to create folder: {e}")
        raise typer.Exit(1)

    folder_id = result.get("id", "unknown")
    print_success(f"Created folder '{name}' (ID: {folder_id})")


@app.command("move")
def move_file(
    file_id: str = typer.Argument(..., help="File or folder ID to move"),
    to: str = typer.Option(..., "--to", "-t", help="Target folder ID"),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Move a file or folder to a different location.

    Examples:
        vdojo files move file-123 --to folder-456
    """
    client = _get_client(profile)

    try:
        client.put(f"/api/v1/files/{file_id}/move", {"folder_id": to})
    except Exception as e:
        print_error(f"Failed to move: {e}")
        raise typer.Exit(1)

    print_success(f"Moved to folder {to}")


@app.command("rename")
def rename_file(
    file_id: str = typer.Argument(..., help="File or folder ID to rename"),
    name: str = typer.Option(..., "--name", "-n", help="New name"),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Rename a file or folder.

    Examples:
        vdojo files rename file-123 --name "new-name.pdf"
        vdojo files rename folder-456 --name "New Folder Name"
    """
    client = _get_client(profile)

    try:
        client.put(f"/api/v1/files/{file_id}", {"name": name})
    except Exception as e:
        print_error(f"Failed to rename: {e}")
        raise typer.Exit(1)

    print_success(f"Renamed to '{name}'")


@app.command("copy")
def copy_file(
    file_id: str = typer.Argument(..., help="File ID to copy"),
    to: Optional[str] = typer.Option(None, "--to", "-t", help="Target folder ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New filename"),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Copy a file.

    Examples:
        vdojo files copy file-123 --to folder-456
        vdojo files copy file-123 --name "copy-of-report.pdf"
    """
    client = _get_client(profile)

    data: dict = {}
    if to:
        data["folder_id"] = to
    if name:
        data["name"] = name

    if not data:
        print_error("Specify --to or --name")
        raise typer.Exit(1)

    try:
        result = client.post(f"/api/v1/files/{file_id}/copy", data)
    except Exception as e:
        print_error(f"Failed to copy: {e}")
        raise typer.Exit(1)

    new_id = result.get("id", "unknown")
    print_success(f"Created copy (ID: {new_id})")


@app.command("share")
def share_file(
    file_id: str = typer.Argument(..., help="File ID to share"),
    user: Optional[str] = typer.Option(
        None, "--user", "-u", help="User ID to share with"
    ),
    public: bool = typer.Option(False, "--public", help="Generate public link"),
    permission: str = typer.Option(
        "view", "--permission", "-r", help="Permission level: view, edit, admin"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Share a file with users or generate a public link.

    Examples:
        vdojo files share file-123 --public
        vdojo files share file-123 --user user-456
        vdojo files share file-123 --user user-456 --permission edit
    """
    client = _get_client(profile)

    if public:
        try:
            result = client.post(f"/api/v1/files/{file_id}/share", {"is_public": True})
        except Exception as e:
            print_error(f"Failed to share: {e}")
            raise typer.Exit(1)

        public_url = result.get("public_url", result.get("url", "Generated"))
        console.print(f"[green]Public link:[/green] {public_url}")
    elif user:
        try:
            client.post(
                f"/api/v1/files/{file_id}/share",
                {"user_id": user, "permission": permission},
            )
        except Exception as e:
            print_error(f"Failed to share: {e}")
            raise typer.Exit(1)

        print_success(f"Shared with user {user} ({permission} access)")
    else:
        print_error("Specify --user or --public")
        raise typer.Exit(1)


@app.command("unshare")
def unshare_file(
    file_id: str = typer.Argument(..., help="File ID"),
    user: str = typer.Option(..., "--user", "-u", help="User ID to remove share"),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Remove a file share from a user.

    Examples:
        vdojo files unshare file-123 --user user-456
    """
    client = _get_client(profile)

    try:
        client.delete(f"/api/v1/files/{file_id}/share/{user}")
    except Exception as e:
        print_error(f"Failed to unshare: {e}")
        raise typer.Exit(1)

    print_success(f"Removed share from user {user}")


@app.command("shares")
def list_shares(
    file_id: str = typer.Argument(..., help="File ID to list shares for"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table, json, yaml"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """List all shares for a file.

    Examples:
        vdojo files shares file-123
        vdojo files shares file-123 --format json
    """
    client = _get_client(profile)

    try:
        result = client.get(f"/api/v1/files/{file_id}/shares")
    except Exception as e:
        print_error(f"Failed to get shares: {e}")
        raise typer.Exit(1)

    shares = result.get("shares", result.get("data", []))

    if format == "json":
        print_json(shares)
        return
    if format == "yaml":
        print_yaml(shares)
        return

    if not shares:
        print_info("No shares found")
        return

    table = Table(show_header=True, header_style="bold cyan", title="File Shares")
    table.add_column("User ID")
    table.add_column("Permission")
    table.add_column("Shared At")

    for share in shares:
        table.add_row(
            share.get("user_id", "-"),
            share.get("permission", "-"),
            str(share.get("created_at", "-"))[:10],
        )

    console.print(table)


@app.command("link")
def link_file(
    file_id: str = typer.Argument(..., help="File ID to link"),
    object: str = typer.Option(..., "--object", "-o", help="Object API name"),
    record: str = typer.Option(..., "--record", "-r", help="Record ID"),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Link a file to a CRM record.

    Examples:
        vdojo files link file-123 --object accounts --record acc-456
    """
    client = _get_client(profile)

    try:
        client.post(
            f"/api/v1/files/{file_id}/links",
            {"object_api_name": object, "record_id": record},
        )
    except Exception as e:
        print_error(f"Failed to link: {e}")
        raise typer.Exit(1)

    print_success(f"Linked to {object} record {record}")


@app.command("unlink")
def unlink_file(
    file_id: str = typer.Argument(..., help="File ID"),
    link_id: str = typer.Option(..., "--link", "-l", help="Link ID to remove"),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Remove a file-record link.

    Examples:
        vdojo files unlink file-123 --link link-456
    """
    client = _get_client(profile)

    try:
        client.delete(f"/api/v1/files/{file_id}/links/{link_id}")
    except Exception as e:
        print_error(f"Failed to unlink: {e}")
        raise typer.Exit(1)

    print_success("Removed link")


@app.command("links")
def list_links(
    file_id: str = typer.Argument(..., help="File ID to list links for"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table, json, yaml"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """List all record links for a file.

    Examples:
        vdojo files links file-123
    """
    client = _get_client(profile)

    try:
        result = client.get(f"/api/v1/files/{file_id}/links")
    except Exception as e:
        print_error(f"Failed to get links: {e}")
        raise typer.Exit(1)

    links = result.get("links", result.get("data", []))

    if format == "json":
        print_json(links)
        return
    if format == "yaml":
        print_yaml(links)
        return

    if not links:
        print_info("No links found")
        return

    table = Table(show_header=True, header_style="bold cyan", title="File Links")
    table.add_column("Link ID", style="dim")
    table.add_column("Object")
    table.add_column("Record ID")
    table.add_column("Created At")

    for link in links:
        table.add_row(
            link.get("id", "-"),
            link.get("object_api_name", "-"),
            link.get("record_id", "-"),
            str(link.get("created_at", "-"))[:10],
        )

    console.print(table)


@app.command("search")
def search_files(
    query: str = typer.Argument(..., help="Search query"),
    file_type: Optional[str] = typer.Option(
        None, "--type", "-t", help="Filter by type"
    ),
    created_after: Optional[str] = typer.Option(
        None, "--created-after", help="Filter by creation date (YYYY-MM-DD)"
    ),
    format: str = typer.Option(
        "table", "--format", help="Output format: table, json, yaml"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Search for files by name.

    Examples:
        vdojo files search "quarterly report"
        vdojo files search "report" --type document
        vdojo files search "report" --created-after 2024-01-01
    """
    client = _get_client(profile)

    params: dict = {"q": query}
    if file_type:
        params["file_type"] = file_type
    if created_after:
        params["created_after"] = created_after

    try:
        result = client.get("/api/v1/files/search", params=params)
    except Exception as e:
        print_error(f"Search failed: {e}")
        raise typer.Exit(1)

    items = result.get("items", result.get("data", []))

    if format == "json":
        print_json(items)
        return
    if format == "yaml":
        print_yaml(items)
        return

    if not items:
        print_info(f"No files found matching '{query}'")
        return

    table = Table(show_header=True, header_style="bold cyan", title=f"Search: {query}")
    table.add_column("", width=2)
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Size", justify="right")
    table.add_column("ID", style="dim")

    for item in items:
        icon = _get_file_icon(item)
        name = item.get("name", item.get("title", item.get("filename", "-")))
        mime_type = item.get("mime_type", item.get("file_type", "-"))
        file_size = item.get("size", item.get("content_size", 0))
        size = format_size(file_size)
        file_id = item.get("id", "-")
        if len(file_id) > 12:
            file_id = file_id[:8] + "..."

        table.add_row(icon, name, mime_type, size, file_id)

    console.print(table)
    console.print(f"\n[dim]{len(items)} results[/dim]")


@app.command("storage")
def storage_info(
    format: str = typer.Option(
        "table", "--format", help="Output format: table, json, yaml"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="Profile to use"
    ),
) -> None:
    """Show storage usage information.

    Examples:
        vdojo files storage
        vdojo files storage --format json
    """
    client = _get_client(profile)

    try:
        result = client.get("/api/v1/files/storage")
    except Exception as e:
        print_error(f"Failed to get storage info: {e}")
        raise typer.Exit(1)

    if format == "json":
        print_json(result)
        return
    if format == "yaml":
        print_yaml(result)
        return

    used = result.get("used_bytes", result.get("used", 0))
    total = result.get("total_bytes", result.get("total", 0))
    file_count = result.get("file_count", result.get("files", 0))
    folder_count = result.get("folder_count", result.get("folders", 0))

    percent = (used / total * 100) if total > 0 else 0

    console.print("\n[bold]Storage Usage[/bold]")
    console.print(f"  Used: {format_size(used)} / {format_size(total)} ({percent:.1f}%)")
    console.print(f"  Files: {file_count}")
    console.print(f"  Folders: {folder_count}")

    # Visual progress bar
    if total > 0:
        bar_width = 40
        filled = int(bar_width * used / total)
        bar = "█" * filled + "░" * (bar_width - filled)
        color = "green" if percent < 70 else "yellow" if percent < 90 else "red"
        console.print(f"\n  [{color}]{bar}[/{color}]")
