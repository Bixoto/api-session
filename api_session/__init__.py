from typing import Optional, Union, Text

import requests

__version__ = "1.2.0"
READ_METHODS = {"HEAD", "GET", "OPTIONS", "CONNECT", "TRACE"}


class APISession(requests.Session):
    """
    HTTP Session with helpers to call a JSON-based API.
    """

    def __init__(self, base_url: str, user_agent: Optional[str] = None, read_only=False):
        """
        :param base_url: Base URL of the API.
        :param user_agent: Optional user-agent header to use.
        :param read_only: if True, any POST/PUT/DELETE call will fail with an AssertError.
        """
        super().__init__()

        self.base_url = base_url.rstrip("/")
        self.read_only = read_only

        if user_agent is not None:
            self.headers['User-Agent'] = user_agent

    # noinspection PyMethodMayBeStatic
    def raise_for_response(self, response: requests.Response):
        """
        Raise an exception if the response is an error.
        This defaults to `response.raise_for_status` but can be overridden.
        """
        # Override this method as needed
        response.raise_for_status()

    def request(self, method: str, url: Union[str, bytes, Text], *args, bypass_read_only=False, **kwargs):
        """
        :param method: method argument passed to the underlying ``.request()`` method
        :param url: URL argument passed to the underlying ``.request()`` method
        :param args: arguments passed to the underlying ``.request()`` method
        :param bypass_read_only: if True, ignore the ``.read_only`` attribute
        :param kwargs: keyword arguments passed to the underlying ``.request()`` method
        :return:
        """
        if self.read_only and not bypass_read_only and method.upper() not in READ_METHODS:
            raise AssertionError("Can't perform %s action in read-only mode!" % method)
        return super().request(method, url, *args, **kwargs)

    def request_api(self, method: str, path: str, *args, throw=False, **kwargs):
        """
        Wrapper around .request() that prefixes the path with the base API URL.

        :param method: HTTP method
        :param path: API path. This must start with "/"
        :param args: arguments passed to ``.request()``
        :param throw: if True, raise an exception if the response is an error
        :param kwargs: keyword arguments passed to ``.request()``
        :return:
        """
        assert path.startswith("/")

        url = self.base_url + path
        r = self.request(method, url, *args, **kwargs)

        if throw:
            self.raise_for_response(r)
        return r

    def get_api(self, path: str, params: Optional[dict] = None, *, throw=False, **kwargs):
        """
        Equivalent of .get() that prefixes the path with the base API URL.

        :param path: path, starting with a slash
        :param params: GET params
        :param throw: throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('get', path, params=params, throw=throw, **kwargs)

    def get_json_api(self, path: str, params: Optional[dict] = None, *, throw=True, none_on_404=True, **kwargs):
        """
        Equivalent of ``.get_api()`` that parses a JSON response. Return ``None`` on 404s and throws on other errors.

        :param path: URL path. This must start with a slash
        :param params: query params
        :param throw: if True, throw an exception on error
        :param none_on_404: if True (the default), 404 errors are ignored and ``None`` is returned instead.
        :param kwargs: keyword arguments passed to the underlying call
        :return:
        """
        r = self.get_api(path, params=params, throw=False if none_on_404 else throw, **kwargs)
        if none_on_404 and r.status_code == 404:
            return None
        if throw:
            self.raise_for_response(r)
        return r.json()

    def head_api(self, path: str, params: Optional[dict] = None, *, throw=False, **kwargs):
        """
        Equivalent of .head() that prefixes the path with the base API URL.

        :param path: path, starting with a slash
        :param params: query params
        :param throw: throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('head', path, params=params, throw=throw, **kwargs)

    def post_api(self, path: str, *args, throw=False, **kwargs):
        """
        Equivalent of .post() that prefixes the path with the base API URL.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('post', path, *args, throw=throw, **kwargs)

    def put_api(self, path: str, *args, throw=False, **kwargs):
        """
        Equivalent of .put() that prefixes the path with the base API URL.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('put', path, *args, throw=throw, **kwargs)

    def patch_api(self, path: str, *args, throw=False, **kwargs):
        """
        Equivalent of .patch() that prefixes the path with the base API URL.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('patch', path, *args, throw=throw, **kwargs)

    def delete_api(self, path: str, throw=False, **kwargs):
        """
        Equivalent of .delete() that prefixes the path with the base API URL.

        :param path: URL path. This must start with a slash
        :param throw: if True, throw an exception on error
        :return: requests.Response object
        """
        return self.request_api('delete', path, throw=throw, **kwargs)
