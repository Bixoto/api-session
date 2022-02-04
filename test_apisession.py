from requests import HTTPError

from api_session import APISession

import pytest


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


def test_raise_for_response():
    s = APISession("https://httpbin.org")
    response = s.get_api("/status/403")
    assert response.status_code == 403
    with pytest.raises(HTTPError):
        s.raise_for_response(response)


def test_throw():
    s = APISession("https://httpbin.org")

    for method in (s.get_api, s.post_api, s.put_api, s.patch_api, s.delete_api):
        with pytest.raises(HTTPError):
            method("/status/403", throw=True)

        assert method("/status/200", throw=True).ok
