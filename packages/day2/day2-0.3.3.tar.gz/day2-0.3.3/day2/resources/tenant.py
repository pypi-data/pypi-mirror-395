"""Tenant resource implementation for the MontyCloud DAY2 SDK."""

from typing import Optional

from day2.client.base import BaseClient
from day2.exceptions import ValidationError
from day2.models.tenant import (
    CreateTenantInput,
    CreateTenantOutput,
    GetTenantOutput,
    ListAccountsOutput,
    ListTenantCategoriesOutput,
    ListTenantsOutput,
)
from day2.session import Session


class TenantClient(BaseClient):
    """Client for interacting with the Tenants."""

    def __init__(self, session: Session) -> None:
        """Initialize a new TenantClient.

        Args:
            session: MontyCloud session.
        """
        super().__init__(session, "tenant")

    def list_tenants(
        self, page_size: int = 10, page_token: Optional[str] = None
    ) -> ListTenantsOutput:
        """List tenants that the user has access to.

        Args:
            page_size: Number of tenants to be fetched in a page (default: 10, valid range: 1-100).
            page_token: Token for pagination.

        Returns:
            ListTenantsOutput: Object containing list of tenants and pagination info.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.tenant
            >>> response = client.list_tenants(page_size=10)
            >>> for tenant in response.tenants:
            ...     print(f"{tenant.id}: {tenant.name}")
            >>> # To get the next page of results:
            >>> if response.next_page_token:
            ...     next_page = client.list_tenants(page_size=10, page_token=response.next_page_token)
        """
        params: dict[str, object] = {
            "PageSize": page_size,
        }

        if page_token:
            params["PageToken"] = page_token

        response = self._make_request("GET", "tenants/", params=params)
        return ListTenantsOutput.model_validate(response)

    def get_tenant(self, tenant_id: str) -> GetTenantOutput:
        """Get details of a specific tenant.

        Args:
            tenant_id: ID of the tenant to get details for.

        Returns:
            GetTenantOutput: Object containing tenant details.

        Raises:
            ResourceNotFoundError: If the tenant does not exist.
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.tenant
            >>> response = client.get_tenant("123e4567-e89b-12d3-a456-426614174000")
            >>> print(f"Tenant name: {response.name}")
        """
        # The endpoint for getting tenant details is directly using the tenant ID in the path
        response = self._make_request("GET", f"tenants/{tenant_id}")
        return GetTenantOutput.model_validate(response)

    def list_accounts(
        self, tenant_id: str, page_size: int = 10, page_number: int = 1
    ) -> ListAccountsOutput:
        """List accounts associated with a specific tenant.

        Args:
            tenant_id: ID of the tenant to list accounts for.
            page_size: Number of accounts to be fetched in a page (default: 10, valid range: 1-100).
            page_number: Page number for pagination (default: 1).

        Returns:
            ListAccountsOutput: Object containing list of accounts and pagination info.

        Raises:
            ResourceNotFoundError: If the tenant does not exist.
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.tenant
            >>> response = client.list_accounts("tenant-123", page_size=10)
            >>> for account in response.accounts:
            ...     print(f"{account.number}: {account.name}")
        """
        params: dict[str, object] = {
            "PageSize": page_size,
            "PageNumber": page_number,
        }

        response = self._make_request(
            "GET", f"tenants/{tenant_id}/accounts", params=params
        )
        return ListAccountsOutput.model_validate(response)

    def list_categories(
        self, page_size: int = 10, page_number: int = 1
    ) -> ListTenantCategoriesOutput:
        """List available tenant categories.

        Args:
            page_size: Number of categories to be fetched in a page (default: 10, valid range: 1-100).
            page_number: Page number for pagination (default: 1).

        Returns:
            ListTenantCategoriesOutput: Object containing list of tenant categories and pagination info.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.tenant
            >>> response = client.list_categories(page_size=10)
            >>> for category in response.categories:
            ...     print(f"{category.id}: {category.name}")
        """
        params: dict[str, object] = {
            "PageSize": page_size,
            "PageNumber": page_number,
        }

        response = self._make_request("GET", "tenants/categories", params=params)
        return ListTenantCategoriesOutput.model_validate(response)

    def create_tenant(self, data: CreateTenantInput) -> CreateTenantOutput:
        """Create a new tenant.

        Args:
            data: The tenant data to create.

        Returns:
            CreateTenantOutput: Object containing the created tenant details.

        Raises:
            ValidationError: If required fields are missing or invalid.
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.tenant
            >>> data = CreateTenantInput(
            ...     Name="Acme Tenant 2.0 Beta",
            ...     Description="Acme cloud tenant for Cost monitoring",
            ...     OwnerId="884edec2-19b8-4dd3-b1aa-d1b16664e322",
            ...     Feature="Assessment", # AutomatedCloudOps, ContinuousVisibility, Assessment are valid features
            ...     OptionalFeatures=OptionalFeaturesModel(
            ...         SpendAndMAPProjectVisibility=True,
            ...         CostSavingsInsights=True
            ...     )
            ... )
            >>> response = client.create_tenant(data)
            >>> print(f"Created tenant with ID: {response.id}")
        """
        # Validate required fields
        if not data.name or data.name.strip() == "":
            raise ValidationError("Name is required", 400)
        if not data.description or data.description.strip() == "":
            raise ValidationError("Description is required", 400)
        if not data.owner_id or data.owner_id.strip() == "":
            raise ValidationError("OwnerId is required", 400)
        if not data.feature or data.feature.strip() == "":
            raise ValidationError("Feature is required", 400)

        # Create the payload with fields in the exact order expected by the API
        payload: dict[str, object] = {
            "Name": data.name,
            "Description": data.description,
            "OwnerId": data.owner_id,
            "Feature": data.feature,
        }

        # Add optional fields if they have values
        if data.category_id is not None:
            payload["CategoryId"] = data.category_id
        if data.optional_features is not None:
            payload["OptionalFeatures"] = {
                "SpendAndMAPProjectVisibility": data.optional_features.spend_and_map_project_visibility,
                "CostSavingsInsights": data.optional_features.cost_savings_insights,
            }

        response = self._make_request("POST", "tenants/", json=payload)
        return CreateTenantOutput.model_validate(response)
