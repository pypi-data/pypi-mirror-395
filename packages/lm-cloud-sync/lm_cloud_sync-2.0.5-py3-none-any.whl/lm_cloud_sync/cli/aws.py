# Description: AWS CLI commands for lm-cloud-sync.
# Description: Provides discover, status, sync, and delete commands for AWS accounts.

import json
import logging
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from lm_cloud_sync.core.config import Settings
from lm_cloud_sync.core.exceptions import ConfigurationError, LMCloudSyncError
from lm_cloud_sync.core.lm_client import LogicMonitorClient
from lm_cloud_sync.providers.aws import AWSProvider

console = Console()
logger = logging.getLogger(__name__)


def get_settings(config_path: str | None = None) -> Settings:
    """Load settings from config file or environment."""
    if config_path:
        path = Path(config_path)
        if not path.exists():
            raise ConfigurationError(f"Config file not found: {config_path}")
        return Settings.from_yaml(path)
    return Settings.from_env()


def get_lm_client(settings: Settings) -> LogicMonitorClient:
    """Create LogicMonitor client from settings."""
    lm = settings.logicmonitor
    if lm.bearer_token:
        return LogicMonitorClient(company=lm.company, bearer_token=lm.bearer_token)
    elif lm.access_id and lm.access_key:
        return LogicMonitorClient(
            company=lm.company, access_id=lm.access_id, access_key=lm.access_key
        )
    else:
        raise ConfigurationError("No valid LM credentials configured")


@click.group()
@click.pass_context
def aws(ctx: click.Context) -> None:
    """AWS account management.

    Discover and sync AWS accounts to LogicMonitor.
    """
    pass


