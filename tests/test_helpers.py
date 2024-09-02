import pytest


@pytest.mark.parametrize("x, expected", [
    ("", ""),
    ("foobar", "foobar"),
    ("foo/bar", "foo%2Fbar"),
    # ...
])
def test_escape_path(x, expected):
    pass
