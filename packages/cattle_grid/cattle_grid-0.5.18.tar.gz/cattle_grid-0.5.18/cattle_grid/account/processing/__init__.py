"""
The exchanges used by cattle_grid are using routing keys
to make processing easier. On the cattle_ground account
router messages are also addressed by account. An account
consists of a grouping of multiple actors.
"""

from faststream.rabbit import RabbitRouter
from .router import create_router


def create_account_router() -> RabbitRouter:
    """Creates a router that moves messages to be routed by user."""
    return create_router()
