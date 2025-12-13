import pytest

from .http_util import parse_content_type_header, should_serve, ContentType


@pytest.mark.parametrize(
    "header,expected",
    [
        ("", []),
        ("text/html", [ContentType.html]),
        ("application/activity+json", [ContentType.activity_pub]),
    ],
)
def test_should_serve(header, expected):
    assert should_serve(header) == expected


def test_none_as_header():
    assert should_serve(None) == [ContentType.other]


def test_parse_content_type_header_example_from_curl():
    header = (
        "multipart/form-data; boundary=------------------------SDk4eo6yT73vkv90ieEbFe"
    )

    parse_content_type_header(header)
