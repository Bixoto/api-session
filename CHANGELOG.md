# api-session Changelog

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
