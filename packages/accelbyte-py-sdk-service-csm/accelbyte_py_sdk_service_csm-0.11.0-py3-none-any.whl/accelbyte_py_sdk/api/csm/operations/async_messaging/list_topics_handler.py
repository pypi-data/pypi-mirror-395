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

# Custom Service Manager

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from accelbyte_py_sdk.core import ApiError, ApiResponse
from accelbyte_py_sdk.core import Operation
from accelbyte_py_sdk.core import HeaderStr
from accelbyte_py_sdk.core import HttpResponse
from accelbyte_py_sdk.core import deprecated

from ...models import ApimodelListTopicsResponse
from ...models import ResponseErrorResponse


class ListTopicsHandler(Operation):
    """List Async Messaging Topics (ListTopicsHandler)

    Required permission : `ADMIN:NAMESPACE:{namespace}:EXTEND:ASYNCMESSAGING:TOPICS [READ]`

    List all Async Messaging Topics inside a game namespace.

    Properties:
        url: /csm/v2/admin/namespaces/{namespace}/asyncmessaging/topics

        method: GET

        tags: ["Async Messaging"]

        consumes: ["application/json"]

        produces: ["application/json"]

        securities: [BEARER_AUTH]

        namespace: (namespace) REQUIRED str in path

        fuzzy_topic_name: (fuzzyTopicName) OPTIONAL str in query

        is_subscribed_by_app_name: (isSubscribedByAppName) OPTIONAL str in query

        is_unsubscribed_by_app_name: (isUnsubscribedByAppName) OPTIONAL str in query

        limit: (limit) OPTIONAL int in query

        offset: (offset) OPTIONAL int in query

    Responses:
        200: OK - ApimodelListTopicsResponse (OK)

        400: Bad Request - ResponseErrorResponse (Bad Request)

        401: Unauthorized - ResponseErrorResponse (Unauthorized)

        403: Forbidden - ResponseErrorResponse (Forbidden)

        500: Internal Server Error - ResponseErrorResponse (Internal Server Error)
    """

    # region fields

    _url: str = "/csm/v2/admin/namespaces/{namespace}/asyncmessaging/topics"
    _path: str = "/csm/v2/admin/namespaces/{namespace}/asyncmessaging/topics"
    _base_path: str = ""
    _method: str = "GET"
    _consumes: List[str] = ["application/json"]
    _produces: List[str] = ["application/json"]
    _securities: List[List[str]] = [["BEARER_AUTH"]]
    _location_query: str = None

    service_name: Optional[str] = "csm"

    namespace: str  # REQUIRED in [path]
    fuzzy_topic_name: str  # OPTIONAL in [query]
    is_subscribed_by_app_name: str  # OPTIONAL in [query]
    is_unsubscribed_by_app_name: str  # OPTIONAL in [query]
    limit: int  # OPTIONAL in [query]
    offset: int  # OPTIONAL in [query]

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
        if hasattr(self, "fuzzy_topic_name"):
            result["fuzzyTopicName"] = self.fuzzy_topic_name
        if hasattr(self, "is_subscribed_by_app_name"):
            result["isSubscribedByAppName"] = self.is_subscribed_by_app_name
        if hasattr(self, "is_unsubscribed_by_app_name"):
            result["isUnsubscribedByAppName"] = self.is_unsubscribed_by_app_name
        if hasattr(self, "limit"):
            result["limit"] = self.limit
        if hasattr(self, "offset"):
            result["offset"] = self.offset
        return result

    # endregion get_x_params methods

    # region is/has methods

    # endregion is/has methods

    # region with_x methods

    def with_namespace(self, value: str) -> ListTopicsHandler:
        self.namespace = value
        return self

    def with_fuzzy_topic_name(self, value: str) -> ListTopicsHandler:
        self.fuzzy_topic_name = value
        return self

    def with_is_subscribed_by_app_name(self, value: str) -> ListTopicsHandler:
        self.is_subscribed_by_app_name = value
        return self

    def with_is_unsubscribed_by_app_name(self, value: str) -> ListTopicsHandler:
        self.is_unsubscribed_by_app_name = value
        return self

    def with_limit(self, value: int) -> ListTopicsHandler:
        self.limit = value
        return self

    def with_offset(self, value: int) -> ListTopicsHandler:
        self.offset = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "namespace") and self.namespace:
            result["namespace"] = str(self.namespace)
        elif include_empty:
            result["namespace"] = ""
        if hasattr(self, "fuzzy_topic_name") and self.fuzzy_topic_name:
            result["fuzzyTopicName"] = str(self.fuzzy_topic_name)
        elif include_empty:
            result["fuzzyTopicName"] = ""
        if (
            hasattr(self, "is_subscribed_by_app_name")
            and self.is_subscribed_by_app_name
        ):
            result["isSubscribedByAppName"] = str(self.is_subscribed_by_app_name)
        elif include_empty:
            result["isSubscribedByAppName"] = ""
        if (
            hasattr(self, "is_unsubscribed_by_app_name")
            and self.is_unsubscribed_by_app_name
        ):
            result["isUnsubscribedByAppName"] = str(self.is_unsubscribed_by_app_name)
        elif include_empty:
            result["isUnsubscribedByAppName"] = ""
        if hasattr(self, "limit") and self.limit:
            result["limit"] = int(self.limit)
        elif include_empty:
            result["limit"] = 0
        if hasattr(self, "offset") and self.offset:
            result["offset"] = int(self.offset)
        elif include_empty:
            result["offset"] = 0
        return result

    # endregion to methods

    # region response methods

    class Response(ApiResponse):
        data_200: Optional[ApimodelListTopicsResponse] = None
        error_400: Optional[ResponseErrorResponse] = None
        error_401: Optional[ResponseErrorResponse] = None
        error_403: Optional[ResponseErrorResponse] = None
        error_500: Optional[ResponseErrorResponse] = None

        def ok(self) -> ListTopicsHandler.Response:
            if self.error_400 is not None:
                err = self.error_400.translate_to_api_error()
                exc = err.to_exception()
                if exc is not None:
                    raise exc  # pylint: disable=raising-bad-type
            if self.error_401 is not None:
                err = self.error_401.translate_to_api_error()
                exc = err.to_exception()
                if exc is not None:
                    raise exc  # pylint: disable=raising-bad-type
            if self.error_403 is not None:
                err = self.error_403.translate_to_api_error()
                exc = err.to_exception()
                if exc is not None:
                    raise exc  # pylint: disable=raising-bad-type
            if self.error_500 is not None:
                err = self.error_500.translate_to_api_error()
                exc = err.to_exception()
                if exc is not None:
                    raise exc  # pylint: disable=raising-bad-type
            return self

        def __iter__(self):
            if self.data_200 is not None:
                yield self.data_200
                yield None
            elif self.error_400 is not None:
                yield None
                yield self.error_400
            elif self.error_401 is not None:
                yield None
                yield self.error_401
            elif self.error_403 is not None:
                yield None
                yield self.error_403
            elif self.error_500 is not None:
                yield None
                yield self.error_500
            else:
                yield None
                yield self.error

    # noinspection PyMethodMayBeStatic
    def parse_response(self, code: int, content_type: str, content: Any) -> Response:
        """Parse the given response.

        200: OK - ApimodelListTopicsResponse (OK)

        400: Bad Request - ResponseErrorResponse (Bad Request)

        401: Unauthorized - ResponseErrorResponse (Unauthorized)

        403: Forbidden - ResponseErrorResponse (Forbidden)

        500: Internal Server Error - ResponseErrorResponse (Internal Server Error)

        ---: HttpResponse (Undocumented Response)

        ---: HttpResponse (Unexpected Content-Type Error)

        ---: HttpResponse (Unhandled Error)
        """
        result = ListTopicsHandler.Response()

        pre_processed_response, error = self.pre_process_response(
            code=code, content_type=content_type, content=content
        )

        if error is not None:
            if not error.is_no_content():
                result.error = ApiError.create_from_http_response(error)
        else:
            code, content_type, content = pre_processed_response

            if code == 200:
                result.data_200 = ApimodelListTopicsResponse.create_from_dict(content)
            elif code == 400:
                result.error_400 = ResponseErrorResponse.create_from_dict(content)
                result.error = result.error_400.translate_to_api_error()
            elif code == 401:
                result.error_401 = ResponseErrorResponse.create_from_dict(content)
                result.error = result.error_401.translate_to_api_error()
            elif code == 403:
                result.error_403 = ResponseErrorResponse.create_from_dict(content)
                result.error = result.error_403.translate_to_api_error()
            elif code == 500:
                result.error_500 = ResponseErrorResponse.create_from_dict(content)
                result.error = result.error_500.translate_to_api_error()
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
    ) -> Tuple[
        Union[None, ApimodelListTopicsResponse],
        Union[None, HttpResponse, ResponseErrorResponse],
    ]:
        """Parse the given response.

        200: OK - ApimodelListTopicsResponse (OK)

        400: Bad Request - ResponseErrorResponse (Bad Request)

        401: Unauthorized - ResponseErrorResponse (Unauthorized)

        403: Forbidden - ResponseErrorResponse (Forbidden)

        500: Internal Server Error - ResponseErrorResponse (Internal Server Error)

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

        if code == 200:
            return ApimodelListTopicsResponse.create_from_dict(content), None
        if code == 400:
            return None, ResponseErrorResponse.create_from_dict(content)
        if code == 401:
            return None, ResponseErrorResponse.create_from_dict(content)
        if code == 403:
            return None, ResponseErrorResponse.create_from_dict(content)
        if code == 500:
            return None, ResponseErrorResponse.create_from_dict(content)

        return self.handle_undocumented_response(
            code=code, content_type=content_type, content=content
        )

    # endregion response methods

    # region static methods

    @classmethod
    def create(
        cls,
        namespace: str,
        fuzzy_topic_name: Optional[str] = None,
        is_subscribed_by_app_name: Optional[str] = None,
        is_unsubscribed_by_app_name: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> ListTopicsHandler:
        instance = cls()
        instance.namespace = namespace
        if fuzzy_topic_name is not None:
            instance.fuzzy_topic_name = fuzzy_topic_name
        if is_subscribed_by_app_name is not None:
            instance.is_subscribed_by_app_name = is_subscribed_by_app_name
        if is_unsubscribed_by_app_name is not None:
            instance.is_unsubscribed_by_app_name = is_unsubscribed_by_app_name
        if limit is not None:
            instance.limit = limit
        if offset is not None:
            instance.offset = offset
        if x_flight_id := kwargs.get("x_flight_id", None):
            instance.x_flight_id = x_flight_id
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> ListTopicsHandler:
        instance = cls()
        if "namespace" in dict_ and dict_["namespace"] is not None:
            instance.namespace = str(dict_["namespace"])
        elif include_empty:
            instance.namespace = ""
        if "fuzzyTopicName" in dict_ and dict_["fuzzyTopicName"] is not None:
            instance.fuzzy_topic_name = str(dict_["fuzzyTopicName"])
        elif include_empty:
            instance.fuzzy_topic_name = ""
        if (
            "isSubscribedByAppName" in dict_
            and dict_["isSubscribedByAppName"] is not None
        ):
            instance.is_subscribed_by_app_name = str(dict_["isSubscribedByAppName"])
        elif include_empty:
            instance.is_subscribed_by_app_name = ""
        if (
            "isUnsubscribedByAppName" in dict_
            and dict_["isUnsubscribedByAppName"] is not None
        ):
            instance.is_unsubscribed_by_app_name = str(dict_["isUnsubscribedByAppName"])
        elif include_empty:
            instance.is_unsubscribed_by_app_name = ""
        if "limit" in dict_ and dict_["limit"] is not None:
            instance.limit = int(dict_["limit"])
        elif include_empty:
            instance.limit = 0
        if "offset" in dict_ and dict_["offset"] is not None:
            instance.offset = int(dict_["offset"])
        elif include_empty:
            instance.offset = 0
        return instance

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {
            "namespace": "namespace",
            "fuzzyTopicName": "fuzzy_topic_name",
            "isSubscribedByAppName": "is_subscribed_by_app_name",
            "isUnsubscribedByAppName": "is_unsubscribed_by_app_name",
            "limit": "limit",
            "offset": "offset",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "namespace": True,
            "fuzzyTopicName": False,
            "isSubscribedByAppName": False,
            "isUnsubscribedByAppName": False,
            "limit": False,
            "offset": False,
        }

    # endregion static methods
