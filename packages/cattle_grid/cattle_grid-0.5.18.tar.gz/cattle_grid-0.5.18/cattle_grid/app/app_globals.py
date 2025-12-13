from typing import Callable
import aiohttp
from faststream.rabbit import RabbitBroker, RabbitExchange
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from cattle_grid.app.load_globals import (
    construct_account_exchange,
    construct_activity_exchange,
    construct_internal_exchange,
)
from cattle_grid.config import load_settings
from cattle_grid.config.application import ApplicationConfig

config = load_settings()

application_config: ApplicationConfig = ApplicationConfig.from_settings(config)
internal_exchange: RabbitExchange = construct_internal_exchange(config)
activity_exchange: RabbitExchange = construct_activity_exchange(config)
account_exchange: RabbitExchange = construct_account_exchange(config)

broker: RabbitBroker | None = None

engine: AsyncEngine | None = None
async_session_maker: Callable[[], AsyncSession] | None = None
session: aiohttp.ClientSession | None = None
