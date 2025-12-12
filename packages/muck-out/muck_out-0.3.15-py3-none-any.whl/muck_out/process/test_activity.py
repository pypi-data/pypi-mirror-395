import pytest
from muck_out.testing import load_asset
from .activity import activity_stub, normalize_activity


def test_mastodon_like():
    mastodon_like = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "https://mastodon.social/users/the_milkman#likes/251507741",
        "type": "Like",
        "actor": "https://mastodon.social/users/the_milkman",
        "object": "https://dev.bovine.social/html_display/object/01999580-e682-799a-8a43-ae9f5742d148",
    }

    actor_id = "http://local.test/actor/id"

    result = activity_stub(mastodon_like, actor_id=actor_id)

    assert result.to == [actor_id]


@pytest.mark.parametrize(
    "name", ["fep_c0e0_emoji_react", "fep_c0e0_custom_emoji_react"]
)
def test_emoji_reaction(name):
    """Example from [FEP-c0e0: Emoji reactions](https://fediverse.codeberg.page/fep/fep/c0e0/)"""
    emoji_react = load_asset(name)

    result = activity_stub(emoji_react)

    assert result.type == "Like"


def test_internal_cattle_grid_test():
    activity = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Accept",
        "actor": "http://cattle_grid/actor/Twle_a-3qNL7cHZra5c8Kg",
        "to": ["http://cattle_grid/actor/484KcCWjPNCVl0BQFenJiQ"],
        "published": "2025-11-16T14:56:13Z",
        "object": "follow:cf8684cc-5738-4862-b84f-80e44721572b",
        "id": "http://cattle_grid/object/019a8d2a-a69c-7a9a-addd-82f0d34d5a6a",
    }

    result = normalize_activity(activity)

    assert result
    assert result.type == "Accept"
