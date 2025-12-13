"""Role resource implementation for the MontyCloud DAY2 SDK."""

from day2.client.base import BaseClient
from day2.models.role import ListRolesOutput
from day2.session import Session


class AuthorizationClient(BaseClient):
    """Client for interacting with Role."""

    def __init__(self, session: Session) -> None:
        """Initialize a new AuthorizationClient.

        Args:
            session: MontyCloud session.
        """
        super().__init__(session, "role")

    def list_roles(self) -> ListRolesOutput:
        """List all available roles.
        This endpoint retrieves the list of roles that can be assigned to the users.

        Returns:
            ListRolesOutput: Object containing list of roles.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.authorization
            >>> response = client.list_roles()
            >>> for role in response.roles:
            ...     print(f"Role ID: {role.id}")
            ...     print(f" Name: {role.name}")
            ...     print(f" Description: {role.description}")
        """
        response = self._make_request("GET", "roles")
        return ListRolesOutput.model_validate(response)
