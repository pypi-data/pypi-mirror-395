# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from bluehive import BlueHive, AsyncBlueHive
from tests.utils import assert_matches_type
from bluehive.types import (
    EmployeeListResponse,
    EmployeeCreateResponse,
    EmployeeDeleteResponse,
    EmployeeUpdateResponse,
    EmployeeLinkUserResponse,
    EmployeeRetrieveResponse,
    EmployeeUnlinkUserResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEmployees:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: BlueHive) -> None:
        employee = client.employees.create(
            email="dev@stainless.com",
            first_name="x",
            last_name="x",
        )
        assert_matches_type(EmployeeCreateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: BlueHive) -> None:
        employee = client.employees.create(
            email="dev@stainless.com",
            first_name="x",
            last_name="x",
            active_account="Active",
            address={
                "city": "x",
                "postal_code": "x",
                "state": "x",
                "street1": "x",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            blurb="blurb",
            departments=["string"],
            dob="7321-69-10",
            employer_id="employer_id",
            extended_fields=[
                {
                    "name": "x",
                    "value": "x",
                }
            ],
            phone=[
                {
                    "number": "x",
                    "type": "Cell",
                }
            ],
            title="title",
        )
        assert_matches_type(EmployeeCreateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: BlueHive) -> None:
        response = client.employees.with_raw_response.create(
            email="dev@stainless.com",
            first_name="x",
            last_name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = response.parse()
        assert_matches_type(EmployeeCreateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: BlueHive) -> None:
        with client.employees.with_streaming_response.create(
            email="dev@stainless.com",
            first_name="x",
            last_name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = response.parse()
            assert_matches_type(EmployeeCreateResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: BlueHive) -> None:
        employee = client.employees.retrieve(
            "employeeId",
        )
        assert_matches_type(EmployeeRetrieveResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: BlueHive) -> None:
        response = client.employees.with_raw_response.retrieve(
            "employeeId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = response.parse()
        assert_matches_type(EmployeeRetrieveResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: BlueHive) -> None:
        with client.employees.with_streaming_response.retrieve(
            "employeeId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = response.parse()
            assert_matches_type(EmployeeRetrieveResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employee_id` but received ''"):
            client.employees.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update(self, client: BlueHive) -> None:
        employee = client.employees.update(
            _id="x",
        )
        assert_matches_type(EmployeeUpdateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: BlueHive) -> None:
        employee = client.employees.update(
            _id="x",
            active_account="Active",
            address={
                "city": "x",
                "postal_code": "x",
                "state": "x",
                "street1": "x",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            blurb="blurb",
            departments=["string"],
            dob="7321-69-10",
            email="dev@stainless.com",
            employer_id="employer_id",
            extended_fields=[
                {
                    "name": "x",
                    "value": "x",
                }
            ],
            first_name="x",
            last_name="x",
            phone=[
                {
                    "number": "x",
                    "type": "Cell",
                }
            ],
            title="title",
        )
        assert_matches_type(EmployeeUpdateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: BlueHive) -> None:
        response = client.employees.with_raw_response.update(
            _id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = response.parse()
        assert_matches_type(EmployeeUpdateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: BlueHive) -> None:
        with client.employees.with_streaming_response.update(
            _id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = response.parse()
            assert_matches_type(EmployeeUpdateResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: BlueHive) -> None:
        employee = client.employees.list(
            employer_id="employerId",
        )
        assert_matches_type(EmployeeListResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: BlueHive) -> None:
        employee = client.employees.list(
            employer_id="employerId",
            limit="269125115713",
            offset="269125115713",
        )
        assert_matches_type(EmployeeListResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: BlueHive) -> None:
        response = client.employees.with_raw_response.list(
            employer_id="employerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = response.parse()
        assert_matches_type(EmployeeListResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: BlueHive) -> None:
        with client.employees.with_streaming_response.list(
            employer_id="employerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = response.parse()
            assert_matches_type(EmployeeListResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: BlueHive) -> None:
        employee = client.employees.delete(
            "employeeId",
        )
        assert_matches_type(EmployeeDeleteResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: BlueHive) -> None:
        response = client.employees.with_raw_response.delete(
            "employeeId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = response.parse()
        assert_matches_type(EmployeeDeleteResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: BlueHive) -> None:
        with client.employees.with_streaming_response.delete(
            "employeeId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = response.parse()
            assert_matches_type(EmployeeDeleteResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employee_id` but received ''"):
            client.employees.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_link_user(self, client: BlueHive) -> None:
        employee = client.employees.link_user(
            employee_id="x",
            user_id="x",
        )
        assert_matches_type(EmployeeLinkUserResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_link_user_with_all_params(self, client: BlueHive) -> None:
        employee = client.employees.link_user(
            employee_id="x",
            user_id="x",
            role=["string"],
        )
        assert_matches_type(EmployeeLinkUserResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_link_user(self, client: BlueHive) -> None:
        response = client.employees.with_raw_response.link_user(
            employee_id="x",
            user_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = response.parse()
        assert_matches_type(EmployeeLinkUserResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_link_user(self, client: BlueHive) -> None:
        with client.employees.with_streaming_response.link_user(
            employee_id="x",
            user_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = response.parse()
            assert_matches_type(EmployeeLinkUserResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_unlink_user(self, client: BlueHive) -> None:
        employee = client.employees.unlink_user(
            employee_id="employeeId",
            user_id="userId",
        )
        assert_matches_type(EmployeeUnlinkUserResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_unlink_user(self, client: BlueHive) -> None:
        response = client.employees.with_raw_response.unlink_user(
            employee_id="employeeId",
            user_id="userId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = response.parse()
        assert_matches_type(EmployeeUnlinkUserResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_unlink_user(self, client: BlueHive) -> None:
        with client.employees.with_streaming_response.unlink_user(
            employee_id="employeeId",
            user_id="userId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = response.parse()
            assert_matches_type(EmployeeUnlinkUserResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEmployees:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.create(
            email="dev@stainless.com",
            first_name="x",
            last_name="x",
        )
        assert_matches_type(EmployeeCreateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.create(
            email="dev@stainless.com",
            first_name="x",
            last_name="x",
            active_account="Active",
            address={
                "city": "x",
                "postal_code": "x",
                "state": "x",
                "street1": "x",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            blurb="blurb",
            departments=["string"],
            dob="7321-69-10",
            employer_id="employer_id",
            extended_fields=[
                {
                    "name": "x",
                    "value": "x",
                }
            ],
            phone=[
                {
                    "number": "x",
                    "type": "Cell",
                }
            ],
            title="title",
        )
        assert_matches_type(EmployeeCreateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employees.with_raw_response.create(
            email="dev@stainless.com",
            first_name="x",
            last_name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = await response.parse()
        assert_matches_type(EmployeeCreateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employees.with_streaming_response.create(
            email="dev@stainless.com",
            first_name="x",
            last_name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = await response.parse()
            assert_matches_type(EmployeeCreateResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.retrieve(
            "employeeId",
        )
        assert_matches_type(EmployeeRetrieveResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employees.with_raw_response.retrieve(
            "employeeId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = await response.parse()
        assert_matches_type(EmployeeRetrieveResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employees.with_streaming_response.retrieve(
            "employeeId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = await response.parse()
            assert_matches_type(EmployeeRetrieveResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employee_id` but received ''"):
            await async_client.employees.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.update(
            _id="x",
        )
        assert_matches_type(EmployeeUpdateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.update(
            _id="x",
            active_account="Active",
            address={
                "city": "x",
                "postal_code": "x",
                "state": "x",
                "street1": "x",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            blurb="blurb",
            departments=["string"],
            dob="7321-69-10",
            email="dev@stainless.com",
            employer_id="employer_id",
            extended_fields=[
                {
                    "name": "x",
                    "value": "x",
                }
            ],
            first_name="x",
            last_name="x",
            phone=[
                {
                    "number": "x",
                    "type": "Cell",
                }
            ],
            title="title",
        )
        assert_matches_type(EmployeeUpdateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employees.with_raw_response.update(
            _id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = await response.parse()
        assert_matches_type(EmployeeUpdateResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employees.with_streaming_response.update(
            _id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = await response.parse()
            assert_matches_type(EmployeeUpdateResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.list(
            employer_id="employerId",
        )
        assert_matches_type(EmployeeListResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.list(
            employer_id="employerId",
            limit="269125115713",
            offset="269125115713",
        )
        assert_matches_type(EmployeeListResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employees.with_raw_response.list(
            employer_id="employerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = await response.parse()
        assert_matches_type(EmployeeListResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employees.with_streaming_response.list(
            employer_id="employerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = await response.parse()
            assert_matches_type(EmployeeListResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.delete(
            "employeeId",
        )
        assert_matches_type(EmployeeDeleteResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employees.with_raw_response.delete(
            "employeeId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = await response.parse()
        assert_matches_type(EmployeeDeleteResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employees.with_streaming_response.delete(
            "employeeId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = await response.parse()
            assert_matches_type(EmployeeDeleteResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `employee_id` but received ''"):
            await async_client.employees.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_link_user(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.link_user(
            employee_id="x",
            user_id="x",
        )
        assert_matches_type(EmployeeLinkUserResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_link_user_with_all_params(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.link_user(
            employee_id="x",
            user_id="x",
            role=["string"],
        )
        assert_matches_type(EmployeeLinkUserResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_link_user(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employees.with_raw_response.link_user(
            employee_id="x",
            user_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = await response.parse()
        assert_matches_type(EmployeeLinkUserResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_link_user(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employees.with_streaming_response.link_user(
            employee_id="x",
            user_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = await response.parse()
            assert_matches_type(EmployeeLinkUserResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_unlink_user(self, async_client: AsyncBlueHive) -> None:
        employee = await async_client.employees.unlink_user(
            employee_id="employeeId",
            user_id="userId",
        )
        assert_matches_type(EmployeeUnlinkUserResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_unlink_user(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.employees.with_raw_response.unlink_user(
            employee_id="employeeId",
            user_id="userId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        employee = await response.parse()
        assert_matches_type(EmployeeUnlinkUserResponse, employee, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_unlink_user(self, async_client: AsyncBlueHive) -> None:
        async with async_client.employees.with_streaming_response.unlink_user(
            employee_id="employeeId",
            user_id="userId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            employee = await response.parse()
            assert_matches_type(EmployeeUnlinkUserResponse, employee, path=["response"])

        assert cast(Any, response.is_closed) is True
