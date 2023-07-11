from json import JSONDecodeError

import pytest
from requests import HTTPError

from api_session import APISession


@pytest.fixture()
def httpbin_session():
    return APISession("https://httpbin.org")


def test_offline():
    s = APISession("https://example.org", offline=True)
    with pytest.raises(AssertionError):
        s.get("/")


def test_read_only():
    s = APISession("https://example.org", read_only=True)

    with pytest.raises(AssertionError):
        s.post_api("/something")

    with pytest.raises(AssertionError):
        s.post("/something")

    with pytest.raises(AssertionError):
        s.put("/something")

    with pytest.raises(AssertionError):
        s.delete("/something")


def test_user_agent():
    s = APISession("https://example.org", read_only=True, user_agent="Foo")
    assert s.headers.get("user-agent") == "Foo"


def test_raise_for_response(httpbin_session):
    response = httpbin_session.get_api("/status/403")
    assert response.status_code == 403
    with pytest.raises(HTTPError):
        httpbin_session.raise_for_response(response)


def test_throw(httpbin_session):
    for method in (httpbin_session.get_api, httpbin_session.post_api, httpbin_session.put_api,
                   httpbin_session.patch_api, httpbin_session.delete_api, httpbin_session.head_api):
        with pytest.raises(HTTPError):
            method("/status/403", throw=True)

        assert method("/status/200", throw=True).ok


def test_get_json_api_none_on_404(httpbin_session):
    assert httpbin_session.none_on_404 is True

    with pytest.raises(HTTPError):
        httpbin_session.get_json_api("/status/404", none_on_404=False)

    assert httpbin_session.get_json_api("/status/404") is None
    assert httpbin_session.get_json_api("/status/404", none_on_404=True) is None

    assert isinstance(httpbin_session.get_json_api("/headers"), dict)

    httpbin_session.none_on_404 = False
    with pytest.raises(HTTPError):
        httpbin_session.get_json_api("/status/404")

    with pytest.raises(HTTPError):
        httpbin_session.get_json_api("/status/404", none_on_404=False)

    assert httpbin_session.get_json_api("/status/404", none_on_404=True) is None


def test_get_json_api_none_on_empty(httpbin_session):
    assert httpbin_session.none_on_empty is False

    with pytest.raises(JSONDecodeError):
        httpbin_session.get_json_api("/status/204")

    assert httpbin_session.get_json_api("/status/204", none_on_empty=True) is None

    httpbin_session.none_on_empty = True
    assert httpbin_session.get_json_api("/status/204") is None
    assert httpbin_session.get_json_api("/status/204", none_on_empty=True) is None

    with pytest.raises(JSONDecodeError):
        httpbin_session.get_json_api("/status/204", none_on_empty=False)
