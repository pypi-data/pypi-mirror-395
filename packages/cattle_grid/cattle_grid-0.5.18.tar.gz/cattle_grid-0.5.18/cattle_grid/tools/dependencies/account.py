import logging
from typing import Annotated

from fast_depends import Depends
from faststream import Context

logger = logging.getLogger(__name__)


RoutingKey = Annotated[str, Context("message.raw_message.routing_key")]
"""The AMQP routing key"""


def name_from_routing_key(
    routing_key: RoutingKey,
) -> str:
    """
    ```pycon
    >>> name_from_routing_key("receiving.alice")
    'alice'

    >>> name_from_routing_key("receiving.alice.action.fetch")
    'alice'

    ```
    """
    logger.info(routing_key)
    return routing_key.split(".")[1]


AccountName = Annotated[str, Depends(name_from_routing_key)]
"""Assigns the account name extracted from the routing key"""
