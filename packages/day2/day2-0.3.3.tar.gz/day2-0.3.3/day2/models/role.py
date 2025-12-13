"""Role models for the MontyCloud SDK."""

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class RoleModel(BaseModel):
    """Details of a role.

    Attributes:
        description: Detailed description of the role and the permissions it grants
        id: Unique identifier for the role
        name: Name of the role
    """

    description: str = Field(
        ...,
        alias="Description",
        description="Detailed description of the role and the permissions it grants",
    )
    id: str = Field(..., alias="ID", description="Unique identifier for the role")
    name: str = Field(..., alias="Name", description="Name of the role")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListRolesOutput(BaseModel):
    """Output model for list roles API.

    Attributes:
        role: List all available roles that can be assigned to the users
    """

    roles: List[RoleModel] = Field(
        default=[],
        alias="Roles",
        description="List all available roles that can be assigned to the users",
    )

    # Allow extra fields
    model_config = ConfigDict(extra="allow")
