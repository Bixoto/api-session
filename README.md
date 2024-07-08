# api-session

**api-session** is a small module providing an extended `requests.Session` class to work with JSON APIs.

We use it at [Bixoto](https://bixoto.com/) as a basis for JSON API clients such as [PyMagento][] or
[PyBigBuy][].

It aims at factoring the common parts of these clients while staying very lightweight (<100 SLOC).

[PyMagento]: https://github.com/Bixoto/PyMagento
[PyBigBuy]: https://github.com/Bixoto/PyBigBuy

## Features

* base URL: the base API URL is given only once on object creation; subsequent calls use `.get("/path")`
* read-only flag: if given, prevents the API from doing `POST` and similar calls
* offline flag: if given, prevents the API from doing any call. This is useful for tests.
* `requests.Session` inheritance: the class inherits from `requests.Session`, so it stays 100% compatible with it
* (since 1.4) Response bodies are included in exception messages for 4xx errors. This behavior can be customized.

## Install

    pip install api-session

Or with Poetry:

    poetry add api-session

Dependency: Python 3.8+.

## Usage

```python3
from api_session import APISession

client = APISession("https://httpbin.org")

client.get_json_api("/get")
# => {...}
```
