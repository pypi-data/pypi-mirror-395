from .clean import clean_schema


def test_clean_json_schema_one_element():
    schema = {
        "anyOf": [{"type": "string"}, {"type": "null"}],
        "default": None,
        "description": "A location related to the hashtag",
        "title": "Href",
    }

    result = clean_schema(schema)

    assert result == {
        "type": "string",
        "description": "A location related to the hashtag",
        "title": "Href",
    }


def test_clean_json_schema_properties():
    schema = {
        "type": {
            "const": "Hashtag",
            "default": "Hashtag",
            "title": "Type",
            "type": "string",
        },
        "href": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "default": None,
            "description": "A location related to the hashtag",
            "title": "Href",
        },
        "name": {
            "description": "The actual hashtag",
            "examples": ["#cow"],
            "title": "Name",
            "type": "string",
        },
    }

    result = clean_schema(schema)

    assert result == {
        "href": {
            "description": "A location related to the hashtag",
            "title": "Href",
            "type": "string",
        },
        "name": {
            "description": "The actual hashtag",
            "examples": ["#cow"],
            "title": "Name",
            "type": "string",
        },
        "type": {
            "const": "Hashtag",
            "default": "Hashtag",
            "title": "Type",
            "type": "string",
        },
    }


def test_clean_attachment():
    schema = {
        "anyOf": [
            {
                "items": {"additionalProperties": True, "type": "object"},
                "type": "array",
            },
            {"type": "null"},
        ],
        "default": None,
        "description": "A list of objects that are attached to the original object",
        "title": "",
    }

    result = clean_schema(schema)

    assert result == {
        "description": "A list of objects that are attached to the original object",
        "items": {"additionalProperties": True, "type": "object"},
        "type": "array",
    }
