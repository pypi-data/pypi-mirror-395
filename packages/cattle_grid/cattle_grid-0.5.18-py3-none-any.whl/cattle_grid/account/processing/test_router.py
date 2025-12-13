import pytest

from cattle_grid.activity_pub.actor import create_actor
from cattle_grid.app import app_globals

from cattle_grid.database.account import Account, ActorForAccount
from cattle_grid.model.extension import MethodInformationModel
from cattle_grid.dependencies.globals import global_container


from .testing import *  # noqa


async def test_fetch_nothing_happens(test_broker, subscriber_mock):
    with pytest.raises(Exception):
        await test_broker.publish(
            {"uri": "http://remote/ap/actor/bob"},
            routing_key="send.alice.request.fetch",
            exchange=app_globals.account_exchange,
        )

    subscriber_mock.assert_not_called()


async def test_fetch_requires_actor(sql_session, test_broker, subscriber_mock):
    account = Account(name="alice", password_hash="password")
    actor = await create_actor(
        sql_session, "http://localhost/", preferred_username="alice"
    )
    sql_session.add_all(
        [account, ActorForAccount(actor=actor.actor_id, account=account)]
    )
    await sql_session.commit()

    fetch_uri = "http://remote/ap/actor/bob"

    with pytest.raises(Exception):
        await test_broker.publish(
            {
                "uri": fetch_uri,
                "actor": "http://localhost/other",
            },
            routing_key="send.alice.request.fetch",
            exchange=app_globals.account_exchange,
        )

    subscriber_mock.assert_not_called()


async def test_fetch(test_broker, subscriber_mock, test_actor):
    fetch_uri = "http://remote/ap/actor/bob"

    await test_broker.publish(
        {"uri": fetch_uri, "actor": test_actor.actor_id},
        routing_key="send.alice.request.fetch",
        exchange=app_globals.account_exchange,
    )

    subscriber_mock.assert_called_once()
    args = subscriber_mock.call_args[0][0]

    assert args["uri"] == fetch_uri
    assert args["actor"] == test_actor.actor_id


async def test_getting_info(test_broker, receive_subscriber_mock, test_actor):
    global_container.method_information = [
        MethodInformationModel(routing_key="test", module="test")
    ]

    await test_broker.publish(
        {"action": "info", "data": {}, "actor": ""},
        routing_key="send.alice.request.info",
        exchange=app_globals.account_exchange,
    )

    receive_subscriber_mock.assert_called_once()
    args = receive_subscriber_mock.call_args[0][0]

    assert args["actors"] == [{"id": test_actor.actor_id, "name": "NO NAME"}]

    assert len(args["methodInformation"]) > 0
