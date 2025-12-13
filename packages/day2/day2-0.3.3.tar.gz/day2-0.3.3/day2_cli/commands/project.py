"""Project commands for the MontyCloud DAY2 CLI."""

from typing import Optional

import click
from rich.console import Console

from day2.exceptions import Day2Error, ProfileNotFoundError
from day2_cli.utils.context import get_enhanced_context, with_common_options
from day2_cli.utils.exit_codes import handle_error_with_exit
from day2_cli.utils.output_formatter import format_list_output

console = Console()


@click.group()
def project() -> None:
    """Project commands."""


@project.command("list")
@with_common_options(include_tenant_id=True)
def list_projects(
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """
    List projects.

    List all projects for a tenant.

    If --tenant-id is not provided, uses the default tenant configured with 'day2 profile create' or 'day2 auth login'.

    """
    try:
        # Get enhanced context with tenant resolution
        context = get_enhanced_context(
            output=output,
            profile=profile,
            tenant_id=tenant_id,
            require_tenant=True,
        )
        session = context["session"]
        output_format = context["output_format"]
        resolved_tenant_id = context["tenant_id"]

        response = session.project.list_projects(
            tenant_id=resolved_tenant_id,
        )

        if not response.projects:
            console.print("[yellow]No projects found.[/yellow]")
            return

        project_list = []
        for project_item in response.projects:
            if output_format == "json":
                # Convert to dict with snake_case for consistency
                project_dict = {
                    "project_id": project_item.project_id,
                    "name": project_item.name,
                    "description": project_item.description,
                    "accounts": [
                        {
                            "account_name": acc.account_name,
                            "account_number": acc.account_number,
                            "account_id": acc.account_id,
                            "status": acc.status,
                            "regions": [
                                {
                                    "region_code": r.region_code,
                                    "status": r.status,
                                }
                                for r in acc.regions
                            ],
                        }
                        for acc in project_item.accounts
                    ],
                    "environments": project_item.environments,
                    "users": project_item.users,
                    "metadata": (
                        {
                            "budget_exist": project_item.metadata.budget_exist,
                            "budget_value": project_item.metadata.budget_value,
                            "group_name": project_item.metadata.group_name,
                            "owner": project_item.metadata.owner,
                            "point_person": project_item.metadata.point_person,
                        }
                        if project_item.metadata
                        else None
                    ),
                    "created_by": project_item.created_by,
                    "created_on": project_item.created_on,
                    "modified_by": project_item.modified_by,
                    "modified_on": project_item.modified_on,
                }
            else:
                account_details = []
                for account in project_item.accounts:
                    acc_num = account.account_number
                    account_details.append(acc_num)

                accounts_display = (
                    ", ".join(account_details) if account_details else "N/A"
                )

                metadata_display = "N/A"
                if project_item.metadata:
                    metadata_parts = []

                    budget_val = project_item.metadata.budget_value or 0
                    metadata_parts.append(f"Budget: ${budget_val:,}")

                    owner = project_item.metadata.owner or ""
                    if owner.strip():
                        metadata_parts.append(f"Owner: {owner.strip()}")

                    group = project_item.metadata.group_name or ""
                    if group.strip():
                        metadata_parts.append(f"Group: {group.strip()}")

                    contact = project_item.metadata.point_person or ""
                    if contact.strip():
                        metadata_parts.append(f"Point Person: {contact.strip()}")

                    if metadata_parts:
                        metadata_display = "\n".join(metadata_parts)
                    else:
                        metadata_display = "No metadata"

                project_dict = {
                    "id": project_item.project_id,
                    "name": project_item.name,
                    "description": project_item.description or "N/A",
                    "accounts": accounts_display,
                    "environments": project_item.environments or 0,
                    "users": project_item.users or 0,
                    "metadata": metadata_display,
                    "created_by": project_item.created_by or "N/A",
                    "created_on": project_item.created_on or "N/A",
                    "modified_by": project_item.modified_by or "N/A",
                    "modified_on": project_item.modified_on or "N/A",
                }

            project_list.append(project_dict)

        columns = {
            "id": "Project Id",
            "name": "Name",
            "description": "Description",
            "accounts": "Accounts",
            "environments": "Environments",
            "users": "Users",
            "metadata": "Metadata",
            "created_by": "Created By",
            "created_on": "Created On",
            "modified_by": "Modified By",
            "modified_on": "Modified On",
        }

        format_list_output(
            project_list,
            f"Project list for Tenant: {resolved_tenant_id}",
            columns,
            format_override=output_format,
        )
        if output_format != "json":
            console.print(
                "[yellow] Note: Nested fields may not display clearly in table format. Use --output json for full details.[/yellow]"
            )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)


