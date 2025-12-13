from collections.abc import Callable
from dataclasses import dataclass


from faststream.rabbit import RabbitRoute, RabbitRouter, RabbitQueue

from cattle_grid.app import access_methods


def rabbit_queue_for_name_and_routing_key(name, routing_key, number: int):
    return RabbitQueue(
        name.replace(" ", "_") + f"_{routing_key}_{number}",
        routing_key=routing_key,
        durable=True,
    )


@dataclass
class Route:
    func: Callable
    routing_key: str
    name: str
    exchange_name: str

    def build(self, routing_keys):
        if self.exchange_name == "activity":
            exchange = access_methods.get_activity_exchange()
        elif self.exchange_name == "account":
            exchange = access_methods.get_account_exchange()
        else:
            raise Exception(f"unknown exchange name {self.exchange_name}")

        number = len([x for x in routing_keys if x == self.routing_key])

        routing_keys.append(self.routing_key)

        return RabbitRoute(
            self.func,
            queue=rabbit_queue_for_name_and_routing_key(
                self.name, self.routing_key, number
            ),
            exchange=exchange,
            title=self.routing_key,
        )


def build_router(routes: list[Route]) -> RabbitRouter:
    routing_keys = []
    handlers = []
    for route in routes:
        handlers.append(route.build(routing_keys))
    return RabbitRouter(handlers=handlers)
