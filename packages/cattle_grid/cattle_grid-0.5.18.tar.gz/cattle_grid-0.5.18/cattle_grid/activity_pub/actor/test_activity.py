from cattle_grid.testing.fixtures import *  # noqa

from .activity import update_for_actor_profile, delete_for_actor_profile

from . import create_actor


async def test_update_for_actor_profile(sql_session):
    actor = await create_actor(sql_session, "http://localhost/ap/")

    activity = update_for_actor_profile(actor)

    assert activity["type"] == "Update"
    obj = activity["object"]

    assert obj["type"] == "Person"
    assert activity["cc"]


async def test_delete_for_actor_profile(sql_session):
    actor = await create_actor(sql_session, "http://localhost/ap/")

    activity = delete_for_actor_profile(actor)

    assert activity["type"] == "Delete"

    assert activity["object"] == actor.actor_id
