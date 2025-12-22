# api-session Changelog

## 1.5.3

* We now use `uv` to manage the project instead of Poetry. This shouldn’t have any outside impact.

## 1.5.2 (2025/10/01)

* Relax the Python requirement to avoid Poetry errors with `api-session requires Python <4.0,>=3.9`

## 1.5.1 (2025/06/18)

* Add strict type hints

## 1.5.0 (2025/04/18)

* Drop support for Python 3.8

## 1.4.3 (2025/04/09)

* Add explicit types for Mypy

## 1.4.2 (2024/09/02)

* Add `escape_path` helper
* Add Python 3.13 support
* Declare `__all__` not to expose imports
* Relax `requests` dependency

## 1.4.1 (2024/08/01)

* Fix the missing `response` (and `request`) attributes on the `HTTPError`s re-raised in `raise_for_response`

## 1.4.0 (2024/07/08)

* Change the default `raise_for_response` implementation to include the response body in the error message if the status
  is 4xx. This criterion can be changed by overriding the new method `include_body_in_exception`. One can also override
  `raise_for_response` to completely customize the exceptions raised by the library.

## 1.3.6 (2024/01/22)

* `post_json_api`: fix docstring
* Add `put_json_api`, `patch_json_api`, `delete_json_api`

## 1.3.5 (2023/11/15)

* Add `max_retries` to the constructor

## 1.3.4 (2023/11/15)

* Add `post_json_api`
* Add `timeout` to the constructor to specify a default timeout for all requests
* Add official support for Python 3.12

## 1.3.3 (2023/05/10)

* Add `offline` as an equivalent of `read_only` for all methods

## 1.3.2 (2022/10/13)

* Add `JSONDict` to type `dict`s from JSON responses.

## 1.3.1 (2022/05/25)

* Add `none_on_empty` constructor and `get_json_api` optional argument to return `None` on empty bodies. This is
  disabled by default so the current behavior doesn’t change.

## 1.3.0 (2022/04/21)

* Move `api_session.READ_METHODS` to `APISession.READ_METHODS` to make it easier to override
* Add `.none_on_404` to set the default for `.get_json_api`’s argument of the same name

## 1.2.1 (2022/04/01)

* `throw` defaults to `None` instead of `False` in all methods. This allows a class that overrides `request_api` to
  know if the parameter was set (`True` or `False`) or not (`None`).

## 1.2.0 (2022/02/04)

* Add `.patch_api` method
* Support `read_only` in the base `request()` method as well
* Don’t throw if `get_json_api` is called with `throw=True, none_on_404=True` (the default) and
  encounters a 404 error. This is the documented behavior but the logic wasn’t correctly
  implemented.

## 1.1.1 (2022/02/04)

* Fix `user_agent` support

## 1.1.0 (2022/02/03)

* Add `bypass_read_only` optional parameter to `request_api()`

## 1.0.0 (2022/01/13)

* Add `.head_api()`
* This releases moves to 1.x because the library API is stable

## 0.1.1 (2021/12/21)

* Add `py.typed` to mark the module as PEP-561-compliant

## 0.1.0 (2021/10/11)

Initial public release.
