"""Command-line interface for AnomalyArmor.

Usage:
    armor auth login
    armor assets list
    armor freshness get <asset>
    armor schema changes --severity critical
    armor alerts list --status triggered
"""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

import typer
from rich.console import Console
from rich.table import Table

from armor.config import (
    DEFAULT_API_URL,
    Config,
    clear_config,
    get_config_path,
    load_config,
    save_config,
)
from armor.exceptions import (
    ArmorError,
    AuthenticationError,
    DataStaleError,
    NotFoundError,
    RateLimitError,
)

if TYPE_CHECKING:
    from armor.client import Client

app = typer.Typer(
    name="armor",
    help="AnomalyArmor CLI for data observability",
    add_completion=False,
)

console = Console()

# Exit codes per TECH-593 spec
EXIT_SUCCESS = 0
EXIT_STALENESS = 1
EXIT_AUTH_ERROR = 2
EXIT_NOT_FOUND = 3
EXIT_RATE_LIMIT = 4
EXIT_GENERAL_ERROR = 5


def handle_api_error(e: ArmorError) -> NoReturn:
    """Handle API errors with appropriate exit codes."""
    console.print(f"[red]Error:[/red] {e.message}")

    if isinstance(e, AuthenticationError):
        raise typer.Exit(EXIT_AUTH_ERROR)
    if isinstance(e, NotFoundError):
        raise typer.Exit(EXIT_NOT_FOUND)
    if isinstance(e, RateLimitError):
        retry_after = getattr(e, "retry_after", 60)
        console.print(f"[yellow]Retry after {retry_after} seconds[/yellow]")
        raise typer.Exit(EXIT_RATE_LIMIT)

    raise typer.Exit(EXIT_GENERAL_ERROR)


def get_client() -> Client:
    """Get an authenticated client."""
    from armor import Client

    try:
        return Client()
    except AuthenticationError as e:
        console.print(f"[red]Authentication error:[/red] {e.message}")
        console.print("Run 'armor auth login' to authenticate.")
        raise typer.Exit(EXIT_AUTH_ERROR) from e


# ============================================================================
# Auth commands
# ============================================================================

auth_app = typer.Typer(help="Authentication commands")
app.add_typer(auth_app, name="auth")


@auth_app.command("login")
def auth_login(
    api_key: str = typer.Option(
        ...,
        "--api-key",
        "-k",
        help="Your API key (starts with aa_live_)",
        prompt="Enter your API key",
        hide_input=True,
    ),
    api_url: str | None = typer.Option(
        None,
        "--api-url",
        help="API URL (defaults to production)",
    ),
) -> None:
    """Authenticate with AnomalyArmor."""
    # Validate the key format
    if not api_key.startswith("aa_live_") and not api_key.startswith("aa_test_"):
        console.print("[red]Error:[/red] Invalid API key format. Key should start with 'aa_live_'")
        raise typer.Exit(EXIT_AUTH_ERROR)

    # Test the key by making a request
    from armor import Client

    try:
        client = Client(api_key=api_key, api_url=api_url)
        # Try to get API key usage to verify auth works
        client.api_keys.usage()
        client.close()
    except AuthenticationError as e:
        console.print(f"[red]Authentication failed:[/red] {e.message}")
        raise typer.Exit(EXIT_AUTH_ERROR)
    except ArmorError as e:
        handle_api_error(e)

    # Save config
    config = Config(
        api_key=api_key,
        api_url=api_url or DEFAULT_API_URL,
        timeout=30,
        retry_attempts=3,
    )
    save_config(config)

    console.print("[green]Successfully authenticated![/green]")
    console.print(f"Config saved to: {get_config_path()}")


@auth_app.command("status")
def auth_status() -> None:
    """Check authentication status."""
    config = load_config()

    if not config.api_key:
        console.print("[yellow]Not authenticated.[/yellow]")
        console.print("Run 'armor auth login' to authenticate.")
        raise typer.Exit(EXIT_AUTH_ERROR)

    # Mask the key
    masked_key = config.api_key[:12] + "..." + config.api_key[-4:]
    console.print("[green]Authenticated[/green]")
    console.print(f"API Key: {masked_key}")
    console.print(f"API URL: {config.api_url}")


@auth_app.command("logout")
def auth_logout() -> None:
    """Remove stored credentials."""
    clear_config()
    console.print("[green]Logged out successfully.[/green]")


# ============================================================================
# Assets commands
# ============================================================================

assets_app = typer.Typer(help="Asset management commands")
app.add_typer(assets_app, name="assets")


