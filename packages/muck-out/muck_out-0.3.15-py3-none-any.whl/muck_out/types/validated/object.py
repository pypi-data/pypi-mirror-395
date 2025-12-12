from typing import Any
from pydantic import Field

from muck_out.pydantic_types import PlainText
from muck_out.types.common import CommonObject

from .common import Common


class Object(Common, CommonObject):
    attributed_to: str = Field(
        examples=["https://actor.example/"],
        description="id of the actor that authored this object",
        alias="attributedTo",
    )
    content: str | None = Field(default=None, description="The content of the object")
    content_plain: PlainText | None = Field(
        default=None,
        description="The content of the object stripped of html",
        alias="contentPlain",
    )

    attachment: list[dict[str, Any]] | None = Field(
        None,
        description="A list of objects that are attached to the original object",
    )
    url: list[dict[str, Any]] = Field(
        default=[],
        description="A list of urls that expand on the content of the object",
    )
    sensitive: bool | None = Field(
        None,
        description="""
    Marks the object as sensitive. Currently, used by everyone, a better way would be an element of the tag list that labels the object as sensitive due a reason
    """,
    )
