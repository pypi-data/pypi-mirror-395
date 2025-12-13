from __future__ import annotations

import json
import logging
from collections.abc import Callable, Generator, Mapping, MutableMapping
from typing import (
    TYPE_CHECKING,
    Any,
    ParamSpec,
    TypeGuard,
    TypeVar,
    cast,
)

import requests
from ape_pie import APIClient

from openklant_client.exceptions import (
    BadRequest,
    Forbidden,
    InvalidJSONResponse,
    NonJSONResponse,
    NotFound,
    ResponseError,
    StructuredErrorResponse,
    Unauthorized,
)
from openklant_client.types.pagination import PaginatedResponseBody

if TYPE_CHECKING:
    JSONPrimitive = str | int | None | float
    JSONValue = JSONPrimitive | "JSONObject" | list["JSONValue"]
    JSONObject = dict[str, JSONValue]

logger = logging.getLogger(__name__)

ResourceResponse = MutableMapping[str, Any]

P = ParamSpec("P")
T = TypeVar("T")


def _is_error_response(data: Any) -> bool:
    """Check if response data matches error response structure."""
    if not isinstance(data, dict):
        return False
    required_keys = {"type", "code", "title", "status", "detail", "instance"}
    return required_keys.issubset(data.keys())


def _is_validation_error_response(data: Any) -> bool:
    """Check if response data matches validation error response structure."""
    if not _is_error_response(data):
        return False
    return data.get("status") == 400 and "invalidParams" in data


class ResourceMixin:
    http_client: APIClient

    def __init__(self, http_client: APIClient):
        self.http_client = http_client

    @staticmethod
    def process_response(response: requests.Response) -> TypeGuard[JSONValue]:
        response_data = None
        try:
            content_type = response.headers.get("Content-Type", "")
            # Note: there are currently no non-JSON responses defined in the
            # spec, the obvious example would be e.g. something like a blob
            # download. Until such endpoints are encountered, we treat non-JSON
            # as an error.
            if not content_type.lower().startswith("application/json"):
                raise NonJSONResponse(response)

            response_data = response.json()
        except (requests.exceptions.JSONDecodeError, json.JSONDecodeError) as exc:
            raise InvalidJSONResponse(response) from exc

        match response.status_code:
            case code if code >= 200 and code < 300 and response_data:
                return response_data
            case code if code >= 400 and code < 500 and response_data:
                exc_class = StructuredErrorResponse
                is_valid_error = _is_error_response(response_data)

                match code:
                    case 400:
                        if _is_validation_error_response(response_data):
                            raise BadRequest(response, response_data)
                        exc_class = BadRequest
                    case 401:
                        exc_class = Unauthorized
                    case 403:
                        exc_class = Forbidden
                    case 404:
                        exc_class = NotFound
                    case _:
                        pass

                if is_valid_error:
                    raise exc_class(response, response_data)
                # JSON body, but not in expected schema. Fall through to
                # generic ErrorResponse
            case _:
                pass

        raise ResponseError(response, msg="Error response")

    @staticmethod
    def _process_params(params: Mapping | None) -> None | Mapping:
        # The default approach to serializing lists in the requests library is
        # not supported by OpenKlant 2. See:
        # https://github.com/maykinmedia/open-klant/issues/250
        if params is None:
            return params

        transposed_params = dict(params)
        for key, val in params.items():
            if isinstance(val, list):
                transposed_params[key] = ",".join(str(element) for element in val)

        return transposed_params

    def _paginator(
        self,
        paginated_data: PaginatedResponseBody[T],
        max_requests: int | None = None,
    ) -> Generator[T, Any, None]:
        def row_iterator(
            _data: PaginatedResponseBody[T], num_requests=0
        ) -> Generator[T, Any, None]:
            for result in _data["results"]:
                yield cast(T, result)

            if next_url := _data.get("next"):
                if max_requests and num_requests >= max_requests:
                    logger.info(
                        "Number of requests while retrieving paginated "
                        "results reached maximum (%s), returning results. "
                        "Next URL: %s",
                        max_requests,
                        next_url,
                    )
                    return

                response = self.http_client.get(next_url)
                num_requests += 1
                response.raise_for_status()
                data = response.json()

                yield from row_iterator(data, num_requests)

        return row_iterator(paginated_data)

    def _get(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Mapping | None = None,
    ) -> requests.Response:
        return self.http_client.request(
            "get", path, headers=headers, params=self._process_params(params)
        )

    def _post(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Mapping | None = None,
        data: Any = None,
    ) -> requests.Response:
        return self.http_client.request(
            "post",
            path,
            headers=headers,
            json=data,
            params=self._process_params(params),
        )

    def _put(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Mapping | None = None,
        data: Any = None,
    ) -> requests.Response:
        return self.http_client.request(
            "put", path, headers=headers, json=data, params=self._process_params(params)
        )

    def _delete(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Mapping | None = None,
    ) -> requests.Response:
        return self.http_client.request(
            "delete",
            path,
            headers=headers,
            params=self._process_params(params),
        )

    def _patch(
        self,
        path: str,
        headers: Mapping | None = None,
        params: Mapping | None = None,
        data: Any = None,
    ) -> requests.Response:
        return self.http_client.request(
            "patch",
            path,
            headers=headers,
            params=self._process_params(params),
            json=data,
        )

    def _options(
        self,
        path: str,
        headers: Mapping | None = None,
        params: MutableMapping | None = None,
    ) -> requests.Response:
        return self.http_client.request(
            "delete",
            path,
            headers=headers,
            params=self._process_params(params),
        )

    def _make_list_iter(
        self, f: Callable[P, PaginatedResponseBody[T]]
    ) -> Callable[P, Generator[T, Any, Any]]:
        """Create a fully paginated iterator for the resource list() method."""

        def inner(*args: P.args, **kwargs: P.kwargs) -> Generator[T, Any, None]:
            return self._paginator(f(*args, **kwargs))

        return inner


class ConvenienceMethodMixin(ResourceMixin):
    http_client: APIClient

    def __init__(self, http_client: APIClient):
        self.http_client = http_client

    def __call__(self):
        raise NotImplementedError(
            "You must implement the _call__ method to invoke the convenience method"
        )
