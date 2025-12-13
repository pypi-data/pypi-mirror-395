"""Azure Account resource implementation for the MontyCloud DAY2 SDK."""

from day2.client.base import BaseClient
from day2.models.azure_account import GenerateOnboardingCommandOutput
from day2.session import Session


class AzureAccountClient(BaseClient):
    """Client for interacting with the Azure Account service."""

    def __init__(self, session: Session) -> None:
        """Initialize a new AzureAccountClient.

        Args:
            session: MontyCloud session.
        """
        super().__init__(session, "azure_account")

    def get_onboarding_command(self, tenant_id: str) -> GenerateOnboardingCommandOutput:
        """Generate an Azure onboarding command for the specified tenant.

        Args:
            tenant_id: The ID of the tenant to generate the onboarding command for.

        Returns:
            GenerateOnboardingCommandOutput: Object containing the account ID, script text, and type.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.azure_account
            >>> response = client.get_onboarding_command(tenant_id="tenant-123")
            >>> print(f"Account ID: {response.account_id}")
            >>> print(f"Onboarding Command: {response.onboarding_command}")
            >>> print(f"Type: {response.type}")
        """
        response = self._make_request(
            "POST", f"tenants/{tenant_id}/accounts/azure/onboarding-template"
        )
        return GenerateOnboardingCommandOutput.model_validate(response)
