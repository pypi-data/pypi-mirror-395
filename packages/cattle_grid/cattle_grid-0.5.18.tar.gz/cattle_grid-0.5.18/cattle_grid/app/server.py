from fastapi import FastAPI

from cattle_grid.version import __version__


def build_fastapi_app(lifespan, extensions):
    from cattle_grid.activity_pub.server import router as ap_router
    from cattle_grid.auth import auth_router
    from cattle_grid.account.server import router as fe_router
    from cattle_grid.account.rabbit import rabbit_router

    from cattle_grid.extensions.load import add_routes_to_api

    tags_description = [
        {
            "name": "activity_pub",
            "description": "Endpoints used and consumed by other Fediverse applications to communicate through cattle_grid",
        },
        {
            "name": "auth",
            "description": """Authentication endpoints
    
The auth endpoint allows one to check the HTTP Signature
and reject requests with an invalid one, only based on the
headers. This step then occurs before the request is passed
to the application. Furthermore, this behavior can be shared
accross many services.""",
        },
    ]

    app = FastAPI(
        lifespan=lifespan,
        title="cattle_grid",
        description="middle ware for the Fediverse",
        version=__version__,
        openapi_tags=tags_description,
    )

    app.include_router(ap_router)
    app.include_router(
        auth_router,
        prefix="/auth",
    )

    app.include_router(fe_router, prefix="/fe")
    app.include_router(rabbit_router)

    add_routes_to_api(app, extensions)

    @app.get("/")
    async def main() -> str:
        return "cattle_grid"

    return app


def build_lifespan(extensions):
    from faststream.rabbit import RabbitBroker
    from contextlib import asynccontextmanager
    from cattle_grid.app.lifespan import run_broker, common_lifespan
    from cattle_grid.testing.accounts import create_test_accounts
    from cattle_grid.exchange.exception import exception_middleware
    from cattle_grid.database import upgrade_sql_alchemy

    from cattle_grid.extensions.load import lifespan_from_extensions

    from cattle_grid.dependencies.globals import global_container
    from cattle_grid.app import app_globals
    from cattle_grid.app.router import add_routers_to_broker

    @asynccontextmanager
    async def lifespan(app: FastAPI, broker: RabbitBroker | None = None):
        if broker is None:
            broker = global_container.broker
        broker.add_middleware(exception_middleware)
        async with common_lifespan():  # type:ignore
            await upgrade_sql_alchemy(app_globals.engine)

            async with lifespan_from_extensions(extensions):
                if app_globals.config.processor_in_app:
                    add_routers_to_broker(broker, extensions, app_globals.config)
                await create_test_accounts()

                async with run_broker(broker):
                    yield

    return lifespan
