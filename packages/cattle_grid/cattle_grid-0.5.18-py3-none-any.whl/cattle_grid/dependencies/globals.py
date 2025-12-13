import logging

from dataclasses import dataclass
from typing import Callable, Awaitable, Dict, List
from functools import cached_property


from sqlalchemy.ext.asyncio import AsyncEngine
from dynaconf import Dynaconf
from dynaconf.utils import DynaconfDict

from faststream.rabbit import RabbitBroker

from cattle_grid.app import app_globals

from cattle_grid.config.logging import configure_logging
from cattle_grid.config.rewrite import RewriteConfiguration
from cattle_grid.config import load_settings, default_filenames
from cattle_grid.model.lookup import LookupMethod
from cattle_grid.model.extension import MethodInformationModel


logger = logging.getLogger(__name__)


@dataclass
class GlobalContainer:
    method_information: List[MethodInformationModel] | None = None

    transformer: Callable[[Dict], Awaitable[Dict]] | None = None
    lookup: LookupMethod | None = None

    _config: Dynaconf | DynaconfDict | None = None
    _rewrite_rules: RewriteConfiguration | None = None

    def __post_init__(self):
        self.load_config()

    def get_config(self):
        if self._config is None:
            raise ValueError("Config not loaded")
        return self._config

    @property
    def config(self):
        if self._config is None:
            raise ValueError("Config not loaded")
        return self._config

    def load_config(self, filenames: list[str] = default_filenames):
        self._config = load_settings(filenames)
        self._rewrite_rules = RewriteConfiguration.from_rules(
            self._config.get("rewrite")  # type: ignore
        )
        configure_logging(self._config)

    @cached_property
    def broker(self) -> RabbitBroker:
        if not app_globals.application_config:
            raise Exception("Please configure application")

        amqp_url = app_globals.application_config.amqp_url
        if amqp_url == "amqp://:memory:":
            return RabbitBroker("amqp://localhost")
        return RabbitBroker(amqp_url)

    def get_broker(self) -> RabbitBroker:
        return self.broker

    def get_rewrite_rules(self) -> RewriteConfiguration:
        if not self._rewrite_rules:
            raise ValueError("Rules not loaded")
        return self._rewrite_rules


global_container = GlobalContainer()


def get_transformer() -> Callable[[Dict], Awaitable[Dict]]:
    global global_container

    if not global_container.transformer:
        raise ValueError("Transformer not initialized")

    return global_container.transformer


def get_lookup() -> LookupMethod:
    global global_container

    if not global_container.lookup:
        raise ValueError("Lookup not initialized")

    return global_container.lookup


def get_engine() -> AsyncEngine:
    if not app_globals.engine:
        raise ValueError("Engine not initialized")

    return app_globals.engine


def get_method_information() -> List[MethodInformationModel]:
    global global_container

    if global_container.method_information is None:
        raise ValueError("Method information not initialized")

    return global_container.method_information
