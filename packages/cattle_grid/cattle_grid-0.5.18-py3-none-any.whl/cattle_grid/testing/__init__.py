import logging


from contextlib import contextmanager
from unittest.mock import AsyncMock
import aiohttp
from dynaconf import Dynaconf
from dynaconf.utils import DynaconfDict

from cattle_grid.app import app_globals

logger = logging.getLogger(__name__)


@contextmanager
def mocked_config(config: Dynaconf | dict):
    """overrides the configuration stored in `app_globals.config`
    with the value in dict, afterwards resets the original value."""
    if isinstance(config, dict):
        config = DynaconfDict(config)
    old_app_config = app_globals.config

    app_globals.config = config

    yield

    app_globals.config = old_app_config


@contextmanager
def mocked_session():
    """overrides the global session"""
    old_session = app_globals.session

    app_globals.session = AsyncMock(aiohttp.ClientSession)

    yield

    app_globals.session = old_session
