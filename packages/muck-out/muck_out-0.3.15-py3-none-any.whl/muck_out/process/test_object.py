import pytest

from muck_out.types import ObjectStub, Object
from muck_out.testing import load_asset
from . import object_stub, normalize_object


@pytest.mark.parametrize(
    "data", [{"content": "text"}, {"content": ["text"]}, {"contentMap": {"en": "text"}}]
)
def test_processes_content(data):
    result = object_stub(data)
    assert result.content == "text"


def test_object():
    obj = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "https://comments.bovine.social/pages/aHR0cHM6Ly9ib3ZpbmUuY29kZWJlcmcucGFnZS9jb21tZW50cy8=",
        "type": "Page",
        "to": ["https://www.w3.org/ns/activitystreams#Public"],
        "cc": [],
        "attributedTo": "https://comments.bovine.social/actor/rF4xnx1QraAIU3Krg-2Qzg",
        "name": "Comment Tracking System",
        "summary": None,
        "url": [
            {
                "type": "Link",
                "mediaType": "text/html",
                "href": "https://bovine.codeberg.page/comments/",
            }
        ],
        "context": "https://comments.bovine.social/pages/aHR0cHM6Ly9ib3ZpbmUuY29kZWJlcmcucGFnZS9jb21tZW50cy8=/context",
        "replies": "https://comments.bovine.social/pages/aHR0cHM6Ly9ib3ZpbmUuY29kZWJlcmcucGFnZS9jb21tZW50cy8=/replies",
        "likes": "https://comments.bovine.social/pages/aHR0cHM6Ly9ib3ZpbmUuY29kZWJlcmcucGFnZS9jb21tZW50cy8=/likes",
        "shares": "https://comments.bovine.social/pages/aHR0cHM6Ly9ib3ZpbmUuY29kZWJlcmcucGFnZS9jb21tZW50cy8=/shares",
    }

    stub = object_stub(obj)

    assert isinstance(stub, ObjectStub)

    normalized = normalize_object(obj)

    assert isinstance(normalized, Object)


def test_peertube():
    obj = load_asset("peertube_video")
    old_content = obj.get("content")

    normalize_object(obj)

    assert obj["content"] == old_content


def test_tag_transformation():
    object_stub({"tag": {"type": "Hashtag", "name": "#cow"}})


def test_content_plain():
    obj = {
        "id": "https://domain.test/users/34783",
        "type": "Note",
        "published": "2025-11-11T00:00:00Z",
        "url": "https://domain.test/actor/123",
        "attributedTo": "https://domain.test/actor",
        "to": ["https://www.w3.org/ns/activitystreams#Public"],
        "content": "<p><b>bold</b></p>",
    }

    result = normalize_object(obj)

    assert result.content == obj.get("content")
    assert result.content_plain == "bold"


def test_atlas_object():
    obj = load_asset("atlas_note")

    result = normalize_object(obj)

    assert result.type == "Note"
