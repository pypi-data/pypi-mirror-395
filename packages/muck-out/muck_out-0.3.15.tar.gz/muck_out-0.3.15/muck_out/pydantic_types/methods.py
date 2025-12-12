from bovine.activitystreams.utils import id_for_object
from muck_out.transform.utils import sanitize_html


def safe_html(x) -> str | None:
    if x is None:
        return None
    if isinstance(x, list):
        if len(x) == 0:
            return None
        x = x[0]
    return sanitize_html(x)


def safe_id_for_object(x):
    if isinstance(x, list):
        if len(x) == 0:
            return None
        x = x[0]
    return id_for_object(x)


def single_element_list_to_element(x: str | None | list[str]) -> str | None:
    """Returns a sanitized version of the result:

    ```python
    >>> single_element_list_to_element(None)

    >>> single_element_list_to_element("Note")
    'Note'

    >>> single_element_list_to_element([])

    >>> single_element_list_to_element(["Note"])
    'Note'

    >>> single_element_list_to_element(["Note", "Article"])
    Traceback (most recent call last):
    ...
    ValueError: Cannot handle lists of more than 1 element

    """

    if isinstance(x, list):
        if len(x) > 1:
            raise ValueError("Cannot handle lists of more than 1 element")
        if len(x) == 1:
            return x[0]
        return None
    return x
