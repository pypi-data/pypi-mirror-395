import asyncio

from behave_auto_docstring import given, when

from bovine.activitystreams import factories_for_actor_object
from cattle_grid.testing.features import publish_as


@when('"{alice}" likes the ActivityPub object')
async def alice_likes(context, alice):
    """Alice likes the object given by [alice_fetches_the_activity_pub_object][cattle_grid.testing.features.steps.fetch.alice_fetches_the_activity_pub_object]"""
    alice_actor = context.actors[alice]
    activity_factory, _ = factories_for_actor_object(alice_actor)

    activity = (
        activity_factory.like(
            context.fetch_response.get("id"),
            to={context.fetch_response.get("attributedTo")},
        )
        .as_public()
        .build()
    )

    await publish_as(
        context,
        alice,
        "publish_activity",
        {"actor": alice_actor.get("id"), "data": activity},
    )

    await asyncio.sleep(0.3)


@when('"{alice}" undoes the interaction the ActivityPub object')
async def alice_undoes(context, alice):
    """Alice undoes the last interaction with the object given by
    [alice_fetches_the_activity_pub_object][cattle_grid.testing.features.steps.fetch.alice_fetches_the_activity_pub_object]
    """
    alice_actor = context.actors[alice]
    activity_factory, _ = factories_for_actor_object(alice_actor)

    activity = (
        activity_factory.undo(
            context.interaction_id,
            to={context.fetch_response.get("attributedTo")},
        )
        .as_public()
        .build()
    )

    await publish_as(
        context,
        alice,
        "publish_activity",
        {"actor": alice_actor.get("id"), "data": activity},
    )

    await asyncio.sleep(0.3)


@given('"{alice}" liked the ActivityPub object')
def alice_liked(context, alice):
    """alias for

    ```gherkin
        Given "{alice}" fetches the ActivityPub object
        When "{alice}" likes the ActivityPub object
        Then For "{alice}", the "likes" collection contains "one" element
    ```
    """
    context.execute_steps(f"""
        Given "{alice}" fetches the ActivityPub object
        When "{alice}" likes the ActivityPub object
        Then For "{alice}", the "likes" collection contains "one" element
""")


@when('"{alice}" announces the ActivityPub object')
async def alice_shares(context, alice):
    """Sends an announce activity"""
    alice_actor = context.actors[alice]
    activity_factory, _ = factories_for_actor_object(alice_actor)

    activity = (
        activity_factory.announce(
            context.fetch_response.get("id"),
            to={context.fetch_response.get("attributedTo")},
        )
        .as_public()
        .build()
    )

    await publish_as(
        context,
        alice,
        "publish_activity",
        {"actor": alice_actor.get("id"), "data": activity},
    )

    await asyncio.sleep(0.3)


@given('"{alice}" announced the ActivityPub object')
def alice_announced(context, alice):
    """alias for

    ```gherkin
        Given "{alice}" fetches the ActivityPub object
        When "{alice}" announces the ActivityPub object
        Then For "{alice}", the "shares" collection contains "one" element
    ```
    """
    context.execute_steps(f"""
        Given "{alice}" fetches the ActivityPub object
        When "{alice}" announces the ActivityPub object
        Then For "{alice}", the "shares" collection contains "one" element
""")


@when('"{alice}" replies to the ActivityPub object with "{text}"')
async def alice_replies(context, alice, text):
    """Replies with text to the ActivityPub object"""
    alice_actor = context.actors[alice]
    _, object_factory = factories_for_actor_object(alice_actor)

    reply = (
        object_factory.reply(context.fetch_response, content=text).as_public().build()
    )
    reply["type"] = "Note"

    await publish_as(
        context,
        alice,
        "publish_object",
        {"actor": alice_actor.get("id"), "data": reply},
    )

    await asyncio.sleep(0.3)


@given('"{alice}" replied to the ActivityPub object')
def alice_replied(context, alice):
    """alias for

    ```gherkin
        Given "{alice}" fetches the ActivityPub object
        When "{alice}" replies to the ActivityPub object with "Nice post!"
        Then For "{alice}", the "replies" collection contains "one" element
    ```
    """
    context.execute_steps(f"""
        Given "{alice}" fetches the ActivityPub object
        When "{alice}" replies to the ActivityPub object with "Nice post!"
        Then For "{alice}", the "replies" collection contains "one" element
""")


@given('"{alice}" replied to the ActivityPub object with "{text}')
def alice_replied_with(context, alice, text):
    """alias for

    ```gherkin
        Given "{alice}" fetches the ActivityPub object
        When "{alice}" replies to the ActivityPub object with "{text}"
        Then For "{alice}", the "replies" collection contains "one" element
    ```
    """
    context.execute_steps(f"""
        Given "{alice}" fetches the ActivityPub object
        When "{alice}" replies to the ActivityPub object with "{text}"
        Then For "{alice}", the "replies" collection contains "one" element
""")


@when('"{alice}" deletes her reply to the ActivityPub object')  # type: ignore
async def alice_deletes_reply(context, alice):
    """Deletes the reply in `context.interaction_id."""
    alice_actor = context.actors[alice]
    activity_factory, _ = factories_for_actor_object(alice_actor)

    activity = (
        activity_factory.delete(
            context.interaction_id,
            to={context.fetch_response.get("attributedTo")},
        )
        .as_public()
        .build()
    )

    await publish_as(
        context,
        alice,
        "publish_activity",
        {"actor": alice_actor.get("id"), "data": activity},
    )

    await asyncio.sleep(0.3)


@when('"{alice}" updates her reply with "{text}"')
async def alice_update_post(context, alice, text):
    """Updates the reply in `context.interaction_id."""
    alice_actor = context.actors[alice]
    activity_factory, object_factory = factories_for_actor_object(alice_actor)

    reply = (
        object_factory.reply(context.fetch_response, content=text).as_public().build()
    )
    reply["type"] = "Note"

    reply["id"] = context.interaction_id

    activity = activity_factory.update(reply).build()

    await publish_as(
        context,
        alice,
        "publish_activity",
        {"actor": alice_actor.get("id"), "data": activity},
    )

    await asyncio.sleep(0.3)
