import json
from pydantic import BaseModel
from .clean import clean_schema


def to_json_schema(model: BaseModel, filename: str):
    schema = model.model_json_schema()
    schema = clean_schema(schema)
    with open(filename, "w") as f:
        json.dump(schema, f, indent=2)
