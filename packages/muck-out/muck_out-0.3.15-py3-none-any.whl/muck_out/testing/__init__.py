import json
from typing import Any


def load_asset(name: str) -> dict[str, Any]:
    """
    Loads a test asset.

    ```python
    >>> result = load_asset("mastodon_actor_update")
    >>> result["type"]
    'Update'

    ```
    """
    with open(f"docs/assets/{name}.json") as fp:
        return json.load(fp)
