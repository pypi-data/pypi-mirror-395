from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class SerializationOptions(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias=True,
        validate_by_name=True,
    )


class WithActor(SerializationOptions):
    actor: str = Field(
        description="actor_id of the actor that received the message",
        examples=["http://host.example/actor"],
    )


class WithTransformedData(SerializationOptions):
    data: dict[str, Any] = Field(
        examples=[
            {
                "raw": {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "Create",
                    "actor": "http://host.example/actor/1",
                }
            }
        ],
        description="""The data that was exchanged. We note that this data was processed by the transformers.""",
    )
