from typing import Optional, Union, Text, Dict, Any, Tuple

import requests
from requests import HTTPError
from requests.adapters import HTTPAdapter
from urllib3 import Timeout, Retry

__version__ = "1.4.0"

# We can’t really do better than Any for now.
# See https://github.com/python/typing/issues/182.
JSONDict = Dict[str, Any]


class APISession(requests.Session):
    """
    HTTP Session with helpers to call a JSON-based API.
    """
    READ_METHODS = {"HEAD", "GET", "OPTIONS", "CONNECT", "TRACE"}

    def __init__(self, base_url: str, user_agent: Optional[str] = None, read_only=False, *,
                 offline=False,
                 none_on_404=True,
                 none_on_empty=False,
                 timeout: Optional[Union[int, Tuple[int, int], Timeout]] = None,
                 max_retries: Optional[Union[int, bool, Retry]] = None):
        """
        :param base_url: Base URL of the API.
        :param user_agent: Optional user-agent header to use.
        :param read_only: if True, any POST/PUT/DELETE call will fail with an AssertError.
        :param none_on_404: set the default for the argument of the same name in ``.get_json_api`` calls. This can still
          be overridden by passing it explicitly when calling the method.
        :param none_on_empty: set the default for the argument of the same name in ``.get_json_api`` calls. This can
          still be overridden by passing it explicitly when calling the method.
        :param timeout: default timeout to use for all requests
        :param max_retries: if set, the session mounts a ``HTTPAdapter`` with this parameter
        """
        super().__init__()

        self.base_url = base_url.rstrip("/")
        self.read_only = read_only
        self.offline = offline
        self.none_on_404 = none_on_404
        self.none_on_empty = none_on_empty
        self.timeout = timeout

        if max_retries is not None:
            adapter = HTTPAdapter(max_retries=max_retries)
            self.mount("https://", adapter)
            # noinspection HttpUrlsUsage
            self.mount("http://", adapter)

        if user_agent is not None:
            self.headers['User-Agent'] = user_agent

    # noinspection PyMethodMayBeStatic
    def raise_for_response(self, response: requests.Response):
        """
        Raise an exception if the response is an error.

        The default implementation wraps `response.raise_for_status`, and if `include_body_in_exception(response)` is
        `True`, it appends the response body to the error message.
        """
        try:
            response.raise_for_status()
        except HTTPError as ex:
            if self.include_body_in_exception(response):
                raise HTTPError(
                    str(ex) + f". Body: {response.text}"
                ) from ex.__cause__
            raise

    # noinspection PyMethodMayBeStatic
    def include_body_in_exception(self, response: requests.Response) -> bool:
        """
        Test if the exception for this response should include the response body in its message string.
        The default exception messages from `requests` don't include the body of the response, but this often contains
        more information about the error.

        By default, this tests if the status code is 4xx.
        """
        return response.status_code // 100 == 4

    def request(self, method: Union[str, bytes], url: Union[str, bytes, Text], *args, bypass_read_only=False, **kwargs):
        """
        :param method: method argument passed to the underlying ``.request()`` method
        :param url: URL argument passed to the underlying ``.request()`` method
        :param args: arguments passed to the underlying ``.request()`` method
        :param bypass_read_only: if True, ignore the ``.read_only`` attribute
        :param kwargs: keyword arguments passed to the underlying ``.request()`` method
        :return:
        """
        if self.offline:
            raise AssertionError("Can't perform %r action in offline mode!" % method)

        if self.read_only and not bypass_read_only and method.upper() not in self.READ_METHODS:
            raise AssertionError("Can't perform %r action in read-only mode!" % method)

        if "timeout" not in kwargs and self.timeout is not None:
            kwargs["timeout"] = self.timeout

        return super().request(method, url, *args, **kwargs)

    def request_api(self, method: str, path: str, *args, throw: Optional[bool] = None, **kwargs):
        """
        Wrapper around .request() that prefixes the path with the base API URL.

        :param method: HTTP method
        :param path: API path. This must start with "/"
        :param args: arguments passed to ``.request()``
        :param throw: if True, raise an exception if the response is an error.
        :param kwargs: keyword arguments passed to ``.request()``
        :return:
        """
        assert path.startswith("/")

        url = self.base_url + path
        r = self.request(method, url, *args, **kwargs)

        if throw:
            self.raise_for_response(r)
        return r

    def get_api(self, path: str, params: Optional[dict] = None, *, throw: Optional[bool] = None, **kwargs):
        """
        Equivalent of .get() that prefixes the path with the base API URL.

        :param path: path, starting with a slash
        :param params: GET params
        :param throw: throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('get', path, params=params, throw=throw, **kwargs)

    def get_json_api(self, path: str, params: Optional[dict] = None, *,
                     throw=True,
                     none_on_404: Optional[bool] = None,
                     none_on_empty: Optional[bool] = None,
                     **kwargs):
        """
        Equivalent of ``.get_api()`` that parses a JSON response. Return ``None`` on 404s and throws on other errors.

        :param path: URL path. This must start with a slash
        :param params: query params
        :param throw: if True, throw an exception on error
        :param none_on_404: if True, 404 errors are ignored and ``None`` is returned instead. This default on
          the ``.none_on_404`` instance attribute if set, ``True`` otherwise.
        :param none_on_empty: if True, successful responses that contain an empty body are treated as if they contained
          the JSON string ``null`` (= ``None`` in Python). If ``False``, the JSON decoding would raise on such responses.
        :param kwargs: keyword arguments passed to the underlying call
        :return:
        """
        none_on_404 = none_on_404 is True or (none_on_404 is None and self.none_on_404)
        none_on_empty = none_on_empty is True or (none_on_empty is None and self.none_on_empty)

        r = self.get_api(path, params=params, throw=False if none_on_404 else throw, **kwargs)
        if r.status_code == 404 and none_on_404:
            return None
        if throw:
            self.raise_for_response(r)

        if none_on_empty and not r.text:
            return None

        return r.json()

    def head_api(self, path: str, params: Optional[dict] = None, *, throw: Optional[bool] = None, **kwargs):
        """
        Equivalent of .head() that prefixes the path with the base API URL.

        :param path: URL path. This must start with a slash
        :param params: query params
        :param throw: throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('head', path, params=params, throw=throw, **kwargs)

    def post_api(self, path: str, *args, throw: Optional[bool] = None, **kwargs):
        """
        Equivalent of .post() that prefixes the path with the base API URL.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('post', path, *args, throw=throw, **kwargs)

    def post_json_api(self, path: str, *args, throw=True, **kwargs):
        """
        Equivalent of ``.post_api()`` that parses a JSON response.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error. The default is ``True``, because in the case in which the
          server doesn’t return JSON when there’s an error, this would fail at the JSON-decoding step and mask the real
          error. Use ``throw=False`` to disable this behavior.
        :return:
        """
        return self.post_api(path, *args, throw=throw, **kwargs).json()

    def put_api(self, path: str, *args, throw: Optional[bool] = None, **kwargs):
        """
        Equivalent of .put() that prefixes the path with the base API URL.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('put', path, *args, throw=throw, **kwargs)

    def put_json_api(self, path: str, *args, throw=True, **kwargs):
        """
        Equivalent of ``.put_api()`` that parses a JSON response.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error. The default is ``True``, because in the case in which the
          server doesn’t return JSON when there’s an error, this would fail at the JSON-decoding step and mask the real
          error. Use ``throw=False`` to disable this behavior.
        :return:
        """
        return self.put_api(path, *args, throw=throw, **kwargs).json()

    def patch_api(self, path: str, *args, throw: Optional[bool] = None, **kwargs):
        """
        Equivalent of .patch() that prefixes the path with the base API URL.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('patch', path, *args, throw=throw, **kwargs)

    def patch_json_api(self, path: str, *args, throw=True, **kwargs):
        """
        Equivalent of ``.patch_api()`` that parses a JSON response.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error. The default is ``True``, because in the case in which the
          server doesn’t return JSON when there’s an error, this would fail at the JSON-decoding step and mask the real
          error. Use ``throw=False`` to disable this behavior.
        :return:
        """
        return self.patch_api(path, *args, throw=throw, **kwargs).json()

    def delete_api(self, path: str, throw: Optional[bool] = None, **kwargs):
        """
        Equivalent of .delete() that prefixes the path with the base API URL.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('delete', path, throw=throw, **kwargs)

    def delete_json_api(self, path: str, throw=True, **kwargs):
        """
        Equivalent of ``.delete_api()`` that parses a JSON response.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error. The default is ``True``, because in the case in which the
          server doesn’t return JSON when there’s an error, this would fail at the JSON-decoding step and mask the real
          error. Use ``throw=False`` to disable this behavior.
        :return:
        """
        return self.delete_api(path, throw=throw, **kwargs).json()
