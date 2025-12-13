from faststream.rabbit import RabbitExchange

from . import app_globals


def raise_if_none(exchange: RabbitExchange | None) -> RabbitExchange:
    if exchange is None:
        raise Exception("Exchange is not configured")
    return exchange


def get_internal_exchange() -> RabbitExchange:
    return raise_if_none(app_globals.internal_exchange)


def get_activity_exchange() -> RabbitExchange:
    return raise_if_none(app_globals.activity_exchange)


def get_account_exchange() -> RabbitExchange:
    return raise_if_none(app_globals.account_exchange)
