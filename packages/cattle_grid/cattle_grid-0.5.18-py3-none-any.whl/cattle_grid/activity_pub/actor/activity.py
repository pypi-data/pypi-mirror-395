from cattle_grid.database.activity_pub_actor import Actor

from bovine.activitystreams import factories_for_actor_object
from .transform import actor_to_object


def update_for_actor_profile(actor: Actor) -> dict:
    """Creates an update for the Actor"""

    actor_profile = actor_to_object(actor)
    activity_factory, _ = factories_for_actor_object(actor_profile)

    return (
        activity_factory.update(actor_profile, followers=actor_profile["followers"])
        .as_public()
        .build()
    )


def delete_for_actor_profile(actor: Actor) -> dict:
    """Creates a delete activity for the Actor"""

    actor_profile = actor_to_object(actor)
    activity_factory, _ = factories_for_actor_object(actor_profile)

    result = (
        activity_factory.delete(
            actor_profile.get("id"), followers=actor_profile["followers"]
        )
        .as_public()
        .build()
    )

    result["cc"].append(actor_profile["following"])

    return result
