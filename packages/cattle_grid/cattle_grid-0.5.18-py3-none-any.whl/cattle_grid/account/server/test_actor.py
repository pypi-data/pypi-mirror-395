import json
import pytest

from unittest.mock import AsyncMock, MagicMock

from cattle_grid.testing.fixtures import *  # noqa
from .testing import *  # noqa


@pytest.mark.parametrize(
    "endpoint,data",
    [
        ("/actor/lookup", {"actorId": "bad_actor", "uri": "http://remote.test/"}),
        ("/actor/trigger/method", {"actor": "bad_actor", "data": {}, "method": "none"}),
    ],
)
def test_bad_actor(test_client, bearer_header, endpoint, data):
    result = test_client.post(
        endpoint,
        json=data,
        headers=bearer_header,
    )

    assert result.status_code == 400


def test_lookup_no_result(test_client, actor_id, bearer_header, test_broker):
    test_broker.request = AsyncMock(
        return_value=MagicMock(body=json.dumps({"raw": {}}))
    )
    result = test_client.post(
        "/actor/lookup",
        json={"actorId": actor_id, "uri": "http://remote.test/"},
        headers=bearer_header,
    )

    assert result.status_code == 200
    assert result.json() == {"raw": {}}


def test_lookup_result(test_client, actor_id, bearer_header, test_broker):
    test_broker.request = AsyncMock(
        return_value=MagicMock(body=json.dumps({"raw": {"data": 1}}))
    )

    result = test_client.post(
        "/actor/lookup",
        json={"actorId": actor_id, "uri": "http://remote.test/"},
        headers=bearer_header,
    )

    assert result.status_code == 200
    assert result.json() == {"raw": {"data": 1}}


def test_perform_action(test_client, actor_id, bearer_header, test_broker):
    data = {"actor": actor_id, "data": {"moo": "yes"}}

    result = test_client.post(
        "/actor/trigger/method",
        json=data,
        headers=bearer_header,
    )

    assert result.status_code == 202
    test_broker.publish.assert_awaited_once()

    args = test_broker.publish.call_args.args[0]

    assert args == data
