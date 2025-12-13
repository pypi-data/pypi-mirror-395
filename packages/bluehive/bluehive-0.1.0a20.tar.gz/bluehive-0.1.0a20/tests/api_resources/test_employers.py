# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from bluehive import BlueHive, AsyncBlueHive
from tests.utils import assert_matches_type
from bluehive.types import (
    EmployerListResponse,
    EmployerCreateResponse,
    EmployerRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEmployers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: BlueHive) -> None:
        employer = client.employers.create(
            address={
                "city": "city",
                "state": "state",
                "street1": "street1",
                "zip_code": "zipCode",
            },
            email="dev@stainless.com",
            name="name",
            phones=[{"number": "number"}],
        )
        assert_matches_type(EmployerCreateResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: BlueHive) -> None:
        employer = client.employers.create(
            address={
                "city": "city",
                "state": "state",
                "street1": "street1",
                "zip_code": "zipCode",
                "country": "country",
                "street2": "street2",
            },
            email="dev@stainless.com",
            name="name",
            phones=[
                {
                    "number": "number",
                    "primary": True,
                    "type": "type",
                }
            ],
            billing_address={"foo": "bar"},
            checkr={
                "id": "id",
                "status": "status",
            },
            demo=True,
            employee_consent=True,
            metadata={"foo": "bar"},
            onsite_clinic=True,
            website="website",
        )
        assert_matches_type(EmployerCreateResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: BlueHive) -> None:
        response = client.employers.with_raw_response.create(
            address={
                "city": "city",
                "state": "state",
                "street1": "street1",
                "zip_code": "zipCode",
            },
            email="dev@stainless.com",
            name="name",
            phones=[{"number": "number"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employer = response.parse()
        assert_matches_type(EmployerCreateResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: BlueHive) -> None:
        with client.employers.with_streaming_response.create(
            address={
                "city": "city",
                "state": "state",
                "street1": "street1",
                "zip_code": "zipCode",
            },
            email="dev@stainless.com",
            name="name",
            phones=[{"number": "number"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employer = response.parse()
            assert_matches_type(EmployerCreateResponse, employer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: BlueHive) -> None:
        employer = client.employers.retrieve(
            "employerId",
        )
        assert_matches_type(EmployerRetrieveResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: BlueHive) -> None:
        response = client.employers.with_raw_response.retrieve(
            "employerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employer = response.parse()
        assert_matches_type(EmployerRetrieveResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: BlueHive) -> None:
        with client.employers.with_streaming_response.retrieve(
            "employerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employer = response.parse()
            assert_matches_type(EmployerRetrieveResponse, employer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            client.employers.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: BlueHive) -> None:
        employer = client.employers.list(
            login_token="login-token",
            user_id="user-id",
        )
        assert_matches_type(EmployerListResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: BlueHive) -> None:
        response = client.employers.with_raw_response.list(
            login_token="login-token",
            user_id="user-id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employer = response.parse()
        assert_matches_type(EmployerListResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: BlueHive) -> None:
        with client.employers.with_streaming_response.list(
            login_token="login-token",
            user_id="user-id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employer = response.parse()
            assert_matches_type(EmployerListResponse, employer, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEmployers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncBlueHive) -> None:
        employer = await async_client.employers.create(
            address={
                "city": "city",
                "state": "state",
                "street1": "street1",
                "zip_code": "zipCode",
            },
            email="dev@stainless.com",
            name="name",
            phones=[{"number": "number"}],
        )
        assert_matches_type(EmployerCreateResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncBlueHive) -> None:
        employer = await async_client.employers.create(
            address={
                "city": "city",
                "state": "state",
                "street1": "street1",
                "zip_code": "zipCode",
                "country": "country",
                "street2": "street2",
            },
            email="dev@stainless.com",
            name="name",
            phones=[
                {
                    "number": "number",
                    "primary": True,
                    "type": "type",
                }
            ],
            billing_address={"foo": "bar"},
            checkr={
                "id": "id",
                "status": "status",
            },
            demo=True,
            employee_consent=True,
            metadata={"foo": "bar"},
            onsite_clinic=True,
            website="website",
        )
        assert_matches_type(EmployerCreateResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employers.with_raw_response.create(
            address={
                "city": "city",
                "state": "state",
                "street1": "street1",
                "zip_code": "zipCode",
            },
            email="dev@stainless.com",
            name="name",
            phones=[{"number": "number"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employer = await response.parse()
        assert_matches_type(EmployerCreateResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employers.with_streaming_response.create(
            address={
                "city": "city",
                "state": "state",
                "street1": "street1",
                "zip_code": "zipCode",
            },
            email="dev@stainless.com",
            name="name",
            phones=[{"number": "number"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employer = await response.parse()
            assert_matches_type(EmployerCreateResponse, employer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBlueHive) -> None:
        employer = await async_client.employers.retrieve(
            "employerId",
        )
        assert_matches_type(EmployerRetrieveResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employers.with_raw_response.retrieve(
            "employerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employer = await response.parse()
        assert_matches_type(EmployerRetrieveResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employers.with_streaming_response.retrieve(
            "employerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employer = await response.parse()
            assert_matches_type(EmployerRetrieveResponse, employer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employer_id` but received ''"):
            await async_client.employers.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBlueHive) -> None:
        employer = await async_client.employers.list(
            login_token="login-token",
            user_id="user-id",
        )
        assert_matches_type(EmployerListResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employers.with_raw_response.list(
            login_token="login-token",
            user_id="user-id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employer = await response.parse()
        assert_matches_type(EmployerListResponse, employer, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employers.with_streaming_response.list(
            login_token="login-token",
            user_id="user-id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employer = await response.parse()
            assert_matches_type(EmployerListResponse, employer, path=["response"])

        assert cast(Any, response.is_closed) is True
