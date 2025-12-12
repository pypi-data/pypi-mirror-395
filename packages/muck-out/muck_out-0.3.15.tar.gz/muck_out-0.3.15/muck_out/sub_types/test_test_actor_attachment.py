from pydantic import BaseModel

from . import ActorAttachment, PropertyValue


class Helper(BaseModel):
    value: ActorAttachment


def test_unknown():
    result = Helper.model_validate({"value": {"type": "Other"}})

    assert isinstance(result.value, dict)


def test_property_value():
    property_value = {"type": "PropertyValue", "name": "key", "value": "value"}
    result = Helper.model_validate({"value": property_value})

    assert isinstance(result.value, PropertyValue)


def test_property_value_as_value():
    property_value = PropertyValue.model_validate(
        {"type": "PropertyValue", "name": "key", "value": "value"}
    )
    result = Helper.model_validate({"value": property_value})

    assert isinstance(result.value, PropertyValue)


def test_property_value_removes_html():
    property_value = {
        "type": "PropertyValue",
        "name": "Blog",
        "value": '<a href="http://value.example/" target="_blank" rel="nofollow noopener noreferrer me" translate="no"><span class="invisible">http://</span><span class="">value.example/</span><span class="invisible"></span></a>',
    }
    result = Helper.model_validate({"value": property_value})
    assert isinstance(result.value, PropertyValue)
    assert result.value.value == "http://value.example/"
