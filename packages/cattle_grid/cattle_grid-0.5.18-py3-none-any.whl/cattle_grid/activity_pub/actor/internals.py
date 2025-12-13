import logging


from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from bovine import BovineActor

from cattle_grid.database.activity_pub_actor import (
    Actor,
    PublicIdentifier,
    Follower,
    Following,
    ActorStatus,
)
from cattle_grid.database.activity_pub import Credential


logger = logging.getLogger(__name__)


async def bovine_actor_for_actor_id(
    session: AsyncSession, actor_id: str
) -> BovineActor | None:
    """Uses the information stored in
    [Credential][cattle_grid.database.activity_pub.Credential] to construct a bovine actor

    :params actor_id:
    :returns:
    """
    credential = await session.scalar(
        select(Credential).where(Credential.actor_id == actor_id)
    )

    if credential is None:
        logger.warning("No credential found for %s", actor_id)
        return None

    return BovineActor(
        public_key_url=credential.identifier,
        actor_id=actor_id,
        secret=credential.secret,
    )


async def delete_actor(session: AsyncSession, actor: Actor):
    """Deletes an actor

    :param actor: Actor to be deleted
    """
    await session.execute(
        delete(PublicIdentifier).where(PublicIdentifier.actor_id == actor.id)
    )
    actor.status = ActorStatus.deleted
    await session.commit()


async def remove_from_followers_following(
    session: AsyncSession, actor_id_to_remove: str
):
    """Removes actor_id from all occurring followers and following"""
    await session.execute(
        delete(Follower).where(Follower.follower == actor_id_to_remove)
    )
    await session.execute(
        delete(Following).where(Following.following == actor_id_to_remove)
    )
