import logging
from sqlalchemy.ext.asyncio import AsyncSession

from .account import list_permissions
from cattle_grid.database.account import Account
from cattle_grid.app import app_globals

logger = logging.getLogger(__name__)


def base_urls_for_permissions(permissions: list[str]) -> list[str]:
    settings = app_globals.config

    if "admin" in permissions:
        frontend_settings = settings.get("frontend", {})

        return frontend_settings.get("base_urls", [])

    permission_settings = settings.get("permissions", {})
    return sum(
        (permission_settings.get(p, {}).get("base_urls", []) for p in permissions),
        [],
    )


async def allowed_base_urls(session: AsyncSession, account: Account) -> list[str]:
    """Returns the set of base_urls the account
    is allowed to use to create an actor"""
    await session.refresh(account, attribute_names=["permissions"])

    permissions = list_permissions(account)

    return base_urls_for_permissions(permissions)


async def can_create_actor_at_base_url(
    session: AsyncSession, account: Account, base_url: str
) -> bool:
    """Checks if the account is allowed to create an actor
    at the base url"""
    allowed_urls = await allowed_base_urls(session, account)

    if base_url in allowed_urls:
        return True

    logger.warning(
        "%s tried to create an actor with base url %s, not in set of allowed %s",
        account.name,
        base_url,
        ", ".join(allowed_urls),
    )

    return False
