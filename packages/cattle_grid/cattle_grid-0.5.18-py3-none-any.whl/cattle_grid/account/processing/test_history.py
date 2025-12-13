from unittest.mock import AsyncMock
from faststream.rabbit import RabbitBroker, TestRabbitBroker, RabbitQueue
import pytest
from sqlalchemy import select

from cattle_grid.app import app_globals
from cattle_grid.database.account import EventHistory
from cattle_grid.model.account import EventInformation, EventType
from cattle_grid.testing.fixtures import *  # noqa

from .history import create_account_history_router


@pytest.fixture
async def mock_combined():
    return AsyncMock()


@pytest.fixture
async def broker_with_history(mock_combined):
    broker = RabbitBroker()

    broker.include_router(create_account_history_router())
    broker.subscriber(
        RabbitQueue("test_combined", routing_key="combined.*"),
        exchange=app_globals.account_exchange,
    )(mock_combined)

    async with TestRabbitBroker(broker) as tbr:
        yield tbr


@pytest.mark.parametrize("event_type", [EventType.incoming, EventType.outgoing])
async def test_incoming_event(
    event_type,
    broker_with_history,
    account_for_test,
    actor_with_account,
    sql_session,
    mock_combined,
):
    routing_key = f"receive.{account_for_test.name}.{event_type}.ACTIVITY"

    await broker_with_history.publish(
        EventInformation(
            event_type=event_type, actor=actor_with_account.actor_id, data={}
        ),
        exchange=app_globals.account_exchange,
        routing_key=routing_key,
    )

    result = await sql_session.scalar(select(EventHistory))

    assert result

    mock_combined.assert_awaited_once()
