from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any


from cattle_grid.dependencies import SqlAsyncEngine


def skip_method_information(routing_key):
    """Method information is not created for subscribtions to incoming.* or outgoing.*

    as only cattle_grid should publish to these
    routing keys

    ```pycon
    >>> skip_method_information("incoming.test")
    True

    >>> skip_method_information("outgoing.test")
    True

    >>> skip_method_information("test")
    False

    ```
    """

    if routing_key.startswith("incoming.") or routing_key.startswith("outgoing."):
        return True

    return False


def lifespan_for_sql_alchemy_base_class(
    base_class,
) -> Callable[[SqlAsyncEngine], Any]:
    """Creates a lifespan that creates the sql alchemy models for the base_class.

    Usage

    ```python
    extension = Extension(
        name="my sample extension",
        module=__name__,
        lifespan=lifespan_for_sql_alchemy_base_class(Base),
    )
    ```
    """

    @asynccontextmanager
    async def lifespan(engine: SqlAsyncEngine):
        async with engine.begin() as conn:
            await conn.run_sync(base_class.metadata.create_all)

        yield

    return lifespan
