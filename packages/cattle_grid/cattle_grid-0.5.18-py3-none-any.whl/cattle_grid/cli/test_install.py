import pytest
import click

from dynaconf.utils import DynaconfDict

from click.testing import CliRunner

from .install import add_install_commands


@pytest.fixture
def config():
    settings = DynaconfDict(
        {
            "db_url": "some",
            "amqp_url": "some",
            "frontend": {"base_urls": ["http://host.test"]},
        }
    )
    return settings


@pytest.fixture
def cli(tmp_path, config):
    @click.group()
    @click.pass_context
    def main(ctx):
        ctx.ensure_object(dict)
        ctx.obj["config"] = config

    add_install_commands(main)

    return main


def test_basic_command(cli):
    result = CliRunner().invoke(cli, ["install", "verify", "--dry-run"])

    assert result.exit_code == 0
