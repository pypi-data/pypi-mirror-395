import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from cattle_grid.testing.fixtures import *  # noqa
from cattle_grid.activity_pub import create_actor
from cattle_grid.database.account import Account

from . import extension


@pytest.fixture(autouse=True)
def configure_extension():
    extension.configure(
        {
            "registration_types": [
                {
                    "name": "abel",
                    "permissions": ["admin"],
                    "extra_parameters": ["fediverse"],
                    "create_default_actor_on": "http://abel",
                }
            ]
        }
    )


@pytest.fixture
def test_client():
    app = FastAPI()
    app.include_router(extension.api_router)

    return TestClient(app)


async def test_register_actor_already_exists(test_client, sql_session):
    await create_actor(sql_session, "http://abel", preferred_username="alice")

    response = test_client.post(
        "/register/abel",
        json={
            "password": "secret",
            "name": "alice",
            "fediverse": "acct:alice@host.test",
        },
    )

    assert response.status_code == 409


async def test_register(test_client, sql_session):
    response = test_client.post(
        "/register/abel",
        json={
            "password": "secret",
            "name": "alice",
            "fediverse": "acct:alice@host.test",
        },
    )

    assert response.status_code == 201

    account = await sql_session.scalar(
        select(Account)
        .where(Account.name == "alice")
        .options(joinedload(Account.actors))
    )
    assert account

    assert len(account.actors) == 1

    actor = account.actors[0]

    assert actor.name == "default"
