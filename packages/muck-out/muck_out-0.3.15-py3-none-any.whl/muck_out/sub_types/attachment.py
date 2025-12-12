from typing import Annotated
from pydantic import BaseModel, Discriminator, Field, Tag

from muck_out.pydantic_types import PlainText


class PropertyValue(BaseModel):
    """
    Key value pairs in the attachment of an actor
    as used by Mastodon
    """

    type: str = Field("PropertyValue", description="""Fixed type for serialization""")

    name: PlainText = Field(
        examples=["Pronouns"],
        description="Key of the value",
    )

    value: PlainText = Field(
        examples=["They/them"],
        description="Value",
    )


def discriminator_actor_attachment(v):
    match v:
        case PropertyValue() | {"type": "PropertyValue"}:
            return "PropertyValue"

    return "unknown"


ActorAttachment = Annotated[
    (Annotated[PropertyValue, Tag("PropertyValue")] | Annotated[dict, Tag("unknown")]),
    Discriminator(discriminator_actor_attachment),
]
"""Discriminates between the possible values of an attachment to an actor"""
