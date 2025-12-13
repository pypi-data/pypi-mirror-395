import pytest

from cattle_grid.model.exchange_update_actor import (
    UpdateActionType,
    UpdatePropertyValueAction,
)
from .property_value import (
    InvalidPropertyValueException,
    find_key_in_attachments,
    handle_update_property_value,
)

from cattle_grid.testing.fixtures import *  # noqa


@pytest.mark.parametrize(
    "attachments, expected",
    [
        ([], None),
        (["string"], None),
        ([{"name": "string"}], None),
        ([{"name": "key"}], None),
        ([{"type": "PropertyValue", "name": "key"}], 0),
        ([{"type": "PropertyValue", "name": "other"}], None),
    ],
)
def test_find_key_in_attachments(attachments, expected):
    assert find_key_in_attachments(attachments, "key") == expected


def test_handle_update_property_value(actor_for_test):
    handle_update_property_value(
        actor_for_test,
        UpdatePropertyValueAction(
            action=UpdateActionType.update_property_value, key="key", value="value"
        ),
    )

    attachments = actor_for_test.profile.get("attachment")
    assert len(attachments) == 1


def test_handle_update_property_value_no_value(actor_for_test):
    with pytest.raises(InvalidPropertyValueException):
        handle_update_property_value(
            actor_for_test,
            UpdatePropertyValueAction(
                action=UpdateActionType.update_property_value, key="key", value=None
            ),
        )
