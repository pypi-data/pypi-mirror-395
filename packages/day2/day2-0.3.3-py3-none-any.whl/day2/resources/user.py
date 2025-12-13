"""User resource client for the MontyCloud DAY2 SDK."""

import logging
from typing import TYPE_CHECKING, Optional

from day2.client.base import BaseClient
from day2.client.user_context import UserContext
from day2.models.user import CreateUserInput, CreateUserOutput, ListUsersOutput

if TYPE_CHECKING:
    from day2.session import Session

logger = logging.getLogger(__name__)


class UserClient(BaseClient):
    """Client for interacting with Users."""

    def __init__(self, session: "Session") -> None:
        """Initialize a new UserClient.

        Args:
            session: MontyCloud session.
        """
        super().__init__(session, "user")

    def get_user(self) -> Optional[UserContext]:
        """Get information about the authenticated user.

        Returns:
            UserContext containing the user's information if successful,
            None if the request fails.
        """
        try:
            # Use _make_request instead of directly calling session.request
            response_data = self._make_request("GET", "auth/user")
            if response_data:
                logger.debug("Retrieved user context: %s", response_data)
                return UserContext.from_dict(response_data)
            logger.warning("Failed to get user context: empty response")
            return None
        except Exception as e:  # pylint: disable=broad-except
            logger.warning("Error retrieving user context: %s", e)
            return None

    def list_users(self, tenant_id: str) -> ListUsersOutput:
        """Retrieves list of Users for a specific tenant.

        Args:
            tenant_id: ID of the tenant to list users for.

        Returns:
            ListUsersOutput: Object containing list of users.

        Raises:
            ResourceNotFoundError: If the tenant does not exist.
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.user
            >>> response = client.list_users(tenant_id="your-tenant-id")
            >>> for user in response.users:
            ...     print(f"{user.user_id}: {user.name} {user.email}")
        """

        response = self._make_request("GET", f"tenants/{tenant_id}/users")
        return ListUsersOutput.model_validate(response)

    def create_user(self, tenant_id: str, data: CreateUserInput) -> CreateUserOutput:
        """Create user for a tenant.

        !!! info "Federated Access Roles"
            This operation is available only if the tenant's **FAA** feature is enabled.

            - Allowed FAA roles: `AdminUser`, `PowerUser`, `ReadOnlyUser`
            - Users with the **Business Admin** or **Cloud Admin** role may be assigned **any** FAA role.
            - Users with the **Read Only** role can be assigned **only** the `ReadOnlyUser` FAA role.

        Args:
            tenant_id: ID of the tenant to create user for.
            data: The user data to create.

        Returns:
            CreateUserOutput: Object containing the created user id.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.user
            # The payload for creating a user varies based on the role type:
            # 1. For Cloud Admin and Business Admin roles, FederatedAccessRoles can include one or more of PowerUser, ReadOnlyUser, AdminUser, or omitted.
            # 2. For the Read Only role, FederatedAccessRoles must be ReadOnlyUser or omitted.
            # 3. For Project Owner, Project User, and Reports Access roles, the Projects field must include at least one project ID and FederatedAccessRoles should not be provided.
            >>> data = CreateUserInput(
            ...     Name="UserName",
            ...     Email="username@example.com",
            ...     TemporaryPassword="*********",
            ...     RoleId="13acd9eb-6a65-41f8-a941-d4c6edb3f1c9",
            ...     Projects = ["8e5a5792-89a4-45fc-9260-dd673015df03"],
            ... )
            >>> response = client.create_user(tenant_id="your-tenant-id", data=data)
            >>> print(f"Created user with ID: {response.user_id}")
        """

        create_user_payload: dict[str, str | list[str]] = {
            "Name": data.name,
            "Email": data.email,
            "TemporaryPassword": data.temporary_password,
            "RoleId": data.role_id,
        }

        # Add optional fields if they have values
        if data.projects:
            create_user_payload["Projects"] = data.projects
        if data.federated_access_roles:
            create_user_payload["FederatedAccessRoles"] = data.federated_access_roles

        response = self._make_request(
            "POST", f"tenants/{tenant_id}/users", json=create_user_payload
        )
        return CreateUserOutput.model_validate(response)
