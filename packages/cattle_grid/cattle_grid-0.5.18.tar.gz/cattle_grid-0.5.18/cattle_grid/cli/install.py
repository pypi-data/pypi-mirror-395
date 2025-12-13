import asyncio
import logging
import aiohttp
import click

from cattle_grid.config.application import ApplicationConfig

logger = logging.getLogger(__name__)


async def verify_connectivity(base_urls: list[str]):
    async with aiohttp.ClientSession() as session:
        for x in base_urls:
            logger.info("Verifying connectivity for %s", x)
            url = f"{x}/.well-known/nodeinfo"
            async with session.get(url) as response:
                if response.status != 200:
                    logger.warning(f"Got status {response.status} for {url}")
                content_type = response.headers["content-type"]
                if content_type != "application/jrd+json":
                    logger.warning(f"Got content type {content_type} for {url}")


def add_install_commands(main: click.Group):
    @main.group()
    def install(): ...

    @install.command()
    @click.option("--dry-run", default=False, is_flag=True)
    @click.pass_context
    def verify(ctx, dry_run):
        """verifies the installation. Current checks that the base_urls have a correctly configured nodeinfo response"""

        app_config = ApplicationConfig.from_settings(ctx.obj["config"])
        base_urls = app_config.frontend_config.base_urls

        if not dry_run:
            asyncio.run(verify_connectivity(base_urls))
        else:
            logger.info("Got base urls %s", ", ".join(base_urls))
