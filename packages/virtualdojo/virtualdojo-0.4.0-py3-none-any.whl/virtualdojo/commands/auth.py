"""Authentication commands for VirtualDojo CLI."""

import os
import time
from typing import Optional

import httpx
import typer
from rich.prompt import Prompt

from .. import DEFAULT_SERVER_URL, DEV_URLS
from ..config import Credentials, Profile, config_manager
from ..client import SyncVirtualDojoClient
from ..exceptions import APIError, AuthenticationError, NetworkError
from ..utils.output import console, print_error, print_success, print_warning

app = typer.Typer(help="Authentication commands")

# Environment variable names for credentials
ENV_API_KEY = "VIRTUALDOJO_API_KEY"
ENV_PASSWORD = "VIRTUALDOJO_PASSWORD"
ENV_EMAIL = "VIRTUALDOJO_EMAIL"
ENV_TENANT = "VIRTUALDOJO_TENANT"
ENV_SERVER = "VIRTUALDOJO_SERVER"


def resolve_server_url(server: Optional[str], warn_http: bool = True) -> str:
    """Resolve server URL from shorthand or full URL.

    Supports shortcuts like 'local', 'staging', 'production' or full URLs.

    Args:
        server: Server URL or shorthand
        warn_http: Whether to warn about insecure HTTP connections
    """
    if not server:
        return DEFAULT_SERVER_URL

    # Check for shorthand aliases
    server_lower = server.lower()
    if server_lower in DEV_URLS:
        resolved = DEV_URLS[server_lower]
        if warn_http and resolved.startswith("http://"):
            _warn_insecure_connection(resolved)
        return resolved

    # If it doesn't start with http, assume https
    if not server.startswith("http://") and not server.startswith("https://"):
        # Check if it looks like localhost
        if server.startswith("localhost") or server.startswith("127.0.0.1"):
            resolved = f"http://{server}"
            if warn_http:
                _warn_insecure_connection(resolved)
            return resolved
        return f"https://{server}"

    # Warn about explicit HTTP URLs (except localhost)
    if warn_http and server.startswith("http://"):
        if not ("localhost" in server or "127.0.0.1" in server):
            _warn_insecure_connection(server)

    return server


def _warn_insecure_connection(url: str) -> None:
    """Warn user about insecure HTTP connection."""
    print_warning(
        f"Using insecure HTTP connection to {url}. "
        "Credentials will be transmitted in plaintext."
    )
    console.print(
        "[dim]  For production use, always use HTTPS. "
        "Set VIRTUALDOJO_SERVER env var or use --server with https://[/dim]"
    )


