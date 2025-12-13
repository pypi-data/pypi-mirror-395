"""The before_all, _scenario, and after_scenario functions
need to be imported in your environment.py file, e.g.

```python title="features/environment.py"
--8<-- "./features/environment.py"
```
"""

import aiohttp
import asyncio
import logging

from almabtrieb import Almabtrieb
from behave.runner import Context
from behave.model import Scenario

from almabtrieb.stream import StreamNoNewItemException

from cattle_grid.app import app_globals
from cattle_grid.account.account import delete_account
from cattle_grid.database import database_session
from .reporting import publish_reporting

logger = logging.getLogger(__name__)


async def create_session(context: Context):
    if not context.session:
        context.session = aiohttp.ClientSession()


async def log_errors_in_connection(name: str, connection: Almabtrieb):
    try:
        while item := await connection.error().next(timeout=0.3):
            print(f"{name} got the error")
            print(item)
            print()
    except StreamNoNewItemException:
        ...


async def send_delete_for_actor(context: Context, name: str, connection: Almabtrieb):
    if name in context.actors:
        await connection.trigger(
            "delete_actor",
            {
                "actor": context.actors[name].get("id"),
            },
        )
        await asyncio.sleep(0.02)


async def close_session(context: Context):
    async with database_session(db_url=app_globals.config.db_url) as session:  # type: ignore
        for name, connection in context.connections.items():
            await log_errors_in_connection(name, connection)
            try:
                await send_delete_for_actor(context, name, connection)
                await delete_account(session, name, name)
            except Exception as e:
                logger.exception(e)
            connection.task.cancel()
            try:
                await connection.task
            except asyncio.CancelledError:
                pass

    await context.session.close()


def before_all(context: Context):
    """Called in features/environment.py

    Ensures that default variables, `context.session`, `.actors`, `.connections`
    exist.
    """
    context.session = None

    context.actors = {}
    context.connections = {}


def before_scenario(context: Context, scenario: Scenario):
    """Called in features/environment.py

    Opens an [aiohttp.ClientSession][] and sets it to `context.session`.
    """
    asyncio.get_event_loop().run_until_complete(create_session(context))

    context.actors = {}
    context.connections = {}

    asyncio.get_event_loop().run_until_complete(
        publish_reporting(
            "scenario",
            {
                "name": scenario.name,
                "file": scenario.filename,
                "description": scenario.description,
            },
        )
    )


def after_scenario(context: Context, scenario: Scenario):
    """Called in features/environment.py

    Deletes the created actors and associated accounts.
    Closes the aiohttp.ClientSession.
    """

    asyncio.get_event_loop().run_until_complete(
        publish_reporting(
            "scenario_end",
            {},
        )
    )

    if context.session:
        asyncio.get_event_loop().run_until_complete(close_session(context))
        context.session = None
