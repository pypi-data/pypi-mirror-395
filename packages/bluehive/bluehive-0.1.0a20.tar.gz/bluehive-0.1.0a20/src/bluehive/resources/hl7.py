# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import hl7_send_results_params
from .._types import Body, Query, Headers, NotGiven, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["Hl7Resource", "AsyncHl7Resource"]


class Hl7Resource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> Hl7ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#accessing-raw-response-data-eg-headers
        """
        return Hl7ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> Hl7ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#with_streaming_response
        """
        return Hl7ResourceWithStreamingResponse(self)

    def send_results(
        self,
        *,
        employee_id: str,
        file: hl7_send_results_params.File,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> str:
        """
        Send lab results or documents via HL7

        Args:
          employee_id: Employee ID to send results for

          file: File containing the results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/hl7/results",
            body=maybe_transform(
                {
                    "employee_id": employee_id,
                    "file": file,
                },
                hl7_send_results_params.Hl7SendResultsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class AsyncHl7Resource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncHl7ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncHl7ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHl7ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#with_streaming_response
        """
        return AsyncHl7ResourceWithStreamingResponse(self)

    async def send_results(
        self,
        *,
        employee_id: str,
        file: hl7_send_results_params.File,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> str:
        """
        Send lab results or documents via HL7

        Args:
          employee_id: Employee ID to send results for

          file: File containing the results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/hl7/results",
            body=await async_maybe_transform(
                {
                    "employee_id": employee_id,
                    "file": file,
                },
                hl7_send_results_params.Hl7SendResultsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class Hl7ResourceWithRawResponse:
    def __init__(self, hl7: Hl7Resource) -> None:
        self._hl7 = hl7

        self.send_results = to_raw_response_wrapper(
            hl7.send_results,
        )


class AsyncHl7ResourceWithRawResponse:
    def __init__(self, hl7: AsyncHl7Resource) -> None:
        self._hl7 = hl7

        self.send_results = async_to_raw_response_wrapper(
            hl7.send_results,
        )


class Hl7ResourceWithStreamingResponse:
    def __init__(self, hl7: Hl7Resource) -> None:
        self._hl7 = hl7

        self.send_results = to_streamed_response_wrapper(
            hl7.send_results,
        )


class AsyncHl7ResourceWithStreamingResponse:
    def __init__(self, hl7: AsyncHl7Resource) -> None:
        self._hl7 = hl7

        self.send_results = async_to_streamed_response_wrapper(
            hl7.send_results,
        )
