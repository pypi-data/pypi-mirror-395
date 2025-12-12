import logging
from typing import Any
from urllib.parse import urlparse

from muck_out.types import ActorStub, Actor

logger = logging.getLogger(__name__)


def calculate_identifiers(stub: ActorStub) -> list[str]:
    if not stub.id:
        return []
    try:
        domain = urlparse(stub.id).netloc

        if stub.preferred_username:
            return [f"acct:{stub.preferred_username}@{domain}", stub.id]

        return [stub.id]
    except Exception:
        return []


def actor_stub(data: dict[str, Any]) -> ActorStub:
    """Returns the stub actor"""

    icon = data.get("icon")
    if isinstance(icon, list):
        if len(icon) > 0:
            data["icon"] = icon[0]
        else:
            data["icon"] = None

    stub = ActorStub.model_validate(data)

    if data.get("identifiers") is None:
        stub.identifiers = calculate_identifiers(stub)

    return stub


def normalize_actor(data: dict[str, Any]) -> Actor | None:
    """Normalizes an ActivityPub actor"""
    stub = actor_stub(data)

    if stub.inbox is None:
        return None

    if stub.identifiers is None or len(stub.identifiers) == 0:
        if stub.id is None:
            return
        stub.identifiers = [stub.id]

    return Actor.model_validate(stub.model_dump(by_alias=True))
