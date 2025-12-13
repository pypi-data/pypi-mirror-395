from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, computed_field


class OrderedCollection(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True, validate_by_name=True)

    field_context: Literal["https://www.w3.org/ns/activitystreams"] = Field(
        default="https://www.w3.org/ns/activitystreams", alias="@context"
    )

    type: Literal["OrderedCollection"] = Field(
        default="OrderedCollection", description="the type"
    )

    id: str = Field(
        examples=["https://actor.example/followers"],
        description="The URI of the object",
    )

    items: Annotated[
        list[str],
        Field(
            default=[],
            examples=[["https://actor.example/one", "https://actor.example/two"]],
            description="The elements of the list",
            alias="orderedItems",
        ),
    ]

    @computed_field
    @property
    def totalItems(self) -> int:
        return len(self.items)
