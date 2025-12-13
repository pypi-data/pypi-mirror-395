import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import select

from cattle_grid.testing.fixtures import *  # noqa
from cattle_grid.database.account import Account

from . import extension


@pytest.fixture(autouse=True)
def configure_extension():
    extension.configure(
        {
            "registration_types": [
                {
                    "name": "test_name",
                    "permissions": ["permission_one", "permission_two"],
                    "extra_parameters": ["fediverse"],
                }
            ]
        }
    )


@pytest.fixture
def test_client():
    app = FastAPI()
    app.include_router(extension.api_router)

    return TestClient(app)


async def test_register_with_form_data(test_client, sql_session):
    response = test_client.post(
        "/register/test_name",
        data={
            "password": "secret",
            "name": "alice",
            "fediverse": "acct:alice@host.test",
        },
    )

    assert response.status_code == 201

    account = await sql_session.scalar(select(Account).where(Account.name == "alice"))
    assert account

    assert account.meta_information == {
        "fediverse": "acct:alice@host.test",
    }
    await sql_session.refresh(account, attribute_names=["permissions"])
    assert len(account.permissions) == 2
