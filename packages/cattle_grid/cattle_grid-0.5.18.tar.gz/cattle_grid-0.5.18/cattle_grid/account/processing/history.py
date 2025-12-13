"""Handles creating the history for the actor"""

from faststream.rabbit import RabbitRouter, RabbitQueue
from uuid6 import uuid7

from cattle_grid.account.processing.annotations import AccountFromRoutingKey
from cattle_grid.app import app_globals
from cattle_grid.database.account import EventHistory
from cattle_grid.dependencies import AccountExchangePublisher, CommittingSession
from cattle_grid.model.account import EventInformation, EventType


async def history_for_incoming_outgoing(
    message: EventInformation,
    account: AccountFromRoutingKey,
    session: CommittingSession,
    publisher: AccountExchangePublisher,
):
    if message.history_id:
        raise Exception("Event already has history id")
    if message.event_type not in [EventType.incoming, EventType.outgoing]:
        raise Exception("You shouldn't be here")

    history_id = uuid7()

    for_db = EventHistory(
        id=history_id,
        account=account,
        event_type=message.event_type,
        data=message.data,
        actor=message.actor,
    )

    session.add(for_db)

    message.history_id = history_id

    await publisher(message, routing_key=f"combined.{account.name}")


def create_account_history_router():
    account_history_router = RabbitRouter()

    for event_type in ["incoming", "outgoing"]:
        queue = RabbitQueue(
            f"account_history_{event_type}",
            routing_key=f"receive.*.{event_type}.*",
            durable=True,
        )

        account_history_router.subscriber(
            queue,
            exchange=app_globals.account_exchange,
        )(history_for_incoming_outgoing)

    return account_history_router
