# api-session Changelog

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
