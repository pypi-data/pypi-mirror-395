import os

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from worker import exceptions


class API(object):
    HTTP_METHODS = ("get", "post", "patch", "put", "delete")
    options = {"api_url": "API_ROOT_URL", "api_key": "API_KEY", "app_name": "APP_NAME"}

    def __init__(self, *args, **kwargs):
        self.configure(self.options, kwargs)

    def configure(self, options, values):
        for attribute, environment_key in options.items():
            value = values.pop(attribute, os.getenv(environment_key, None))
            if not value:
                error = "No {0} parameter or {1} environment variable defined".format(attribute, environment_key)
                raise exceptions.Misconfigured(error)

            setattr(self, attribute, value)

    def get(self, *args, **kwargs):
        return self.call("get", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.call("post", *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.call("patch", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.call("put", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.call("delete", *args, **kwargs)

    def call(self, method, path, **kwargs):
        content_type = kwargs.pop("content_type", "application/json")
        timeout = kwargs.pop("timeout", 30)
        headers = {
            "Authorization": "API {0}".format(self.api_key),
            "Content-Type": content_type,
            "X-Corva-App": self.app_name,
        }

        method = method.lower()
        if method not in self.HTTP_METHODS:
            raise exceptions.APIError("Invalid HTTP method {0}".format(method))

        retry_count = kwargs.pop("retry_count", 5)
        retry_strategy = Retry(
            total=retry_count,
            status_forcelist=[408, 429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
            backoff_factor=0.3,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("http://", adapter)
        http.mount("https://", adapter)
        http_method = getattr(http, method)

        data = kwargs.pop("data", None)
        if not path.startswith(self.api_url):
            path = "{0}{1}".format(self.api_url, path)

        response = http_method(url=path, data=data, params=kwargs, headers=headers, timeout=timeout)

        # closing the http connection after a request
        http.close()

        asset_id = kwargs.get("asset_id", "Unknown") or "Unknown"

        if response.status_code == 401:
            raise exceptions.APIError("Unable to reach Corva API")

        if response.status_code == 403:
            raise exceptions.Forbidden("No access to asset {0}".format(asset_id))

        if response.status_code == 404:
            raise exceptions.NotFound("Not Found")

        if not response.ok:
            raise exceptions.APIError(f"{response.status_code} - {response.reason}")

        result = Result(response, **kwargs)
        return result

    def get_by_id(self, path, **kwargs):
        """
        Get a document with the given kwargs ('collection', 'id')
        :param path: API path
        :param kwargs: 'collection' and 'id' kwargs are required
        :return: a result object
        """
        collection = kwargs.pop("collection", None)
        component_id = kwargs.pop("id", None)
        path = "{0}{1}{2}/{3}".format(self.api_url, path, collection, component_id)

        result = self.get(path)
        return result


class Result(object):
    def __init__(self, response, **kwargs):
        self.response = response
        self.params = kwargs
        self.data = None

        try:
            self.data = response.json()
        except Exception:
            if not (response.status_code == 200 and response.content == b""):
                raise exceptions.APIError("Invalid API response")

    def __repr__(self):
        return repr(self.data)

    def __iter__(self):
        return iter(self.data)

    @property
    def status(self):
        return self.response.status_code

    @property
    def count(self):
        if not self.data:
            return 0

        if isinstance(self.data, list):
            return len(self.data)

        if isinstance(self.data, dict):
            return 1

        return 0


def convert_python_sdk_api_to_worker_api(python_sdk_api) -> API:
    """
    In cases that the python sdk api is used,
    this function converts it to worker api.

    Args:
        python_sdk_api (Api): Corva Python SDK Api

    Returns:
        API: Worker API object
    """
    return API(api_url=python_sdk_api.api_url, api_key=python_sdk_api.api_key, app_name=python_sdk_api.app_key)
