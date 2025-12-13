# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
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
from ...types.employers import service_bundle_create_params, service_bundle_update_params
from ...types.employers.service_bundle_list_response import ServiceBundleListResponse
from ...types.employers.service_bundle_create_response import ServiceBundleCreateResponse
from ...types.employers.service_bundle_update_response import ServiceBundleUpdateResponse
from ...types.employers.service_bundle_retrieve_response import ServiceBundleRetrieveResponse

__all__ = ["ServiceBundlesResource", "AsyncServiceBundlesResource"]


class ServiceBundlesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ServiceBundlesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ServiceBundlesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ServiceBundlesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#with_streaming_response
        """
        return ServiceBundlesResourceWithStreamingResponse(self)

    def create(
        self,
        employer_id: str,
        *,
        bundle_name: str,
        service_ids: SequenceNotStr[str],
        _id: str | Omit = omit,
        limit: float | Omit = omit,
        occurrence: str | Omit = omit,
        recurring: bool | Omit = omit,
        roles: Optional[SequenceNotStr[str]] | Omit = omit,
        start_date: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ServiceBundleCreateResponse:
        """
        Create Service Bundle

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        return self._post(
            f"/v1/employers/{employer_id}/service-bundles",
            body=maybe_transform(
                {
                    "bundle_name": bundle_name,
                    "service_ids": service_ids,
                    "_id": _id,
                    "limit": limit,
                    "occurrence": occurrence,
                    "recurring": recurring,
                    "roles": roles,
                    "start_date": start_date,
                },
                service_bundle_create_params.ServiceBundleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceBundleCreateResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        employer_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ServiceBundleRetrieveResponse:
        """
        Get Service Bundle

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/employers/{employer_id}/service-bundles/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceBundleRetrieveResponse,
        )

    def update(
        self,
        id: str,
        *,
        employer_id: str,
        bundle_name: str,
        service_ids: SequenceNotStr[str],
        _id: str | Omit = omit,
        limit: float | Omit = omit,
        occurrence: str | Omit = omit,
        recurring: bool | Omit = omit,
        roles: Optional[SequenceNotStr[str]] | Omit = omit,
        start_date: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ServiceBundleUpdateResponse:
        """
        Update Service Bundle

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._put(
            f"/v1/employers/{employer_id}/service-bundles/{id}",
            body=maybe_transform(
                {
                    "bundle_name": bundle_name,
                    "service_ids": service_ids,
                    "_id": _id,
                    "limit": limit,
                    "occurrence": occurrence,
                    "recurring": recurring,
                    "roles": roles,
                    "start_date": start_date,
                },
                service_bundle_update_params.ServiceBundleUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceBundleUpdateResponse,
        )

    def list(
        self,
        employer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ServiceBundleListResponse:
        """
        List Service Bundles

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        return self._get(
            f"/v1/employers/{employer_id}/service-bundles",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceBundleListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        employer_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete Service Bundle

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/v1/employers/{employer_id}/service-bundles/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncServiceBundlesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncServiceBundlesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncServiceBundlesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncServiceBundlesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/bluehive-health/bluehive-sdk-python#with_streaming_response
        """
        return AsyncServiceBundlesResourceWithStreamingResponse(self)

    async def create(
        self,
        employer_id: str,
        *,
        bundle_name: str,
        service_ids: SequenceNotStr[str],
        _id: str | Omit = omit,
        limit: float | Omit = omit,
        occurrence: str | Omit = omit,
        recurring: bool | Omit = omit,
        roles: Optional[SequenceNotStr[str]] | Omit = omit,
        start_date: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ServiceBundleCreateResponse:
        """
        Create Service Bundle

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        return await self._post(
            f"/v1/employers/{employer_id}/service-bundles",
            body=await async_maybe_transform(
                {
                    "bundle_name": bundle_name,
                    "service_ids": service_ids,
                    "_id": _id,
                    "limit": limit,
                    "occurrence": occurrence,
                    "recurring": recurring,
                    "roles": roles,
                    "start_date": start_date,
                },
                service_bundle_create_params.ServiceBundleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceBundleCreateResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        employer_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ServiceBundleRetrieveResponse:
        """
        Get Service Bundle

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/employers/{employer_id}/service-bundles/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceBundleRetrieveResponse,
        )

    async def update(
        self,
        id: str,
        *,
        employer_id: str,
        bundle_name: str,
        service_ids: SequenceNotStr[str],
        _id: str | Omit = omit,
        limit: float | Omit = omit,
        occurrence: str | Omit = omit,
        recurring: bool | Omit = omit,
        roles: Optional[SequenceNotStr[str]] | Omit = omit,
        start_date: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ServiceBundleUpdateResponse:
        """
        Update Service Bundle

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._put(
            f"/v1/employers/{employer_id}/service-bundles/{id}",
            body=await async_maybe_transform(
                {
                    "bundle_name": bundle_name,
                    "service_ids": service_ids,
                    "_id": _id,
                    "limit": limit,
                    "occurrence": occurrence,
                    "recurring": recurring,
                    "roles": roles,
                    "start_date": start_date,
                },
                service_bundle_update_params.ServiceBundleUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceBundleUpdateResponse,
        )

    async def list(
        self,
        employer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ServiceBundleListResponse:
        """
        List Service Bundles

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        return await self._get(
            f"/v1/employers/{employer_id}/service-bundles",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceBundleListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        employer_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete Service Bundle

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not employer_id:
            raise ValueError(f"Expected a non-empty value for `employer_id` but received {employer_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/v1/employers/{employer_id}/service-bundles/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ServiceBundlesResourceWithRawResponse:
    def __init__(self, service_bundles: ServiceBundlesResource) -> None:
        self._service_bundles = service_bundles

        self.create = to_raw_response_wrapper(
            service_bundles.create,
        )
        self.retrieve = to_raw_response_wrapper(
            service_bundles.retrieve,
        )
        self.update = to_raw_response_wrapper(
            service_bundles.update,
        )
        self.list = to_raw_response_wrapper(
            service_bundles.list,
        )
        self.delete = to_raw_response_wrapper(
            service_bundles.delete,
        )


class AsyncServiceBundlesResourceWithRawResponse:
    def __init__(self, service_bundles: AsyncServiceBundlesResource) -> None:
        self._service_bundles = service_bundles

        self.create = async_to_raw_response_wrapper(
            service_bundles.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            service_bundles.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            service_bundles.update,
        )
        self.list = async_to_raw_response_wrapper(
            service_bundles.list,
        )
        self.delete = async_to_raw_response_wrapper(
            service_bundles.delete,
        )


class ServiceBundlesResourceWithStreamingResponse:
    def __init__(self, service_bundles: ServiceBundlesResource) -> None:
        self._service_bundles = service_bundles

        self.create = to_streamed_response_wrapper(
            service_bundles.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            service_bundles.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            service_bundles.update,
        )
        self.list = to_streamed_response_wrapper(
            service_bundles.list,
        )
        self.delete = to_streamed_response_wrapper(
            service_bundles.delete,
        )


class AsyncServiceBundlesResourceWithStreamingResponse:
    def __init__(self, service_bundles: AsyncServiceBundlesResource) -> None:
        self._service_bundles = service_bundles

        self.create = async_to_streamed_response_wrapper(
            service_bundles.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            service_bundles.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            service_bundles.update,
        )
        self.list = async_to_streamed_response_wrapper(
            service_bundles.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            service_bundles.delete,
        )
