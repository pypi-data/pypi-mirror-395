from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator

from cattle_grid.account.permissions import base_urls_for_permissions


class RegistrationType(BaseModel):
    """Configuration for one registration path"""

    name: str = Field(
        examples=["dev"],
        description="name of the registration. Will be part of the path, i.e. `/register/{name}`",
    )

    permissions: list[str] = Field(
        examples=["admin"],
        description="List of permissions given to the registering account.",
        min_length=1,
    )

    extra_parameters: list[str] = Field(
        default=[],
        description="Extra parameters that should be in the request, will be stored in the actors meta information",
        examples=["fediverse"],
    )

    create_default_actor_on: str | None = Field(
        default=None,
        examples=["http://domain.example"],
        description="Attempt to create an actor on the specified base_url. The actor will be given the acct-uri `acct:{name}@{domain}`, where domain is taken from the base_url",
    )

    @model_validator(mode="after")
    def check_default_actor_on_is_allowed(self) -> Self:
        if not self.create_default_actor_on:
            return self
        allowed_base_urls = base_urls_for_permissions(self.permissions)

        if self.create_default_actor_on not in allowed_base_urls:
            raise Exception("Base url is not allowed")

        return self


class RegisterConfiguration(BaseModel):
    """Configuration for the register endpoint"""

    registration_types: list[RegistrationType] = Field(
        examples=[
            RegistrationType(name="dev", permissions=["dev"]),
        ],
        description="List of registration types",
    )
