import json
import logging
from behave_auto_docstring import when, then
from almabtrieb.stream import StreamNoNewItemException
from bovine.activitystreams import factories_for_actor_object

from cattle_grid.testing.features import (
    publish_as,
    id_generator_for_actor,
    fetch_request,
    send_message_as_actor,
)

logger = logging.getLogger(__name__)


@when('"{actor}" sends "{target}" a message saying "{text}"')
async def send_message(context, actor, target, text):
    """Used to send a message. The message has the format (with a lot of stuff omitted)

    ```json
    {
        "type": "Create",
        "object": {
            "type": "Note",
            "content": text,
            "to": [actor_id_of_target]
        }
    }
    ```
    """
    alice = context.actors[actor]
    activity_factory, object_factory = factories_for_actor_object(
        alice, id_generator=id_generator_for_actor(alice)
    )

    bob_id = context.actors[target].get("id")

    note = object_factory.note(content=text, to={bob_id}).build()
    activity = activity_factory.create(note).build()

    await publish_as(
        context,
        actor,
        "send_message",
        send_message_as_actor(alice, activity),
    )


@then('"{actor}" receives an activity')
async def receive_activity(context, actor):
    """Ensures that an incoming activity was received
    and stores it in `context.activity`.
    """

    data = await context.connections[actor].next_incoming()
    assert data.get("event_type") == "incoming"

    context.activity = data["data"]["raw"]

    assert context.activity["@context"]


@then('"{actor}" does not receive an activity')
async def not_receive_activity(context, actor):
    """Ensures that no incoming activity was received"""

    try:
        result = await context.connections[actor].next_incoming()

        assert result is None, f"Received activity {json.dumps(result, indent=2)}"
    except StreamNoNewItemException:
        ...


@then('the received activity is of type "{activity_type}"')
def check_activity_type(context, activity_type):
    """Checks that the received activity from [cattle_grid.testing.features.steps.messaging.receive_activity][]
    is of type `activity_type`.
    """

    received = context.activity
    if "raw" in received:
        received = received["raw"]

    import json

    logger.debug(json.dumps(received, indent=2))

    assert received.get("type") == activity_type, (
        f"Activity {received} has the wrong type"
    )


@then('"{actor}" receives a message saying "{text}"')
async def receive_message(context, actor, text):
    """Used to check if the last message received by actor
    is saying the correct thing.

    The received object is stored in `context.received_object`.
    """

    data = await context.connections[actor].next_incoming()

    assert data.get("event_type") == "incoming"
    activity = data.get("data")

    if "raw" in activity:
        activity = activity["raw"]

    assert activity.get("type") == "Create", f"got {activity}"
    assert activity.get("@context"), f"got {activity}"

    obj = activity.get("object", {})
    assert obj.get("content") == text, f"""got {obj.get("content")}"""

    context.received_object = obj


@then('"{bob}" can lookup this message by id')
async def check_lookup_message(context, bob):
    obj_id = context.received_object.get("id")

    result = await fetch_request(context, bob, obj_id)

    assert isinstance(result, dict), f"got {result}"
    assert result == context.received_object, result


@when('"{actor}" messages her followers "{text}"')
async def send_message_followers(context, actor, text):
    """Used to send a message to the followers. The message has the format (with a lot of stuff omitted)

    ```json
    {
        "type": "Create",
        "object": {
            "type": "Note",
            "content": text,
            "to": [followers_collection_of_actor]
        }
    }
    ```
    """
    for connection in context.connections.values():
        await connection.clear_incoming()

    alice = context.actors[actor]

    activity_factory, object_factory = factories_for_actor_object(
        alice, id_generator=id_generator_for_actor(alice)
    )
    note = object_factory.note(content=text).as_followers().build()
    activity = activity_factory.create(note).build()

    await publish_as(
        context,
        actor,
        "send_message",
        send_message_as_actor(alice, activity),
    )


@then('the embedded object is of type "{object_type}"')
def check_embedded_object_type(context, object_type):
    received = context.activity
    if "raw" in received:
        received = received["raw"]

    obj = received.get("object", {})

    assert obj.get("type") == object_type, f"Embedded object {obj} has the wrong type"
