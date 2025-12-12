from . import normalize_data
from .testing import load_asset


def test_actor_update():
    actor_update = load_asset("mastodon_actor_update")

    result = normalize_data(actor_update)

    assert result.activity

    assert result.embedded_actor
