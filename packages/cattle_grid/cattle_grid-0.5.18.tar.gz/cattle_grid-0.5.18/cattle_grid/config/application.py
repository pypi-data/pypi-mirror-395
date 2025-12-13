import logging
from dynaconf import Dynaconf
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class FrontendConfig(BaseModel):
    """Configuration for the frontend"""

    base_urls: list[str] = Field(
        default=[],
        description="List of possible base urls. Accounts in the admin group can create actors one these. Other accounts need to have an appropriate permission.",
    )

    timeout_amqp_request: float = Field(
        default=10.0, description="Timeout when performing an AMQP RPC call"
    )


class ApplicationConfig(BaseModel):
    """Configuration values relevant to the base application"""

    db_url: str = Field(description="Database URL")
    amqp_url: str = Field(description="location of the rabbitmq broker")
    testing: bool = Field(description="wether the application is in testing mode")

    frontend_config: FrontendConfig = Field(description="frontend configuration")

    @staticmethod
    def from_settings(settings: Dynaconf) -> "ApplicationConfig":
        db_url = settings.get("db_url")
        if db_url is None:
            db_url = settings.db_uri
            logger.warning("Please update db_uri to db_url")

        amqp_url = settings.get("amqp_url")
        if amqp_url is None:
            amqp_url = settings.amqp_uri
            logger.warning("Please update amqp_uri to amqp_url")

        testing = settings.get("testing", {}).get("enabled", False)
        if testing:
            logger.warning("Running in TESTING mode")

        frontend_config = FrontendConfig.model_validate(settings.get("frontend", {}))

        return ApplicationConfig(
            db_url=db_url,
            amqp_url=amqp_url,
            testing=testing,
            frontend_config=frontend_config,
        )
