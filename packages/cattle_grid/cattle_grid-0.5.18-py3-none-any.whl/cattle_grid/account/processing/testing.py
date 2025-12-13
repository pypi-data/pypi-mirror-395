import pytest

from unittest.mock import AsyncMock

from faststream.rabbit import RabbitBroker, TestRabbitBroker, RabbitQueue

from cattle_grid.activity_pub.actor import create_actor
from cattle_grid.app import app_globals
from cattle_grid.testing.fixtures import *  # noqa

from .router import create_router
from cattle_grid.database.account import Account, ActorForAccount


@pytest.fixture
async def subscriber_mock():
    return AsyncMock(return_value=None)


@pytest.fixture
async def receive_subscriber_mock():
    return AsyncMock(return_value=None)


@pytest.fixture
async def test_account(sql_session):
    account = Account(name="alice", password_hash="password")
    sql_session.add(account)
    await sql_session.commit()
    return account


@pytest.fixture
async def test_actor(sql_session, test_account):
    actor = await create_actor(
        sql_session, "http://localhost/", preferred_username="alice"
    )
    sql_session.add(ActorForAccount(actor=actor.actor_id, account=test_account))
    await sql_session.commit()
    return actor


@pytest.fixture
async def test_broker(subscriber_mock, receive_subscriber_mock):
    br = RabbitBroker("amqp://guest:guest@localhost:5672/")
    br.include_router(create_router())

    async def mock(msg):
        await subscriber_mock(msg)

        return {"type": "Person", "data": "blank"}

    br.subscriber("send_message", exchange=app_globals.activity_exchange)(mock)
    br.subscriber("fetch_object", exchange=app_globals.internal_exchange)(mock)

    @br.subscriber(
        RabbitQueue("queue2", routing_key="receive.*.response.*"),
        exchange=app_globals.account_exchange,
    )
    async def receive_mock(msg):
        await receive_subscriber_mock(msg)

    br.subscriber(
        RabbitQueue("queue4", routing_key="reply-to-here"),
        exchange=app_globals.account_exchange,
    )(AsyncMock())

    async with TestRabbitBroker(br, with_real=False) as tbr:
        yield tbr
