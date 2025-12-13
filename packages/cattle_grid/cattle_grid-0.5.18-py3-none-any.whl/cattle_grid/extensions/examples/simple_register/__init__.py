"""
This extension is meant to create an endpoint, where people can register.
It is deployed on [dev.bovine.social](https://dev.bovine.social), and can
be seen as an opportunity to test cattle_grid's public APIs.

Sample configuration, see [RegisterConfiguration][cattle_grid.extensions.examples.simple_register.config.RegisterConfiguration]
for details.

```toml
[[extensions]]
module = "cattle_grid.extensions.examples.simple_register"
api_prefix = "/simple_register"

[[extensions.config.registration_types]]
name = "dev"
permissions = ["dev"]
extra_parameters = ["fediverse"]
create_default_actor_on = "https://dev.bovine.social"
```

The parameter `create_default_actor_on` causes an actor to be created.
It will

* have the acct-uri `acct:{name}@dev.bovine.social`.
* be linked to the account `name` with the name `default`.
* automatically accept followers.

"""

from fastapi import HTTPException, Request

from cattle_grid.account import (
    create_account,
    AccountAlreadyExists,
    add_actor_to_account,
)
from cattle_grid.activity_pub import create_actor, compute_acct_uri, identifier_exists
from cattle_grid.dependencies.fastapi import SqlSession
from cattle_grid.extensions import Extension
from cattle_grid.tools.fastapi.http_util import parse_content_type_header


from .config import RegisterConfiguration

extension = Extension("simple_register", __name__, config_class=RegisterConfiguration)
"""Definition of the extension"""


def determine_registration_type(config: RegisterConfiguration, name):
    for registration_type in config.registration_types:
        if registration_type.name == name:
            return registration_type
    return None


@extension.post("/register/{name}", status_code=201)
async def post_register(
    name,
    request: Request,
    config: extension.ConfigFastAPI,  # type: ignore
    session: SqlSession,
):
    registration_type = determine_registration_type(config, name)

    if registration_type is None:
        raise HTTPException(404)

    content_type_header = parse_content_type_header(
        request.headers.get("content-type", "")
    )

    if content_type_header.media_type == "application/json":
        body = await request.json()
    elif content_type_header.media_type in [
        "application/x-www-form-urlencoded",
        "multipart/form-data",
    ]:
        body = await request.form()
    else:
        raise HTTPException(400, detail="Content type not understood")

    expected_keys = {"name", "password"} | set(registration_type.extra_parameters)

    if expected_keys != set(body.keys()):
        raise HTTPException(422)

    if any(not isinstance(body[x], str) for x in body):
        raise HTTPException(422)

    account_name: str = body["name"]  # type: ignore

    if registration_type.create_default_actor_on:
        acct_uri = compute_acct_uri(
            registration_type.create_default_actor_on, account_name
        )
        if await identifier_exists(session, acct_uri):
            raise HTTPException(409, f"Acct URI {acct_uri} already exists")
    meta_information: dict[str, str] = {
        key: body[key] for key in registration_type.extra_parameters
    }  # type: ignore
    try:
        account = await create_account(
            session=session,
            name=account_name,
            password=body["password"],  # type: ignore
            permissions=registration_type.permissions,
            meta_information=meta_information,
        )

        if registration_type.create_default_actor_on and account:
            actor = await create_actor(
                session,
                base_url=registration_type.create_default_actor_on,
                preferred_username=account_name,
                automatically_accept_followers=True,
            )
            await add_actor_to_account(session, account, actor, name="default")

    except AccountAlreadyExists:
        raise HTTPException(409)
