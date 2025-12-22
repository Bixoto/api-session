# api-session

**api-session** is a small module providing an extended `requests.Session` class to work with JSON APIs.

We use it at [Bixoto](https://bixoto.com/) as a basis for JSON API clients such as [PyMagento][] or [PyBigBuy][].

It aims at factoring the common parts of these clients while staying very lightweight (<100 SLOC).

[PyMagento]: https://github.com/Bixoto/PyMagento

[PyBigBuy]: https://github.com/Bixoto/PyBigBuy

## Features

* Base URL: the base API URL is given only once on object creation; subsequent calls use `.get("/path")`
* Read-only flag: if given, prevents the API from doing `POST` and similar calls
* Offline flag: if given, prevents the API from doing any call. This is useful for tests.
* `requests.Session` inheritance: the class inherits from `requests.Session`, so it stays 100% compatible with it
* Response bodies are included in exception messages for 4xx errors. This behavior can be customized.

## Install

    pip install api-session

With Poetry:

    poetry add api-session

With uv:

    uv add api-session

Dependency: Python 3.9+.

* Versions 1.5.x require Python 3.9+
* Versions 1.4.x and before require Python 3.8+

## Usage

```python3
from api_session import APISession

client = APISession("https://httpbin.org")

client.get_json_api("/get")
# => {...}
```

A typical usage is to inherit from the session to implement an API client class:

```python3
from typing import Any, cast

from api_session import APISession


class FooApiClient(APISession):
    def __init__(
            self,
            token: str,
            **kwargs: Any,
    ):
        super().__init__(base_url="https://foo-api.example.com/v1", **kwargs)
        self.headers["Authorization"] = f"Bearer {token}"

    def get_stuff(self) -> list[dict[str, Any]]:
        return cast(list[dict[str, Any]],
                    self.get_json_api("/get-stuff"))

    def create_stuff(self, stuff: dict[str, Any]) -> bool:
        return cast(bool, self.post_json_api("/create-stuff", json=stuff))


# Then use it:
my_client = FooApiClient("my-token")
my_client.create_stuff({"foo": "bar"})  # => True
for stuff in my_client.get_stuff():
    print(stuff)
```
