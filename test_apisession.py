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
