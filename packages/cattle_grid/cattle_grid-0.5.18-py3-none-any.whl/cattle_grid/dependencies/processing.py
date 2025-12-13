"""
Furthermore, you may use the annotations from [muck_out.cattle_grid][] starting
with Fetch or Parsed.

"""

import logging

from typing import Annotated
from fast_depends import Depends

from bovine.activitystreams import factories_for_actor_object
from bovine.activitystreams.activity_factory import ActivityFactory
from bovine.activitystreams.object_factory import ObjectFactory
from sqlalchemy import select


from cattle_grid.activity_pub import actor_to_object
from cattle_grid.database.account import Account, ActorForAccount
from cattle_grid.database.activity_pub_actor import Actor
from cattle_grid.dependencies import SqlSession
from cattle_grid.tools.dependencies import ActorId


logger = logging.getLogger(__name__)


class ProcessingError(ValueError): ...


async def actor_for_message(session: SqlSession, actor_id: ActorId):
    actor = await session.scalar(select(Actor).where(Actor.actor_id == actor_id))

    if actor is None:
        raise ProcessingError("Actor not found")

    return actor


MessageActor = Annotated[Actor, Depends(actor_for_message)]
"""Returns the actor for the message"""


def get_actor_profile(actor: MessageActor):
    return actor_to_object(actor)


ActorProfile = Annotated[dict, Depends(get_actor_profile)]
"""Returns the actor profile of the actor processing the
message"""


def get_factories_for_actor(profile: ActorProfile):
    return factories_for_actor_object(profile)


FactoriesForActor = Annotated[
    tuple[ActivityFactory, ObjectFactory], Depends(get_factories_for_actor)
]
"""Returns the activity and object factories for the actor"""


async def determine_account(session: SqlSession, actor_id: ActorId):
    actor_for_account = await session.scalar(
        select(ActorForAccount).where(ActorForAccount.actor == actor_id)
    )
    if actor_for_account is None:
        raise ProcessingError(
            "Either actor does not exist or is not attached to an account"
        )

    return actor_for_account.account


AccountForActor = Annotated[Account, Depends(determine_account)]
"""Returns the account associated with the actor or raises an error"""


async def determine_permissions(session: SqlSession, account: AccountForActor):
    await session.refresh(account, attribute_names=["permissions"])

    return [p.name for p in account.permissions]


PermissionsForAccount = Annotated[list[str], Depends(determine_permissions)]
"""Returns the permissions of the account associated with the actor"""
