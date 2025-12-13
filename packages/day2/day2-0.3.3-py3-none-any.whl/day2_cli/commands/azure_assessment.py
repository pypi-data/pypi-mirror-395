"""Azure Assessment commands for the MontyCloud DAY2 CLI."""

import json
from typing import Optional, Tuple

import click
from rich.console import Console

from day2.exceptions import Day2Error, ProfileNotFoundError
from day2.models.azure_assessment import CreateAssessmentInput
from day2_cli.utils.context import get_enhanced_context, with_common_options
from day2_cli.utils.exit_codes import ExitCodes, exit_with_error, handle_error_with_exit
from day2_cli.utils.helpers import format_datetime_string
from day2_cli.utils.output_formatter import (
    format_item_output,
    format_list_output,
    format_simple_output,
)

console = Console()


@click.group(name="azure-assessment")
def azure_assessment() -> None:
    """Azure assessment commands."""


@azure_assessment.command("list")
@click.option("--keyword", help="Filter by keyword")
@click.option("--page-number", type=int, help="Page number for pagination")
@click.option(
    "--page-size", type=int, default=10, help="Page size (valid range: 1-100)"
)
@with_common_options(include_tenant_id=True)
def list_azure_assessments(
    keyword: Optional[str],
    page_number: Optional[int],
    page_size: int,
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """List Azure assessments for a tenant.

    If --tenant-id is not provided, uses the default tenant configured with 'day2 profile create' or 'day2 auth login'.
    """
    try:
        # Get enhanced context with tenant resolution
        context = get_enhanced_context(
            output=output, profile=profile, tenant_id=tenant_id, require_tenant=True
        )
        session = context["session"]
        output_format = context["output_format"]
        resolved_tenant_id = context["tenant_id"]

        # Call the client method with explicit parameters for Azure assessments
        result = session.azure_assessment.list_assessments(
            tenant_id=resolved_tenant_id,
            keyword=keyword,
            page_number=page_number,
            page_size=page_size,
        )

        if not result.assessments:
            format_simple_output(
                "No Azure assessments found.", format_override=output_format
            )
            return

        # Convert assessment objects to dictionaries for the formatter
        assessments_data = []
        for assessment_item in result.assessments:
            created_at = format_datetime_string(assessment_item.created_at)
            last_run_at = format_datetime_string(assessment_item.last_run_at)

            # Include Azure-specific fields
            assessments_data.append(
                {
                    "id": assessment_item.id,
                    "name": assessment_item.name,
                    "description": assessment_item.description or "N/A",
                    "scope": assessment_item.scope,
                    "review_owner": getattr(assessment_item, "review_owner", "N/A"),
                    "created_at": created_at,
                    "last_run_at": last_run_at,
                }
            )

        # Define column mapping for the formatter
        columns = {
            "id": "Assessment ID",
            "name": "Name",
            "description": "Description",
            "review_owner": "Review Owner",
            "created_at": "Created At",
            "last_run_at": "Last Run At",
        }

        # Format and output the results
        format_list_output(
            items=assessments_data,
            title=f"Azure Assessments for Tenant: {resolved_tenant_id}",
            columns=columns,
            format_override=output_format,
        )

        # Display pagination information for Azure
        if hasattr(result, "has_more") and result.has_more:
            next_page = (page_number or 1) + 1
            format_simple_output(
                f"More results available. Use --page-number={next_page} to get the next page.",
                format_override=output_format,
            )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)


@azure_assessment.command("create")
@click.option("--name", required=True, help="Name of the Azure assessment")
@click.option("--description", help="Description of the Azure assessment")
@click.option("--review-owner", help="Review owner of the assessment")
@click.option(
    "--scope",
    required=True,
    help='Scope of the Azure assessment as JSON string. Format: [{"SubscriptionId": "11111111-1111-1111-1111-111111111111", "ResourceGroups": ["rg-web", "rg-database"]}]',
)
@click.option(
    "--environment", default="PRODUCTION", help="Environment (default: PRODUCTION)"
)
@click.option("--industry-type", help="Industry type (e.g., Technology)")
@click.option("--industry", help="Industry (e.g., Software)")
@click.option("--diagram-url", help="URL to the architecture diagram")
@with_common_options(include_tenant_id=True)
def create_azure_assessment(
    name: str,
    description: Optional[str],
    review_owner: Optional[str],
    scope: str,
    environment: str,
    industry_type: Optional[str],
    industry: Optional[str],
    diagram_url: Optional[str],
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """Create a new Azure assessment.

    If --tenant-id is not provided, uses the default tenant configured with 'day2 profile create' or 'day2 auth login'.
    """
    try:
        # Validate required inputs first before creating session
        if not scope:
            exit_with_error(
                "Scope is required for Azure assessments",
                ExitCodes.VALIDATION_ERROR,
            )

        try:
            scope_data = json.loads(scope)
            if not isinstance(scope_data, list):
                exit_with_error(
                    "Azure scope must be a JSON array of subscription objects",
                    ExitCodes.VALIDATION_ERROR,
                )
        except json.JSONDecodeError:
            exit_with_error(
                "Scope must be a valid JSON string for Azure",
                ExitCodes.VALIDATION_ERROR,
            )

        # Get enhanced context with tenant resolution
        context = get_enhanced_context(
            output=output, profile=profile, tenant_id=tenant_id, require_tenant=True
        )
        session = context["session"]
        output_format = context["output_format"]
        resolved_tenant_id = context["tenant_id"]

        # Set default values for optional parameters
        description_value = description or ""
        review_owner_value = review_owner or ""

        azure_input = CreateAssessmentInput(
            AssessmentName=name,
            Description=description_value,
            Scope=scope_data,
            ReviewOwner=review_owner_value,
            Environment=environment,
            IndustryType=industry_type,
            Industry=industry,
            DiagramURL=diagram_url,
        )
        result = session.azure_assessment.create_assessment(
            tenant_id=resolved_tenant_id, data=azure_input
        )
        title = "Azure Assessment Created Successfully"
        assessment_data = {
            "ID": result.id,
            "Name": name,
            "Description": description_value or "N/A",
            "Environment": environment,
            "Review Owner": review_owner_value or "N/A",
            "Industry Type": industry_type or "N/A",
            "Industry": industry or "N/A",
            "Diagram URL": diagram_url or "N/A",
        }

        # Format and output the result
        format_item_output(
            item=assessment_data,
            title=title,
            format_override=output_format,
        )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)


