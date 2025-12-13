from dataclasses import dataclass
import json

from typing import Annotated, Awaitable, Callable

from fast_depends import Depends
from faststream import Context
from faststream.rabbit import RabbitExchange, RabbitBroker

from cattle_grid.config.rewrite import RewriteConfiguration
from cattle_grid.model.extension import MethodInformationModel
from cattle_grid.model.lookup import LookupMethod
from cattle_grid.app import access_methods

from .globals import (
    get_transformer,
    get_lookup,
    global_container,
    get_method_information,
)


Transformer = Annotated[Callable[..., Awaitable[dict]], Depends(get_transformer)]
"""The transformer loaded from extensions"""

LookupAnnotation = Annotated[LookupMethod, Depends(get_lookup)]
"""The lookup method loaded from extensions"""


InternalExchange = Annotated[
    RabbitExchange, Depends(access_methods.get_internal_exchange)
]
"""The interal activity exchange"""

ActivityExchange = Annotated[
    RabbitExchange, Depends(access_methods.get_activity_exchange)
]
"""The activity exchange"""

AccountExchange = Annotated[
    RabbitExchange, Depends(access_methods.get_account_exchange)
]
"""The account exchange"""


CorrelationId = Annotated[str, Context("message.correlation_id")]
"""The correlation id of the message"""

MethodInformation = Annotated[
    list[MethodInformationModel], Depends(get_method_information)
]
"""Returns the information about the methods that are a part of the exchange"""


RewriteRules = Annotated[
    RewriteConfiguration, Depends(global_container.get_rewrite_rules)
]
"""Rewturns the rewrite configuration"""


class BasePublisherClass:
    async def __call__(self, *args, **kwargs):
        kwargs_updated = {**kwargs}
        kwargs_updated.update(
            dict(exchange=self.exchange, correlation_id=self.correlation_id)
        )
        return await self.broker.publish(*args, **kwargs_updated)


class BaseRequesterClass:
    async def __call__(self, *args, **kwargs):
        kwargs_updated = {**kwargs}
        kwargs_updated.update(
            dict(exchange=self.exchange, correlation_id=self.correlation_id)
        )
        result = await self.broker.request(*args, **kwargs_updated)
        return json.loads(result.body)


@dataclass
class ActivityExchangePublisherClass(BasePublisherClass):
    correlation_id: CorrelationId
    exchange: ActivityExchange
    broker: RabbitBroker = Context()


@dataclass
class ActivityExchangeRequesterClass(BaseRequesterClass):
    correlation_id: CorrelationId
    exchange: ActivityExchange
    broker: RabbitBroker = Context()


@dataclass
class InternalExchangePublisherClass(BasePublisherClass):
    correlation_id: CorrelationId
    exchange: InternalExchange
    broker: RabbitBroker = Context()


@dataclass
class AccountExchangePublisherClass(BasePublisherClass):
    correlation_id: CorrelationId
    exchange: AccountExchange
    broker: RabbitBroker = Context()


@dataclass
class InternalExchangeRequesterClass(BaseRequesterClass):
    correlation_id: CorrelationId
    exchange: InternalExchange
    broker: RabbitBroker = Context()
