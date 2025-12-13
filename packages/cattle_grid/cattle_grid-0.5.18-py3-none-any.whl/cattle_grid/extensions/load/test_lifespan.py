from unittest.mock import AsyncMock, MagicMock
from contextlib import asynccontextmanager
from faststream.rabbit import RabbitBroker

import pytest

from cattle_grid.dependencies.globals import global_container
from cattle_grid.extensions import Extension

from .lifespan import iterate_lifespans, lifespan_for_extension


def call_from_context(func):
    @asynccontextmanager
    async def context():
        func()
        yield

    return context


async def test_iterate_lifespans_empty_list():
    async with iterate_lifespans([]):
        pass


async def test_iterate_lifespans_one_item():
    one = MagicMock()
    async with iterate_lifespans([call_from_context(one)]):  # type: ignore
        pass

    one.assert_called_once()


async def test_iterate_lifespans_three_items():
    mocks = [MagicMock(), MagicMock(), MagicMock()]

    async with iterate_lifespans([call_from_context(x) for x in mocks]):  # type: ignore
        pass

    for mock in mocks:
        mock.assert_called_once()


@pytest.mark.parametrize("broker", [True, False])
async def test_lifespan_for_extension(broker):
    extension = Extension("name", __name__)
    lifespan = lifespan_for_extension(extension, include_broker=broker)
    async with lifespan(AsyncMock()):
        ...


async def test_lifespan_for_extension_with_broker():
    mock_broker = AsyncMock(RabbitBroker)
    extension = Extension("name", __name__)
    extension.subscribe("mock-topic")(AsyncMock())

    old_broker = global_container.broker
    global_container.broker = mock_broker

    lifespan = lifespan_for_extension(extension, include_broker=True)

    async with lifespan(AsyncMock()):
        mock_broker.start.assert_awaited_once()
        mock_broker.publish.assert_awaited_once()

    mock_broker.stop.assert_awaited_once()

    global_container.broker = old_broker


async def test_lifespan_for_extension_with_broker_no_method_information():
    mock_broker = AsyncMock(RabbitBroker)
    extension = Extension("name", __name__)
    extension.subscribe("incoming.AnimalSound")(AsyncMock())

    old_broker = global_container.broker
    global_container.broker = mock_broker

    lifespan = lifespan_for_extension(extension, include_broker=True)

    async with lifespan(AsyncMock()):
        mock_broker.start.assert_awaited_once()
        mock_broker.publish.assert_not_awaited()

    mock_broker.stop.assert_awaited_once()

    global_container.broker = old_broker