@azure_assessment.command("findings")
@click.argument("assessment-id")
@click.option(
    "--severity",
    multiple=True,
    help="Filter by severity (High, Medium, Low) - Azure specific values (can be used multiple times)",
)
@click.option(
    "--status",
    multiple=True,
    help="Filter by status (Failed, Passed) - Azure specific values (can be used multiple times)",
)
@click.option(
    "--resource-group",
    multiple=True,
    help="Filter by Azure resource group (can be used multiple times)",
)
@click.option(
    "--subscription-id",
    multiple=True,
    help="Filter by Azure subscription ID (can be used multiple times)",
)
@click.option(
    "--resource-type",
    multiple=True,
    help="Filter by Azure resource type (e.g., microsoft.compute/virtualmachines) (can be used multiple times)",
)
@click.option(
    "--category",
    multiple=True,
    help="Filter by finding category (Security, Governance, etc.) (can be used multiple times)",
)
@click.option(
    "--resource-id",
    help="Filter by Azure resource ID (single value)",
)
@click.option(
    "--check-title",
    help="Filter by specific check title",
)
@click.option("--page-token", help="Page token for pagination")
@click.option(
    "--page-size", type=int, default=10, help="Page size (valid range: 1-200)"
)
@with_common_options(include_tenant_id=True)
def list_azure_findings(
    assessment_id: str,
    severity: Tuple[str, ...],
    status: Tuple[str, ...],
    resource_group: Tuple[str, ...],
    subscription_id: Tuple[str, ...],
    resource_type: Tuple[str, ...],
    category: Tuple[str, ...],
    resource_id: Optional[str],
    check_title: Optional[str],
    page_token: Optional[str],
    page_size: int,
    output: Optional[str] = None,
    profile: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> None:
    """List findings for an Azure assessment.

    If --tenant-id is not provided, uses the default tenant configured with 'day2 profile create' or 'day2 auth login'.

    ASSESSMENT-ID: ID of the Azure assessment to list findings for.
    """
    try:
        # Get enhanced context with tenant resolution
        context = get_enhanced_context(
            output=output, profile=profile, tenant_id=tenant_id, require_tenant=True
        )
        session = context["session"]
        output_format = context["output_format"]
        resolved_tenant_id = context["tenant_id"]

        result = session.azure_assessment.list_findings(
            tenant_id=resolved_tenant_id,
            assessment_id=assessment_id,
            resource_id=resource_id,
            resource_type=list(resource_type) if resource_type else None,
            resource_group=list(resource_group) if resource_group else None,
            severity=list(severity) if severity else None,
            category=list(category) if category else None,
            subscription_id=list(subscription_id) if subscription_id else None,
            status=list(status) if status else None,
            check_title=check_title,
            page_size=page_size,
            page_token=page_token,
        )
        title = f"Azure Findings for Assessment: {assessment_id}"

        if not result.records:
            format_simple_output(
                "No Azure findings found.",
                format_override=output_format,
            )
            return

        findings_list = result.records

        # Process Azure findings
        findings_data = []
        for finding in findings_list:
            findings_data.append(
                {
                    "resource_id": finding.resource_id,
                    "resource_name": finding.resource_name,
                    "resource_type": finding.resource_type,
                    "resource_group": finding.resource_group,
                    "subscription_id": finding.subscription_id,
                    "severity": finding.severity,
                    "status": finding.status,
                    "category": finding.category,
                    "check_title": finding.check_title,
                    "description": finding.description,
                    "additional_information": finding.additional_information,
                    "recommended_actions": finding.recommended_actions,
                    "created_at": format_datetime_string(finding.created_at),
                    "updated_at": format_datetime_string(finding.updated_at),
                }
            )

        # Define column mapping for the formatter
        columns = {
            "resource_id": "Resource ID",
            "resource_name": "Resource Name",
            "resource_type": "Resource Type",
            "resource_group": "Resource Group",
            "subscription_id": "Subscription ID",
            "severity": "Severity",
            "status": "Status",
            "category": "Category",
            "check_title": "Check Title",
            "description": "Description",
            "recommended_actions": "Recommended Actions",
            "created_at": "Created At",
            "updated_at": "Updated At",
        }

        # Format and output the results
        format_list_output(
            items=findings_data,
            title=title,
            columns=columns,
            format_override=output_format,
        )

        # Display pagination information
        if result.next_page_token:
            format_simple_output(
                f"More results available. Use --page-token={result.next_page_token} to get the next page.",
                format_override=output_format,
            )

    except (Day2Error, ProfileNotFoundError) as e:
        handle_error_with_exit(e)
