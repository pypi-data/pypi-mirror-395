# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, Union, Iterable, cast
from datetime import datetime
from typing_extensions import Literal, overload

import httpx

from ..types import (
    order_create_params,
    order_update_params,
    order_update_status_params,
    order_upload_results_params,
    order_retrieve_results_params,
    order_send_for_employee_params,
    order_schedule_appointment_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import required_args, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.order_create_response import OrderCreateResponse
from ..types.order_update_response import OrderUpdateResponse
from ..types.order_retrieve_response import OrderRetrieveResponse
from ..types.order_update_status_response import OrderUpdateStatusResponse
from ..types.order_upload_results_response import OrderUploadResultsResponse
from ..types.order_retrieve_results_response import OrderRetrieveResultsResponse
from ..types.order_send_for_employee_response import OrderSendForEmployeeResponse
from ..types.order_schedule_appointment_response import OrderScheduleAppointmentResponse

__all__ = ["OrdersResource", "AsyncOrdersResource"]


class OrdersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OrdersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#accessing-raw-response-data-eg-headers
        """
        return OrdersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrdersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#with_streaming_response
        """
        return OrdersResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        payment_method: Literal["self-pay", "employer-sponsored"],
        person: order_create_params.Variant0Person,
        provider_id: str,
        services: Iterable[order_create_params.Variant0Service],
        _id: str | Omit = omit,
        brand_id: str | Omit = omit,
        due_date: Union[str, datetime] | Omit = omit,
        due_dates: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        employee_id: str | Omit = omit,
        employee_ids: SequenceNotStr[str] | Omit = omit,
        employer_id: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        provider_created: bool | Omit = omit,
        providers_ids: Iterable[order_create_params.Variant0ProvidersID] | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        re_captcha_token: str | Omit = omit,
        services_ids: SequenceNotStr[str] | Omit = omit,
        token_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderCreateResponse:
        """
        Create orders for consumers (self-pay or employer-sponsored), employers, or bulk
        orders. Consolidates functionality from legacy Order.createOrder and
        Order.SendOrder methods.

        Args:
          metadata: Optional arbitrary metadata (<=10KB when JSON stringified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        employee_id: str,
        employer_id: str,
        services: Iterable[order_create_params.Variant1Service],
        _id: str | Omit = omit,
        brand_id: str | Omit = omit,
        due_date: Union[str, datetime] | Omit = omit,
        due_dates: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        employee_ids: SequenceNotStr[str] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        payment_method: Literal["self-pay", "employer-sponsored"] | Omit = omit,
        person: order_create_params.Variant1Person | Omit = omit,
        provider_created: bool | Omit = omit,
        provider_id: str | Omit = omit,
        providers_ids: Iterable[order_create_params.Variant1ProvidersID] | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        re_captcha_token: str | Omit = omit,
        services_ids: SequenceNotStr[str] | Omit = omit,
        token_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderCreateResponse:
        """
        Create orders for consumers (self-pay or employer-sponsored), employers, or bulk
        orders. Consolidates functionality from legacy Order.createOrder and
        Order.SendOrder methods.

        Args:
          metadata: Optional arbitrary metadata (<=10KB when JSON stringified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        employee_id: str,
        employer_id: str,
        providers_ids: Iterable[order_create_params.Variant2ProvidersID],
        services_ids: SequenceNotStr[str],
        _id: str | Omit = omit,
        brand_id: str | Omit = omit,
        due_date: Union[str, datetime] | Omit = omit,
        due_dates: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        employee_ids: SequenceNotStr[str] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        payment_method: Literal["self-pay", "employer-sponsored"] | Omit = omit,
        person: order_create_params.Variant2Person | Omit = omit,
        provider_created: bool | Omit = omit,
        provider_id: str | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        re_captcha_token: str | Omit = omit,
        services: Iterable[order_create_params.Variant2Service] | Omit = omit,
        token_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderCreateResponse:
        """
        Create orders for consumers (self-pay or employer-sponsored), employers, or bulk
        orders. Consolidates functionality from legacy Order.createOrder and
        Order.SendOrder methods.

        Args:
          metadata: Optional arbitrary metadata (<=10KB when JSON stringified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        employee_ids: SequenceNotStr[str],
        employer_id: str,
        providers_ids: Iterable[order_create_params.Variant3ProvidersID],
        services_ids: SequenceNotStr[str],
        _id: str | Omit = omit,
        brand_id: str | Omit = omit,
        due_date: Union[str, datetime] | Omit = omit,
        due_dates: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        employee_id: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        payment_method: Literal["self-pay", "employer-sponsored"] | Omit = omit,
        person: order_create_params.Variant3Person | Omit = omit,
        provider_created: bool | Omit = omit,
        provider_id: str | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        re_captcha_token: str | Omit = omit,
        services: Iterable[order_create_params.Variant3Service] | Omit = omit,
        token_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderCreateResponse:
        """
        Create orders for consumers (self-pay or employer-sponsored), employers, or bulk
        orders. Consolidates functionality from legacy Order.createOrder and
        Order.SendOrder methods.

        Args:
          metadata: Optional arbitrary metadata (<=10KB when JSON stringified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["payment_method", "person", "provider_id", "services"],
        ["employee_id", "employer_id", "services"],
        ["employee_id", "employer_id", "providers_ids", "services_ids"],
        ["employee_ids", "employer_id", "providers_ids", "services_ids"],
    )
    def create(
        self,
        *,
        payment_method: Literal["self-pay", "employer-sponsored"] | Omit = omit,
        person: order_create_params.Variant0Person
        | order_create_params.Variant1Person
        | order_create_params.Variant2Person
        | order_create_params.Variant3Person
        | Omit = omit,
        provider_id: str | Omit = omit,
        services: Iterable[order_create_params.Variant0Service]
        | Iterable[order_create_params.Variant1Service]
        | Iterable[order_create_params.Variant2Service]
        | Iterable[order_create_params.Variant3Service]
        | Omit = omit,
        _id: str | Omit = omit,
        brand_id: str | Omit = omit,
        due_date: Union[str, datetime] | Omit = omit,
        due_dates: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        employee_id: str | Omit = omit,
        employee_ids: SequenceNotStr[str] | Omit = omit,
        employer_id: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        provider_created: bool | Omit = omit,
        providers_ids: Iterable[order_create_params.Variant0ProvidersID]
        | Iterable[order_create_params.Variant1ProvidersID]
        | Iterable[order_create_params.Variant2ProvidersID]
        | Iterable[order_create_params.Variant3ProvidersID]
        | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        re_captcha_token: str | Omit = omit,
        services_ids: SequenceNotStr[str] | Omit = omit,
        token_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderCreateResponse:
        return cast(
            OrderCreateResponse,
            self._post(
                "/v1/orders",
                body=maybe_transform(
                    {
                        "payment_method": payment_method,
                        "person": person,
                        "provider_id": provider_id,
                        "services": services,
                        "_id": _id,
                        "brand_id": brand_id,
                        "due_date": due_date,
                        "due_dates": due_dates,
                        "employee_id": employee_id,
                        "employee_ids": employee_ids,
                        "employer_id": employer_id,
                        "metadata": metadata,
                        "provider_created": provider_created,
                        "providers_ids": providers_ids,
                        "quantities": quantities,
                        "re_captcha_token": re_captcha_token,
                        "services_ids": services_ids,
                        "token_id": token_id,
                    },
                    order_create_params.OrderCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, OrderCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        order_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderRetrieveResponse:
        """
        Retrieve details for a specific order

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return self._get(
            f"/v1/orders/{order_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRetrieveResponse,
        )

    def update(
        self,
        order_id: str,
        *,
        metadata: Dict[str, object] | Omit = omit,
        services: Iterable[order_update_params.Service] | Omit = omit,
        status: Literal[
            "order_sent", "order_accepted", "order_refused", "employee_confirmed", "order_fulfilled", "order_complete"
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderUpdateResponse:
        """Update order details and associated order items.

        Allows updating order status,
        metadata, and modifying order item services.

        Args:
          metadata: Arbitrary metadata to update on the order (non-indexed passthrough, <=10KB when
              JSON stringified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return self._post(
            f"/v1/orders/{order_id}",
            body=maybe_transform(
                {
                    "metadata": metadata,
                    "services": services,
                    "status": status,
                },
                order_update_params.OrderUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderUpdateResponse,
        )

    def retrieve_results(
        self,
        order_id: str,
        *,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        service_id: str | Omit = omit,
        since: Union[str, datetime] | Omit = omit,
        status: str | Omit = omit,
        until: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderRetrieveResultsResponse:
        """Retrieve results for an order.

        Supports filtering by serviceId, status, date
        window, and pagination.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return self._get(
            f"/v1/orders/{order_id}/results",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "service_id": service_id,
                        "since": since,
                        "status": status,
                        "until": until,
                    },
                    order_retrieve_results_params.OrderRetrieveResultsParams,
                ),
            ),
            cast_to=OrderRetrieveResultsResponse,
        )

    def schedule_appointment(
        self,
        order_id: str,
        *,
        appointment: order_schedule_appointment_params.Appointment,
        order_access_code: str | Omit = omit,
        provider_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderScheduleAppointmentResponse:
        """Schedule an appointment or walk-in for an existing order.

        Sends HL7 SIU^S12
        message for appointment booking.

        Args:
          order_access_code: Order access code for authorization

          provider_id: Provider ID for authorization

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return self._post(
            f"/v1/orders/{order_id}/schedule-appointment",
            body=maybe_transform(
                {
                    "appointment": appointment,
                    "order_access_code": order_access_code,
                    "provider_id": provider_id,
                },
                order_schedule_appointment_params.OrderScheduleAppointmentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderScheduleAppointmentResponse,
        )

    def send_for_employee(
        self,
        *,
        employee_id: str,
        employer_id: str,
        providers_ids: Iterable[order_send_for_employee_params.ProvidersID],
        services_ids: SequenceNotStr[str],
        login_token: str,
        user_id: str,
        brand_id: str | Omit = omit,
        due_date: str | Omit = omit,
        due_dates: SequenceNotStr[str] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        provider_created: bool | Omit = omit,
        provider_id: str | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderSendForEmployeeResponse:
        """Send an order for a specific employee.

        Requires API key, login token, and user
        ID. This endpoint specifically handles employer-to-employee order sending.

        Args:
          employee_id: Employee ID to send order to

          employer_id: Employer ID sending the order

          providers_ids: Array mapping each service (by index) to a provider; serviceId optional

          services_ids: Array of service IDs to include in the order

          brand_id: Brand ID for branded orders

          due_date: Due date for the order (date or date-time ISO string)

          due_dates: Array of due dates per service

          metadata: Optional arbitrary metadata to store on the order (non-indexed passthrough,
              <=10KB when JSON stringified)

          provider_created: Whether this order is being created by a provider (affects permission checking)

          provider_id: Single provider ID (shortcut when all services map to one provider)

          quantities: Service ID to quantity mapping

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"login-token": login_token, "user-id": user_id, **(extra_headers or {})}
        return cast(
            OrderSendForEmployeeResponse,
            self._post(
                "/v1/orders/send",
                body=maybe_transform(
                    {
                        "employee_id": employee_id,
                        "employer_id": employer_id,
                        "providers_ids": providers_ids,
                        "services_ids": services_ids,
                        "brand_id": brand_id,
                        "due_date": due_date,
                        "due_dates": due_dates,
                        "metadata": metadata,
                        "provider_created": provider_created,
                        "provider_id": provider_id,
                        "quantities": quantities,
                    },
                    order_send_for_employee_params.OrderSendForEmployeeParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, OrderSendForEmployeeResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def update_status(
        self,
        order_id: str,
        *,
        status: Literal[
            "order_sent", "order_accepted", "order_refused", "employee_confirmed", "order_fulfilled", "order_complete"
        ],
        message: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderUpdateStatusResponse:
        """
        Update the status of an existing order

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return self._put(
            f"/v1/orders/{order_id}/status",
            body=maybe_transform(
                {
                    "status": status,
                    "message": message,
                },
                order_update_status_params.OrderUpdateStatusParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderUpdateStatusResponse,
        )

    def upload_results(
        self,
        order_id: str,
        *,
        captcha_token: str,
        order_access_code: str,
        service_id: str,
        dob: str | Omit = omit,
        file_ids: SequenceNotStr[str] | Omit = omit,
        files: Iterable[order_upload_results_params.File] | Omit = omit,
        last_name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderUploadResultsResponse:
        """Upload test results for a specific order item.

        Supports both existing fileIds
        and base64 encoded files. Requires order access code and employee verification.

        Args:
          dob: Date of birth in YYYY-MM-DD format

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return self._post(
            f"/v1/orders/{order_id}/upload-results",
            body=maybe_transform(
                {
                    "captcha_token": captcha_token,
                    "order_access_code": order_access_code,
                    "service_id": service_id,
                    "dob": dob,
                    "file_ids": file_ids,
                    "files": files,
                    "last_name": last_name,
                },
                order_upload_results_params.OrderUploadResultsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderUploadResultsResponse,
        )


class AsyncOrdersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOrdersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOrdersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrdersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#with_streaming_response
        """
        return AsyncOrdersResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        payment_method: Literal["self-pay", "employer-sponsored"],
        person: order_create_params.Variant0Person,
        provider_id: str,
        services: Iterable[order_create_params.Variant0Service],
        _id: str | Omit = omit,
        brand_id: str | Omit = omit,
        due_date: Union[str, datetime] | Omit = omit,
        due_dates: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        employee_id: str | Omit = omit,
        employee_ids: SequenceNotStr[str] | Omit = omit,
        employer_id: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        provider_created: bool | Omit = omit,
        providers_ids: Iterable[order_create_params.Variant0ProvidersID] | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        re_captcha_token: str | Omit = omit,
        services_ids: SequenceNotStr[str] | Omit = omit,
        token_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderCreateResponse:
        """
        Create orders for consumers (self-pay or employer-sponsored), employers, or bulk
        orders. Consolidates functionality from legacy Order.createOrder and
        Order.SendOrder methods.

        Args:
          metadata: Optional arbitrary metadata (<=10KB when JSON stringified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        employee_id: str,
        employer_id: str,
        services: Iterable[order_create_params.Variant1Service],
        _id: str | Omit = omit,
        brand_id: str | Omit = omit,
        due_date: Union[str, datetime] | Omit = omit,
        due_dates: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        employee_ids: SequenceNotStr[str] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        payment_method: Literal["self-pay", "employer-sponsored"] | Omit = omit,
        person: order_create_params.Variant1Person | Omit = omit,
        provider_created: bool | Omit = omit,
        provider_id: str | Omit = omit,
        providers_ids: Iterable[order_create_params.Variant1ProvidersID] | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        re_captcha_token: str | Omit = omit,
        services_ids: SequenceNotStr[str] | Omit = omit,
        token_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderCreateResponse:
        """
        Create orders for consumers (self-pay or employer-sponsored), employers, or bulk
        orders. Consolidates functionality from legacy Order.createOrder and
        Order.SendOrder methods.

        Args:
          metadata: Optional arbitrary metadata (<=10KB when JSON stringified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        employee_id: str,
        employer_id: str,
        providers_ids: Iterable[order_create_params.Variant2ProvidersID],
        services_ids: SequenceNotStr[str],
        _id: str | Omit = omit,
        brand_id: str | Omit = omit,
        due_date: Union[str, datetime] | Omit = omit,
        due_dates: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        employee_ids: SequenceNotStr[str] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        payment_method: Literal["self-pay", "employer-sponsored"] | Omit = omit,
        person: order_create_params.Variant2Person | Omit = omit,
        provider_created: bool | Omit = omit,
        provider_id: str | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        re_captcha_token: str | Omit = omit,
        services: Iterable[order_create_params.Variant2Service] | Omit = omit,
        token_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderCreateResponse:
        """
        Create orders for consumers (self-pay or employer-sponsored), employers, or bulk
        orders. Consolidates functionality from legacy Order.createOrder and
        Order.SendOrder methods.

        Args:
          metadata: Optional arbitrary metadata (<=10KB when JSON stringified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        employee_ids: SequenceNotStr[str],
        employer_id: str,
        providers_ids: Iterable[order_create_params.Variant3ProvidersID],
        services_ids: SequenceNotStr[str],
        _id: str | Omit = omit,
        brand_id: str | Omit = omit,
        due_date: Union[str, datetime] | Omit = omit,
        due_dates: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        employee_id: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        payment_method: Literal["self-pay", "employer-sponsored"] | Omit = omit,
        person: order_create_params.Variant3Person | Omit = omit,
        provider_created: bool | Omit = omit,
        provider_id: str | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        re_captcha_token: str | Omit = omit,
        services: Iterable[order_create_params.Variant3Service] | Omit = omit,
        token_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderCreateResponse:
        """
        Create orders for consumers (self-pay or employer-sponsored), employers, or bulk
        orders. Consolidates functionality from legacy Order.createOrder and
        Order.SendOrder methods.

        Args:
          metadata: Optional arbitrary metadata (<=10KB when JSON stringified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["payment_method", "person", "provider_id", "services"],
        ["employee_id", "employer_id", "services"],
        ["employee_id", "employer_id", "providers_ids", "services_ids"],
        ["employee_ids", "employer_id", "providers_ids", "services_ids"],
    )
    async def create(
        self,
        *,
        payment_method: Literal["self-pay", "employer-sponsored"] | Omit = omit,
        person: order_create_params.Variant0Person
        | order_create_params.Variant1Person
        | order_create_params.Variant2Person
        | order_create_params.Variant3Person
        | Omit = omit,
        provider_id: str | Omit = omit,
        services: Iterable[order_create_params.Variant0Service]
        | Iterable[order_create_params.Variant1Service]
        | Iterable[order_create_params.Variant2Service]
        | Iterable[order_create_params.Variant3Service]
        | Omit = omit,
        _id: str | Omit = omit,
        brand_id: str | Omit = omit,
        due_date: Union[str, datetime] | Omit = omit,
        due_dates: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        employee_id: str | Omit = omit,
        employee_ids: SequenceNotStr[str] | Omit = omit,
        employer_id: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        provider_created: bool | Omit = omit,
        providers_ids: Iterable[order_create_params.Variant0ProvidersID]
        | Iterable[order_create_params.Variant1ProvidersID]
        | Iterable[order_create_params.Variant2ProvidersID]
        | Iterable[order_create_params.Variant3ProvidersID]
        | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        re_captcha_token: str | Omit = omit,
        services_ids: SequenceNotStr[str] | Omit = omit,
        token_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderCreateResponse:
        return cast(
            OrderCreateResponse,
            await self._post(
                "/v1/orders",
                body=await async_maybe_transform(
                    {
                        "payment_method": payment_method,
                        "person": person,
                        "provider_id": provider_id,
                        "services": services,
                        "_id": _id,
                        "brand_id": brand_id,
                        "due_date": due_date,
                        "due_dates": due_dates,
                        "employee_id": employee_id,
                        "employee_ids": employee_ids,
                        "employer_id": employer_id,
                        "metadata": metadata,
                        "provider_created": provider_created,
                        "providers_ids": providers_ids,
                        "quantities": quantities,
                        "re_captcha_token": re_captcha_token,
                        "services_ids": services_ids,
                        "token_id": token_id,
                    },
                    order_create_params.OrderCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, OrderCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        order_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderRetrieveResponse:
        """
        Retrieve details for a specific order

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return await self._get(
            f"/v1/orders/{order_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRetrieveResponse,
        )

    async def update(
        self,
        order_id: str,
        *,
        metadata: Dict[str, object] | Omit = omit,
        services: Iterable[order_update_params.Service] | Omit = omit,
        status: Literal[
            "order_sent", "order_accepted", "order_refused", "employee_confirmed", "order_fulfilled", "order_complete"
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderUpdateResponse:
        """Update order details and associated order items.

        Allows updating order status,
        metadata, and modifying order item services.

        Args:
          metadata: Arbitrary metadata to update on the order (non-indexed passthrough, <=10KB when
              JSON stringified)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return await self._post(
            f"/v1/orders/{order_id}",
            body=await async_maybe_transform(
                {
                    "metadata": metadata,
                    "services": services,
                    "status": status,
                },
                order_update_params.OrderUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderUpdateResponse,
        )

    async def retrieve_results(
        self,
        order_id: str,
        *,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        service_id: str | Omit = omit,
        since: Union[str, datetime] | Omit = omit,
        status: str | Omit = omit,
        until: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderRetrieveResultsResponse:
        """Retrieve results for an order.

        Supports filtering by serviceId, status, date
        window, and pagination.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return await self._get(
            f"/v1/orders/{order_id}/results",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "service_id": service_id,
                        "since": since,
                        "status": status,
                        "until": until,
                    },
                    order_retrieve_results_params.OrderRetrieveResultsParams,
                ),
            ),
            cast_to=OrderRetrieveResultsResponse,
        )

    async def schedule_appointment(
        self,
        order_id: str,
        *,
        appointment: order_schedule_appointment_params.Appointment,
        order_access_code: str | Omit = omit,
        provider_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderScheduleAppointmentResponse:
        """Schedule an appointment or walk-in for an existing order.

        Sends HL7 SIU^S12
        message for appointment booking.

        Args:
          order_access_code: Order access code for authorization

          provider_id: Provider ID for authorization

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return await self._post(
            f"/v1/orders/{order_id}/schedule-appointment",
            body=await async_maybe_transform(
                {
                    "appointment": appointment,
                    "order_access_code": order_access_code,
                    "provider_id": provider_id,
                },
                order_schedule_appointment_params.OrderScheduleAppointmentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderScheduleAppointmentResponse,
        )

    async def send_for_employee(
        self,
        *,
        employee_id: str,
        employer_id: str,
        providers_ids: Iterable[order_send_for_employee_params.ProvidersID],
        services_ids: SequenceNotStr[str],
        login_token: str,
        user_id: str,
        brand_id: str | Omit = omit,
        due_date: str | Omit = omit,
        due_dates: SequenceNotStr[str] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        provider_created: bool | Omit = omit,
        provider_id: str | Omit = omit,
        quantities: Dict[str, int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderSendForEmployeeResponse:
        """Send an order for a specific employee.

        Requires API key, login token, and user
        ID. This endpoint specifically handles employer-to-employee order sending.

        Args:
          employee_id: Employee ID to send order to

          employer_id: Employer ID sending the order

          providers_ids: Array mapping each service (by index) to a provider; serviceId optional

          services_ids: Array of service IDs to include in the order

          brand_id: Brand ID for branded orders

          due_date: Due date for the order (date or date-time ISO string)

          due_dates: Array of due dates per service

          metadata: Optional arbitrary metadata to store on the order (non-indexed passthrough,
              <=10KB when JSON stringified)

          provider_created: Whether this order is being created by a provider (affects permission checking)

          provider_id: Single provider ID (shortcut when all services map to one provider)

          quantities: Service ID to quantity mapping

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"login-token": login_token, "user-id": user_id, **(extra_headers or {})}
        return cast(
            OrderSendForEmployeeResponse,
            await self._post(
                "/v1/orders/send",
                body=await async_maybe_transform(
                    {
                        "employee_id": employee_id,
                        "employer_id": employer_id,
                        "providers_ids": providers_ids,
                        "services_ids": services_ids,
                        "brand_id": brand_id,
                        "due_date": due_date,
                        "due_dates": due_dates,
                        "metadata": metadata,
                        "provider_created": provider_created,
                        "provider_id": provider_id,
                        "quantities": quantities,
                    },
                    order_send_for_employee_params.OrderSendForEmployeeParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, OrderSendForEmployeeResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def update_status(
        self,
        order_id: str,
        *,
        status: Literal[
            "order_sent", "order_accepted", "order_refused", "employee_confirmed", "order_fulfilled", "order_complete"
        ],
        message: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderUpdateStatusResponse:
        """
        Update the status of an existing order

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return await self._put(
            f"/v1/orders/{order_id}/status",
            body=await async_maybe_transform(
                {
                    "status": status,
                    "message": message,
                },
                order_update_status_params.OrderUpdateStatusParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderUpdateStatusResponse,
        )

    async def upload_results(
        self,
        order_id: str,
        *,
        captcha_token: str,
        order_access_code: str,
        service_id: str,
        dob: str | Omit = omit,
        file_ids: SequenceNotStr[str] | Omit = omit,
        files: Iterable[order_upload_results_params.File] | Omit = omit,
        last_name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrderUploadResultsResponse:
        """Upload test results for a specific order item.

        Supports both existing fileIds
        and base64 encoded files. Requires order access code and employee verification.

        Args:
          dob: Date of birth in YYYY-MM-DD format

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not order_id:
            raise ValueError(f"Expected a non-empty value for `order_id` but received {order_id!r}")
        return await self._post(
            f"/v1/orders/{order_id}/upload-results",
            body=await async_maybe_transform(
                {
                    "captcha_token": captcha_token,
                    "order_access_code": order_access_code,
                    "service_id": service_id,
                    "dob": dob,
                    "file_ids": file_ids,
                    "files": files,
                    "last_name": last_name,
                },
                order_upload_results_params.OrderUploadResultsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderUploadResultsResponse,
        )


class OrdersResourceWithRawResponse:
    def __init__(self, orders: OrdersResource) -> None:
        self._orders = orders

        self.create = to_raw_response_wrapper(
            orders.create,
        )
        self.retrieve = to_raw_response_wrapper(
            orders.retrieve,
        )
        self.update = to_raw_response_wrapper(
            orders.update,
        )
        self.retrieve_results = to_raw_response_wrapper(
            orders.retrieve_results,
        )
        self.schedule_appointment = to_raw_response_wrapper(
            orders.schedule_appointment,
        )
        self.send_for_employee = to_raw_response_wrapper(
            orders.send_for_employee,
        )
        self.update_status = to_raw_response_wrapper(
            orders.update_status,
        )
        self.upload_results = to_raw_response_wrapper(
            orders.upload_results,
        )


class AsyncOrdersResourceWithRawResponse:
    def __init__(self, orders: AsyncOrdersResource) -> None:
        self._orders = orders

        self.create = async_to_raw_response_wrapper(
            orders.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            orders.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            orders.update,
        )
        self.retrieve_results = async_to_raw_response_wrapper(
            orders.retrieve_results,
        )
        self.schedule_appointment = async_to_raw_response_wrapper(
            orders.schedule_appointment,
        )
        self.send_for_employee = async_to_raw_response_wrapper(
            orders.send_for_employee,
        )
        self.update_status = async_to_raw_response_wrapper(
            orders.update_status,
        )
        self.upload_results = async_to_raw_response_wrapper(
            orders.upload_results,
        )


class OrdersResourceWithStreamingResponse:
    def __init__(self, orders: OrdersResource) -> None:
        self._orders = orders

        self.create = to_streamed_response_wrapper(
            orders.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            orders.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            orders.update,
        )
        self.retrieve_results = to_streamed_response_wrapper(
            orders.retrieve_results,
        )
        self.schedule_appointment = to_streamed_response_wrapper(
            orders.schedule_appointment,
        )
        self.send_for_employee = to_streamed_response_wrapper(
            orders.send_for_employee,
        )
        self.update_status = to_streamed_response_wrapper(
            orders.update_status,
        )
        self.upload_results = to_streamed_response_wrapper(
            orders.upload_results,
        )


class AsyncOrdersResourceWithStreamingResponse:
    def __init__(self, orders: AsyncOrdersResource) -> None:
        self._orders = orders

        self.create = async_to_streamed_response_wrapper(
            orders.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            orders.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            orders.update,
        )
        self.retrieve_results = async_to_streamed_response_wrapper(
            orders.retrieve_results,
        )
        self.schedule_appointment = async_to_streamed_response_wrapper(
            orders.schedule_appointment,
        )
        self.send_for_employee = async_to_streamed_response_wrapper(
            orders.send_for_employee,
        )
        self.update_status = async_to_streamed_response_wrapper(
            orders.update_status,
        )
        self.upload_results = async_to_streamed_response_wrapper(
            orders.upload_results,
        )
