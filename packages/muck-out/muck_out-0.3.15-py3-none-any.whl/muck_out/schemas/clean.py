def clean_definition(schema: dict) -> dict:
    if schema.get("default") is not None:
        return schema

    any_of = schema.get("anyOf", [])

    if len(any_of) != 2:
        return schema

    if any_of[0].get("type") == "null":
        any_other = any_of[1]
    elif any_of[1].get("type") == "null":
        any_other = any_of[0]
    else:
        return schema

    del schema["anyOf"]
    del schema["default"]

    schema = {**schema, **any_other}

    return schema


def clean_schema(schema: dict) -> dict:
    new_schema = {}

    for key, value in schema.items():
        if isinstance(value, dict):
            new_schema[key] = clean_schema(value)
        else:
            if key == "title" and value == "":
                ...
            else:
                new_schema[key] = value

    new_schema = clean_definition(new_schema)

    return new_schema