@project.command("list-requests")
@click.option(
    "--status",
    type=click.Choice(["PENDING", "INACTIVE"], case_sensitive=False),
    help="Filter by request status",
)
@with_common_options(include_tenant_id=True)
def list_project_requests(
    status: Optional[str] = None,
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """
    List project requests.

    This command lists all project requests for a tenant.
    """
    try:
        # Get enhanced context with tenant resolution
        context = get_enhanced_context(
            output=output,
            profile=profile,
            tenant_id=tenant_id,
            require_tenant=True,
        )
        session = context["session"]
        output_format = context["output_format"]
        resolved_tenant_id = context["tenant_id"]

        # Pass status filter directly to the SDK method
        response = session.project.list_project_requests(
            tenant_id=resolved_tenant_id,
            status=status.upper() if status else None,
        )

        if not response.project_requests:
            if status:
                console.print(
                    f"[yellow]No project requests found with status "
                    f"{status.upper()}.[/yellow]"
                )
            else:
                console.print("[yellow]No project requests found.[/yellow]")
            return

        request_list = []
        for request_item in response.project_requests:
            if output_format == "json":
                # Convert to dict with snake_case for consistency
                request_dict = {
                    "request_id": request_item.request_id,
                    "name": request_item.name,
                    "description": request_item.description,
                    "status": request_item.status,
                    "status_change_message": (request_item.status_change_message),
                    "status_changed_by": request_item.status_changed_by,
                    "metadata": (
                        {
                            "budget_exist": request_item.metadata.budget_exist,
                            "budget_value": request_item.metadata.budget_value,
                            "group_name": request_item.metadata.group_name,
                            "owner": request_item.metadata.owner,
                            "point_person": request_item.metadata.point_person,
                        }
                        if request_item.metadata
                        else None
                    ),
                    "created_at": request_item.created_at,
                    "created_by": request_item.created_by,
                    "modified_at": request_item.modified_at,
                    "modified_by": request_item.modified_by,
                }
            else:
                # Table format - format metadata for display
                metadata_display = "N/A"
                if request_item.metadata:
                    metadata_parts = []

                    budget_val = request_item.metadata.budget_value or 0
                    metadata_parts.append(f"Budget: ${budget_val:,}")

                    owner = request_item.metadata.owner or ""
                    if owner.strip():
                        metadata_parts.append(f"Owner: {owner.strip()}")

                    group = request_item.metadata.group_name or ""
                    if group.strip():
                        metadata_parts.append(f"Group: {group.strip()}")

                    contact = request_item.metadata.point_person or ""
                    if contact.strip():
                        metadata_parts.append(f"Point Person: {contact.strip()}")

                    if metadata_parts:
                        metadata_display = "\n".join(metadata_parts)
                    else:
                        metadata_display = "No metadata"

                request_dict = {
                    "id": request_item.request_id,
                    "name": request_item.name,
                    "description": request_item.description or "N/A",
                    "status": request_item.status or "N/A",
                    "status_change_message": (
                        request_item.status_change_message or "N/A"
                    ),
                    "status_changed_by": (request_item.status_changed_by or "N/A"),
                    "metadata": metadata_display,
                    "created_at": request_item.created_at or "N/A",
                    "created_by": request_item.created_by or "N/A",
                    "modified_at": request_item.modified_at or "N/A",
                    "modified_by": request_item.modified_by or "N/A",
                }

            request_list.append(request_dict)
        columns = {
            "id": "Request Id",
            "name": "Name",
            "description": "Description",
            "status": "Status",
            "status_change_message": "Status Change Message",
            "status_changed_by": "Status Changed By",
            "metadata": "Metadata",
            "created_at": "Created At",
            "created_by": "Created By",
            "modified_at": "Modified At",
            "modified_by": "Modified By",
        }

        format_list_output(
            request_list,
            f"Project Requests for Tenant: {resolved_tenant_id}",
            columns,
            format_override=output_format,
        )
        if output_format != "json":
            console.print(
                "[yellow] Note: Nested fields may not display clearly in table format. Use --output json for full details.[/yellow]"
            )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)
