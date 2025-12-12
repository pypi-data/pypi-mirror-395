from typing import Annotated
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from muck_out.pydantic_types import HtmlStringOrNone, IdFieldOrNone, UrlList
from muck_out.sub_types import ActorAttachment, TagType
from muck_out.transform.list_utils import transform_to_list


class CommonActor(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias=True,
        validate_by_name=True,
        field_title_generator=lambda field_name, field_info: "",
    )
    inbox: IdFieldOrNone = Field(
        default=None,
        examples=["https://actor.example/inbox"],
        description="The inbox of the actor",
    )

    outbox: IdFieldOrNone = Field(
        default=None,
        examples=["https://actor.example/outbox"],
        description="The outbox of the actor",
    )

    followers: IdFieldOrNone = Field(
        default=None,
        examples=["https://actor.example/followers"],
        description="The followers collection of the actor",
    )

    following: IdFieldOrNone = Field(
        default=None,
        examples=["https://actor.example/following"],
        description="The following collection of the actor",
    )

    summary: HtmlStringOrNone = Field(
        default=None,
        examples=["My Fediverse account"],
        description="Description of the actor",
    )

    name: HtmlStringOrNone = Field(
        default=None,
        examples=["Alice"],
        description="Display name of the actor",
    )

    url: UrlList = Field(
        default=[],
        description="A list of urls connected to the actor",
    )

    attachment: Annotated[list[ActorAttachment], BeforeValidator(transform_to_list)] = (
        Field(
            default=[],
            description="""attachments ... currently used for property values""",
        )
    )

    tag: Annotated[list[TagType], BeforeValidator(transform_to_list)] = Field(
        default=[],
        description="A list of objects that expand on the summary of the actor",
    )

    manually_approves_followers: bool | None = Field(
        default=None,
        alias="manuallyApprovesFollowers",
        description="If set to false, one can assume that te actor automatically replies to follow requests",
    )
