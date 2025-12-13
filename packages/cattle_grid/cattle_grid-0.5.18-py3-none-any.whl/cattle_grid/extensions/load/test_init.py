from cattle_grid.model.lookup import Lookup
from cattle_grid.testing import mocked_session

from . import build_lookup, load_extension, collect_method_information


async def test_build_lookup():
    extensions = [
        load_extension({"module": "cattle_grid.extensions.examples.webfinger_lookup"})
    ]
    with mocked_session():
        lookup = build_lookup(extensions)
        data = Lookup(uri="http://remote.example", actor="http://actor.example")
        await lookup(data)


async def test_collect_method_information():
    extensions = [
        load_extension({"module": "cattle_grid.extensions.examples.simple_storage"})
    ]

    method_information = collect_method_information(extensions)

    assert len(method_information) == 3

    assert {x.routing_key for x in method_information} == {
        "publish_activity",
        "publish_object",
        "admin_simple_storage",
    }
