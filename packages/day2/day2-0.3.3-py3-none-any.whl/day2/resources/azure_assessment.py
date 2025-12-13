"""Azure Assessment resource implementation for the MontyCloud DAY2 SDK."""

from typing import Any, Dict, List, Optional, Union

from day2.client.base import BaseClient
from day2.models.azure_assessment import (
    CreateAssessmentInput,
    CreateAssessmentOutput,
    ListAssessmentsOutput,
    ListFindingsOutput,
)
from day2.session import Session


class AzureAssessmentClient(BaseClient):
    """Client for interacting with Azure Assessment service."""

    def __init__(self, session: Session) -> None:
        """Initialize a new AzureAssessmentClient.

        Args:
            session: MontyCloud session.
        """
        super().__init__(session, "azure_assessment")

    def list_assessments(
        self,
        tenant_id: str,
        keyword: Optional[str] = None,
        page_size: int = 10,
        page_number: Optional[int] = None,
    ) -> ListAssessmentsOutput:
        """List Azure assessments in a tenant.

        Args:
            tenant_id: The ID of the tenant to list assessments for.
            keyword: Optional keyword to filter assessments by name or description.
            page_size: The number of assessments per page (default: 10, valid range: 1-100).
            page_number: Page number for pagination.

        Returns:
            ListAssessmentsOutput: Object containing list of Azure assessments and pagination info.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.azure_assessment
            >>> response = client.list_assessments("tenant-123")
            >>> for assessment in response.assessments:
            ...     print(f"{assessment.name}: {assessment.description}")
        """
        params = {}
        if keyword:
            params["Keyword"] = keyword
        if page_size:
            params["PageSize"] = str(page_size)
        if page_number:
            params["PageNumber"] = str(page_number)

        endpoint = f"tenants/{tenant_id}/azure/azure-wafr/assessments"
        response = self._make_request("GET", endpoint, params=params)
        return ListAssessmentsOutput.model_validate(response)

    def create_assessment(
        self, tenant_id: str, data: CreateAssessmentInput
    ) -> CreateAssessmentOutput:
        """Create a new Azure assessment in a tenant.

        Args:
            tenant_id: The ID of the tenant to create the assessment in.
            data: The Azure assessment data to create.

        Returns:
            CreateAssessmentOutput: Object containing the created assessment details.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.azure_assessment
            >>> data = CreateAssessmentInput(
            ...     name="Azure Assessment",
            ...     description="Azure assessment description",
            ...     scope=[{"SubscriptionId": "subscription-id", "ResourceGroups": ["rg-1", "rg-2"]}],
            ...     review_owner="Azure Team",
            ...     environment="PRODUCTION",
            ...     industry_type="Software",
            ...     industry="Technology",
            ...     diagram_url="https://example.com/architecture-diagram"
            ... )
            >>> response = client.create_assessment("tenant-123", data)
            >>> print(f"Created Azure assessment with ID: {response.id}")
        """
        # Create the payload for Azure assessment
        azure_payload: Dict[str, Any] = {
            "AssessmentName": data.name,
            "Description": data.description,
            "Scope": data.scope,
            "ReviewOwner": data.review_owner,
            "Environment": data.environment,
        }

        # Add optional fields if provided
        if data.industry_type:
            azure_payload["IndustryType"] = data.industry_type
        if data.industry:
            azure_payload["Industry"] = data.industry
        if data.diagram_url:
            azure_payload["DiagramURL"] = data.diagram_url

        response = self._make_request(
            "POST",
            f"tenants/{tenant_id}/azure/azure-wafr/assessments",
            json=azure_payload,
        )
        return CreateAssessmentOutput.model_validate(response)

    def list_findings(
        self,
        tenant_id: str,
        assessment_id: str,
        page_size: int = 10,
        page_token: Optional[str] = None,
        severity: Optional[List[str]] = None,
        status: Optional[List[str]] = None,
        resource_type: Optional[List[str]] = None,
        resource_id: Optional[str] = None,
        resource_group: Optional[List[str]] = None,
        subscription_id: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        check_title: Optional[str] = None,
    ) -> ListFindingsOutput:
        """List findings for a specific Azure assessment in a tenant.

        Args:
            tenant_id: ID of the tenant the assessment belongs to.
            assessment_id: ID of the assessment to list findings for.
            page_size: The number of findings per page (default: 10, valid range: 1-100).
            page_token: Token for pagination.
            severity: Optional list of severities to filter findings by ('High', 'Medium', 'Low').
            status: Optional list of statuses to filter findings by ('Failed', 'Passed').
            resource_type: Optional list of resource types to filter findings by.
            resource_id: Optional resource ID to filter findings by (single value).
            resource_group: Optional list of resource groups to filter findings by.
            subscription_id: Optional list of subscription IDs to filter findings by.
            category: Optional list of categories to filter findings by.
            check_title: Optional check title to filter findings by.

        Returns:
            ListFindingsOutput: Object containing list of Azure findings and pagination info.

        Raises:
            ResourceNotFoundError: If the assessment does not exist.
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key", api_secret_key="your-secret-key")
            >>> client = session.azure_assessment
            >>> response = client.list_findings(
            ...     tenant_id="tenant-123",
            ...     assessment_id="assessment-123",
            ...     resource_group=["vm-test-01_group"],
            ...     page_size=10
            ... )
            >>> for finding in response.records:
            ...     print(f"{finding.resource_id}: {finding.check_title}")
        """
        params: Dict[str, Union[str, List[str]]] = {}

        # Add Azure parameters
        if resource_id is not None:
            params["ResourceId"] = resource_id
        if check_title is not None:
            params["CheckTitle"] = check_title
        if page_size is not None:
            params["PageSize"] = str(page_size)
        if page_token is not None:
            params["PageToken"] = page_token

        # Add list parameters for Azure
        azure_list_params = [
            ("ResourceType", resource_type),
            ("ResourceGroup", resource_group),
            ("Severity", severity),
            ("Category", category),
            ("SubscriptionId", subscription_id),
            ("Status", status),
        ]

        for param_name, param_value in azure_list_params:
            if param_value is not None and param_value:
                params[param_name] = param_value

        endpoint = (
            f"tenants/{tenant_id}/azure/azure-wafr/assessments/{assessment_id}/findings"
        )
        response = self._make_request("GET", endpoint, params=params)
        return ListFindingsOutput.model_validate(response)
