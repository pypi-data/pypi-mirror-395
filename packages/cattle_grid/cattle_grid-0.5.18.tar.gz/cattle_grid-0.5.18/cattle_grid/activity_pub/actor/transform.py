from bovine.activitystreams import Actor as AsActor
from bovine.activitystreams.utils.property_value import property_value_context
from bovine.types import Visibility

from cattle_grid.database.activity_pub_actor import Actor

from .identifiers import determine_preferred_username, collect_identifiers_for_actor

from .helper import endpoints_object_from_actor_id


def actor_to_object(actor: Actor) -> dict:
    """Transform the actor to an object

    !!! warning
        The `actor.identifiers` needs to be fetched from the database for this to work properly

    """

    sorted_identifiers = collect_identifiers_for_actor(actor)

    preferred_username = determine_preferred_username(
        sorted_identifiers, actor.actor_id
    )
    attachments = actor.profile.get("attachment")
    result = AsActor(
        id=actor.actor_id,
        outbox=actor.outbox_uri,
        inbox=actor.inbox_uri,
        followers=actor.followers_uri,
        following=actor.following_uri,
        public_key=actor.public_key,
        public_key_name=actor.public_key_name,
        preferred_username=preferred_username,
        type=actor.profile.get("type", "Person"),
        name=actor.profile.get("name"),
        summary=actor.profile.get("summary"),
        url=actor.profile.get("url"),
        icon=actor.profile.get("image", actor.profile.get("icon")),
        properties={
            "attachment": attachments,
            "published": actor.created_at.isoformat(),
        },
    ).build(visibility=Visibility.OWNER)

    result["identifiers"] = sorted_identifiers
    result["endpoints"] = endpoints_object_from_actor_id(actor.actor_id)

    result["@context"].append(
        {"manuallyApprovesFollowers": "as:manuallyApprovesFollowers"}
    )
    result["manuallyApprovesFollowers"] = not actor.automatically_accept_followers

    if attachments:
        result["@context"].append(property_value_context)

    return result
