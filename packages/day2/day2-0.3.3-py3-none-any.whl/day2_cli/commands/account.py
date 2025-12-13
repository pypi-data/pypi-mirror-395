"""Account commands for the MontyCloud DAY2 CLI."""

from typing import Optional

import click
from rich.console import Console

from day2.exceptions import Day2Error, ProfileNotFoundError
from day2_cli.utils.context import get_enhanced_context, with_common_options
from day2_cli.utils.exit_codes import handle_error_with_exit
from day2_cli.utils.output_formatter import format_item_output, format_list_output

console = Console()


@click.group(name="account")
def account() -> None:
    """Account commands."""


# Generate AWS Onboarding Template
@account.command("generate-onboarding-template")
@click.option(
    "--account-type",
    type=click.Choice(["STANDALONE", "MANAGEMENT"], case_sensitive=False),
    required=True,
    help="Type of AWS account to onboard: STANDALONE or MANAGEMENT",
)
@click.option(
    "--account-name",
    type=str,
    required=True,
    help="Name of the AWS account to onboard.",
)
@click.option(
    "--account-number",
    type=str,
    required=True,
    help="AWS account number to onboard.",
)
@click.option(
    "--regions",
    type=str,
    required=False,
    help="Comma-separated list of AWS regions to onboard - Required for Assessment Feature type (Audit Permissions), not supported by other feature types (AutomatedCloudOps, ContinuousVisibility).",
)
@with_common_options(include_tenant_id=True)
def generate_onboarding_template(
    account_type: str,
    account_name: str,
    account_number: str,
    regions: str,
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """Generate an AWS onboarding template for a specific tenant.

    This command generates an AWS CloudFormation template for onboarding AWS accounts
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

        # Convert comma-separated regions to list if provided
        regions_list = []  # Default to empty list
        if regions:
            regions_list = [region.strip() for region in regions.split(",")]

        # Generate the AWS onboarding template
        result = session.account.get_onboarding_template(
            tenant_id=resolved_tenant_id,
            account_type=account_type.upper(),
            account_name=account_name,
            account_number=account_number,
            regions=regions_list,
        )

        # Convert template details to dictionary for output
        template_dict = {
            "account_id": result.account_id,
            "expires_on": result.expires_on,
            "onboarding_template_url": result.onboarding_template_url,
        }

        # Format and output the template details
        format_item_output(
            template_dict,
            f"AWS Onboarding Template for {account_type} Account",
            output_format,
        )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)


@account.command("list")
@click.option(
    "--page-size",
    type=int,
    default=10,
    help="Page size, Default is 10. Valid range: 1-100",
)
@click.option(
    "--page-number",
    type=int,
    default=1,
    help="Page number for pagination, Default is 1",
)
@with_common_options(include_tenant_id=True)
def list_accounts(
    page_size: int = 10,
    page_number: int = 1,
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """List accounts for a specific tenant.

    This command lists all accounts in a tenant.
    If --tenant-id is not provided, uses the default tenant configured with `day2 profile create` or `day2 auth login`.
    """
    try:
        # Get enhanced context
        context = get_enhanced_context(
            output=output, profile=profile, tenant_id=tenant_id, require_tenant=True
        )
        session = context["session"]
        output_format = context["output_format"]
        resolved_tenant_id = context["tenant_id"]

        result = session.account.list_accounts(
            tenant_id=resolved_tenant_id, page_size=page_size, page_number=page_number
        )

        if not result.accounts:
            console.print("[yellow]No accounts found.[/yellow]")
            return

        # Convert account objects to dictionaries for output
        account_list = []
        for account_item in result.accounts:
            account_dict = {
                "account_id": account_item.account_id,
                "number": account_item.number,
                "name": account_item.name,
                "status": account_item.status,
                "type": account_item.type,
                "permission_model": account_item.permission_model,
                "onboarded_date": account_item.onboarded_date,
            }
            account_list.append(account_dict)

        # Define columns for table output
        columns = {
            "account_id": "Account ID",
            "number": "Number",
            "name": "Name",
            "status": "Status",
            "type": "Type",
            "permission_model": "Permission Model",
            "onboarded_date": "Onboarded Date",
        }

        # Format and output the account list
        format_list_output(
            account_list,
            f"Accounts for Tenant {resolved_tenant_id}",
            columns,
            output_format,
        )

        # Check if there are more accounts
        if result.has_more:
            console.print(
                f"[yellow]More results available. Use --page-number={result.page_number + 1} to get the next page.[/yellow]"
            )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)


# List Region Status
@account.command("list-region-status")
@click.option(
    "--account-id",
    type=str,
    required=True,
    help="ID of the account to get Region Status for",
)
@with_common_options(include_tenant_id=True)
def list_region_status(
    account_id: str,
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """List region status for an account.

    This command retrieves the discovery and operational status for all regions
    under a specific tenant and account.
    """
    try:
        # Get enhanced context with tenant resolution
        context = get_enhanced_context(
            profile=profile,
            tenant_id=tenant_id,
            require_tenant=True,
        )

        session = context["session"]
        resolved_tenant_id = context["tenant_id"]
        output_format = output or "table"

        # Get Region Status from the API
        result = session.account.list_region_status(
            tenant_id=resolved_tenant_id, account_id=account_id
        )

        if not result.region_status:
            console.print("[yellow]No region status found.[/yellow]")
            return

        # Convert region status objects to dictionaries for output
        regions_list = []
        for region_status in result.region_status:
            # Handle error display differently for JSON vs table output
            if output_format == "json":
                # For JSON output, include the full RegionStatusErrorDetail structure
                json_error_value = None
                if region_status.error:
                    json_error_value = [
                        {"step": error_detail.step, "reason": error_detail.reason}
                        for error_detail in region_status.error
                    ]

                region_dict = {
                    "region_code": region_status.region_code,
                    "status": region_status.status,
                    "discovery_status": region_status.discovery_status or "N/A",
                    "error": json_error_value,
                }
            else:
                # For table output, format as readable string
                table_error_value = "N/A"
                if region_status.error:
                    # Convert list of RegionStatusErrorDetail objects to readable string
                    error_parts = []
                    for error_detail in region_status.error:
                        error_parts.append(
                            f"{error_detail.step}: {error_detail.reason}"
                        )
                    table_error_value = "\n".join(error_parts)

                region_dict = {
                    "region_code": region_status.region_code,
                    "status": region_status.status,
                    "discovery_status": region_status.discovery_status or "N/A",
                    "error": table_error_value,
                }
            regions_list.append(region_dict)

        # Define columns for table output
        columns = {
            "region_code": "Region Code",
            "status": "Status",
            "discovery_status": "Discovery Status",
            "error": "Error",
        }

        # Format and output the regions list
        format_list_output(
            regions_list,
            f"Region Status for Account {account_id} (Tenant {resolved_tenant_id})",
            columns,
            output_format,
        )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)
