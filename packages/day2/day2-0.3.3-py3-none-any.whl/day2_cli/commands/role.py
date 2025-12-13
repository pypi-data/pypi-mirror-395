"""Role commands for the MontyCloud DAY2 CLI."""

from typing import Optional

import click
from rich.console import Console

from day2.exceptions import Day2Error, ProfileNotFoundError
from day2_cli.utils.context import get_enhanced_context
from day2_cli.utils.exit_codes import handle_error_with_exit
from day2_cli.utils.output_formatter import format_list_output

console = Console()


@click.group(name="role")
def role() -> None:
    """Role commands."""


@role.command("list")
@click.option(
    "--output",
    type=click.Choice(["table", "json"], case_sensitive=False),
    help="Output format (table or json)",
)
@click.option(
    "--profile",
    type=str,
    help="Configuration profile to use",
)
def list_roles(
    output: Optional[str] = None,
    profile: Optional[str] = None,
) -> None:
    """List all available roles.

    This command retrieves the list of roles that can be assigned to the users.
    """
    try:
        # Get enhanced context
        context = get_enhanced_context(
            output=output, profile=profile, require_tenant=False
        )
        session = context["session"]
        output_format = context["output_format"]

        # List roles
        result = session.authorization.list_roles()

        if not result.roles:
            console.print("[yellow]No roles found.[/yellow]")
            return

        # Convert role objects to dictionaries for output
        role_list = []
        for role_item in result.roles:
            role_dict = {
                "id": role_item.id,
                "name": role_item.name,
                "description": role_item.description,
            }
            role_list.append(role_dict)

        # Define columns for table output
        columns = {
            "id": "ID",
            "name": "Name",
            "description": "Description",
        }

        # Format and output the roles list
        format_list_output(
            role_list,
            "Roles",
            columns,
            output_format,
        )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)
