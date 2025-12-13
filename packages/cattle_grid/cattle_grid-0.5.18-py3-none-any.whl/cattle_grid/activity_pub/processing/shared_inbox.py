from sqlalchemy import select

from bovine.activitystreams.utils import recipients_for_object

from cattle_grid.model import ActivityMessage, SharedInboxMessage
from cattle_grid.database.activity_pub_actor import Actor, Following
from cattle_grid.activity_pub.enqueuer import (
    determine_activity_type,
)
from cattle_grid.dependencies import InternalExchangePublisher, SqlSession


def to_result_set(result):
    return set(result.all())


async def handle_shared_inbox_message(
    message: SharedInboxMessage,
    session: SqlSession,
    publisher: InternalExchangePublisher,
):
    """
    This method is used to handle incoming messages from the shared inbox.
    """

    recipients = recipients_for_object(message.data)
    sender = message.data.get("actor")

    if sender is None:
        return

    local_actor_ids = to_result_set(
        await session.scalars(
            select(Actor.actor_id).where(Actor.actor_id.in_(recipients))
        )
    )
    following_actor_ids = {
        x.actor.actor_id
        for x in await session.scalars(
            select(Following)
            .where(Following.following == sender)
            .where(Following.accepted)
        )
    }
    activity_type = determine_activity_type(message.data)
    if activity_type is None:
        return

    for actor in local_actor_ids | following_actor_ids:
        new_message = ActivityMessage(actor=actor, data=message.data)
        await publisher(new_message, routing_key=f"incoming.{activity_type}")
