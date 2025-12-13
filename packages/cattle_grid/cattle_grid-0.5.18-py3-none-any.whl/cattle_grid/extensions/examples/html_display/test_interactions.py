from bovine.activitystreams import factories_for_actor_object
from muck_out import normalize_data
import pytest

from typing import Any

from cattle_grid.app import app_globals
from cattle_grid.model import ActivityMessage


from .testing import *  # noqa


@pytest.mark.parametrize("interaction", ["likes", "shares", "replies"])
def test_interaction_collections(test_client, published_object, interaction):
    object_id = published_object["id"]
    response = test_client.get(
        object_id,
        headers={
            "x-ap-location": object_id,
            "x-cattle-grid-requester": "http://remote.test/actor",
        },
    )

    assert response.status_code == 200
    data = response.json()
    interaction_collection = data[interaction]

    response = test_client.get(
        interaction_collection,
        headers={
            "x-ap-location": interaction_collection,
            "x-cattle-grid-requester": "http://remote.test/actor",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == interaction_collection
    assert data["type"] == "OrderedCollection"


async def interact(remote_actor, test_broker, interaction: str, obj: dict[str, Any]):
    activity_factory, object_factory = factories_for_actor_object(
        {"id": remote_actor}, id_generator=lambda: f"{remote_actor}/id"
    )
    actor = obj.get("attributedTo", "broken")
    activity = {}
    routing_key = None

    match interaction:
        case "likes":
            activity = activity_factory.like(obj.get("id"), to={actor}).build()
            routing_key = "incoming.Like"
        case "shares":
            activity = activity_factory.announce(obj.get("id"), to={actor}).build()
            routing_key = "incoming.Announce"
        case "replies":
            reply = object_factory.reply(obj, content="oh a reply").build()
            activity = activity_factory.create(reply).build()
            routing_key = "incoming.Create"

    normalized = normalize_data(activity).model_dump()
    msg = ActivityMessage(actor=actor, data={"raw": activity, "parsed": normalized})

    await test_broker.publish(
        msg,
        routing_key=routing_key,
        exchange=app_globals.activity_exchange,
    )


@pytest.mark.parametrize("interaction", ["likes", "shares", "replies"])
async def test_interaction_collection_with_interaction(
    test_client,
    published_object,
    interaction,
    test_broker,
):
    remote_actor = "http://remote.test/actor"
    object_id = published_object["id"]
    response = test_client.get(
        object_id,
        headers={
            "x-ap-location": object_id,
            "x-cattle-grid-requester": remote_actor,
        },
    )

    assert response.status_code == 200
    data = response.json()
    interaction_collection = data[interaction]

    await interact(remote_actor, test_broker, interaction, data)

    response = test_client.get(
        interaction_collection,
        headers={
            "x-ap-location": interaction_collection,
            "x-cattle-grid-requester": "http://remote.test/actor",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == interaction_collection
    assert data["type"] == "OrderedCollection"
    assert data.get("orderedItems")


@pytest.mark.parametrize("interaction", ["likes", "shares", "replies"])
async def test_interaction_no_object(
    interaction,
    test_broker,
):
    remote_actor = "http://remote.test/actor"
    data = {"id": "http://remote.test/unknown", "attributedTo": remote_actor}
    await interact(remote_actor, test_broker, interaction, data)