@aws.command()
@click.option("--config", "-c", "config_path", help="Path to config file")
@click.option(
    "--auto-discover",
    is_flag=True,
    required=True,
    help="Use AWS Organizations API to discover accounts (required)",
)
@click.option("--output", "-o", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def discover(
    ctx: click.Context,
    config_path: str | None,
    auto_discover: bool,
    output: str,
) -> None:
    """Discover AWS accounts.

    Lists all AWS accounts in your organization.
    Requires --auto-discover flag and organizations:ListAccounts permission.

    \b
    Examples:
        lm-cloud-sync aws discover --auto-discover
        lm-cloud-sync aws discover --auto-discover --output json
    """
    try:
        settings = get_settings(config_path)
        provider = AWSProvider(config=settings.aws)

        with console.status("[bold green]Discovering AWS accounts..."):
            accounts = provider.discover(auto_discover=auto_discover)

        if output == "json":
            data = [
                {
                    "account_id": a.resource_id,
                    "display_name": a.display_name,
                    "status": a.status,
                    "email": getattr(a, "email", None),
                }
                for a in accounts
            ]
            console.print_json(json.dumps(data, indent=2))
        else:
            if not accounts:
                console.print("[yellow]No accounts found[/yellow]")
                return

            table = Table(title=f"AWS Accounts ({len(accounts)} found)")
            table.add_column("Account ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Email", style="blue")
            table.add_column("Status", style="yellow")

            for account in accounts:
                table.add_row(
                    account.resource_id,
                    account.display_name,
                    getattr(account, "email", "") or "",
                    account.status,
                )

            console.print(table)

    except LMCloudSyncError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error during discovery")
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


@aws.command()
@click.option("--config", "-c", "config_path", help="Path to config file")
@click.option("--show-orphans", is_flag=True, help="Show orphaned integrations")
@click.option("--output", "-o", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def status(
    ctx: click.Context,
    config_path: str | None,
    show_orphans: bool,
    output: str,
) -> None:
    """Show AWS sync status.

    Compares AWS accounts with existing LogicMonitor integrations.

    \b
    Examples:
        lm-cloud-sync aws status
        lm-cloud-sync aws status --show-orphans
    """
    try:
        settings = get_settings(config_path)
        provider = AWSProvider(config=settings.aws)

        with console.status("[bold green]Fetching status..."):
            with get_lm_client(settings) as client:
                integrations = provider.list_integrations(client)

        if output == "json":
            data = {
                "integrations": [
                    {
                        "account_id": g.resource_id,
                        "name": g.name,
                        "lm_group_id": g.id,
                    }
                    for g in integrations
                ],
                "count": len(integrations),
            }
            console.print_json(json.dumps(data, indent=2))
        else:
            console.print(f"\n[bold]LogicMonitor AWS Integrations: {len(integrations)}[/bold]")

            if integrations:
                table = Table(title="Existing Integrations")
                table.add_column("Account ID", style="cyan")
                table.add_column("LM Group Name", style="green")
                table.add_column("LM Group ID", style="yellow")

                for group in integrations:
                    table.add_row(
                        group.resource_id,
                        group.name,
                        str(group.id) if group.id else "",
                    )

                console.print(table)
            else:
                console.print("[yellow]No AWS integrations found in LogicMonitor[/yellow]")

            if show_orphans:
                console.print(
                    "\n[dim]Note: Use 'aws discover --auto-discover' to find accounts "
                    "and compare with integrations[/dim]"
                )

    except LMCloudSyncError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error during status check")
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


@aws.command()
@click.option("--config", "-c", "config_path", help="Path to config file")
@click.option(
    "--auto-discover",
    is_flag=True,
    required=True,
    help="Use AWS Organizations API to discover accounts (required)",
)
@click.option("--dry-run", is_flag=True, help="Preview changes without applying")
@click.option("--delete-orphans", is_flag=True, help="Delete orphaned integrations")
@click.option("--parent-group-id", "-p", type=int, help="LogicMonitor parent group ID for new integrations")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def sync(
    ctx: click.Context,
    config_path: str | None,
    auto_discover: bool,
    dry_run: bool,
    delete_orphans: bool,
    parent_group_id: int | None,
    yes: bool,
) -> None:
    """Sync AWS accounts to LogicMonitor.

    Creates LogicMonitor integrations for AWS accounts.
    Requires --auto-discover flag and appropriate AWS/LM permissions.

    \b
    Prerequisites:
    1. AWS credentials with organizations:ListAccounts permission
    2. IAM role (LogicMonitorRole) created in each target account
    3. LogicMonitor Bearer token

    \b
    Examples:
        lm-cloud-sync aws sync --auto-discover --dry-run
        lm-cloud-sync aws sync --auto-discover --yes
        lm-cloud-sync aws sync --auto-discover --parent-group-id 123 --yes
        lm-cloud-sync aws sync --auto-discover --delete-orphans --yes
    """
    try:
        settings = get_settings(config_path)
        provider = AWSProvider(config=settings.aws)

        # Get parent group ID (CLI flag takes precedence)
        parent_id = parent_group_id or settings.aws.parent_group_id or settings.logicmonitor.parent_group_id

        if dry_run:
            console.print("[bold yellow]DRY RUN MODE - No changes will be made[/bold yellow]\n")

        # Discover accounts
        with console.status("[bold green]Discovering AWS accounts..."):
            accounts = provider.discover(auto_discover=auto_discover)

        console.print(f"Found [bold]{len(accounts)}[/bold] AWS accounts")

        # Get existing integrations
        with console.status("[bold green]Fetching existing integrations..."):
            with get_lm_client(settings) as client:
                integrations = provider.list_integrations(client)

        existing_ids = {g.resource_id for g in integrations}
        account_ids = {a.resource_id for a in accounts}

        # Calculate changes
        to_create = [a for a in accounts if a.resource_id not in existing_ids]
        to_skip = [a for a in accounts if a.resource_id in existing_ids]
        orphans = [g for g in integrations if g.resource_id not in account_ids]

        console.print(f"  To create: [green]{len(to_create)}[/green]")
        console.print(f"  Already exists: [yellow]{len(to_skip)}[/yellow]")
        if orphans:
            console.print(f"  Orphaned: [red]{len(orphans)}[/red]")

        if to_create:
            console.print("\n[bold]Accounts to integrate:[/bold]")
            for account in to_create:
                console.print(f"  - {account.resource_id} ({account.display_name})")

        if orphans and delete_orphans:
            console.print("\n[bold red]Integrations to delete:[/bold red]")
            for group in orphans:
                console.print(f"  - {group.resource_id} (LM Group ID: {group.id})")

        if not to_create and not (orphans and delete_orphans):
            console.print("\n[green]Nothing to do - all accounts are in sync[/green]")
            return

        # Confirm unless --yes or --dry-run
        if not dry_run and not yes and not click.confirm("\nProceed with sync?"):
            console.print("[yellow]Aborted[/yellow]")
            return

        # Execute sync
        if dry_run:
            console.print("\n[yellow]DRY RUN - Would have made the following changes:[/yellow]")
            for account in to_create:
                console.print(f"  [green]CREATE[/green] AWS - {account.resource_id}")
            if orphans and delete_orphans:
                for group in orphans:
                    console.print(f"  [red]DELETE[/red] {group.name} (ID: {group.id})")
        else:
            with get_lm_client(settings) as client:
                result = provider.sync(
                    client=client,
                    dry_run=False,
                    auto_discover=auto_discover,
                    create_missing=True,
                    delete_orphans=delete_orphans,
                    parent_id=parent_id,
                    name_template="AWS - {resource_id}",
                    custom_properties=settings.sync.custom_properties,
                )

                console.print("\n[bold]Sync Results:[/bold]")
                console.print(f"  Created: [green]{len(result.created)}[/green]")
                console.print(f"  Skipped: [yellow]{len(result.skipped)}[/yellow]")
                if result.deleted:
                    console.print(f"  Deleted: [red]{len(result.deleted)}[/red]")
                if result.failed:
                    console.print(f"  Failed: [red]{len(result.failed)}[/red]")
                    for resource_id, error in result.failed.items():
                        console.print(f"    - {resource_id}: {error}")

    except LMCloudSyncError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error during sync")
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


@aws.command()
@click.option("--config", "-c", "config_path", help="Path to config file")
@click.option("--account-id", required=True, help="AWS account ID to delete integration for")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def delete(
    ctx: click.Context,
    config_path: str | None,
    account_id: str,
    yes: bool,
) -> None:
    """Delete an AWS integration from LogicMonitor.

    \b
    Examples:
        lm-cloud-sync aws delete --account-id 123456789012
        lm-cloud-sync aws delete --account-id 123456789012 --yes
    """
    try:
        settings = get_settings(config_path)
        provider = AWSProvider(config=settings.aws)

        with get_lm_client(settings) as client:
            integrations = provider.list_integrations(client)

            # Find the integration
            target = None
            for group in integrations:
                if group.resource_id == account_id:
                    target = group
                    break

            if not target:
                console.print(
                    f"[yellow]No integration found for AWS account {account_id}[/yellow]"
                )
                return

            console.print(f"Found integration: {target.name} (ID: {target.id})")

            if not yes and not click.confirm("Delete this integration?"):
                console.print("[yellow]Aborted[/yellow]")
                return

            if target.id:
                provider.delete_integration(client, target.id)
                console.print(f"[green]Deleted integration for account {account_id}[/green]")
            else:
                console.print("[red]Cannot delete: group ID not found[/red]")

    except LMCloudSyncError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error during delete")
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)
