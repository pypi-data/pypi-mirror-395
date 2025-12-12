# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: operation.j2

# pylint: disable=duplicate-code
# pylint: disable=line-too-long
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-statements
# pylint: disable=unused-import

# AccelByte Gaming Services Iam Service

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from accelbyte_py_sdk.core import ApiError, ApiResponse
from accelbyte_py_sdk.core import Operation
from accelbyte_py_sdk.core import HeaderStr
from accelbyte_py_sdk.core import HttpResponse
from accelbyte_py_sdk.core import deprecated

from ...models import RestErrorResponse


class CheckUserAvailability(Operation):
    """Check user's account availability (CheckUserAvailability)

    Check user's account availability.
    Available field :
    - displayName
    - uniqueDisplayName
    - username

    If request include access token with user ID data, that user ID will be excluded from availability check.
    For example, in case user update his emailAddress, he can use his own emailAddress to update his account.

    Response Code :
    - Account Available : 404 (not found)
    - Account Not Available : 204 (no content)

    Properties:
        url: /iam/v3/public/namespaces/{namespace}/users/availability

        method: GET

        tags: ["Users"]

        consumes: []

        produces: ["application/json"]

        securities: [BEARER_AUTH]

        namespace: (namespace) REQUIRED str in path

        field: (field) REQUIRED str in query

        query: (query) REQUIRED str in query

    Responses:
        204: No Content - (No Content)

        400: Bad Request - RestErrorResponse (20002: validation error)

        404: Not Found - (Not Found)

        422: Unprocessable Entity - RestErrorResponse (20002: validation error)
    """

    # region fields

    _url: str = "/iam/v3/public/namespaces/{namespace}/users/availability"
    _path: str = "/iam/v3/public/namespaces/{namespace}/users/availability"
    _base_path: str = ""
    _method: str = "GET"
    _consumes: List[str] = []
    _produces: List[str] = ["application/json"]
    _securities: List[List[str]] = [["BEARER_AUTH"]]
    _location_query: str = None

    service_name: Optional[str] = "iam"

    namespace: str  # REQUIRED in [path]
    field: str  # REQUIRED in [query]
    query: str  # REQUIRED in [query]

    # endregion fields

    # region properties

    @property
    def url(self) -> str:
        return self._url

    @property
    def path(self) -> str:
        return self._path

    @property
    def base_path(self) -> str:
        return self._base_path

    @property
    def method(self) -> str:
        return self._method

    @property
    def consumes(self) -> List[str]:
        return self._consumes

    @property
    def produces(self) -> List[str]:
        return self._produces

    @property
    def securities(self) -> List[List[str]]:
        return self._securities

    @property
    def location_query(self) -> str:
        return self._location_query

    # endregion properties

    # region get methods

    # endregion get methods

    # region get_x_params methods

    def get_all_params(self) -> dict:
        return {
            "path": self.get_path_params(),
            "query": self.get_query_params(),
        }

    def get_path_params(self) -> dict:
        result = {}
        if hasattr(self, "namespace"):
            result["namespace"] = self.namespace
        return result

    def get_query_params(self) -> dict:
        result = {}
        if hasattr(self, "field"):
            result["field"] = self.field
        if hasattr(self, "query"):
            result["query"] = self.query
        return result

    # endregion get_x_params methods

    # region is/has methods

    # endregion is/has methods

    # region with_x methods

    def with_namespace(self, value: str) -> CheckUserAvailability:
        self.namespace = value
        return self

    def with_field(self, value: str) -> CheckUserAvailability:
        self.field = value
        return self

    def with_query(self, value: str) -> CheckUserAvailability:
        self.query = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "namespace") and self.namespace:
            result["namespace"] = str(self.namespace)
        elif include_empty:
            result["namespace"] = ""
        if hasattr(self, "field") and self.field:
            result["field"] = str(self.field)
        elif include_empty:
            result["field"] = ""
        if hasattr(self, "query") and self.query:
            result["query"] = str(self.query)
        elif include_empty:
            result["query"] = ""
        return result

    # endregion to methods

    # region response methods

    class Response(ApiResponse):
        data_204: Optional[HttpResponse] = None
        error_400: Optional[RestErrorResponse] = None
        error_404: Optional[HttpResponse] = None
        error_422: Optional[RestErrorResponse] = None

        def ok(self) -> CheckUserAvailability.Response:
            if self.error_400 is not None:
                err = self.error_400.translate_to_api_error()
                exc = err.to_exception()
                if exc is not None:
                    raise exc  # pylint: disable=raising-bad-type
            if self.error_404 is not None:
                err = ApiError.create_from_http_response(self.error_404)
                exc = err.to_exception()
                if exc is not None:
                    raise exc  # pylint: disable=raising-bad-type
            if self.error_422 is not None:
                err = self.error_422.translate_to_api_error()
                exc = err.to_exception()
                if exc is not None:
                    raise exc  # pylint: disable=raising-bad-type
            return self

        def __iter__(self):
            if self.data_204 is not None:
                yield self.data_204
                yield None
            elif self.error_400 is not None:
                yield None
                yield self.error_400
            elif self.error_404 is not None:
                yield None
                yield self.error_404
            elif self.error_422 is not None:
                yield None
                yield self.error_422
            else:
                yield None
                yield self.error

    # noinspection PyMethodMayBeStatic
    def parse_response(self, code: int, content_type: str, content: Any) -> Response:
        """Parse the given response.

        204: No Content - (No Content)

        400: Bad Request - RestErrorResponse (20002: validation error)

        404: Not Found - (Not Found)

        422: Unprocessable Entity - RestErrorResponse (20002: validation error)

        ---: HttpResponse (Undocumented Response)

        ---: HttpResponse (Unexpected Content-Type Error)

        ---: HttpResponse (Unhandled Error)
        """
        result = CheckUserAvailability.Response()

        pre_processed_response, error = self.pre_process_response(
            code=code, content_type=content_type, content=content
        )

        if error is not None:
            if not error.is_no_content():
                result.error = ApiError.create_from_http_response(error)
        else:
            code, content_type, content = pre_processed_response

            if code == 204:
                result.data_204 = None
            elif code == 400:
                result.error_400 = RestErrorResponse.create_from_dict(content)
                result.error = result.error_400.translate_to_api_error()
            elif code == 404:
                result.error_404 = HttpResponse.create(code, content)
                result.error = ApiError.create_from_http_response(result.error_404)
            elif code == 422:
                result.error_422 = RestErrorResponse.create_from_dict(content)
                result.error = result.error_422.translate_to_api_error()
            else:
                result.error = ApiError.create_from_http_response(
                    HttpResponse.create_undocumented_response(
                        code=code, content_type=content_type, content=content
                    )
                )

        result.status_code = str(code)
        result.content_type = content_type

        if 400 <= code <= 599 or result.error is not None:
            result.is_success = False

        return result

    # noinspection PyMethodMayBeStatic
    @deprecated
    def parse_response_x(
        self, code: int, content_type: str, content: Any
    ) -> Tuple[None, Union[None, HttpResponse, RestErrorResponse]]:
        """Parse the given response.

        204: No Content - (No Content)

        400: Bad Request - RestErrorResponse (20002: validation error)

        404: Not Found - (Not Found)

        422: Unprocessable Entity - RestErrorResponse (20002: validation error)

        ---: HttpResponse (Undocumented Response)

        ---: HttpResponse (Unexpected Content-Type Error)

        ---: HttpResponse (Unhandled Error)
        """
        pre_processed_response, error = self.pre_process_response(
            code=code, content_type=content_type, content=content
        )
        if error is not None:
            return None, None if error.is_no_content() else error
        code, content_type, content = pre_processed_response

        if code == 204:
            return None, None
        if code == 400:
            return None, RestErrorResponse.create_from_dict(content)
        if code == 404:
            return None, HttpResponse.create(code, "Not Found")
        if code == 422:
            return None, RestErrorResponse.create_from_dict(content)

        return self.handle_undocumented_response(
            code=code, content_type=content_type, content=content
        )

    # endregion response methods

    # region static methods

    @classmethod
    def create(
        cls, namespace: str, field: str, query: str, **kwargs
    ) -> CheckUserAvailability:
        instance = cls()
        instance.namespace = namespace
        instance.field = field
        instance.query = query
        if x_flight_id := kwargs.get("x_flight_id", None):
            instance.x_flight_id = x_flight_id
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> CheckUserAvailability:
        instance = cls()
        if "namespace" in dict_ and dict_["namespace"] is not None:
            instance.namespace = str(dict_["namespace"])
        elif include_empty:
            instance.namespace = ""
        if "field" in dict_ and dict_["field"] is not None:
            instance.field = str(dict_["field"])
        elif include_empty:
            instance.field = ""
        if "query" in dict_ and dict_["query"] is not None:
            instance.query = str(dict_["query"])
        elif include_empty:
            instance.query = ""
        return instance

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {
            "namespace": "namespace",
            "field": "field",
            "query": "query",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "namespace": True,
            "field": True,
            "query": True,
        }

    # endregion static methods
