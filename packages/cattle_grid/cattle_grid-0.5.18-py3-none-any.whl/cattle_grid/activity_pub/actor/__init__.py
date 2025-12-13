import logging

from bovine.crypto import generate_rsa_public_private_key
from sqlalchemy.ext.asyncio import AsyncSession


from cattle_grid.database.activity_pub_actor import (
    Actor,
    PublicIdentifier,
    ActorStatus,
    PublicIdentifierStatus,
)
from cattle_grid.database.activity_pub import Credential

from .identifiers import (
    identifier_in_list_exists,
)
from .helper import compute_acct_uri, new_url


logger = logging.getLogger(__name__)


class DuplicateIdentifierException(Exception):
    """Raised if an identifier already exists and one tries to create an actor with it"""


async def create_actor(
    session: AsyncSession,
    base_url: str,
    preferred_username: str | None = None,
    identifiers: dict = {},
    profile: dict = {},
    automatically_accept_followers: bool = False,
):
    """Creates a new actor in the database"""

    public_key, private_key = generate_rsa_public_private_key()
    public_key_name = "legacy-key-1"
    actor_id = new_url(base_url, "actor")

    if preferred_username:
        if "webfinger" in identifiers:
            raise ValueError("webfinger key set in identifiers")
        identifiers = {
            **identifiers,
            "webfinger": compute_acct_uri(base_url, preferred_username),
        }

    if "activitypub_id" not in identifiers:
        identifiers = {**identifiers, "activitypub_id": actor_id}

    identifier_already_exists = await identifier_in_list_exists(
        session, list(identifiers.values())
    )

    if identifier_already_exists:
        raise DuplicateIdentifierException("identifier already exists")

    actor = Actor(
        actor_id=actor_id,
        inbox_uri=new_url(base_url, "inbox"),
        outbox_uri=f"{actor_id}/outbox",
        following_uri=f"{actor_id}/following",
        followers_uri=f"{actor_id}/followers",
        public_key_name=public_key_name,
        public_key=public_key,
        profile={**profile},
        automatically_accept_followers=automatically_accept_followers,
        status=ActorStatus.active,
    )
    session.add(actor)

    for name, identifier in identifiers.items():
        session.add(
            PublicIdentifier(
                actor=actor,
                name=name,
                identifier=identifier,
                status=PublicIdentifierStatus.verified,
            )
        )

    credential = Credential(
        actor_id=actor_id,
        identifier=f"{actor_id}#{public_key_name}",
        secret=private_key,
    )
    session.add(credential)

    logging.info("Created actor with id '%s'", actor_id)

    await session.commit()
    await session.refresh(actor, attribute_names=["identifiers"])

    return actor
