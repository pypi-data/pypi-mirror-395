from pydantic import BeforeValidator
from typing import Annotated, Any

from muck_out.transform.utils import remove_html
from muck_out.transform import transform_to_list_of_uris, transform_url

from .methods import safe_html, safe_id_for_object, single_element_list_to_element


HtmlStringOrNone = Annotated[str | None, BeforeValidator(safe_html)]
"""Used for strings, which may contain html"""

IdFieldOrNone = Annotated[str | None, BeforeValidator(safe_id_for_object)]
"""Used for fields meant to contain an id"""


UrlList = Annotated[list[dict[str, Any]], BeforeValidator(transform_url)]
"""Transforms a list of urls"""

TransformToListOfUris = Annotated[list[str], BeforeValidator(transform_to_list_of_uris)]
"""Transforms a list of recipients, ensuring it is a list of URIs"""

PlainText = Annotated[str, BeforeValidator(remove_html)]
"""Ensures a field is plain text, i.e. not containing any html"""

IdOrNone = Annotated[str | None, BeforeValidator(single_element_list_to_element)]
"""Type that ensures a single element list is rendered as an element"""
