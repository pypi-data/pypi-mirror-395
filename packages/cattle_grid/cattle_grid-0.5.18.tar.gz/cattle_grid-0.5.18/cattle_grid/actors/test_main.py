from click.testing import CliRunner

from cattle_grid.testing.cli import *  # noqa

from .__main__ import main


def test_list(db_url, create_database):
    runner = CliRunner(env={"CATTLE_GRID_DB_URL": db_url})
    result = runner.invoke(main, ["list"])

    assert result.exit_code == 0
