import pytest

from cattle_grid.database.activity_pub_actor import Follower
from cattle_grid.testing.fixtures import *  # noqa

from .requester import update_recipients_for_actor


@pytest.mark.parametrize(
    "builder",
    [
        lambda x: set(),
        lambda x: {x.followers_uri},
        lambda x: {x.actor_id + "/followers"},
    ],
)
async def test_update_recipients_for_actor(sql_session, actor_for_test, builder):
    result = await update_recipients_for_actor(
        sql_session, actor_for_test, builder(actor_for_test)
    )

    assert result == set()


@pytest.mark.parametrize(
    "builder",
    [
        lambda x: {x.followers_uri},
        lambda x: {x.actor_id + "/followers"},
    ],
)
async def test_update_recipients_for_actor_follower(
    sql_session, actor_for_test, builder
):
    follower = Follower(
        actor=actor_for_test,
        follower="http://remote.test/follower",
        request="http://remote.test/request_id",
        accepted=True,
    )

    sql_session.add(follower)
    await sql_session.commit()

    result = await update_recipients_for_actor(
        sql_session, actor_for_test, builder(actor_for_test)
    )

    assert result == {"http://remote.test/follower"}
