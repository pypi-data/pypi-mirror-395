"""User models for the MontyCloud SDK."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    """Details of a user in a tenant.

    Attributes:
        name: Name of the user
        email: Email address of the user
        user_id: Unique identifier of the user
    """

    name: str = Field(alias="Name")
    email: str = Field(alias="Email")
    user_id: str = Field(alias="UserId")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListUsersOutput(BaseModel):
    """Output model for ListUsers API.

    Attributes:
        users: List of users in the tenant
    """

    users: List[User] = Field(alias="Users", default=[])

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class CreateUserInput(BaseModel):
    """
    Input model for CreateUser API.

    Attributes:
        name: Name of the user
        email: Email address of the user
        temporary_password: Temporary password for the user
        role_id: Role ID for the user
        projects: (Optional) Project(s) List of project ids for project roles. Applicable for project specific roles
        federated_access_roles: (Optional) List of federated access roles. Applicable for admin roles
    """

    name: str = Field(alias="Name")
    email: str = Field(alias="Email")
    temporary_password: str = Field(alias="TemporaryPassword")
    role_id: str = Field(alias="RoleId")
    projects: Optional[List[str]] = Field(None, alias="Projects")
    federated_access_roles: Optional[List[str]] = Field(
        None, alias="FederatedAccessRoles"
    )

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class CreateUserOutput(BaseModel):
    """Output model for CreateUser API.

    Attributes:
       user_id: Unique identifier of the created user
    """

    user_id: str = Field(alias="UserId")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")
