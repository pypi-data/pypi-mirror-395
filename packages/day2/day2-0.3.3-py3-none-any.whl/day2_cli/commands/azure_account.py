"""Azure Account commands for the MontyCloud DAY2 CLI."""

from typing import Optional

import click
from rich.console import Console

from day2.exceptions import Day2Error, ProfileNotFoundError
from day2_cli.utils.context import get_enhanced_context, with_common_options
from day2_cli.utils.exit_codes import handle_error_with_exit
from day2_cli.utils.output_formatter import format_item_output

console = Console()


@click.group(name="azure-account")
def azure_account() -> None:
    """Azure Account commands."""


# Generate Azure Onboarding Template
@azure_account.command("generate-onboarding-command")
@with_common_options(include_tenant_id=True)
def generate_onboarding_command(
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """Generate an Azure onboarding command for a specific tenant.

    This command generates an Azure onboarding command for onboarding Azure subscriptions
    to DAY2.
    """
    try:
        # Get enhanced context with tenant resolution
        context = get_enhanced_context(
            output=output, profile=profile, tenant_id=tenant_id, require_tenant=True
        )
        session = context["session"]
        output_format = context["output_format"]
        resolved_tenant_id = context["tenant_id"]

        # Get the Azure onboarding command
        result = session.azure_account.get_onboarding_command(
            tenant_id=resolved_tenant_id
        )

        # Convert template details to dictionary for output
        template_dict = {
            "account_id": result.account_id,
            "onboarding_command": result.onboarding_command,
            "type": result.type,
        }

        # Format and output the command details
        format_item_output(
            template_dict,
            "Azure Onboarding Command",
            output_format,
        )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)
