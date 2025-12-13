"""ActivityPub related functionality"""

import logging
from fastapi import APIRouter, Depends, HTTPException

from bovine.activitystreams.utils import as_list
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from cattle_grid.database.activity_pub_actor import Actor
from cattle_grid.dependencies.fastapi import SqlSession

from cattle_grid.activity_pub import actor_to_object
from cattle_grid.activity_pub.actor.relationship import (
    followers_for_actor,
    following_for_actor,
)

from cattle_grid.tools.fastapi import ActivityResponse, ActivityPubHeaders

from .validate import validate_request
from .types import OrderedCollection

logger = logging.getLogger(__name__)

ap_router = APIRouter(tags=["activity_pub_actor"])


def extract_html_url(actor: Actor) -> str | None:
    urls = as_list(actor.profile.get("url", []))

    for url in urls:
        if isinstance(url, str):
            return url
        if url.get("mediaType").startswith("text/html"):
            return url.get("href")

    return None


@ap_router.get("/actor/{id_str}", response_class=ActivityResponse)
async def actor_profile(headers: ActivityPubHeaders, session: SqlSession):
    """Returns the actor"""
    logger.debug("Request for actor at %s", headers.x_ap_location)
    actor = await session.scalar(
        select(Actor)
        .where(Actor.actor_id == headers.x_ap_location)
        .options(joinedload(Actor.identifiers))
    )

    if headers.x_cattle_grid_should_serve == "html":
        if not actor:
            raise HTTPException(404)
        html_url = extract_html_url(actor)
        if html_url:
            return RedirectResponse(html_url)
        raise HTTPException(406)

    actor = await validate_request(session, actor, headers.x_cattle_grid_requester)

    result = actor_to_object(actor)
    return result


async def get_actor_for_collection(
    headers: ActivityPubHeaders, session: SqlSession
) -> Actor:
    actor_id = headers.x_ap_location
    for endpoint in ["/outbox", "/following", "/followers"]:
        actor_id = actor_id.removesuffix(endpoint)

    actor = await session.scalar(select(Actor).where(Actor.actor_id == actor_id))
    actor = await validate_request(session, actor, headers.x_cattle_grid_requester)

    return actor


@ap_router.get("/actor/{id_str}/outbox", response_class=ActivityResponse)
async def actor_outbox(
    headers: ActivityPubHeaders, actor=Depends(get_actor_for_collection)
) -> OrderedCollection:
    """Returns an empty ordered collection as outbox"""
    return OrderedCollection(id=headers.x_ap_location)  # type: ignore


@ap_router.get("/actor/{id_str}/followers", response_class=ActivityResponse)
async def actor_followers(
    headers: ActivityPubHeaders,
    session: SqlSession,
    actor=Depends(get_actor_for_collection),
) -> OrderedCollection:
    """Returns the followers collection"""
    followers = await followers_for_actor(session, actor)

    return OrderedCollection(id=headers.x_ap_location, items=list(followers))


@ap_router.get("/actor/{id_str}/following", response_class=ActivityResponse)
async def actor_following(
    headers: ActivityPubHeaders,
    session: SqlSession,
    actor=Depends(get_actor_for_collection),
) -> OrderedCollection:
    """Returns the following collection"""
    following = await following_for_actor(session, actor)

    return OrderedCollection(id=headers.x_ap_location, items=list(following))


@ap_router.get("/outbox/{id_str}", response_class=ActivityResponse, deprecated=True)
async def outbox(headers: ActivityPubHeaders, session: SqlSession) -> OrderedCollection:
    """Returns an empty ordered collection as outbox

    Deprecated use /actor/{id_str}/outbox
    """
    actor = await session.scalar(
        select(Actor).where(Actor.outbox_uri == headers.x_ap_location)
    )
    actor = await validate_request(session, actor, headers.x_cattle_grid_requester)

    return OrderedCollection(id=headers.x_ap_location)  # type: ignore


@ap_router.get("/following/{id_str}", response_class=ActivityResponse, deprecated=True)
async def following(
    id_str, headers: ActivityPubHeaders, session: SqlSession
) -> OrderedCollection:
    """Returns the following

    Deprecated use /actor/{id_str}/following
    """

    actor = await session.scalar(
        select(Actor).where(Actor.following_uri == headers.x_ap_location)
    )
    actor = await validate_request(session, actor, headers.x_cattle_grid_requester)

    following = await following_for_actor(session, actor)
    return OrderedCollection(id=headers.x_ap_location, items=list(following))


@ap_router.get("/followers/{id_str}", response_class=ActivityResponse, deprecated=True)
async def followers(
    id_str, headers: ActivityPubHeaders, session: SqlSession
) -> OrderedCollection:
    """Returns the followers

    Deprecated use /actor/{id_str}/followers
    """
    actor = await session.scalar(
        select(Actor).where(Actor.followers_uri == headers.x_ap_location)
    )
    actor = await validate_request(session, actor, headers.x_cattle_grid_requester)

    followers = await followers_for_actor(session, actor)
    return OrderedCollection(id=headers.x_ap_location, items=list(followers))
