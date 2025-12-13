"""User commands for the MontyCloud DAY2 CLI."""

from typing import Optional

import click
from rich.console import Console

from day2.exceptions import Day2Error, ProfileNotFoundError
from day2.models.user import CreateUserInput
from day2_cli.utils.context import get_enhanced_context, with_common_options
from day2_cli.utils.exit_codes import handle_error_with_exit
from day2_cli.utils.output_formatter import format_item_output, format_list_output

console = Console()


@click.group()
def user() -> None:
    """User commands."""


@user.command("list")
@with_common_options(include_tenant_id=True)
def list_users(
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """List users associated with a specific tenant.

    This command lists all the users in the tenant.
    """
    try:
        # Get enhanced context
        context = get_enhanced_context(
            output=output, profile=profile, tenant_id=tenant_id, require_tenant=True
        )
        session = context["session"]
        resolved_tenant_id = context["tenant_id"]
        output_format = context["output_format"]

        result = session.user.list_users(resolved_tenant_id)

        if not result.users:
            console.print("[yellow]No users found.[/yellow]")
            return

        # Convert user objects to dictionaries for output
        user_list = []
        for user_item in result.users:
            user_dict = {
                "name": user_item.name,
                "email": user_item.email,
                "user_id": user_item.user_id,
            }
            user_list.append(user_dict)

        # Define columns for table output
        columns = {
            "name": "Name",
            "email": "Email",
            "user_id": "User ID",
        }

        # Format and output the user list
        format_list_output(
            user_list,
            f"Users for Tenant: {resolved_tenant_id}",
            columns,
            output_format,
        )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)


@user.command("create")
@click.option("--name", required=True, help="Name of the user")
@click.option("--email", required=True, help="Email id of the user")
@click.option(
    "--temporary-password", required=True, help="Temporary password of the user"
)
@click.option("--role-id", required=True, help="Role ID to be assigned to the user")
@click.option(
    "--projects",
    help="Comma-separated list of project ids to be assigned to the user",
)
@click.option(
    "--federated-access-roles",
    help="Comma-separated list of federated access roles to be assigned to the user",
)
@with_common_options(include_tenant_id=True)
def create_user(
    name: str,
    email: str,
    temporary_password: str,
    role_id: str,
    projects: Optional[str],
    federated_access_roles: Optional[str],
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """Create user for a tenant.

    This command creates a new user for a tenant.

    !!! info "Federated Access Roles"
        This operation is available only if the tenant's **FAA** feature is enabled.

        - Allowed FAA roles: `AdminUser`, `PowerUser`, `ReadOnlyUser`
        - Users with the **Business Admin** or **Cloud Admin** role may be assigned **any** FAA role.
        - Users with the **Read Only** role can be assigned **only** the `ReadOnlyUser` FAA role.
    """
    try:
        # Get enhanced context
        context = get_enhanced_context(
            output=output, profile=profile, tenant_id=tenant_id, require_tenant=True
        )
        session = context["session"]
        resolved_tenant_id = context["tenant_id"]
        output_format = context["output_format"]

        # Parse projects if provided
        project_ids = (
            [project.strip() for project in projects.split(",")] if projects else None
        )

        federated_access_roles_list = (
            [role.strip() for role in federated_access_roles.split(",")]
            if federated_access_roles
            else None
        )

        # Create a CreateUserInput object
        create_user_input = CreateUserInput(
            Name=name,
            Email=email,
            TemporaryPassword=temporary_password,
            RoleId=role_id,
            Projects=project_ids,
            FederatedAccessRoles=federated_access_roles_list,
        )

        result = session.user.create_user(
            tenant_id=resolved_tenant_id, data=create_user_input
        )

        # Create user data for output
        user_output_data = {
            "userId": result.user_id,
        }

        # Format and output the result
        format_item_output(
            item=user_output_data,
            title="User Created Successfully",
            format_override=output_format,
        )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)
