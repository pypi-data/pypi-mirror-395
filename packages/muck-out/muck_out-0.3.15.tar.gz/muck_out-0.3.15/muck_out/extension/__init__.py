from cattle_grid.extensions import Extension
from cattle_grid.dependencies.transformer import ActorTransforming

from muck_out.extension.config import MuckOutConfiguration

from .. import normalize_data

extension = Extension(
    name="muck out", module=__name__, config_class=MuckOutConfiguration
)


@extension.transform(inputs=["raw"], outputs=["parsed"])
async def muck_out(data: dict, actor: ActorTransforming, config: extension.Config):  # type: ignore
    actor_id = actor.actor_id if actor else None

    normalized = normalize_data(
        data["raw"], actor_id=actor_id, drop_context=config.drop_context
    )

    return {"parsed": normalized.model_dump(by_alias=True, exclude_none=True)}
