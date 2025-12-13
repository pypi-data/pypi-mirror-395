import logging
from unittest.mock import AsyncMock, MagicMock
from faststream.rabbit import (
    RabbitBroker,
    TestRabbitBroker,
    RabbitExchange,
    ExchangeType,
    RabbitQueue,
)
import pytest

from .account import RoutingKey

from .processing import AccountPublisher, AccountRequester

logger = logging.getLogger(__name__)


@pytest.fixture
async def test_exchange():
    return RabbitExchange("test.exchange", type=ExchangeType.TOPIC, durable=True)


@pytest.fixture
async def mock_subscriber():
    return AsyncMock()


async def publisher_subscriber(publisher: AccountPublisher):
    await publisher("test.publisher", {"test": "data"})


async def requester_subscriber(requester: AccountRequester):
    await requester("test.requester", {"test": "data"})


@pytest.fixture
async def test_broker(test_exchange, mock_subscriber):
    broker = RabbitBroker()

    broker.subscriber(
        RabbitQueue("test", routing_key="send.*.publisher"), exchange=test_exchange
    )(publisher_subscriber)

    broker.subscriber(
        RabbitQueue("test", routing_key="send.*.requester"), exchange=test_exchange
    )(requester_subscriber)

    @broker.subscriber(
        RabbitQueue("test2", routing_key="send.alice.test.*"), exchange=test_exchange
    )
    async def test_subscriber(routing_key: RoutingKey):
        return await mock_subscriber(routing_key)

    async with TestRabbitBroker(broker) as tbr:
        yield tbr


async def test_publisher(test_broker, test_exchange, mock_subscriber):
    await test_broker.publish(
        {"key": "value"}, exchange=test_exchange, routing_key="send.alice.publisher"
    )
    mock_subscriber.assert_awaited_once_with("send.alice.test.publisher")


async def test_requester(test_broker, test_exchange, mock_subscriber):
    mock_subscriber.return_value = MagicMock(body=b'"{}"')

    await test_broker.publish(
        {"key": "value"}, exchange=test_exchange, routing_key="send.alice.requester"
    )
    mock_subscriber.assert_awaited_once_with("send.alice.test.requester")
