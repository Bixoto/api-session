from api_session import APISession

import pytest


def test_read_only():
    s = APISession("https://example.org", read_only=True)

    with pytest.raises(RuntimeError):
        s.post_api("/something")
