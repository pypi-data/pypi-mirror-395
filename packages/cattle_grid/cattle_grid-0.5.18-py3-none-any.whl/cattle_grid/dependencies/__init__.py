"""Dependencies injected by fast_depends

cattle_grid uses dependencies to manage objects, one needs access to.
This works by declaring them using [fast_depends.Depends][] and then
injecting them using [fast_depends.inject][].

For example if you want to make a webrequest using the
[aiohttp.ClientSession][], you could use

```python
from cattle_grid.dependencies import ClientSession

async def web_request(session: ClientSession):
    response = await session.get("...")
```

This function can then be called via

```python
from fast_depends import inject

await inject(web_request)()
```

This package contains annotations that should be available in all code
using cattle_grid, i.e. extensions. The sub packages contain methods
for more specific use cases.
"""

import aiohttp
import logging

from typing import Annotated, Callable
from dynaconf import Dynaconf
from fast_depends import Depends


from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from cattle_grid.app import app_globals as app_globals

from .globals import get_engine, global_container
from .internals import (
    AccountExchangePublisherClass,
    ActivityExchangePublisherClass,
    ActivityExchangeRequesterClass,
    InternalExchangePublisherClass,
    InternalExchangeRequesterClass,
    AccountExchange,  # noqa: F401
    ActivityExchange,  # noqa: F401
)


logger = logging.getLogger(__name__)


async def get_client_session():
    yield app_globals.session


ClientSession = Annotated[aiohttp.ClientSession, Depends(get_client_session)]
"""The [aiohttp.ClientSession][] used by the application"""


SqlAsyncEngine = Annotated[AsyncEngine, Depends(get_engine)]
"""Returns the SqlAlchemy AsyncEngine"""


async def with_sql_session():
    if app_globals.async_session_maker is None:
        raise Exception("Database not initialized")
    async with app_globals.async_session_maker() as session:
        yield session


SqlSession = Annotated[AsyncSession, Depends(with_sql_session)]
"""SQL session that does not commit afterwards"""


async def with_session_commit(session: SqlSession):
    yield session
    await session.commit()


CommittingSession = Annotated[AsyncSession, Depends(with_session_commit)]
"""Session that commits the transaction"""

Config = Annotated[Dynaconf, Depends(global_container.get_config)]
"""Returns the configuration"""


AccountExchangePublisher = Annotated[Callable, Depends(AccountExchangePublisherClass)]
"""Publishes a message to the activity exchange"""

InternalExchangePublisher = Annotated[Callable, Depends(InternalExchangePublisherClass)]
"""Publishes a message to the internal exchange"""

InternalExchangeRequester = Annotated[Callable, Depends(InternalExchangeRequesterClass)]
"""Request a message to the internal exchange. """

ActivityExchangePublisher = Annotated[Callable, Depends(ActivityExchangePublisherClass)]
"""Publishes a message to the activity exchange. Sample usage:

```python
async def my_method(publisher: ActivityExchangePublisher):
    message = {"actor": my_actor_id, "data": {"type": "Activity"}}
    await publisher(message, routing_key="send_message")
```
"""

ActivityExchangeRequester = Annotated[Callable, Depends(ActivityExchangeRequesterClass)]
"""Publishes a message to the activity exchange. Sample usage:

```python
async def my_method(requester: ActivityRequesterPublisher):
    message = {"actor": my_actor_id, "data": {"type": "Activity"}}
    await requester(message, routing_key="fetch")
```
"""