@assets_app.command("list")
def assets_list(
    source: str | None = typer.Option(None, "--source", "-s", help="Filter by source type"),
    asset_type: str | None = typer.Option(None, "--type", "-t", help="Filter by asset type"),
    search: str | None = typer.Option(None, "--search", help="Search in names"),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results"),
) -> None:
    """List assets."""
    client = get_client()

    try:
        assets = client.assets.list(
            source=source,
            asset_type=asset_type,
            search=search,
            limit=limit,
        )
    except ArmorError as e:
        handle_api_error(e)

    if not assets:
        console.print("No assets found.")
        return

    table = Table(title="Assets")
    table.add_column("Qualified Name", style="cyan")
    table.add_column("Type")
    table.add_column("Source")
    table.add_column("Active")

    for asset in assets:
        table.add_row(
            asset.qualified_name,
            asset.asset_type,
            asset.source_type or "-",
            "Yes" if asset.is_active else "No",
        )

    console.print(table)
    console.print(f"\nShowing {len(assets)} assets")


@assets_app.command("get")
def assets_get(asset_id: str = typer.Argument(..., help="Asset ID or qualified name")) -> None:
    """Get asset details."""
    client = get_client()

    try:
        asset = client.assets.get(asset_id)
    except ArmorError as e:
        handle_api_error(e)

    console.print(f"[bold]Asset:[/bold] {asset.qualified_name}")
    console.print(f"ID: {asset.id}")
    console.print(f"Type: {asset.asset_type}")
    console.print(f"Source: {asset.source_type or '-'}")
    console.print(f"Active: {'Yes' if asset.is_active else 'No'}")
    if asset.description:
        console.print(f"Description: {asset.description}")


# ============================================================================
# Freshness commands
# ============================================================================

freshness_app = typer.Typer(help="Freshness monitoring commands")
app.add_typer(freshness_app, name="freshness")


@freshness_app.command("summary")
def freshness_summary() -> None:
    """Get freshness summary."""
    client = get_client()

    try:
        summary = client.freshness.summary()
    except ArmorError as e:
        handle_api_error(e)

    console.print("[bold]Freshness Summary[/bold]")
    console.print(f"Total Assets: {summary.total_assets}")
    console.print(f"Fresh: [green]{summary.fresh_count}[/green]")
    console.print(f"Stale: [red]{summary.stale_count}[/red]")
    console.print(f"Unknown: [yellow]{summary.unknown_count}[/yellow]")
    console.print(f"Freshness Rate: {summary.freshness_rate}%")


@freshness_app.command("get")
def freshness_get(
    asset_id: str = typer.Argument(..., help="Asset ID or qualified name"),
) -> None:
    """Check freshness for an asset."""
    client = get_client()

    try:
        status = client.freshness.get(asset_id)
    except ArmorError as e:
        handle_api_error(e)

    console.print(f"[bold]Asset:[/bold] {status.qualified_name}")
    console.print("Status: ", end="")

    if status.status == "fresh":
        console.print("[green]Fresh[/green]")
    elif status.status == "stale":
        console.print("[red]Stale[/red]")
    elif status.status == "unknown":
        console.print("[yellow]Unknown[/yellow]")
    else:
        console.print(status.status)

    if status.last_update_time:
        console.print(f"Last Update: {status.last_update_time}")
    if status.hours_since_update is not None:
        console.print(f"Hours Since Update: {status.hours_since_update:.1f}")
    if status.staleness_threshold_hours:
        console.print(f"Threshold: {status.staleness_threshold_hours}h")

    # Exit with staleness code if stale
    if status.is_stale:
        raise typer.Exit(EXIT_STALENESS)


