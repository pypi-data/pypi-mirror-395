# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from bluehive import BlueHive, AsyncBlueHive
from tests.utils import assert_matches_type
from bluehive.types.employers import (
    ServiceBundleListResponse,
    ServiceBundleCreateResponse,
    ServiceBundleUpdateResponse,
    ServiceBundleRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestServiceBundles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: BlueHive) -> None:
        service_bundle = client.employers.service_bundles.create(
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        )
        assert_matches_type(ServiceBundleCreateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: BlueHive) -> None:
        service_bundle = client.employers.service_bundles.create(
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
            _id="_id",
            limit=0,
            occurrence="occurrence",
            recurring=True,
            roles=["string"],
            start_date="startDate",
        )
        assert_matches_type(ServiceBundleCreateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: BlueHive) -> None:
        response = client.employers.service_bundles.with_raw_response.create(
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_bundle = response.parse()
        assert_matches_type(ServiceBundleCreateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: BlueHive) -> None:
        with client.employers.service_bundles.with_streaming_response.create(
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_bundle = response.parse()
            assert_matches_type(ServiceBundleCreateResponse, service_bundle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_create(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            client.employers.service_bundles.with_raw_response.create(
                employer_id="",
                bundle_name="x",
                service_ids=["string"],
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: BlueHive) -> None:
        service_bundle = client.employers.service_bundles.retrieve(
            id="id",
            employer_id="employerId",
        )
        assert_matches_type(ServiceBundleRetrieveResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: BlueHive) -> None:
        response = client.employers.service_bundles.with_raw_response.retrieve(
            id="id",
            employer_id="employerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_bundle = response.parse()
        assert_matches_type(ServiceBundleRetrieveResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: BlueHive) -> None:
        with client.employers.service_bundles.with_streaming_response.retrieve(
            id="id",
            employer_id="employerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_bundle = response.parse()
            assert_matches_type(ServiceBundleRetrieveResponse, service_bundle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            client.employers.service_bundles.with_raw_response.retrieve(
                id="id",
                employer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.employers.service_bundles.with_raw_response.retrieve(
                id="",
                employer_id="employerId",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update(self, client: BlueHive) -> None:
        service_bundle = client.employers.service_bundles.update(
            id="id",
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        )
        assert_matches_type(ServiceBundleUpdateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: BlueHive) -> None:
        service_bundle = client.employers.service_bundles.update(
            id="id",
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
            _id="_id",
            limit=0,
            occurrence="occurrence",
            recurring=True,
            roles=["string"],
            start_date="startDate",
        )
        assert_matches_type(ServiceBundleUpdateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: BlueHive) -> None:
        response = client.employers.service_bundles.with_raw_response.update(
            id="id",
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_bundle = response.parse()
        assert_matches_type(ServiceBundleUpdateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: BlueHive) -> None:
        with client.employers.service_bundles.with_streaming_response.update(
            id="id",
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_bundle = response.parse()
            assert_matches_type(ServiceBundleUpdateResponse, service_bundle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            client.employers.service_bundles.with_raw_response.update(
                id="id",
                employer_id="",
                bundle_name="x",
                service_ids=["string"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.employers.service_bundles.with_raw_response.update(
                id="",
                employer_id="employerId",
                bundle_name="x",
                service_ids=["string"],
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: BlueHive) -> None:
        service_bundle = client.employers.service_bundles.list(
            "employerId",
        )
        assert_matches_type(ServiceBundleListResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: BlueHive) -> None:
        response = client.employers.service_bundles.with_raw_response.list(
            "employerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_bundle = response.parse()
        assert_matches_type(ServiceBundleListResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: BlueHive) -> None:
        with client.employers.service_bundles.with_streaming_response.list(
            "employerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_bundle = response.parse()
            assert_matches_type(ServiceBundleListResponse, service_bundle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_list(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            client.employers.service_bundles.with_raw_response.list(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: BlueHive) -> None:
        service_bundle = client.employers.service_bundles.delete(
            id="id",
            employer_id="employerId",
        )
        assert service_bundle is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: BlueHive) -> None:
        response = client.employers.service_bundles.with_raw_response.delete(
            id="id",
            employer_id="employerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_bundle = response.parse()
        assert service_bundle is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: BlueHive) -> None:
        with client.employers.service_bundles.with_streaming_response.delete(
            id="id",
            employer_id="employerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_bundle = response.parse()
            assert service_bundle is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            client.employers.service_bundles.with_raw_response.delete(
                id="id",
                employer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.employers.service_bundles.with_raw_response.delete(
                id="",
                employer_id="employerId",
            )


class TestAsyncServiceBundles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncBlueHive) -> None:
        service_bundle = await async_client.employers.service_bundles.create(
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        )
        assert_matches_type(ServiceBundleCreateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncBlueHive) -> None:
        service_bundle = await async_client.employers.service_bundles.create(
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
            _id="_id",
            limit=0,
            occurrence="occurrence",
            recurring=True,
            roles=["string"],
            start_date="startDate",
        )
        assert_matches_type(ServiceBundleCreateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employers.service_bundles.with_raw_response.create(
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_bundle = await response.parse()
        assert_matches_type(ServiceBundleCreateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employers.service_bundles.with_streaming_response.create(
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_bundle = await response.parse()
            assert_matches_type(ServiceBundleCreateResponse, service_bundle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_create(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            await async_client.employers.service_bundles.with_raw_response.create(
                employer_id="",
                bundle_name="x",
                service_ids=["string"],
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBlueHive) -> None:
        service_bundle = await async_client.employers.service_bundles.retrieve(
            id="id",
            employer_id="employerId",
        )
        assert_matches_type(ServiceBundleRetrieveResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employers.service_bundles.with_raw_response.retrieve(
            id="id",
            employer_id="employerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_bundle = await response.parse()
        assert_matches_type(ServiceBundleRetrieveResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employers.service_bundles.with_streaming_response.retrieve(
            id="id",
            employer_id="employerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_bundle = await response.parse()
            assert_matches_type(ServiceBundleRetrieveResponse, service_bundle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            await async_client.employers.service_bundles.with_raw_response.retrieve(
                id="id",
                employer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.employers.service_bundles.with_raw_response.retrieve(
                id="",
                employer_id="employerId",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncBlueHive) -> None:
        service_bundle = await async_client.employers.service_bundles.update(
            id="id",
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        )
        assert_matches_type(ServiceBundleUpdateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncBlueHive) -> None:
        service_bundle = await async_client.employers.service_bundles.update(
            id="id",
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
            _id="_id",
            limit=0,
            occurrence="occurrence",
            recurring=True,
            roles=["string"],
            start_date="startDate",
        )
        assert_matches_type(ServiceBundleUpdateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employers.service_bundles.with_raw_response.update(
            id="id",
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_bundle = await response.parse()
        assert_matches_type(ServiceBundleUpdateResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employers.service_bundles.with_streaming_response.update(
            id="id",
            employer_id="employerId",
            bundle_name="x",
            service_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_bundle = await response.parse()
            assert_matches_type(ServiceBundleUpdateResponse, service_bundle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            await async_client.employers.service_bundles.with_raw_response.update(
                id="id",
                employer_id="",
                bundle_name="x",
                service_ids=["string"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.employers.service_bundles.with_raw_response.update(
                id="",
                employer_id="employerId",
                bundle_name="x",
                service_ids=["string"],
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBlueHive) -> None:
        service_bundle = await async_client.employers.service_bundles.list(
            "employerId",
        )
        assert_matches_type(ServiceBundleListResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employers.service_bundles.with_raw_response.list(
            "employerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_bundle = await response.parse()
        assert_matches_type(ServiceBundleListResponse, service_bundle, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employers.service_bundles.with_streaming_response.list(
            "employerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_bundle = await response.parse()
            assert_matches_type(ServiceBundleListResponse, service_bundle, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            await async_client.employers.service_bundles.with_raw_response.list(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncBlueHive) -> None:
        service_bundle = await async_client.employers.service_bundles.delete(
            id="id",
            employer_id="employerId",
        )
        assert service_bundle is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employers.service_bundles.with_raw_response.delete(
            id="id",
            employer_id="employerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        service_bundle = await response.parse()
        assert service_bundle is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employers.service_bundles.with_streaming_response.delete(
            id="id",
            employer_id="employerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            service_bundle = await response.parse()
            assert service_bundle is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            await async_client.employers.service_bundles.with_raw_response.delete(
                id="id",
                employer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.employers.service_bundles.with_raw_response.delete(
                id="",
                employer_id="employerId",
            )
