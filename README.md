# api-session

**api-session** is a small module providing an extended `requests.Session` class to work with JSON APIs.

It aims at factoring the common parts of these clients while staying very lightweight (<100 SLOC). It only _augments_
the `requests.Session` class, so the base methods are still available.

We use it at [Bixoto](https://bixoto.com/) as a basis for JSON API clients such as [PyMagento][] or [PyBigBuy][].

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

With uv:

    uv add api-session

With Poetry:

    poetry add api-session

Dependency: Python 3.9+.

* Versions 1.5.x require Python 3.9+
* Versions 1.4.x and before require Python 3.8+

## Usage

```python3
from api_session import APISession

# The only requirement is to pass the base URL of the API you want to use.
# This does not prevent you from calling other URLs.
client = APISession("https://httpbin.org")

# All requests methods are available:
client.get("https://example.com")
client.head("https://example.com")
client.post("https://example.com")
client.put("https://example.com")
client.delete("https://example.com")
client.options("https://example.com")

# In addition, *_api methods call the base URL:
client.get_api("/foo")      # GET https://httpbin.org/foo
client.head_api("/foo")     # HEAD https://httpbin.org/foo
client.post_api("/foo")     # POST https://httpbin.org/foo
client.put_api("/foo")      # PUT https://httpbin.org/foo
client.delete_api("/foo")   # DELETE https://httpbin.org/foo
client.options_api("/foo")  # OPTIONS https://httpbin.org/foo

# For JSON API, use the _*_json_api methods. They call `.json()` on the response, so you don’t have to:
client.get_json_api("/foo")    # equivalent of client.get("https://httpbin.org/foo").json()
client.post_json_api("/bar")   # equivalent of client.post("https://httpbin.org/bar").json()
client.put_json_api("/baz")    # equivalent of client.put("https://httpbin.org/baz").json()
client.delete_json_api("/qux") # equivalent of client.delete("https://httpbin.org/qux").json()
```

A typical usage is to inherit from the session to implement an API client class:

```python3
from typing import Any
from api_session import APISession


class FooApiClient(APISession):
    def __init__(self, token: str, **kwargs):
        # Set the base URL used by all API calls
        super().__init__(base_url="https://foo-api.example.com/v1", **kwargs)

        # Add your own setup, like headers
        self.headers["Authorization"] = f"Bearer {token}"

    def get_stuff(self) -> list[dict]:
        return self.get_json_api("/get-stuff")

    def create_stuff(self, stuff: dict[str, Any]) -> bool:
        return self.post_json_api("/create-stuff", json=stuff)

# Then use it:
my_client = FooApiClient("my-token")
my_client.create_stuff({"foo": "bar"})  # => True
for thing in my_client.get_stuff():
    print(thing)
```
