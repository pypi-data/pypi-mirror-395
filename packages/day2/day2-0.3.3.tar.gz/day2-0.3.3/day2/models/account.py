"""Account models for the MontyCloud SDK."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class GenerateOnboardingTemplateInput(BaseModel):
    """Pydantic model for input of Generate Onboarding Template API.

    Attributes:
        account_type: Type of AWS account to onboard: STANDALONE or MANAGEMENT
        account_name: Name of the AWS account to onboard
        account_number: AWS account number to onboard
        regions: List of AWS regions to onboard
    """

    account_type: str = Field(
        ...,
        alias="AccountType",
        description="Type of AWS account to onboard: STANDALONE or MANAGEMENT",
    )
    account_name: str = Field(
        ...,
        alias="AccountName",
        description="Name of the AWS account to onboard",
    )
    account_number: str = Field(
        ...,
        alias="AccountNumber",
        description="AWS account number to onboard",
    )
    regions: List[str] = Field(
        default_factory=list,
        alias="Regions",
        description="List of AWS regions to onboard - Required for Assessment Feature type (Audit Permissions), not supported by other feature types (AutomatedCloudOps, ContinuousVisibility)",
    )


class AccountItem(BaseModel):
    """Details of an account.

    Attributes:
        account_id: Unique account identifier
        number: AWS account number
        name: Account name
        status: Current status of the account
        type: Type of the account
        permission_model: Permission model used for the account
        onboarded_date: Date when the account was onboarded
    """

    account_id: str = Field(alias="AccountId")
    number: str = Field(alias="Number")
    name: str = Field(alias="Name")
    status: str = Field(alias="Status")
    type: str = Field(alias="Type")
    permission_model: str = Field(alias="PermissionModel")
    onboarded_date: str = Field(alias="OnboardedDate")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class GenerateOnboardingTemplateOutput(BaseModel):
    """Output of generate_onboarding_template operation.

    Attributes:
        account_id: The account ID for the onboarding template
        expires_on: The expiration date and time of the onboarding template
        onboarding_template_url: URL to the generated onboarding template
    """

    account_id: str = Field(
        ...,
        alias="AccountId",
        description="The account ID for the onboarding template",
    )
    expires_on: str = Field(
        ...,
        alias="ExpiresOn",
        description="The expiration date and time of the onboarding template",
    )
    onboarding_template_url: str = Field(
        ...,
        alias="OnboardingTemplateURL",
        description="URL to the generated onboarding template",
    )


class ListAccountsOutput(BaseModel):
    """Output model for ListAccounts API.

    Attributes:
        accounts: List of account details
        has_more: Whether there are more pages of results
        page_number: Current page number
    """

    accounts: List[AccountItem] = Field(alias="Accounts", default=[])
    has_more: bool = Field(alias="HasMore", default=False)
    page_number: int = Field(alias="PageNumber")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class RegionStatusErrorDetail(BaseModel):
    """Error detail information for region status.

    Attributes:
        step: The step where the error occurred
        reason: The reason for the error
    """

    step: str = Field(..., description="The step where the error occurred.")
    reason: str = Field(..., description="The reason for the error.")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class RegionStatus(BaseModel):
    """Region Status information for a single region.

    Attributes:
        discovery_status (Optional[str]): Discovery status of the region (e.g., "COMPLETED", "PENDING", "STARTED").
        error (Optional[List[RegionStatusErrorDetail]]): List of error details if the region connection has encountered issues.
        region_code (str): Code identifying the region (e.g., "us-east-1", "eu-west-1", "ap-south-1").
        status (str): Operational status of the region (e.g., "CONNECTED", "DISCONNECTED", "ACTIVE").
    """

    discovery_status: Optional[str] = Field(alias="DiscoveryStatus", default=None)
    error: Optional[List[RegionStatusErrorDetail]] = Field(alias="Error", default=None)
    region_code: str = Field(alias="RegionCode")
    status: str = Field(alias="Status")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListRegionStatusOutput(BaseModel):
    """Output model for list Region Status API.

    Attributes:
        region_status (List[RegionStatus]): List of Region Status for an AWS account.
    """

    region_status: List[RegionStatus] = Field(alias="RegionStatus", default=[])

    # Allow extra fields
    model_config = ConfigDict(extra="allow")
