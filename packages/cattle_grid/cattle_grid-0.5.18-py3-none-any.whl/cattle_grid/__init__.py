import logging

from fastapi import FastAPI


from .version import __version__

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(run_migration: bool = True) -> FastAPI:
    logger.info("Running cattle grid version %s", __version__)
    from cattle_grid.app import app_globals
    from .app.extensions import init_extensions
    from .config.logging import configure_logging

    configure_logging(app_globals.config)

    logger.info("Configuration loaded")

    import os

    alembic_config = __file__.replace("__init__.py", "alembic.ini")

    if run_migration:
        os.system(f"python -malembic -c {alembic_config} upgrade head")

    extensions = init_extensions(app_globals.config)

    from cattle_grid.app.server import build_fastapi_app, build_lifespan

    lifespan = build_lifespan(extensions)

    app = build_fastapi_app(lifespan, extensions)

    return app
