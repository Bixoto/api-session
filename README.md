# api-session

**api-session** is a small module providing an extended `requests.Session` class to work with (JSON) APIs.

We use it at [Bixoto](https://bixoto.com/) as a basis for JSON API clients such as [PyMagento][].

[PyMagento]: https://github.com/Bixoto/PyMagento

## Features

* base URL: the base API URL is given only once on object creation; subsequent calls use `.get("/path")`
* read-only flag: if given, prevents the API from doing `POST` and similar calls
* `requests.Session` inheritance: the class inherits from `requests.Session`, so it stays 100% compatible with it

## Install

    pip install api-session

Dependency: Python 3.8+.

## Usage

```python3
from api_session import APISession

client = APISession("https://httpbin.org")

client.get_json_api("/get")
# => {...}
```
