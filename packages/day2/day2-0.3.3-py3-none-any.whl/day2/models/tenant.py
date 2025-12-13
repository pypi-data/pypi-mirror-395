"""Tenant models for the MontyCloud SDK."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class OptionalFeaturesModel(BaseModel):
    """Optional features for a tenant.

    Attributes:
        spend_and_map_project_visibility: Enable spend and MAP project visibility
        cost_savings_insights: Enable cost savings insights
    """

    spend_and_map_project_visibility: bool = Field(alias="SpendAndMAPProjectVisibility")
    cost_savings_insights: bool = Field(alias="CostSavingsInsights")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class CreateTenantInput(BaseModel):
    """Input for creating a tenant.

    Attributes:
        name: Name of the tenant
        description: Description of the tenant
        owner_id: UserId of the user to be assigned as the owner of this tenant.
        category_id: Optional category identifier for the tenant
        feature: Feature set associated with the tenant
        optional_features: Optional features configuration for the tenant
    """

    name: str = Field(default="", alias="Name")
    description: str = Field(default="", alias="Description")
    owner_id: str = Field(default="", alias="OwnerId")
    category_id: Optional[str] = Field(None, alias="CategoryId")
    feature: str = Field(default="", alias="Feature")
    optional_features: Optional[OptionalFeaturesModel] = Field(
        None, alias="OptionalFeatures"
    )

    # Allow extra fields
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class CreateTenantOutput(BaseModel):
    """Output model for CreateTenant API.

    Attributes:
        id: Newly created tenant identifier
        name: Name of the newly created tenant
    """

    id: str = Field(alias="ID")
    name: str = Field(alias="Name")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class TenantDetails(BaseModel):
    """Details of a tenant.

    Attributes:
        id: Unique identifier of the tenant
        name: Name of the tenant
        description: Description of the tenant
        parent_tenant_id: ID of the parent tenant
        created_at: Timestamp when the tenant was created
        created_by: UserId of the user who created the tenant
        modified_at: Timestamp of last modification
        modified_by: UserId of the user who last modified the tenant
        owner: UserId of the owner of the tenant
        owner_id: UserId of the owner of the tenant
        document_url: URL to the tenant's documentation
        feature: Feature set associated with the tenant
        category_id: Category identifier for the tenant
    """

    id: Optional[str] = Field(None, alias="ID")
    name: str = Field(alias="Name")
    description: Optional[str] = Field(None, alias="Description")
    parent_tenant_id: Optional[str] = Field(None, alias="ParentTenantId")
    created_at: Optional[datetime] = Field(None, alias="CreatedAt")
    created_by: Optional[str] = Field(None, alias="CreatedBy")
    modified_at: Optional[datetime] = Field(None, alias="ModifiedAt")
    modified_by: Optional[str] = Field(None, alias="ModifiedBy")
    owner: Optional[str] = Field(None, alias="Owner")
    owner_id: Optional[str] = Field(None, alias="Owner")
    document_url: Optional[str] = Field(None, alias="DocumentURL")
    feature: Optional[str] = Field(None, alias="Feature")
    category_id: Optional[str] = Field(None, alias="CategoryId")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListTenantsOutput(BaseModel):
    """Output model for ListTenants API.

    Attributes:
        tenants: List of tenant details
        next_page_token: Token for fetching the next page of results
    """

    tenants: List[TenantDetails] = Field(alias="Tenants", default=[])
    next_page_token: Optional[str] = Field(None, alias="NextPageToken")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class GetTenantOutput(TenantDetails):
    """Details of individual Tenant.

    This class inherits all attributes from TenantDetails without modification.
    See TenantDetails for the complete list of attributes.
    """


class Account(BaseModel):
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


class ListAccountsOutput(BaseModel):
    """Output of list_accounts operation.

    Attributes:
        accounts: List of account details
        has_more: Whether there are more pages of results
        page_number: Current page number
    """

    accounts: List[Account] = Field(alias="Accounts", default=[])
    has_more: bool = Field(alias="HasMore", default=False)
    page_number: int = Field(alias="PageNumber")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class TenantCategory(BaseModel):
    """Details of a tenant category.

    Attributes:
        id: Unique identifier of the category
        name: Name of the category
        description: Description of the category
    """

    id: str = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Description")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListTenantCategoriesOutput(BaseModel):
    """Output model for ListTenantCategories API.

    Attributes:
        categories: List of tenant categories
        has_more: Whether there are more pages of results
        page_number: Current page number
    """

    categories: List[TenantCategory] = Field(alias="Categories", default=[])
    has_more: bool = Field(alias="HasMore", default=False)
    page_number: int = Field(alias="PageNumber")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")
