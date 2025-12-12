from pathlib import Path
import click


from .types import Actor, Activity, Object, Collection
from .derived import ActorHeaderInfo, ObjectMetaInfo
from .sub_types import Hashtag, Mention, PropertyValue
from .schemas import to_json_schema


@click.group
def main(): ...


@main.command()
@click.option("--path", default="docs/schemas/")
def schemas(path: str):
    Path(path).mkdir(exist_ok=True, parents=True)
    for obj, name in [
        (Actor, "actor"),
        (Activity, "activity"),
        (Object, "object"),
        (Collection, "collection"),
        (ActorHeaderInfo, "actor-header-info"),
        (ObjectMetaInfo, "object-meta-info"),
        (Hashtag, "hashtag"),
        (Mention, "mention"),
        (PropertyValue, "property-value"),
    ]:
        to_json_schema(obj, f"{path}/{name}.json")  # type: ignore


if __name__ == "__main__":
    main()
