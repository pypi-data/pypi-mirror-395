import asyncio
import secrets
import logging

from almabtrieb.exceptions import ErrorMessageException


logger = logging.getLogger(__name__)


def id_generator_for_actor(actor):
    def gen():
        return actor.get("id") + "/" + secrets.token_hex(8)

    return gen


async def publish_as(
    context, username: str, method: str, data: dict, timeout: float = 0.3
):
    """Publishes a message through the gateway

    :param data: The message to be published"""
    connection = context.connections[username]

    await connection.trigger(method, data)
    await asyncio.sleep(timeout)


async def fetch_request(context, username: str, uri: str) -> dict | None:
    """Sends a fetch request for the uri through the gateway

    :param context: The behave context
    :param username: username performing the result
    :param uri: URI being looked up
    :return:
    """
    connection = context.connections[username]
    actor = context.actors[username].get("id")

    await asyncio.sleep(0.1)

    try:
        data = await connection.fetch(actor, uri)

        assert data.uri == uri

        return data.data
    except ErrorMessageException:
        return None


def send_message_as_actor(actor, activity):
    return {"actor": actor.get("id"), "data": activity}
