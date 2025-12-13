from bovine import BovineActor
from sqlalchemy.sql import func

from cattle_grid.testing.fixtures import *  # noqa
from cattle_grid.database.activity_pub_actor import Follower, Following


from . import create_actor
from .internals import bovine_actor_for_actor_id, remove_from_followers_following


async def test_get_bovine_actor_not_found(sql_session):
    bovine_actor = await bovine_actor_for_actor_id(
        sql_session, "http://nothing.here/actor"
    )

    assert bovine_actor is None


async def test_get_bovine_actor(sql_session):
    actor = await create_actor(sql_session, "http://localhost/ap/")

    bovine_actor = await bovine_actor_for_actor_id(sql_session, actor.actor_id)

    assert isinstance(bovine_actor, BovineActor)


async def test_remove_from_followers_following(sql_session):
    actor = await create_actor(sql_session, "http://localhost/ap/")

    remote_id = "http://remote.test"

    follower = Follower(actor=actor, follower=remote_id, accepted=True, request="")
    following = Following(actor=actor, following=remote_id, accepted=True, request="")

    sql_session.add_all([follower, following])
    await sql_session.commit()

    await remove_from_followers_following(sql_session, remote_id)

    assert 0 == await sql_session.scalar(func.count(Follower.id))
    assert 0 == await sql_session.scalar(func.count(Following.id))
