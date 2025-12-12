import pytest

from muck_out.sub_types import ObjectLink
from .object import object_stub


e232_example1 = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Note",
    "content": "The bug was reported in #1374",
    "tag": [
        {
            "type": "Link",
            "mediaType": 'application/ld+json; profile="https://www.w3.org/ns/activitystreams"',
            "href": "https://forge.example/tickets/1374",
            "name": "#1374",
        }
    ],
}

e232_example2 = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Note",
    "content": "This is a quote:<br>RE: https://server.example/objects/123",
    "tag": [
        {
            "type": "Link",
            "mediaType": 'application/ld+json; profile="https://www.w3.org/ns/activitystreams"',
            "href": "https://server.example/objects/123",
            "name": "RE: https://server.example/objects/123",
        }
    ],
}


@pytest.mark.parametrize("example", [e232_example1, e232_example2])
def test_normalize_object(example):
    result = object_stub(example)

    assert len(result.tag) == 1
    tag = result.tag[0]

    assert isinstance(tag, ObjectLink)
