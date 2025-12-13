from sqlalchemy import select
from cattle_grid.model.account import CreateActorRequest
from cattle_grid.app import app_globals
from cattle_grid.database.account import ActorForAccount

from .testing import *  # noqa


async def test_create_actor(sql_session, test_broker, account_for_test):
    request = CreateActorRequest(base_url="http://abel", preferred_username="username")  # type: ignore

    await test_broker.publish(
        request,
        routing_key=f"send.{account_for_test.name}.request.create_actor",
        exchange=app_globals.account_exchange,
    )
    result = [x for x in await sql_session.scalars(select(ActorForAccount))]

    assert len(result) == 1


async def test_create_actor_request(sql_session, test_broker, account_for_test):
    request = CreateActorRequest(base_url="http://abel", preferred_username="username")  # type: ignore

    response = await test_broker.request(
        request,
        routing_key=f"send.{account_for_test.name}.request.create_actor",
        exchange=app_globals.account_exchange,
        # reply_to="reply-to-here",
    )
    result = [x for x in await sql_session.scalars(select(ActorForAccount))]

    assert len(result) == 1

    assert response
