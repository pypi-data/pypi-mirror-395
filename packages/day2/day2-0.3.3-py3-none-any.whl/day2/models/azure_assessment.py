"""Azure Assessment Models for MontyCloud DAY2 SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Assessment(BaseModel):
    """Details of an Azure assessment.

    Attributes:
        id: Assessment identifier
        name: Name of the assessment
        description: Description of the assessment
        scope: Scope of the assessment containing subscription and resource group information
        review_owner: Review owner of the assessment
        created_at: Timestamp when the assessment was created
        last_run_at: Timestamp when the assessment was last run (if completed)
    """

    id: str = Field(alias="AssessmentId")
    name: str = Field(alias="AssessmentName")
    description: str = Field(alias="Description")
    scope: Optional[Dict[str, Any]] = Field(None, alias="Scope")
    review_owner: Optional[str] = Field(None, alias="ReviewOwner")
    created_at: Optional[datetime] = Field(None, alias="CreatedAt")
    last_run_at: Optional[datetime] = Field(None, alias="LastRunAt")

    # Allow extra fields and population by name (Python field names)
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class ListAssessmentsOutput(BaseModel):
    """Output of list Azure assessments operation.

    Attributes:
        assessments: List of Azure assessment details
        page_number: Current page number
        has_more: Whether there are more pages available
    """

    assessments: List[Assessment] = Field(alias="Assessments")
    page_number: Optional[int] = Field(None, alias="PageNumber")
    has_more: Optional[bool] = Field(None, alias="HasMore")

    # Allow extra fields and population by name (Python field names)
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class CreateAssessmentInput(BaseModel):
    """Input for creating an Azure assessment.

    Attributes:
        name: Name of the Azure assessment
        description: Description of the assessment
        scope: Array of scope objects containing subscription and resource group information
        review_owner: Review owner of the assessment
        environment: Environment type (e.g., PRODUCTION, DEVELOPMENT)
        industry_type: Type of industry
        industry: Industry category
        diagram_url: URL to the architecture diagram
    """

    name: str = Field(alias="AssessmentName")
    description: str = Field(alias="Description")
    scope: List[Dict[str, Any]] = Field(alias="Scope")
    review_owner: str = Field(alias="ReviewOwner")
    environment: str = Field(alias="Environment")
    industry_type: Optional[str] = Field(None, alias="IndustryType")
    industry: Optional[str] = Field(None, alias="Industry")
    diagram_url: Optional[str] = Field(None, alias="DiagramURL")

    # Allow extra fields and population by name (Python field names)
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class CreateAssessmentOutput(BaseModel):
    """Output of create Azure assessment operation.

    Attributes:
        id: Newly created Azure assessment identifier
    """

    id: str = Field(alias="AssessmentId")

    # Allow extra fields and population by name (Python field names)
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class Finding(BaseModel):
    """Details of an Azure finding.

    Attributes:
        resource_id: ID of the affected resource
        resource_name: Name of the affected resource
        resource_type: Type of the affected resource
        resource_group: Resource group where the resource exists
        severity: Severity level (e.g., High, Medium, Low)
        description: Detailed description of the finding
        status: Current status of the finding (e.g., Failed, Passed)
        category: Category of the finding (e.g., Security, Governance)
        subscription_id: Azure subscription ID where the resource exists
        check_title: Title of the check that generated this finding
        additional_information: Additional information about the finding
        recommended_actions: Recommended actions to address the finding
        created_at: Timestamp when the finding was created
        updated_at: Timestamp when the finding was last updated
    """

    resource_id: Optional[str] = Field(None, alias="ResourceId")
    resource_name: Optional[str] = Field(None, alias="ResourceName")
    resource_type: Optional[str] = Field(None, alias="ResourceType")
    resource_group: Optional[str] = Field(None, alias="ResourceGroup")
    severity: Optional[str] = Field(None, alias="Severity")
    description: Optional[str] = Field(None, alias="Description")
    status: Optional[str] = Field(None, alias="Status")
    category: Optional[str] = Field(None, alias="Category")
    subscription_id: Optional[str] = Field(None, alias="SubscriptionId")
    check_title: Optional[str] = Field(None, alias="CheckTitle")
    additional_information: Optional[dict] = Field(None, alias="AdditionalInformation")
    recommended_actions: Optional[str] = Field(None, alias="RecommendedActions")
    created_at: Optional[datetime] = Field(None, alias="CreatedAt")
    updated_at: Optional[datetime] = Field(None, alias="UpdatedAt")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListFindingsOutput(BaseModel):
    """Output of list Azure findings operation.

    Attributes:
        records: List of Azure finding details
        next_page_token: Token for next page pagination
    """

    records: List[Finding] = Field(alias="Findings", default=[])
    next_page_token: Optional[str] = Field(None, alias="PageToken")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")
