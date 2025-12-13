import pytest

from unittest.mock import AsyncMock

from faststream.rabbit import RabbitBroker, TestRabbitBroker, RabbitQueue

from cattle_grid.app import app_globals
from cattle_grid.testing.fixtures import *  # noqa

from .router import create_router
from cattle_grid.database.account import Account


@pytest.fixture
async def subscriber_mock():
    return AsyncMock(return_value=None)


@pytest.fixture
async def test_account():
    return await Account.create(name="alice", password_hash="password")


@pytest.fixture
async def test_broker(subscriber_mock):
    br = RabbitBroker("amqp://guest:guest@localhost:5672/")
    br.include_router(create_router())

    br.subscriber(
        RabbitQueue("error-queue", routing_key="error.#"),
        exchange=app_globals.account_exchange,
    )(subscriber_mock)

    async with TestRabbitBroker(br) as tbr:
        yield tbr


async def test_exception(test_broker, subscriber_mock, actor_with_account):
    await test_broker.publish(
        {},
        routing_key="send.alice.request.fetch",
        exchange=app_globals.account_exchange,
    )

    subscriber_mock.assert_awaited_once()
