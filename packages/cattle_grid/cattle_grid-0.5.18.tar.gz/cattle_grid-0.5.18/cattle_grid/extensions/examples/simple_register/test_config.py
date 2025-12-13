from pydantic import ValidationError
import pytest

from cattle_grid.testing import mocked_config
from .config import RegistrationType


def test_registration_type_at_least_one_permission():
    with pytest.raises(ValidationError):
        RegistrationType(name="dev", permissions=[])


def test_permissions_and_create_actor_on():
    with mocked_config({"frontend": {"base_urls": ["http://domain.test"]}}):
        RegistrationType(
            name="test",
            permissions=["admin"],
            create_default_actor_on="http://domain.test",
        )

        with pytest.raises(Exception):
            RegistrationType(
                name="test",
                permissions=["admin"],
                create_default_actor_on="http://other.test",
            )