@freshness_app.command("list")
def freshness_list(
    status_filter: str | None = typer.Option(
        None, "--status", "-s", help="Filter by status (fresh, stale, unknown)"
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results"),
) -> None:
    """List freshness status for all assets."""
    client = get_client()

    try:
        statuses = client.freshness.list(status=status_filter, limit=limit)
    except ArmorError as e:
        handle_api_error(e)

    if not statuses:
        console.print("No results found.")
        return

    table = Table(title="Freshness Status")
    table.add_column("Asset", style="cyan")
    table.add_column("Status")
    table.add_column("Hours Since Update")
    table.add_column("Threshold")

    for s in statuses:
        status_style = {
            "fresh": "[green]Fresh[/green]",
            "stale": "[red]Stale[/red]",
            "unknown": "[yellow]Unknown[/yellow]",
            "disabled": "[dim]Disabled[/dim]",
        }.get(s.status, s.status)

        table.add_row(
            s.qualified_name,
            status_style,
            f"{s.hours_since_update:.1f}" if s.hours_since_update else "-",
            f"{s.staleness_threshold_hours}h" if s.staleness_threshold_hours else "-",
        )

    console.print(table)


@freshness_app.command("check")
def freshness_check(
    asset_id: str = typer.Argument(..., help="Asset ID or qualified name"),
    max_age_hours: float | None = typer.Option(
        None, "--max-age", "-m", help="Max acceptable age in hours"
    ),
) -> None:
    """Check if an asset is fresh, fail if stale.

    Useful for CI/CD pipelines to gate on data freshness.
    Exit codes:
        0 - Data is fresh
        1 - Data is stale
        3 - Asset not found

    Example:
        armor freshness check postgresql.mydb.public.users --max-age 24
    """
    client = get_client()

    try:
        status = client.freshness.require_fresh(asset_id, max_age_hours=max_age_hours)
    except DataStaleError as e:
        console.print(f"[red]STALE:[/red] {e.message}")
        console.print(f"Hours since update: {e.hours_since_update:.1f}h")
        console.print(f"Threshold: {e.threshold_hours:.1f}h")
        raise typer.Exit(EXIT_STALENESS)
    except ArmorError as e:
        handle_api_error(e)

    console.print(f"[green]FRESH:[/green] {status.qualified_name}")
    if status.hours_since_update is not None:
        console.print(f"Hours since update: {status.hours_since_update:.1f}h")


@freshness_app.command("refresh")
def freshness_refresh(
    asset_id: str = typer.Argument(..., help="Asset ID or qualified name"),
) -> None:
    """Trigger a freshness check for an asset.

    Requires an API key with read-write or admin scope.

    Example:
        armor freshness refresh postgresql.mydb.public.users
    """
    client = get_client()

    try:
        result = client.freshness.refresh(asset_id)
    except ArmorError as e:
        handle_api_error(e)

    console.print("[green]Refresh initiated[/green]")
    console.print(f"Job ID: {result.get('job_id', 'N/A')}")
    console.print(f"Status: {result.get('status', 'queued')}")


# ============================================================================
# Schema commands
# ============================================================================

schema_app = typer.Typer(help="Schema drift monitoring commands")
app.add_typer(schema_app, name="schema")


@schema_app.command("summary")
def schema_summary() -> None:
    """Get schema changes summary."""
    client = get_client()

    try:
        summary = client.schema.summary()
    except ArmorError as e:
        handle_api_error(e)

    console.print("[bold]Schema Changes Summary[/bold]")
    console.print(f"Total Changes: {summary.total_changes}")
    console.print(f"Unacknowledged: [yellow]{summary.unacknowledged}[/yellow]")
    console.print(f"Critical: [red]{summary.critical_count}[/red]")
    console.print(f"Warning: [yellow]{summary.warning_count}[/yellow]")
    console.print(f"Info: {summary.info_count}")


@schema_app.command("changes")
def schema_changes(
    asset_id: str | None = typer.Option(None, "--asset", "-a", help="Filter by asset"),
    severity: str | None = typer.Option(None, "--severity", "-s", help="Filter by severity"),
    unacknowledged: bool = typer.Option(
        False, "--unacknowledged", "-u", help="Only unacknowledged"
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results"),
) -> None:
    """List schema changes."""
    client = get_client()

    try:
        changes = client.schema.changes(
            asset_id=asset_id,
            severity=severity,
            unacknowledged_only=unacknowledged,
            limit=limit,
        )
    except ArmorError as e:
        handle_api_error(e)

    if not changes:
        console.print("No schema changes found.")
        return

    table = Table(title="Schema Changes")
    table.add_column("Asset", style="cyan")
    table.add_column("Change")
    table.add_column("Severity")
    table.add_column("Column")
    table.add_column("Ack")

    for c in changes:
        sev_style = {
            "critical": "[red]Critical[/red]",
            "warning": "[yellow]Warning[/yellow]",
            "info": "Info",
        }.get(c.severity, c.severity)

        table.add_row(
            c.qualified_name,
            c.change_type,
            sev_style,
            c.column_name or "-",
            "Yes" if c.acknowledged else "No",
        )

    console.print(table)


# ============================================================================
# Alerts commands
# ============================================================================

alerts_app = typer.Typer(help="Alert management commands")
app.add_typer(alerts_app, name="alerts")


@alerts_app.command("summary")
def alerts_summary() -> None:
    """Get alerts summary."""
    client = get_client()

    try:
        summary = client.alerts.summary()
    except ArmorError as e:
        handle_api_error(e)

    console.print("[bold]Alerts Summary[/bold]")
    console.print(f"Total Rules: {summary.total_rules}")
    console.print(f"Active Rules: {summary.active_rules}")
    console.print(f"Recent Alerts: {summary.recent_alerts}")
    console.print(f"Unresolved: [yellow]{summary.unresolved_alerts}[/yellow]")


@alerts_app.command("list")
def alerts_list(
    status: str | None = typer.Option(None, "--status", "-s", help="Filter by status"),
    severity: str | None = typer.Option(None, "--severity", help="Filter by severity"),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results"),
) -> None:
    """List alerts."""
    client = get_client()

    try:
        alerts = client.alerts.list(status=status, severity=severity, limit=limit)
    except ArmorError as e:
        handle_api_error(e)

    if not alerts:
        console.print("No alerts found.")
        return

    table = Table(title="Alerts")
    table.add_column("Asset", style="cyan")
    table.add_column("Message")
    table.add_column("Severity")
    table.add_column("Status")

    for a in alerts:
        sev_style = {
            "critical": "[red]Critical[/red]",
            "warning": "[yellow]Warning[/yellow]",
            "info": "Info",
        }.get(a.severity, a.severity)

        status_style = {
            "triggered": "[red]Triggered[/red]",
            "acknowledged": "[yellow]Acknowledged[/yellow]",
            "resolved": "[green]Resolved[/green]",
        }.get(a.status, a.status)

        table.add_row(
            a.qualified_name or "-",
            a.message[:50] + "..." if len(a.message) > 50 else a.message,
            sev_style,
            status_style,
        )

    console.print(table)


# ============================================================================
# API Keys commands
# ============================================================================

api_keys_app = typer.Typer(help="API key management commands")
app.add_typer(api_keys_app, name="api-keys")


@api_keys_app.command("list")
def api_keys_list(
    include_revoked: bool = typer.Option(False, "--include-revoked", help="Include revoked keys"),
) -> None:
    """List API keys."""
    client = get_client()

    try:
        keys = client.api_keys.list(include_revoked=include_revoked)
    except ArmorError as e:
        handle_api_error(e)

    if not keys:
        console.print("No API keys found.")
        return

    table = Table(title="API Keys")
    table.add_column("Name", style="cyan")
    table.add_column("Key")
    table.add_column("Scope")
    table.add_column("Active")
    table.add_column("Last Used")

    for k in keys:
        table.add_row(
            k.name,
            k.display_key,
            k.scope,
            "[green]Yes[/green]" if k.is_active else "[red]No[/red]",
            str(k.last_used_at)[:10] if k.last_used_at else "Never",
        )

    console.print(table)


@api_keys_app.command("create")
def api_keys_create(
    name: str = typer.Option(..., "--name", "-n", help="Key name", prompt="Key name"),
    scope: str = typer.Option(
        "read-only",
        "--scope",
        "-s",
        help="Permission scope (read-only, read-write, admin)",
    ),
) -> None:
    """Create a new API key."""
    client = get_client()

    try:
        key = client.api_keys.create(name=name, scope=scope)
    except ArmorError as e:
        handle_api_error(e)

    console.print("[green]API key created successfully![/green]")
    console.print()
    console.print(f"[bold]Key:[/bold] {key.key}")
    console.print()
    console.print("[yellow]IMPORTANT: This key will only be shown once![/yellow]")
    console.print("Store it securely.")


@api_keys_app.command("revoke")
def api_keys_revoke(
    key_id: str = typer.Argument(..., help="Key ID to revoke"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
) -> None:
    """Revoke an API key."""
    if not confirm:
        typer.confirm("Are you sure you want to revoke this key?", abort=True)

    client = get_client()

    try:
        client.api_keys.revoke(key_id)
    except ArmorError as e:
        handle_api_error(e)

    console.print("[green]API key revoked successfully.[/green]")


# ============================================================================
# Lineage commands
# ============================================================================

lineage_app = typer.Typer(help="Data lineage commands")
app.add_typer(lineage_app, name="lineage")


@lineage_app.command("get")
def lineage_get(
    asset_id: str = typer.Argument(..., help="Asset ID or qualified name"),
    depth: int = typer.Option(1, "--depth", "-d", help="Depth of lineage (1-5)"),
    direction: str = typer.Option(
        "both", "--direction", help="Direction: upstream, downstream, both"
    ),
) -> None:
    """Get lineage for an asset."""
    client = get_client()

    try:
        lineage = client.lineage.get(asset_id, depth=depth, direction=direction)
    except ArmorError as e:
        handle_api_error(e)

    console.print(f"[bold]Lineage for:[/bold] {lineage.root.qualified_name}")
    console.print()

    if lineage.upstream:
        console.print("[bold]Upstream (dependencies):[/bold]")
        for node in lineage.upstream:
            console.print(f"  - {node.qualified_name}")

    if lineage.downstream:
        console.print("[bold]Downstream (dependents):[/bold]")
        for node in lineage.downstream:
            console.print(f"  - {node.qualified_name}")

    if not lineage.upstream and not lineage.downstream:
        console.print("No lineage information available.")


if __name__ == "__main__":
    app()
