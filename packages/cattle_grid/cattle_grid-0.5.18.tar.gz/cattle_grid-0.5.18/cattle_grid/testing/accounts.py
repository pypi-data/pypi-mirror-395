import logging

from sqlalchemy.ext.asyncio import AsyncSession

from cattle_grid.account.account import AccountAlreadyExists, create_account
from cattle_grid.dependencies.globals import global_container

from cattle_grid.activity_pub.actor import create_actor
from cattle_grid.database.account import ActorForAccount

from cattle_grid.app import app_globals

logger = logging.getLogger(__name__)


async def create_test_accounts(session: AsyncSession | None = None):
    if not app_globals.application_config.testing:
        return

    if not session:
        if not app_globals.async_session_maker:
            raise Exception("Database no tinitialize")
        session = app_globals.async_session_maker()

    logger.warning("running in testing mode")
    logger.warning(
        "\n   __            __  _            \n  / /____  _____/ /_(_)___  ____ _\n / __/ _ \\/ ___/ __/ / __ \\/ __ `/\n/ /_/  __(__  ) /_/ / / / / /_/ / \n\\__/\\___/____/\\__/_/_/ /_/\\__, /  \n                         /____/   \n"
    )
    config = global_container.get_config().testing

    accounts: list[dict] = config.accounts  # type:ignore

    for info in accounts:
        try:
            account = await create_account(
                session,
                info["name"],
                info["password"],
                permissions=info.get("permissions", []),
                meta_information=info.get(
                    "meta_information", {"testing": "created by testing"}
                ),
            )
            logger.info("created account %s", info["name"])

            actors = info.get("actors", [])
            for actor_info in actors:
                actor = await create_actor(
                    session,
                    actor_info.get("base_url"),
                    preferred_username=actor_info.get("handle"),
                )
                actor.automatically_accept_followers = True
                session.add(
                    ActorForAccount(
                        account=account,
                        actor=actor.actor_id,
                        name=actor_info.get("name"),
                    )
                )

                await session.commit()

        except AccountAlreadyExists:
            pass
