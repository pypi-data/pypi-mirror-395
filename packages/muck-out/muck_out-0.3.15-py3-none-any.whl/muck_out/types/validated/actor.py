from pydantic import Field

from muck_out.types.common import CommonActor
from muck_out.pydantic_types.list_utils import ListOfStringsWithAtLeastOneElement

from .common import CommonAll


class Actor(CommonAll, CommonActor):
    """Describes an ActivityPub actor"""

    type: str = Field(
        examples=["Person", "Service", "Application"],
        description="""The type of Actor""",
    )

    icon: dict | None = Field(
        None,
        examples=[{"type": "Image", "url": "https://actor.example/icon.png"}],
        description="The avatar of the actor",
    )

    also_known_as: list[str] | None = Field(
        None,
        examples=[["https://alice.example", "https://alice.example/profile"]],
        alias="alsoKnownAs",
        description="Other uris associated with the actor",
    )

    preferred_username: str | None = Field(
        None, examples=["john"], alias="preferredUsername"
    )

    identifiers: ListOfStringsWithAtLeastOneElement = Field(
        default=[], description="An ordered list of identifiers"
    )
