from faststream import Context, ExceptionMiddleware

import logging

from cattle_grid.model.account import ErrorMessage
from cattle_grid.dependencies import AccountExchangePublisher

from .annotations import AccountName, RoutingKey

logger = logging.getLogger(__name__)

exception_middleware = ExceptionMiddleware()


@exception_middleware.add_handler(Exception)
async def exception_handler(
    exception: Exception,
    name: AccountName,
    routing_key: RoutingKey,
    publisher: AccountExchangePublisher,
    message_body=Context("message.body"),
):
    logger.warning("Processing error occurred for %s", name)
    logger.debug(exception)

    error_message = ErrorMessage(
        message=str(exception).split("\n"),
        routing_key=routing_key,
        original_message_body=message_body.decode(),
    )

    await publisher(error_message, routing_key=f"error.{name}")
