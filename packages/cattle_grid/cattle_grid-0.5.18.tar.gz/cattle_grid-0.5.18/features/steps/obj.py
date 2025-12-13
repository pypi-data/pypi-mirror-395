import os

from behave import given

activity_pub_object = os.environ.get("ACTIVITY_PUB_OBJECT")

if activity_pub_object:

    @given("An ActivityPub object")  # type: ignore
    def step_impl(context):
        context.activity_pub_uri = activity_pub_object
