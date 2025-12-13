from collections.abc import Awaitable, Callable
from dataclasses import dataclass
import json
from typing import Annotated, Any
from fast_depends import Depends
from faststream import Context
from faststream.rabbit import RabbitExchange, ExchangeType, RabbitBroker
from cattle_grid.model.common import WithActor
from .account import AccountName


async def actor_id(message: WithActor) -> str:
    return message.actor


ActorId = Annotated[str, Depends(actor_id)]
"""ActorId of the actor processing the message"""


def current_exchange(exchange_name: str = Context("message.raw_message.exchange")):
    return RabbitExchange(exchange_name, type=ExchangeType.TOPIC, durable=True)


CurrentExchange = Annotated[RabbitExchange, Depends(current_exchange)]
"""Returns the exchange the message was received on"""


@dataclass
class AccountPublisherClass:
    name: AccountName
    exchange: CurrentExchange
    broker: RabbitBroker = Context()

    async def __call__(self, method: str, message):
        routing_key = f"send.{self.name}.{method}"
        await self.broker.publish(
            message, routing_key=routing_key, exchange=self.exchange
        )


AccountPublisher = Annotated[
    Callable[[str, Any], Awaitable[None]], Depends(AccountPublisherClass)
]
"""When processing on the AccountExchange, allows one to publish a message as the current account. Usage

```python
async def my_method(publisher: AccountPublisher):
    await publisher("trigger.publish_activity", {
        "actor": "http://local.example/actor/id",
        "data": {
            "type": "Activity",
            "actor": "http://local.example/actor/id",
        }
    })
```
"""


@dataclass
class AccountRequesterClass:
    name: AccountName
    exchange: CurrentExchange
    broker: RabbitBroker = Context()

    async def __call__(self, method: str, message):
        routing_key = f"send.{self.name}.{method}"
        result = await self.broker.request(
            message, routing_key=routing_key, exchange=self.exchange
        )
        return json.loads(result.body)


AccountRequester = Annotated[
    Callable[[str, Any], Awaitable[dict]], Depends(AccountRequesterClass)
]
"""Similar to AccountPublisher, but uses broker.request."""
