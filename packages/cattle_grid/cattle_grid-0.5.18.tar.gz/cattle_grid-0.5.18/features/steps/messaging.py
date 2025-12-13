from behave import then, given


@then("no result is returned")  # type: ignore
def no_result(context):
    assert context.result is None


@given('"Alice" has messaged "Bob"')  # type: ignore
def step_impl(context):
    context.execute_steps(
        """
        When "Alice" sends "Bob" a message saying "Hello Bob"
        Then "Bob" receives a message saying "Hello Bob"
    """
    )