@app.command("login")
def login(
    server: Optional[str] = typer.Option(
        None,
        "--server",
        "-s",
        help=f"Server URL or shortcut. Env: {ENV_SERVER}. Default: {DEFAULT_SERVER_URL}",
    ),
    tenant: Optional[str] = typer.Option(
        None,
        "--tenant",
        "-t",
        help=f"Tenant ID or subdomain. Env: {ENV_TENANT}. Auto-detected if not provided.",
    ),
    email: Optional[str] = typer.Option(
        None,
        "--email",
        "-e",
        help=f"Email address. Env: {ENV_EMAIL}. Prompts if not provided.",
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        "-k",
        help=f"API key for non-interactive login. Env: {ENV_API_KEY} (preferred).",
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
    """Login to VirtualDojo and save credentials.

    You can login with just email/password - tenant is auto-detected!
    If you belong to multiple tenants, you'll be prompted to choose.

    SECURITY: For CI/CD and scripts, use environment variables instead of
    command-line arguments to avoid exposing credentials in shell history:

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

    Environment variables (for CI/CD):
        VIRTUALDOJO_API_KEY   - API key (preferred over --api-key)
        VIRTUALDOJO_PASSWORD  - Password (avoids interactive prompt)
        VIRTUALDOJO_EMAIL     - Email address
        VIRTUALDOJO_TENANT    - Tenant ID
        VIRTUALDOJO_SERVER    - Server URL
    """
    # Read from environment variables (take precedence over CLI args for security)
    server = server or os.environ.get(ENV_SERVER)
    tenant = tenant or os.environ.get(ENV_TENANT)
    email = email or os.environ.get(ENV_EMAIL)
    api_key = api_key or os.environ.get(ENV_API_KEY)
    password = os.environ.get(ENV_PASSWORD)  # Only from env, never CLI arg

    # Handle --local shortcut
    if local:
        server = "local"

    # Resolve server URL (handles shortcuts like 'local', 'staging')
    resolved_server = resolve_server_url(server)

    # Show which server we're connecting to
    if server and server.lower() in DEV_URLS:
        console.print(f"[dim]Using {server} server: {resolved_server}[/dim]")
    elif not server:
        console.print(f"[dim]Using default server: {resolved_server}[/dim]")

    # Ensure server doesn't have trailing slash
    resolved_server = resolved_server.rstrip("/")

    if api_key:
        # API key login - requires tenant
        if not tenant:
            tenant = Prompt.ask("Tenant ID or subdomain")
        _login_with_api_key(resolved_server, tenant, api_key, profile_name)
    else:
        # Email/password login - tenant is optional (auto-detect)
        if not email:
            email = Prompt.ask("Email")
        if not password:
            password = Prompt.ask("Password", password=True)

        if tenant:
            # Tenant specified - use direct login
            _login_with_password(resolved_server, tenant, email, password, profile_name)
        else:
            # No tenant - use multi-tenant discovery
            _login_multi_tenant(resolved_server, email, password, profile_name)


def _login_with_password(
    server: str,
    tenant: str,
    email: str,
    password: str,
    profile_name: str,
) -> None:
    """Login with email and password."""
    console.print(f"[dim]Logging in to {server}...[/dim]")

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{server}/api/v1/auth/login",
                data={
                    "username": email,
                    "password": password,
                },
                headers={
                    "X-Tenant-ID": tenant,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )

            if response.status_code == 401:
                print_error("Invalid email or password")
                raise typer.Exit(1)

            if response.status_code != 200:
                detail = response.json().get("detail", "Login failed")
                print_error(f"Login failed: {detail}")
                raise typer.Exit(1)

            data = response.json()

        # Save profile
        profile = Profile(
            name=profile_name,
            server=server,
            tenant=tenant,
        )
        config_manager.add_profile(profile, set_default=True)

        # Save credentials
        expires_in = data.get("expires_in", 1800)
        credentials = Credentials(
            profile_name=profile_name,
            token_type="jwt",
            token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            expires_at=time.time() + expires_in,
            user_email=email,
        )
        config_manager.save_credentials(credentials)

        print_success(f"Logged in as {email}")
        console.print(f"  [dim]Profile:[/dim] {profile_name}")
        console.print(f"  [dim]Server:[/dim] {server}")
        console.print(f"  [dim]Tenant:[/dim] {tenant}")

    except httpx.ConnectError:
        print_error(f"Could not connect to {server}")
        raise typer.Exit(1)
    except httpx.TimeoutException:
        print_error("Connection timed out")
        raise typer.Exit(1)


def _login_multi_tenant(
    server: str,
    email: str,
    password: str,
    profile_name: str,
) -> None:
    """Login with email/password, auto-detecting tenant.

    Uses the /login-multi-tenant endpoint to find which tenants
    the user has access to. If only one, logs in directly.
    If multiple, prompts user to choose.
    """
    console.print(f"[dim]Logging in to {server}...[/dim]")

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{server}/api/v1/auth/login-multi-tenant",
                data={
                    "username": email,
                    "password": password,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )

            if response.status_code == 401:
                print_error("Invalid email or password")
                raise typer.Exit(1)

            if response.status_code != 200:
                detail = response.json().get("detail", "Login failed")
                print_error(f"Login failed: {detail}")
                raise typer.Exit(1)

            data = response.json()

        # Check if user has multiple tenants
        if data.get("multiple_tenants"):
            # User has access to multiple tenants - prompt to choose
            available_tenants = data.get("available_tenants", [])
            user_id = data.get("user_id")

            console.print("\n[bold]You have access to multiple tenants:[/bold]")
            for i, tenant_info in enumerate(available_tenants, 1):
                console.print(
                    f"  [{i}] {tenant_info['tenant_name']} "
                    f"[dim]({tenant_info['subdomain']})[/dim] "
                    f"- {tenant_info['user_role']}"
                )

            # Prompt for selection
            while True:
                choice = Prompt.ask(
                    "\nSelect tenant",
                    default="1",
                )
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(available_tenants):
                        selected_tenant = available_tenants[idx]
                        break
                    print_error(f"Please enter a number between 1 and {len(available_tenants)}")
                except ValueError:
                    print_error("Please enter a valid number")

            # Call /select-tenant to get the token
            _select_tenant(
                server=server,
                tenant_id=selected_tenant["tenant_id"],
                tenant_name=selected_tenant["tenant_name"],
                user_id=selected_tenant.get("user_id", user_id),
                email=email,
                profile_name=profile_name,
            )
        else:
            # Single tenant - token already provided
            tenant_info = data.get("tenant", {})
            tenant_id = tenant_info.get("tenant_id", "unknown")
            tenant_name = tenant_info.get("tenant_name", tenant_info.get("subdomain", "unknown"))

            # Save profile
            profile = Profile(
                name=profile_name,
                server=server,
                tenant=tenant_id,
            )
            config_manager.add_profile(profile, set_default=True)

            # Save credentials
            expires_in = data.get("expires_in", 1800)
            credentials = Credentials(
                profile_name=profile_name,
                token_type="jwt",
                token=data["access_token"],
                refresh_token=data.get("refresh_token"),
                expires_at=time.time() + expires_in,
                user_email=email,
            )
            config_manager.save_credentials(credentials)

            print_success(f"Logged in as {email}")
            console.print(f"  [dim]Profile:[/dim] {profile_name}")
            console.print(f"  [dim]Server:[/dim] {server}")
            console.print(f"  [dim]Tenant:[/dim] {tenant_name} ({tenant_id})")

    except httpx.ConnectError:
        print_error(f"Could not connect to {server}")
        raise typer.Exit(1)
    except httpx.TimeoutException:
        print_error("Connection timed out")
        raise typer.Exit(1)


def _select_tenant(
    server: str,
    tenant_id: str,
    tenant_name: str,
    user_id: str,
    email: str,
    profile_name: str,
) -> None:
    """Select a specific tenant after multi-tenant login."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{server}/api/v1/auth/select-tenant",
                json={
                    "tenant_id": tenant_id,
                    "user_id": user_id,
                },
                headers={
                    "Content-Type": "application/json",
                },
            )

            if response.status_code != 200:
                detail = response.json().get("detail", "Tenant selection failed")
                print_error(f"Failed to select tenant: {detail}")
                raise typer.Exit(1)

            data = response.json()

        # Save profile
        profile = Profile(
            name=profile_name,
            server=server,
            tenant=tenant_id,
        )
        config_manager.add_profile(profile, set_default=True)

        # Save credentials
        expires_in = data.get("expires_in", 1800)
        credentials = Credentials(
            profile_name=profile_name,
            token_type="jwt",
            token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            expires_at=time.time() + expires_in,
            user_email=email,
        )
        config_manager.save_credentials(credentials)

        print_success(f"Logged in as {email}")
        console.print(f"  [dim]Profile:[/dim] {profile_name}")
        console.print(f"  [dim]Server:[/dim] {server}")
        console.print(f"  [dim]Tenant:[/dim] {tenant_name} ({tenant_id})")

    except httpx.ConnectError:
        print_error(f"Could not connect to {server}")
        raise typer.Exit(1)
    except httpx.TimeoutException:
        print_error("Connection timed out")
        raise typer.Exit(1)


def _login_with_api_key(
    server: str,
    tenant: str,
    api_key: str,
    profile_name: str,
) -> None:
    """Login with an API key."""
    console.print(f"[dim]Validating API key with {server}...[/dim]")

    try:
        with httpx.Client(timeout=30.0) as client:
            # Validate the API key by calling /users/me
            response = client.get(
                f"{server}/api/v1/users/me",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "X-Tenant-ID": tenant,
                },
            )

            if response.status_code == 401:
                print_error("Invalid API key")
                raise typer.Exit(1)

            if response.status_code != 200:
                detail = response.json().get("detail", "Validation failed")
                print_error(f"API key validation failed: {detail}")
                raise typer.Exit(1)

            user_data = response.json()

        # Save profile
        profile = Profile(
            name=profile_name,
            server=server,
            tenant=tenant,
        )
        config_manager.add_profile(profile, set_default=True)

        # Save credentials (API keys don't expire the same way)
        credentials = Credentials(
            profile_name=profile_name,
            token_type="api_key",
            token=api_key,
            user_email=user_data.get("email"),
            user_id=user_data.get("id"),
        )
        config_manager.save_credentials(credentials)

        print_success(f"Logged in with API key as {user_data.get('email', 'unknown')}")
        console.print(f"  [dim]Profile:[/dim] {profile_name}")
        console.print(f"  [dim]Server:[/dim] {server}")
        console.print(f"  [dim]Tenant:[/dim] {tenant}")

    except httpx.ConnectError:
        print_error(f"Could not connect to {server}")
        raise typer.Exit(1)
    except httpx.TimeoutException:
        print_error("Connection timed out")
        raise typer.Exit(1)


@app.command("logout")
def logout(
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        "-p",
        help="Profile to logout from (default: current profile)",
    ),
    all_profiles: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Logout from all profiles",
    ),
) -> None:
    """Logout and clear stored credentials.

    Examples:
        vdojo auth logout
        vdojo auth logout --profile staging
        vdojo auth logout --all
    """
    if all_profiles:
        # Clear all credentials
        for p in config_manager.list_profiles():
            config_manager.remove_credentials(p.name)
        print_success("Logged out from all profiles")
    else:
        # Clear specific profile
        profile_name = profile or config_manager.config.default_profile
        if not profile_name:
            print_warning("No profile specified and no default profile set")
            raise typer.Exit(0)

        config_manager.remove_credentials(profile_name)
        print_success(f"Logged out from profile '{profile_name}'")


@app.command("whoami")
def whoami(
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        "-p",
        help="Profile to check",
    ),
) -> None:
    """Show current user information.

    Examples:
        vdojo auth whoami
        vdojo auth whoami --profile production
    """
    try:
        client = SyncVirtualDojoClient(profile)
        user_data = client.get("/api/v1/users/me")

        console.print()
        console.print(f"[bold]Logged in as:[/bold] {user_data.get('email', 'Unknown')}")
        console.print(f"[dim]User ID:[/dim] {user_data.get('id', '-')}")
        console.print(f"[dim]Name:[/dim] {user_data.get('full_name', '-')}")

        current_profile = config_manager.get_profile(profile)
        console.print(f"[dim]Profile:[/dim] {current_profile.name}")
        console.print(f"[dim]Server:[/dim] {current_profile.server}")
        console.print(f"[dim]Tenant:[/dim] {current_profile.tenant}")

        creds = config_manager.get_credentials(current_profile.name)
        if creds and creds.token_type:
            console.print(f"[dim]Auth type:[/dim] {creds.token_type}")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("api-key")
def api_key_commands() -> None:
    """Manage API keys (subcommand group)."""
    pass


# API Key subcommands
api_key_app = typer.Typer(help="API key management")


@api_key_app.command("list")
def list_api_keys(
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """List your API keys."""
    try:
        client = SyncVirtualDojoClient(profile)
        result = client.get("/api/v1/api-keys")

        keys = result if isinstance(result, list) else result.get("data", [])

        if not keys:
            console.print("[dim]No API keys found[/dim]")
            return

        from rich.table import Table

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Created")
        table.add_column("Expires")

        for key in keys:
            table.add_row(
                key.get("id", "-")[:8] + "...",
                key.get("name", "-"),
                key.get("created_at", "-")[:10] if key.get("created_at") else "-",
                key.get("expires_at", "Never")[:10] if key.get("expires_at") else "Never",
            )

        console.print(table)

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@api_key_app.command("create")
def create_api_key(
    name: str = typer.Option(..., "--name", "-n", help="Name for the API key"),
    expires_days: Optional[int] = typer.Option(
        None,
        "--expires",
        "-e",
        help="Days until expiration (default: never)",
    ),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Create a new API key."""
    try:
        client = SyncVirtualDojoClient(profile)
        data = {"name": name}
        if expires_days:
            data["expires_in_days"] = expires_days

        result = client.post("/api/v1/api-keys", data)

        print_success("API key created successfully!")
        console.print()
        console.print("[bold yellow]IMPORTANT:[/bold yellow] Save this key now - it won't be shown again!")
        console.print()
        console.print(f"[bold]Key:[/bold] {result.get('key', result.get('api_key', '-'))}")
        console.print(f"[dim]Name:[/dim] {result.get('name', '-')}")
        console.print(f"[dim]ID:[/dim] {result.get('id', '-')}")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@api_key_app.command("revoke")
def revoke_api_key(
    key_id: str = typer.Argument(..., help="API key ID to revoke"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Revoke an API key."""
    if not force:
        confirm = typer.confirm(f"Revoke API key {key_id}?")
        if not confirm:
            raise typer.Abort()

    try:
        client = SyncVirtualDojoClient(profile)
        client.delete(f"/api/v1/api-keys/{key_id}")
        print_success(f"API key {key_id} revoked")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


# Add api-key subcommands
app.add_typer(api_key_app, name="api-key")
