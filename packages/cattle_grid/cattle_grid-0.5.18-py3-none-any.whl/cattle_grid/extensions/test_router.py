from unittest.mock import AsyncMock
import pytest

from . import Extension
from cattle_grid.extensions.testing import with_test_broker_for_extension
from cattle_grid.app import app_globals


@pytest.fixture
def subscriber_one():
    return AsyncMock()


@pytest.fixture
def subscriber_two():
    return AsyncMock()


@pytest.fixture
async def test_broker(subscriber_one, subscriber_two):
    extension = Extension("name", __name__)

    extension.subscribe("topic")(subscriber_one)
    extension.subscribe("topic")(subscriber_two)

    async with with_test_broker_for_extension([extension], {}) as tbr:
        yield tbr


async def test_two_subscriptions(subscriber_one, subscriber_two, test_broker):
    await test_broker.publish(
        {"key": "val"}, routing_key="topic", exchange=app_globals.activity_exchange
    )

    subscriber_one.assert_awaited_once()
    subscriber_two.assert_awaited_once()
