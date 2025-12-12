import logging
from typing import Any

from muck_out.transform.utils import sanitize_html
from muck_out.types import ObjectStub, Object

logger = logging.getLogger(__name__)


def update_for_media_type(data: dict[str, Any]) -> dict[str, Any]:
    try:
        media_type = data.get("mediaType")
        if media_type and media_type.startswith("text/markdown"):
            content = data.get("content")
            if content:
                import markdown

                copy = {**data}
                copy["content"] = markdown.markdown(content)
                return copy
    except ImportError:
        logger.warning(
            "Received markdown content; but markdown extension is not installed; Treating as html"
        )
    except Exception as e:
        logger.info(e)
    return data


def object_stub(data: dict[str, Any]) -> ObjectStub:
    """Constructs a stub from data

    This function is not a direct equivalent to ObjectStub.model_validate
    as functionality happens that is not field to field for

    - `content` filled from `contentMap`

    """

    data = update_for_media_type(data)

    stub = ObjectStub.model_validate(data)

    if stub.content is None:
        content_map = data.get("contentMap")
        if isinstance(content_map, dict):
            values = content_map.values()
            if len(values) > 0:
                stub.content = sanitize_html(list(content_map.values())[0])

    return stub


def normalize_object(obj: dict[str, Any]) -> Object:
    """Normalizes an object

    :params obj: The object to be normalized
    :returns:
    """

    stub = object_stub(obj)
    data = stub.model_dump(by_alias=True)
    if "content" in data:
        data["contentPlain"] = data["content"]
    result = Object.model_validate(data)

    if not any([result.content, result.summary, result.name]):
        raise ValueError(
            "At least one of the properties content, summary, or name should be set"
        )

    return result
