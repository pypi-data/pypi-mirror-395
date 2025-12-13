# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable

import httpx

from ...types import employer_create_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from .service_bundles import (
    ServiceBundlesResource,
    AsyncServiceBundlesResource,
    ServiceBundlesResourceWithRawResponse,
    AsyncServiceBundlesResourceWithRawResponse,
    ServiceBundlesResourceWithStreamingResponse,
    AsyncServiceBundlesResourceWithStreamingResponse,
)
from ...types.employer_list_response import EmployerListResponse
from ...types.employer_create_response import EmployerCreateResponse
from ...types.employer_retrieve_response import EmployerRetrieveResponse

__all__ = ["EmployersResource", "AsyncEmployersResource"]


class EmployersResource(SyncAPIResource):
    @cached_property
    def service_bundles(self) -> ServiceBundlesResource:
        return ServiceBundlesResource(self._client)

    @cached_property
    def with_raw_response(self) -> EmployersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#accessing-raw-response-data-eg-headers
        """
        return EmployersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EmployersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#with_streaming_response
        """
        return EmployersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        address: employer_create_params.Address,
        email: str,
        name: str,
        phones: Iterable[employer_create_params.Phone],
        billing_address: Dict[str, object] | Omit = omit,
        checkr: employer_create_params.Checkr | Omit = omit,
        demo: bool | Omit = omit,
        employee_consent: bool | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        onsite_clinic: bool | Omit = omit,
        website: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmployerCreateResponse:
        """
        Create Employer

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/employers",
            body=maybe_transform(
                {
                    "address": address,
                    "email": email,
                    "name": name,
                    "phones": phones,
                    "billing_address": billing_address,
                    "checkr": checkr,
                    "demo": demo,
                    "employee_consent": employee_consent,
                    "metadata": metadata,
                    "onsite_clinic": onsite_clinic,
                    "website": website,
                },
                employer_create_params.EmployerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmployerCreateResponse,
        )

    def retrieve(
        self,
        employer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmployerRetrieveResponse:
        """
        Get Employer

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        return self._get(
            f"/v1/employers/{employer_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmployerRetrieveResponse,
        )

    def list(
        self,
        *,
        login_token: str,
        user_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmployerListResponse:
        """
        Get Employers for Current User

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"login-token": login_token, "user-id": user_id, **(extra_headers or {})}
        return self._get(
            "/v1/employers/list",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmployerListResponse,
        )


class AsyncEmployersResource(AsyncAPIResource):
    @cached_property
    def service_bundles(self) -> AsyncServiceBundlesResource:
        return AsyncServiceBundlesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEmployersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEmployersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEmployersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#with_streaming_response
        """
        return AsyncEmployersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        address: employer_create_params.Address,
        email: str,
        name: str,
        phones: Iterable[employer_create_params.Phone],
        billing_address: Dict[str, object] | Omit = omit,
        checkr: employer_create_params.Checkr | Omit = omit,
        demo: bool | Omit = omit,
        employee_consent: bool | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        onsite_clinic: bool | Omit = omit,
        website: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmployerCreateResponse:
        """
        Create Employer

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/employers",
            body=await async_maybe_transform(
                {
                    "address": address,
                    "email": email,
                    "name": name,
                    "phones": phones,
                    "billing_address": billing_address,
                    "checkr": checkr,
                    "demo": demo,
                    "employee_consent": employee_consent,
                    "metadata": metadata,
                    "onsite_clinic": onsite_clinic,
                    "website": website,
                },
                employer_create_params.EmployerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmployerCreateResponse,
        )

    async def retrieve(
        self,
        employer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmployerRetrieveResponse:
        """
        Get Employer

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        return await self._get(
            f"/v1/employers/{employer_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmployerRetrieveResponse,
        )

    async def list(
        self,
        *,
        login_token: str,
        user_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmployerListResponse:
        """
        Get Employers for Current User

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"login-token": login_token, "user-id": user_id, **(extra_headers or {})}
        return await self._get(
            "/v1/employers/list",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmployerListResponse,
        )


class EmployersResourceWithRawResponse:
    def __init__(self, employers: EmployersResource) -> None:
        self._employers = employers

        self.create = to_raw_response_wrapper(
            employers.create,
        )
        self.retrieve = to_raw_response_wrapper(
            employers.retrieve,
        )
        self.list = to_raw_response_wrapper(
            employers.list,
        )

    @cached_property
    def service_bundles(self) -> ServiceBundlesResourceWithRawResponse:
        return ServiceBundlesResourceWithRawResponse(self._employers.service_bundles)


class AsyncEmployersResourceWithRawResponse:
    def __init__(self, employers: AsyncEmployersResource) -> None:
        self._employers = employers

        self.create = async_to_raw_response_wrapper(
            employers.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            employers.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            employers.list,
        )

    @cached_property
    def service_bundles(self) -> AsyncServiceBundlesResourceWithRawResponse:
        return AsyncServiceBundlesResourceWithRawResponse(self._employers.service_bundles)


class EmployersResourceWithStreamingResponse:
    def __init__(self, employers: EmployersResource) -> None:
        self._employers = employers

        self.create = to_streamed_response_wrapper(
            employers.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            employers.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            employers.list,
        )

    @cached_property
    def service_bundles(self) -> ServiceBundlesResourceWithStreamingResponse:
        return ServiceBundlesResourceWithStreamingResponse(self._employers.service_bundles)


class AsyncEmployersResourceWithStreamingResponse:
    def __init__(self, employers: AsyncEmployersResource) -> None:
        self._employers = employers

        self.create = async_to_streamed_response_wrapper(
            employers.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            employers.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            employers.list,
        )

    @cached_property
    def service_bundles(self) -> AsyncServiceBundlesResourceWithStreamingResponse:
        return AsyncServiceBundlesResourceWithStreamingResponse(self._employers.service_bundles)
