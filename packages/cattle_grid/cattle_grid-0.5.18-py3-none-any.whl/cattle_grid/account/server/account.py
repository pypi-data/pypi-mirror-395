import logging
from uuid import UUID


from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select

from cattle_grid.dependencies.fastapi import (
    CommittingSession,
    MethodInformation,
    SqlSession,
)
from cattle_grid.activity_pub import (
    create_actor,
    actor_to_object,
    DuplicateIdentifierException,
)
from cattle_grid.model.account import EventInformation, InformationResponse, EventType

from cattle_grid.database.account import ActorForAccount, EventHistory
from cattle_grid.account.processing.info import create_information_response

from cattle_grid.tools import ServerSentEventFromQueueAndTask
from cattle_grid.tools.fastapi import EventStreamResponse

from .responses import CreateActorRequest, EventHistoryResponse
from .dependencies import CurrentAccount
from .streaming import get_message_streamer

logger = logging.getLogger(__name__)

account_router = APIRouter(prefix="/account", tags=["account"])


@account_router.get(
    "/stream/{event_type}",
    response_description="EventSource",
    operation_id="stream",
    response_class=EventStreamResponse,
)
async def stream(
    event_type: EventType,
    account: CurrentAccount,
    request: Request,
    stream_messages=Depends(get_message_streamer),
):
    """EventSource corresponding to all messages received
    by the account.

    This method returns an
    [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)
    providing server sent events."""
    queue, task = stream_messages(account.name, event_type)

    return ServerSentEventFromQueueAndTask(request, queue, task)


@account_router.post(
    "/create",
    status_code=201,
    operation_id="create_actor",
    responses={409: {"description": "Duplicate identifier"}},
)
async def create_actor_method(
    body: CreateActorRequest, account: CurrentAccount, session: CommittingSession
):
    """Allows one to create a new actor. The allowed values for base_url
    can be retrieved using the info endpoint."""
    try:
        actor = await create_actor(
            session, body.base_url, preferred_username=body.handle
        )
    except DuplicateIdentifierException:
        raise HTTPException(409, "Duplicate identifier")

    name = body.name or "from_api"

    session.add(ActorForAccount(account=account, actor=actor.actor_id, name=name))

    return actor_to_object(actor)


@account_router.get("/info", operation_id="account_info")
async def return_account_information(
    account: CurrentAccount, method_information: MethodInformation, session: SqlSession
) -> InformationResponse:
    """Returns information about the server and the account."""

    if not isinstance(method_information, list):
        logger.warning("Method information is not a list")
        method_information = []

    return await create_information_response(session, account, method_information)


@account_router.get("/history", operation_id="event_history")
async def event_history(
    account: CurrentAccount, start_from: str, session: SqlSession
) -> EventHistoryResponse:
    """Not implemented yet"""

    uuid = UUID(start_from)

    response = await session.scalars(
        select(EventHistory)
        .where(EventHistory.account == account)
        .where(EventHistory.id > uuid)
    )

    events = [
        EventInformation(data=x.data, event_type=x.event_type, actor=x.actor)
        for x in response
    ]

    return EventHistoryResponse(events=events)
