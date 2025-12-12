"""
This module defines the basics of the interaction with Neogrid's web API
"""
import logging
from enum import Enum
from typing import Any, Optional

from requests import Session
from requests.adapters import HTTPAdapter, Retry
from requests.models import Response

from preheat_open.configuration import NeogridApiConfig, run_if_production_mode

from ..time import ZoneInfo, datetime

logger = logging.getLogger(__name__)


def api_string_to_datetime(t: str) -> datetime:
    """
    Converts a datetime string from the API to a python datetime

    :param t: datetime in string format
    :return: datetime corresponding to the input
    """
    return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=ZoneInfo("UTC"))


def datetime_to_api_string(t: datetime) -> str:
    """
    Converts a python datetime to a string ready for use in the API I/O

    :param t: datetime to convert to string
    :return: a string with a format compatible with the API
    """
    ts = t.replace(tzinfo=None)
    if (utcoffset := t.utcoffset()) is not None:
        ts = ts - utcoffset
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


class ApiError(Exception):
    pass


def prepare(item: Any, as_json: bool = False) -> Any:
    """
    Method to convert a parameter to a format that can be sent to the API

    :param param: parameter to convert
    :return: converted parameter
    """
    if isinstance(item, str):
        return item
    elif any(isinstance(item, t) for t in [int, float, bool]):
        if as_json:
            return item
        return str(item)
    elif isinstance(item, datetime):
        return datetime_to_api_string(item)
    elif isinstance(item, Enum):
        return item.value
    elif isinstance(item, list):
        if as_json:
            return [prepare(p, as_json=as_json) for p in item]
        return ",".join(map(str, [prepare(p) for p in item]))
    elif isinstance(item, dict):
        if as_json:
            return {k: prepare(v, as_json=as_json) for k, v in item.items()}
        return {k: prepare(v) for k, v in item.items()}
    elif item is None:
        return ""
    else:
        raise ValueError(f"Unsupported API input type: {type(item)}")


class ApiSession:
    """Class to handle API connection sessions"""

    def __init__(self, config: Optional[NeogridApiConfig] = None):
        # Adding protection against remote closing connection
        self.config = config if config else NeogridApiConfig()
        retry_strategy = Retry(
            total=3,
            read=3,
            connect=3,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=["GET", "PUT", "POST"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http_session = Session()
        http_session.mount("https://", adapter)
        http_session.mount("http://", adapter)

        self.timeout_seconds = {
            "GET": 120,
            "PUT": 10,
            "POST": 10,
            "PATCH": 10,
            "DELETE": 10,
        }
        self.base_url = self.config.url
        self.session = http_session
        self.session.headers.update({"Authorization": "Apikey " + self.config.token})
        self.datetime_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        logger.debug("Creating API session [%s]...", self)

    def close(self):
        """Method to close the session"""
        self.session.close()
        logger.debug("Closing API session [%s]...", self)

    def __str__(self) -> str:
        """
        Making a string representation of the session object for use in logging

        :return: string representing the session
        """
        return f"ApiSession({hex(id(self.session))})"

    def __log_api_io(self, msg: str, logging_level: str = "debug") -> None:
        getattr(logger, logging_level)(msg)

    def __check_and_raise_error(self, response: Response | None):
        if response is None:
            raise ApiError(
                "No response received. Most likely because of running in a non-production environment. Please change the runtime mode in the configuration."
            )
        elif response.ok:
            level = "debug"
        else:
            level = "error"
        self.__log_api_io(f"Response: {response.status_code} {response.reason}", level)

        if not response.ok:
            msg = f"""{response.request.method} - FAILED
            URL: {response.request.url}
            Body: {str(response.request.body)}
            Response: {response.text}
            """
            logger.error(msg)
            response.raise_for_status()

    def __send_request(
        self,
        method: str = "GET",
        endpoint: str = "",
        out: str = "json",
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response:
        """
        Method to send a POST request to the API

        :param method: Type of request to send (GET, PUT, POST)
        :param endpoint: URL of the endpoint
        :param out: output type (json or csv)
        :param json: json for the request body
        :param params: params for re request
        :return: API response in request.Response format
        """

        self.__log_api_io(f"{method} /{endpoint} [{self}]")

        path = self.base_url + "/" + endpoint if endpoint else self.base_url

        headers = {"Accept": "text/csv"} if out == "csv" else {}

        if method == "GET":
            response = self.session.request(
                method=method,
                url=path,
                params=prepare(params) if params is not None else params,
                headers=headers,
                json=prepare(json_body, as_json=True)
                if json_body is not None
                else json_body,
                timeout=self.timeout_seconds[method],
            )
        else:
            response = run_if_production_mode(
                function=self.session.request,
                method=method,
                url=path,
                params=prepare(params) if params is not None else params,
                headers=headers,
                json=prepare(json_body, as_json=True)
                if json_body is not None
                else json_body,
                timeout=self.timeout_seconds[method],
            )

        self.__check_and_raise_error(response)

        return response

    def get(
        self,
        endpoint: str = "",
        out: str = "json",
        params: Optional[dict[str, Any]] = None,
    ):
        """
        Method to send a GET request to the API

        :param endpoint: URL of the endpoint
        :param out: output type (json or csv)
        :param params: params for the request
        :return: API response in request.Response format
        """
        return self.__send_request(
            method="GET", endpoint=endpoint, out=out, params=params
        )

    def put(
        self,
        endpoint: str = "",
        out: str = "json",
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response:
        """
        Method to send a PUT request to the API

        :param endpoint: URL of the endpoint
        :param out: output type (json or csv)
        :param json: payload for the request
        :param params: params for the request
        :return: API response in request.Response format
        """
        return self.__send_request(
            method="PUT", endpoint=endpoint, out=out, params=params, json_body=json_body
        )

    def post(
        self,
        endpoint: str = "",
        out: str = "json",
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response:
        """
        Method to send a POST request to the API

        :param endpoint: URL of the endpoint
        :param out: output type (json or csv)
        :param json_payload: payload for the request
        :param timeout: timeout (in seconds) for the call - defaults to PUT_TIMEOUT_SECONDS
        :return: API response in request.Response format
        """
        return self.__send_request(
            method="POST",
            endpoint=endpoint,
            out=out,
            params=params,
            json_body=json_body,
        )

    def patch(
        self,
        endpoint: str = "",
        out: str = "json",
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response:
        """
        Method to send a PATCH request to the API

        :param endpoint: URL of the endpoint
        :param out: output type (json or csv)
        :param json_payload: payload for the request
        :param timeout: timeout (in seconds) for the call - defaults to PUT_TIMEOUT_SECONDS
        :return: API response in request.Response format
        """
        return self.__send_request(
            method="PATCH",
            endpoint=endpoint,
            out=out,
            params=params,
            json_body=json_body,
        )

    def delete(
        self, endpoint: str = "", params: dict[str, Any] | None = None
    ) -> Response:
        """
        Method to send a DELETE request to the API

        :param endpoint: URL of the endpoint
        :param params: params for the request
        :return: API response in request.Response format
        """
        return self.__send_request(method="DELETE", endpoint=endpoint, params=params)
