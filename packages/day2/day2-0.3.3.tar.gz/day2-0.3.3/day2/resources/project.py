"""Project resource implementation for the MontyCloud DAY2 SDK."""

from typing import Optional

from day2.client.base import BaseClient
from day2.models.project import ListProjectRequestsOutput, ListProjectsOutput
from day2.session import Session


class ProjectClient(BaseClient):
    """Client for interacting with Projects."""

    def __init__(self, session: Session) -> None:
        """Initialize a new ProjectClient.

        Args:
            session: MontyCloud session.
        """
        super().__init__(session, "project")

    def list_projects(
        self,
        tenant_id: str,
    ) -> ListProjectsOutput:
        """List all projects for a tenant.

        Args:
            tenant_id: Tenant ID to list projects for.

        Returns:
            ListProjectsOutput: Object containing list of projects.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.project
            >>> response = client.list_projects(tenant_id="tenant-123")
            >>> for project in response.projects:
            ...     print(f"Project ID: {project.project_id}")
            ...     print(f" Project Name: {project.name}")

        """
        response = self._make_request("GET", f"tenants/{tenant_id}/projects")
        return ListProjectsOutput.model_validate(response)

    def list_project_requests(
        self,
        tenant_id: str,
        status: Optional[str] = None,
    ) -> ListProjectRequestsOutput:
        """List all project requests for a tenant.

        Args:
            tenant_id: Tenant ID to list project requests for.
            status: Optional status filter (e.g., "PENDING", "INACTIVE").

        Returns:
            ListProjectRequestsOutput: Object containing list of project
                requests.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.project
            >>> response = client.list_project_requests(tenant_id="tenant-123")
            >>> for request in response.project_requests:
            ...     print(f"Request ID: {request.request_id}")
            ...     print(f" Name: {request.name}")
            ...     print(f" Status: {request.status}")
            >>> # Filter by status
            >>> response = client.list_project_requests(tenant_id="tenant-123", status="PENDING")
        """
        # Build query parameters
        params = {}
        if status:
            params["Status"] = status

        response = self._make_request(
            "GET", f"tenants/{tenant_id}/projects/requests", params=params
        )
        return ListProjectRequestsOutput.model_validate(response)
