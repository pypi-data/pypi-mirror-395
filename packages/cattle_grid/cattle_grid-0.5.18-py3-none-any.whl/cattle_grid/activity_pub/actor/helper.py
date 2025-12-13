import secrets

from urllib.parse import urljoin, urlparse


def shared_inbox_from_actor_id(actor_id: str) -> str:
    """Returns the shared inbox of the actor identified by actor_id

    ```pycon
    >>> shared_inbox_from_actor_id("http://host.test/actor/someId")
    'http://host.test/shared_inbox'

    ```
    """

    return urljoin(actor_id, "/shared_inbox")


def endpoints_object_from_actor_id(actor_id: str) -> dict:
    """Returns the endpoints object of the actor identified by actor_id

    ```pycon
    >>> endpoints_object_from_actor_id("http://host.test/actor/someId")
    {'sharedInbox': 'http://host.test/shared_inbox'}

    ```
    """
    return {"sharedInbox": shared_inbox_from_actor_id(actor_id)}


def compute_acct_uri(base_url: str, preferred_username: str):
    """Computes the acct uri (see [RFC 7565](https://www.rfc-editor.org/rfc/rfc7565))

    ```pycon
    >>> compute_acct_uri("http://host.example/somewhere", "alice")
    'acct:alice@host.example'

    ```

    """
    host = urlparse(base_url).hostname

    return f"acct:{preferred_username}@{host}"


def new_url(base_url: str, url_type: str) -> str:
    token = secrets.token_urlsafe(16)
    return urljoin(base_url, f"{url_type}/{token}")
