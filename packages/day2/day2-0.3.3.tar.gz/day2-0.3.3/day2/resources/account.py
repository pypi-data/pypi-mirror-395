"""Account resource implementation for the MontyCloud DAY2 SDK."""

from typing import List, Optional

from day2.client.base import BaseClient
from day2.client.config import API_VERSION_V2
from day2.models.account import (
    GenerateOnboardingTemplateInput,
    GenerateOnboardingTemplateOutput,
    ListAccountsOutput,
    ListRegionStatusOutput,
)
from day2.session import Session


class AccountClient(BaseClient):
    """Client for interacting with Accounts."""

    def __init__(self, session: Session) -> None:
        """Initialize a new AccountClient.

        Args:
            session: MontyCloud session.
        """
        super().__init__(session, "account")

    def get_onboarding_template(
        self,
        tenant_id: str,
        account_type: str,
        account_name: str,
        account_number: str,
        regions: Optional[List[str]] = None,
    ) -> GenerateOnboardingTemplateOutput:
        """Generate an AWS onboarding template for the specified tenant.

        Args:
            tenant_id: The ID of the tenant to generate the onboarding template for.
            account_type: Type of AWS account to onboard: STANDALONE or MANAGEMENT.
            account_name: Name of the AWS account to onboard.
            account_number: AWS account number to onboard.
            regions: List of AWS regions to onboard - Required for Assessment Feature type (Audit Permissions), not supported by other feature types (AutomatedCloudOps, ContinuousVisibility).

        Returns:
            GenerateOnboardingTemplateOutput: Object containing the account ID, expiration date and time of the onboarding link and onboarding template URL.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.account
            >>> response = client.get_onboarding_template(
            ...     tenant_id="tenant-123",
            ...     account_type="STANDALONE",  # STANDALONE or MANAGEMENT
            ...     account_name="AcmeAccount",
            ...     account_number="123456789012",
            ...     regions=[
            ...         "us-east-1",
            ...         "us-west-2"
            ...     ]  # Required for Assessment Feature type (Audit Permissions)
            ...        # Not supported by other feature types (AutomatedCloudOps, ContinuousVisibility)
            ... )
            >>> print(f"Onboarding URL: {response.onboarding_template_url}")
        """
        data = GenerateOnboardingTemplateInput(
            AccountType=account_type,
            AccountName=account_name,
            AccountNumber=account_number,
            Regions=regions if regions is not None else [],
        )

        response = self._make_request(
            "POST",
            f"tenants/{tenant_id}/accounts/aws/onboarding-template",
            API_VERSION_V2,
            json=data.model_dump(by_alias=True),
        )
        return GenerateOnboardingTemplateOutput.model_validate(response)

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
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.account
            >>> response = client.list_accounts(tenant_id="your-tenant-id", page_size=10)
            >>> for account in response.accounts:
            ...     print(f"Account ID: {account.account_id}")
            ...     print(f"Account Name: {account.name}")
        """
        params: dict[str, object] = {
            "PageSize": page_size,
            "PageNumber": page_number,
        }

        response = self._make_request(
            "GET", f"tenants/{tenant_id}/accounts/", params=params
        )
        return ListAccountsOutput.model_validate(response)

    def list_region_status(
        self, tenant_id: str, account_id: str
    ) -> ListRegionStatusOutput:
        """List Region Status for an AWS account.

        Args:
            tenant_id: ID of the tenant.
            account_id: ID of the account.

        Returns:
            ListRegionStatusOutput: Object containing list of region statuses.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.account
            >>> response = client.list_region_status(tenant_id="your-tenant-id", account_id="your-account-id")
            >>> for region in response.region_status:
            ...     print(f"Region: {region.region_code}")
            ...     print(f" Status: {region.status}")
            ...     print(f" Discovery Status: {region.discovery_status}")
        """
        response = self._make_request(
            "GET", f"tenants/{tenant_id}/accounts/{account_id}/region-status"
        )
        return ListRegionStatusOutput.model_validate(response)
