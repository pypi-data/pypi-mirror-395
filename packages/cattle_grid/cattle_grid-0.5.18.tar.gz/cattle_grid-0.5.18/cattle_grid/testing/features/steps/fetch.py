import json
import logging
from unittest.mock import MagicMock
from behave import when, then, given

from bovine.activitystreams.collection_helper import CollectionHelper

from cattle_grid.testing.features import fetch_request

logger = logging.getLogger(__name__)


@given('"{alice}" fetches the ActivityPub object')  # type: ignore
@when('"{alice}" fetches the ActivityPub object')  # type: ignore
async def alice_fetches_the_activity_pub_object(context, alice):
    """This routine causes the URI stored in
    `context.actiivty_pub_uri` to be fetched by the
    actor corresponding to `alice`.

    ```gherkin
    Given "Alice" fetches the ActivityPub object
    ```

    or

    ```gherkin
    When "Alice" fetches the ActivityPub object
    ```
    """
    result = await fetch_request(context, alice, context.activity_pub_uri)

    assert isinstance(result, dict), json.dumps(result)

    context.fetch_response = result


@then('The response is of type "{object_type}"')  # type: ignore
def check_response_type(context, object_type):
    """Checks that the result in `context.fetch_response is of a predetermined type

    ```gherkin
    Then The response is of type "Page"
    ```
    """
    assert context.fetch_response.get("type") == object_type


@then("The request fails")  # type: ignore
def check_fail(context):
    """Checks that the result in `context.fetch_response indicates failure.

    ```gherkin
    Then The request fails
    ```
    """
    assert context.fetch_response.get("type") == "Tombstone"


@then('The ActivityPub object has a "{collection}" collection')  # type: ignore
def object_has_collection(context, collection):
    """Checks that the result from [alice_fetches_the_activity_pub_object][cattle_grid.testing.features.steps.fetch.alice_fetches_the_activity_pub_object]
    has a property of type "collection"

    ```gherkin
    Then The ActivityPub object has a "likes" collection
    ```
    """
    assert collection in context.fetch_response, json.dumps(context.fetch_response)


async def all_elements_from_collection(fetcher, collection_uri: str):
    actor = MagicMock()
    actor.proxy = fetcher

    collection = CollectionHelper(collection_uri, actor)

    return (await collection.as_collection()).get("items", [])


@then('For "{alice}", the "{collection}" collection contains "{number}" element')  # type: ignore
async def alices_collection_has_number_of_elements(context, alice, collection, number):
    """Checks that the result from [alice_fetches_the_activity_pub_object][cattle_grid.testing.features.steps.fetch.alice_fetches_the_activity_pub_object]
    has a "collection" containing number of elements. Specifying an actor, e.g. "Alice",
    is necessary as a fetch request is performed.

    ```gherkin
    Then For "Alice", the "likes" collection contains "no" element
    ```
    """
    collection_uri = context.fetch_response[collection]

    async def fetcher(uri):
        result = await fetch_request(context, alice, uri)
        logger.debug(json.dumps(result, indent=2))
        return result

    items = await all_elements_from_collection(fetcher, collection_uri)

    # items = result.get("orderedItems", [])

    if number == "no":
        assert len(items) == 0, items
    elif number == "one":
        assert len(items) == 1, items
        context.interaction_id = items[0]
    else:
        raise Exception("Unsupported number of elements")
