from contextlib import asynccontextmanager
import logging
import re

import aiohttp
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from cattle_grid.app import app_globals

logger = logging.getLogger(__name__)


@asynccontextmanager
async def run_broker(broker: RabbitBroker):
    if app_globals.application_config is None:
        raise Exception("Application not configured")

    if app_globals.application_config.amqp_url == "amqp://:memory:":
        logger.warning("Using in memory amqp")
        from faststream.rabbit import TestRabbitBroker

        async with TestRabbitBroker(broker) as br:
            app_globals.broker = br
            yield
    else:
        await broker.start()

        yield
        await broker.stop()


@asynccontextmanager
async def alchemy_database(db_url: str | None = None, echo: bool = False):
    """Initializes the sql alchemy engine"""

    if db_url is None:
        if app_globals.application_config is None:
            raise Exception("Application not configured")
        db_url = app_globals.application_config.db_url

    if app_globals.engine or app_globals.async_session_maker:
        raise ValueError("Database already initialized")

    app_globals.engine = create_async_engine(db_url, echo=echo)
    app_globals.async_session_maker = async_sessionmaker(
        app_globals.engine, expire_on_commit=False
    )
    logger.debug(
        "Connected to %s with sqlalchemy", re.sub("://.*@", "://***:***@", db_url)
    )

    yield app_globals.engine

    await app_globals.engine.dispose()
    app_globals.engine = None
    app_globals.async_session_maker = None


@asynccontextmanager
async def session_lifespan():
    async with aiohttp.ClientSession() as session:
        app_globals.session = session
        yield session
        app_globals.session = None


@asynccontextmanager
async def common_lifespan():
    async with session_lifespan():
        async with alchemy_database():
            yield
