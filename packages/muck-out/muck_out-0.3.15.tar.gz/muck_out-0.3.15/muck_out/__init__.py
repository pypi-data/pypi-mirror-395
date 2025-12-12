"""
This package contains tools to turn ActivityPub messages
into something cleaner. Its takes include

- Normalization
- Validation


"""

import logging

from pydantic import BaseModel, Field

from .types import Activity, Object, Actor, Collection

from .process import (
    normalize_activity,
    normalize_object,
    normalize_collection,
    normalize_actor,
)


logger = logging.getLogger(__name__)


class NormalizationResult(BaseModel):
    object: Object | None = Field(default=None)
    activity: Activity | None = Field(default=None)

    actor: Actor | None = Field(default=None)
    collection: Collection | None = Field(default=None)

    embedded_object: Object | None = Field(default=None)
    embedded_actor: Actor | None = Field(default=None)


def normalize_data(
    data: dict, actor_id: str | None = None, drop_context: bool = False
) -> NormalizationResult:
    """Normalizes the object"""

    def result_or_none(func):
        try:
            result = func(data)
            if drop_context:
                result.field_context = None
            return result
        except Exception as e:
            logger.debug(e)

            return None

    try:
        activity = normalize_activity(data, actor_id=actor_id)
        if drop_context:
            activity.field_context = None
    except Exception as e:
        logger.debug(e)
        activity = None

    if activity and isinstance(activity.object, Object):
        embedded_object = activity.object
        activity.object = embedded_object.id
        if drop_context:
            embedded_object.field_context = None
    else:
        embedded_object = None

    embedded_actor = None

    if activity and activity.type == "Update":
        if activity.actor == activity.object:
            try:
                embedded_actor = normalize_actor(data.get("object"))  # type: ignore
                if drop_context and embedded_actor:
                    embedded_actor.field_context = None

            except Exception:
                ...

    return NormalizationResult(
        object=result_or_none(normalize_object),
        activity=activity,
        embedded_object=embedded_object,
        actor=result_or_none(normalize_actor),
        collection=result_or_none(normalize_collection),
        embedded_actor=embedded_actor,
    )
