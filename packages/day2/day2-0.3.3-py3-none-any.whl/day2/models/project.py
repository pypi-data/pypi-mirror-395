"""Project models for the MontyCloud DAY2 SDK."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AccountRegion(BaseModel):
    """Region information for an account.

    Attributes:
        region_code: Region location code
        status: Status of region
    """

    region_code: str = Field(alias="RegionCode")
    status: str = Field(alias="Status")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class AccountItem(BaseModel):
    """Account information within a project.

    Attributes:
        account_name: Name of account
        account_number: Account number
        account_id: Unique identifier for account
        status: Connection status of account
        regions: List of regions for this account
    """

    account_name: str = Field(alias="AccountName")
    account_number: str = Field(alias="AccountNumber")
    account_id: str = Field(alias="AccountId")
    status: Optional[str] = Field(None, alias="Status")
    regions: List[AccountRegion] = Field(default=[], alias="Regions")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ProjectMetadata(BaseModel):
    """Metadata information for a project.

    Attributes:
        budget_exist: Boolean value if budget exists
        budget_value: Amount of budget
        group_name: Department/category account belongs to
        owner: Owner name
        point_person: Point of contact
    """

    budget_exist: Optional[bool] = Field(None, alias="BudgetExist")
    budget_value: Optional[int] = Field(None, alias="BudgetValue")
    group_name: Optional[str] = Field(None, alias="GroupName")
    owner: Optional[str] = Field(None, alias="Owner")
    point_person: Optional[str] = Field(None, alias="PointPerson")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ProjectItem(BaseModel):
    """Project item in a list response.

    Attributes:
        project_id: Unique identifier for the project
        name: Name of project
        description: Description of project
        accounts: List of accounts associated with project
        environments: Number of environments
        created_by: User who created the project
        created_on: Creation datetime
        modified_by: Modified by username
        modified_on: Modification datetime
        metadata: Project metadata including budget and ownership info
        users: Number of users linked
    """

    project_id: str = Field(alias="ProjectId")
    name: str = Field(alias="Name")
    description: Optional[str] = Field(None, alias="Description")
    accounts: List[AccountItem] = Field(default=[], alias="Accounts")
    environments: Optional[int] = Field(None, alias="Environments")
    created_by: Optional[str] = Field(None, alias="CreatedBy")
    created_on: Optional[str] = Field(None, alias="CreatedOn")
    modified_by: Optional[str] = Field(None, alias="ModifiedBy")
    modified_on: Optional[str] = Field(None, alias="ModifiedOn")
    metadata: Optional[ProjectMetadata] = Field(None, alias="Metadata")
    users: Optional[int] = Field(None, alias="Users")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListProjectsOutput(BaseModel):
    """Output of list_projects operation.

    Attributes:
        projects: List of project details
    """

    projects: List[ProjectItem] = Field(default=[], alias="Projects")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ProjectRequestItem(BaseModel):
    """Project request item in a list response.

    Attributes:
        request_id: Unique identifier for the project request
        name: Name of project request
        description: Description of project request
        status: Status of the project request (e.g. PENDING/INACTIVE)
        status_change_message: Message associated with status change
        status_changed_by: User who changed the status
        created_at: Creation datetime
        created_by: User who created the request
        modified_at: Modification datetime
        modified_by: User who modified the request
        metadata: Project metadata including budget and ownership info
    """

    request_id: str = Field(alias="RequestId")
    name: str = Field(alias="Name")
    description: Optional[str] = Field(None, alias="Description")
    status: Optional[str] = Field(None, alias="Status")
    status_change_message: Optional[str] = Field(None, alias="StatusChangeMessage")
    status_changed_by: Optional[str] = Field(None, alias="StatusChangedBy")
    created_at: Optional[str] = Field(None, alias="CreatedAt")
    created_by: Optional[str] = Field(None, alias="CreatedBy")
    modified_at: Optional[str] = Field(None, alias="ModifiedAt")
    modified_by: Optional[str] = Field(None, alias="ModifiedBy")
    metadata: Optional[ProjectMetadata] = Field(None, alias="Metadata")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListProjectRequestsOutput(BaseModel):
    """Output of list_project_requests operation.

    Attributes:
        project_requests: List of project request details
    """

    project_requests: List[ProjectRequestItem] = Field(
        default=[], alias="ProjectRequests"
    )

    # Allow extra fields
    model_config = ConfigDict(extra="allow")
