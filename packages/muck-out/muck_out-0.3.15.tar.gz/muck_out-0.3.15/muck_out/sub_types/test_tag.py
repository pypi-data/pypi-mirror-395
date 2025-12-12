from pydantic import BaseModel
import pytest

from .tag import Hashtag, Mention, TagType


class Helper(BaseModel):
    value: TagType


@pytest.mark.parametrize(
    "value,expected_type",
    [
        ({"type": "Unknown"}, dict),
        ({"type": "Hashtag", "name": "#cow"}, Hashtag),
        (Hashtag(name="#cow"), Hashtag),
        ({"type": "Mention", "href": "http://remote.test/actor"}, Mention),
        (Mention(href="http://remote.test/actor"), Mention),
    ],
)
def test_tag_type(value, expected_type):
    result = Helper.model_validate({"value": value})

    assert isinstance(result.value, expected_type)
