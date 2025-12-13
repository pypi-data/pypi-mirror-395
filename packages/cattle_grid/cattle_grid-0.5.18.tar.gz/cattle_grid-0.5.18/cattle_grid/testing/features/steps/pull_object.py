from behave_auto_docstring import when, then

from cattle_grid.testing.features import fetch_request


@when('"{actor}" retrieves the object with the actor id of "{target}"')
async def retrieve_object(context, actor, target):
    context.result = await fetch_request(
        context,
        actor,
        context.actors[target].get("id"),
    )


@when('"{actor}" retrieves the object with id "{uri}"')
async def retrieve_object_by_uri(context, actor, uri):
    context.result = await fetch_request(
        context,
        actor,
        uri,
    )


@then('The retrieved object is the profile of "{username}"')
def check_result_is_actor(context, username):
    assert context.result.get("type") == "Person"
    assert context.result.get("id") == context.actors[username].get("id")
