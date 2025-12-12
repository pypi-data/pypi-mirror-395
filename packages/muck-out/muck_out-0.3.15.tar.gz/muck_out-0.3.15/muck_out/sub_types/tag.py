from typing import Annotated, Literal
from pydantic import BaseModel, BeforeValidator, Discriminator, Field, Tag


class Mention(BaseModel):
    """Represents a mention

    ```python
    >>> m = Mention(href="http://actor.example/alice", name="@alice@actor.example")
    >>> m.model_dump()
    {'type': 'Mention',
        'href': 'http://actor.example/alice',
        'name': '@alice@actor.example'}

    ```
    """

    type: Literal["Mention"] = Field(default="Mention")
    href: str = Field(
        description="The location the mentioned party can be retrieved at. In the Fediverse usually an actor URI"
    )
    name: str | None = Field(default=None)


class Hashtag(BaseModel):
    """Represents a hashtag

    ```python
    >>> m = Hashtag(name="#cow")
    >>> m.model_dump(exclude_none=True)
    {'type': 'Hashtag', 'name': '#cow'}

    ```
    """

    type: Literal["Hashtag"] = Field(default="Hashtag")
    href: str | None = Field(
        default=None, description="A location related to the hashtag"
    )
    name: str = Field(description="The actual hashtag", examples=["#cow"])


class ObjectLink(BaseModel):
    """Represents a [FEP-e232: Object Link](https://fediverse.codeberg.page/fep/fep/e232/)"""

    type: Literal["Link"] = Field(default="Link")
    href: str = Field(
        examples=["http://remote.example/object/12345"],
        description="The location of the object",
    )
    mediaType: str = Field(
        examples=[
            '''application/ld+json; profile="https://www.w3.org/ns/activitystreams"''',
            "application/activity+json",
        ],
        description="The media type of the object",
    )
    name: str | None = Field(
        default=None,
        examples=["RE http://remote.example/object/12345"],
        description="The microsyntax used to represent the object",
    )
    rel: str | None = Field(default=None, description="Relation to the object")


def discriminator_tag(v):
    match v:
        case {"type": "Hashtag"} | Hashtag():
            return "Hashtag"
        case {"type": "Mention"} | Mention():
            return "Mention"
        case ObjectLink() | {"type": "Link", "mediaType": str()}:
            return "ObjectLink"
        case dict():
            return "unknown"
        case str():
            return "string"

    raise Exception


def to_link(href: str) -> dict:
    return {"href": href}


TagType = Annotated[
    Annotated[Hashtag, Tag("Hashtag")]
    | Annotated[Mention, Tag("Mention")]
    | Annotated[ObjectLink, Tag("ObjectLink")]
    | Annotated[dict, Tag("unknown")]
    | Annotated[Annotated[dict, BeforeValidator(to_link)], Tag("string")],
    Discriminator(discriminator_tag),
]
