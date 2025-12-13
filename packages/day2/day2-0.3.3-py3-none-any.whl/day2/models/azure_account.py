"""Azure Account models for the MontyCloud SDK."""

from pydantic import BaseModel, ConfigDict, Field


class GenerateOnboardingCommandOutput(BaseModel):
    """Output of generate_azure_onboarding_command operation.

    Attributes:
        account_id: The account ID for the onboarding command
        onboarding_command: The PowerShell command to execute in Azure Cloud Shell for onboarding
        type: Indicates the type of script or command, eg.'PowerShellCommand'
    """

    account_id: str = Field(
        ...,
        alias="AccountId",
        description="The account ID for the onboarding template",
    )
    onboarding_command: str = Field(
        ...,
        alias="OnboardingCommand",
        description="The PowerShell command to execute in Azure Cloud Shell for onboarding",
    )
    type: str = Field(
        ...,
        alias="Type",
        description="Indicates the type of script or command, eg.'PowerShellCommand'",
    )

    # Allow extra fields
    model_config = ConfigDict(extra="allow")
