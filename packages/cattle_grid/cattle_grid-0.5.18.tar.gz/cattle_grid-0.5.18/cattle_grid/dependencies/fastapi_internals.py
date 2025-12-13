import logging
import asyncio
import json

from dataclasses import dataclass
from typing import Annotated


from faststream.rabbit import RabbitBroker, RabbitExchange
from fastapi import Depends

from cattle_grid.app import access_methods, app_globals

from .globals import global_container

Broker = Annotated[RabbitBroker, Depends(global_container.get_broker)]
"""The RabbitMQ broker"""
InternalExchange = Annotated[
    RabbitExchange, Depends(access_methods.get_internal_exchange)
]

ActivityExchange = Annotated[
    RabbitExchange, Depends(access_methods.get_activity_exchange)
]
"""The Activity Exchange"""


logger = logging.getLogger(__name__)


@dataclass
class ActivityExchangePublisherClass:
    exchange: ActivityExchange
    broker: Broker

    async def __call__(self, *args, **kwargs):
        kwargs_updated = {**kwargs}
        kwargs_updated.update(dict(exchange=self.exchange))
        return await self.broker.publish(*args, **kwargs_updated)


@dataclass
class ActivityExchangeRequesterClass:
    exchange: ActivityExchange
    broker: Broker
    timeout: float = app_globals.application_config.frontend_config.timeout_amqp_request

    async def __call__(self, *args, **kwargs):
        try:
            async with asyncio.timeout(self.timeout):
                kwargs_updated = {**kwargs}
                kwargs_updated.update(dict(exchange=self.exchange, timeout=1))
                result = await self.broker.request(*args, **kwargs_updated)
                return json.loads(result.body)

        except TimeoutError as e:
            logger.warning("Ran into timeout")
            logger.exception(e)
            return {}
