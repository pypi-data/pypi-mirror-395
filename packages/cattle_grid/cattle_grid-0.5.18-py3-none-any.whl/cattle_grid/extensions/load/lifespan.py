from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import logging
from typing import Callable, List, AsyncContextManager, Any
from fast_depends import inject
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker

from cattle_grid.app import app_globals
from cattle_grid.app.lifespan import common_lifespan
from cattle_grid.dependencies.globals import global_container
from cattle_grid.extensions import Extension
from cattle_grid.model.extension import (
    AddMethodInformationMessage,
    MethodInformationModel,
)

logger = logging.getLogger(__name__)


def collect_lifespans(
    extensions: List[Extension],
) -> List[Callable[[Any], AsyncContextManager]]:
    """Collects the lifespans from the extensions"""
    return [extension.lifespan for extension in extensions if extension.lifespan]


@asynccontextmanager
async def iterate_lifespans(lifespans: List[Callable[[Any], AsyncContextManager]]):
    if len(lifespans) == 0:
        yield
        return

    async with inject(lifespans[0])():  # type: ignore
        if len(lifespans) == 1:
            yield
        else:
            async with iterate_lifespans(lifespans[1:]):
                yield


async def publish_method_information(
    broker: RabbitBroker, method_information: list[MethodInformationModel]
):
    await broker.publish(
        AddMethodInformationMessage(method_information=method_information),
        exchange=app_globals.activity_exchange,
        routing_key="add_method_information",
    )


def lifespan_for_extension(extension: Extension, include_broker: bool = False):
    broker = None

    if include_broker and extension.activity_router:
        broker = global_container.broker
        broker.include_router(extension.activity_router)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
        async with common_lifespan():
            if broker:
                await broker.start()
                if len(extension.method_information):
                    await publish_method_information(
                        broker, extension.method_information
                    )
            if extension.lifespan:
                async with inject(extension.lifespan)():  # type: ignore
                    yield
            else:
                yield

            if broker:
                await broker.stop()

    return lifespan


@asynccontextmanager
async def lifespan_from_extensions(extensions: list[Extension]):
    """Creates the lifespan from the extensions"""
    lifespans = collect_lifespans(extensions)

    async with iterate_lifespans(lifespans):
        yield
