# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from bluehive import BlueHive, AsyncBlueHive
from tests.utils import assert_matches_type
from bluehive.types import (
    OrderCreateResponse,
    OrderUpdateResponse,
    OrderRetrieveResponse,
    OrderUpdateStatusResponse,
    OrderUploadResultsResponse,
    OrderRetrieveResultsResponse,
    OrderSendForEmployeeResponse,
    OrderScheduleAppointmentResponse,
)
from bluehive._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOrders:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_overload_1(self, client: BlueHive) -> None:
        order = client.orders.create(
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
            },
            provider_id="providerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: BlueHive) -> None:
        order = client.orders.create(
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            provider_id="providerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                    "auto_accept": True,
                }
            ],
            _id="_id",
            brand_id="brandId",
            due_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            due_dates=[parse_datetime("2019-12-27T18:11:19.117Z")],
            employee_id="employeeId",
            employee_ids=["string"],
            employer_id="employerId",
            metadata={"foo": "bar"},
            provider_created=True,
            providers_ids=[
                {
                    "provider_id": "x",
                    "service_id": "x",
                }
            ],
            quantities={"foo": 1},
            re_captcha_token="reCaptchaToken",
            services_ids=["string"],
            token_id="tokenId",
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_overload_1(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.create(
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
            },
            provider_id="providerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_1(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.create(
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
            },
            provider_id="providerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderCreateResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_overload_2(self, client: BlueHive) -> None:
        order = client.orders.create(
            employee_id="employeeId",
            employer_id="employerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: BlueHive) -> None:
        order = client.orders.create(
            employee_id="employeeId",
            employer_id="employerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                    "auto_accept": True,
                }
            ],
            _id="_id",
            brand_id="brandId",
            due_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            due_dates=[parse_datetime("2019-12-27T18:11:19.117Z")],
            employee_ids=["string"],
            metadata={"foo": "bar"},
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            provider_created=True,
            provider_id="providerId",
            providers_ids=[
                {
                    "provider_id": "x",
                    "service_id": "x",
                }
            ],
            quantities={"foo": 1},
            re_captcha_token="reCaptchaToken",
            services_ids=["string"],
            token_id="tokenId",
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_overload_2(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.create(
            employee_id="employeeId",
            employer_id="employerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_2(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.create(
            employee_id="employeeId",
            employer_id="employerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderCreateResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_overload_3(self, client: BlueHive) -> None:
        order = client.orders.create(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_3(self, client: BlueHive) -> None:
        order = client.orders.create(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[
                {
                    "provider_id": "x",
                    "service_id": "x",
                }
            ],
            services_ids=["string"],
            _id="_id",
            brand_id="brandId",
            due_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            due_dates=[parse_datetime("2019-12-27T18:11:19.117Z")],
            employee_ids=["string"],
            metadata={"foo": "bar"},
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            provider_created=True,
            provider_id="providerId",
            quantities={"foo": 1},
            re_captcha_token="reCaptchaToken",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                    "auto_accept": True,
                }
            ],
            token_id="tokenId",
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_overload_3(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.create(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_3(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.create(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderCreateResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_overload_4(self, client: BlueHive) -> None:
        order = client.orders.create(
            employee_ids=["string"],
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_4(self, client: BlueHive) -> None:
        order = client.orders.create(
            employee_ids=["string"],
            employer_id="employerId",
            providers_ids=[
                {
                    "provider_id": "x",
                    "service_id": "x",
                }
            ],
            services_ids=["string"],
            _id="_id",
            brand_id="brandId",
            due_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            due_dates=[parse_datetime("2019-12-27T18:11:19.117Z")],
            employee_id="employeeId",
            metadata={"foo": "bar"},
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            provider_created=True,
            provider_id="providerId",
            quantities={"foo": 1},
            re_captcha_token="reCaptchaToken",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                    "auto_accept": True,
                }
            ],
            token_id="tokenId",
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_overload_4(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.create(
            employee_ids=["string"],
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_4(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.create(
            employee_ids=["string"],
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderCreateResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: BlueHive) -> None:
        order = client.orders.retrieve(
            "orderId",
        )
        assert_matches_type(OrderRetrieveResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.retrieve(
            "orderId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderRetrieveResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.retrieve(
            "orderId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderRetrieveResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            client.orders.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update(self, client: BlueHive) -> None:
        order = client.orders.update(
            order_id="orderId",
        )
        assert_matches_type(OrderUpdateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: BlueHive) -> None:
        order = client.orders.update(
            order_id="orderId",
            metadata={"foo": "bar"},
            services=[
                {
                    "service_id": "x",
                    "due_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "results": {"foo": "bar"},
                    "status": "pending",
                }
            ],
            status="order_sent",
        )
        assert_matches_type(OrderUpdateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.update(
            order_id="orderId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderUpdateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.update(
            order_id="orderId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderUpdateResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            client.orders.with_raw_response.update(
                order_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_results(self, client: BlueHive) -> None:
        order = client.orders.retrieve_results(
            order_id="orderId",
        )
        assert_matches_type(OrderRetrieveResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_results_with_all_params(self, client: BlueHive) -> None:
        order = client.orders.retrieve_results(
            order_id="orderId",
            page=1,
            page_size=1,
            service_id="serviceId",
            since=parse_datetime("2019-12-27T18:11:19.117Z"),
            status="status",
            until=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(OrderRetrieveResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve_results(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.retrieve_results(
            order_id="orderId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderRetrieveResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_results(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.retrieve_results(
            order_id="orderId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderRetrieveResultsResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve_results(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            client.orders.with_raw_response.retrieve_results(
                order_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_schedule_appointment(self, client: BlueHive) -> None:
        order = client.orders.schedule_appointment(
            order_id="orderId",
            appointment={
                "date": "date",
                "date_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "time": "time",
            },
        )
        assert_matches_type(OrderScheduleAppointmentResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_schedule_appointment_with_all_params(self, client: BlueHive) -> None:
        order = client.orders.schedule_appointment(
            order_id="orderId",
            appointment={
                "date": "date",
                "date_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "time": "time",
                "notes": "notes",
                "type": "appointment",
            },
            order_access_code="orderAccessCode",
            provider_id="providerId",
        )
        assert_matches_type(OrderScheduleAppointmentResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_schedule_appointment(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.schedule_appointment(
            order_id="orderId",
            appointment={
                "date": "date",
                "date_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "time": "time",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderScheduleAppointmentResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_schedule_appointment(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.schedule_appointment(
            order_id="orderId",
            appointment={
                "date": "date",
                "date_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "time": "time",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderScheduleAppointmentResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_schedule_appointment(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            client.orders.with_raw_response.schedule_appointment(
                order_id="",
                appointment={
                    "date": "date",
                    "date_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "time": "time",
                },
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_send_for_employee(self, client: BlueHive) -> None:
        order = client.orders.send_for_employee(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "providerId"}],
            services_ids=["string"],
            login_token="login-token",
            user_id="user-id",
        )
        assert_matches_type(OrderSendForEmployeeResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_send_for_employee_with_all_params(self, client: BlueHive) -> None:
        order = client.orders.send_for_employee(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[
                {
                    "provider_id": "providerId",
                    "service_id": "serviceId",
                }
            ],
            services_ids=["string"],
            login_token="login-token",
            user_id="user-id",
            brand_id="brandId",
            due_date="dueDate",
            due_dates=["string"],
            metadata={"foo": "bar"},
            provider_created=True,
            provider_id="providerId",
            quantities={"foo": 1},
        )
        assert_matches_type(OrderSendForEmployeeResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_send_for_employee(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.send_for_employee(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "providerId"}],
            services_ids=["string"],
            login_token="login-token",
            user_id="user-id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderSendForEmployeeResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_send_for_employee(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.send_for_employee(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "providerId"}],
            services_ids=["string"],
            login_token="login-token",
            user_id="user-id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderSendForEmployeeResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_status(self, client: BlueHive) -> None:
        order = client.orders.update_status(
            order_id="orderId",
            status="order_sent",
        )
        assert_matches_type(OrderUpdateStatusResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_status_with_all_params(self, client: BlueHive) -> None:
        order = client.orders.update_status(
            order_id="orderId",
            status="order_sent",
            message="message",
        )
        assert_matches_type(OrderUpdateStatusResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update_status(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.update_status(
            order_id="orderId",
            status="order_sent",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderUpdateStatusResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update_status(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.update_status(
            order_id="orderId",
            status="order_sent",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderUpdateStatusResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update_status(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            client.orders.with_raw_response.update_status(
                order_id="",
                status="order_sent",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_upload_results(self, client: BlueHive) -> None:
        order = client.orders.upload_results(
            order_id="orderId",
            captcha_token="x",
            order_access_code="x",
            service_id="x",
        )
        assert_matches_type(OrderUploadResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_upload_results_with_all_params(self, client: BlueHive) -> None:
        order = client.orders.upload_results(
            order_id="orderId",
            captcha_token="x",
            order_access_code="x",
            service_id="x",
            dob="7321-69-10",
            file_ids=["x"],
            files=[
                {
                    "base64": "x",
                    "name": "x",
                    "type": "x",
                }
            ],
            last_name="x",
        )
        assert_matches_type(OrderUploadResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_upload_results(self, client: BlueHive) -> None:
        response = client.orders.with_raw_response.upload_results(
            order_id="orderId",
            captcha_token="x",
            order_access_code="x",
            service_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderUploadResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_upload_results(self, client: BlueHive) -> None:
        with client.orders.with_streaming_response.upload_results(
            order_id="orderId",
            captcha_token="x",
            order_access_code="x",
            service_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderUploadResultsResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_upload_results(self, client: BlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            client.orders.with_raw_response.upload_results(
                order_id="",
                captcha_token="x",
                order_access_code="x",
                service_id="x",
            )


class TestAsyncOrders:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.create(
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
            },
            provider_id="providerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.create(
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            provider_id="providerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                    "auto_accept": True,
                }
            ],
            _id="_id",
            brand_id="brandId",
            due_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            due_dates=[parse_datetime("2019-12-27T18:11:19.117Z")],
            employee_id="employeeId",
            employee_ids=["string"],
            employer_id="employerId",
            metadata={"foo": "bar"},
            provider_created=True,
            providers_ids=[
                {
                    "provider_id": "x",
                    "service_id": "x",
                }
            ],
            quantities={"foo": 1},
            re_captcha_token="reCaptchaToken",
            services_ids=["string"],
            token_id="tokenId",
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.create(
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
            },
            provider_id="providerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.create(
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
            },
            provider_id="providerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderCreateResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.create(
            employee_id="employeeId",
            employer_id="employerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.create(
            employee_id="employeeId",
            employer_id="employerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                    "auto_accept": True,
                }
            ],
            _id="_id",
            brand_id="brandId",
            due_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            due_dates=[parse_datetime("2019-12-27T18:11:19.117Z")],
            employee_ids=["string"],
            metadata={"foo": "bar"},
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            provider_created=True,
            provider_id="providerId",
            providers_ids=[
                {
                    "provider_id": "x",
                    "service_id": "x",
                }
            ],
            quantities={"foo": 1},
            re_captcha_token="reCaptchaToken",
            services_ids=["string"],
            token_id="tokenId",
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.create(
            employee_id="employeeId",
            employer_id="employerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.create(
            employee_id="employeeId",
            employer_id="employerId",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderCreateResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_overload_3(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.create(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_3(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.create(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[
                {
                    "provider_id": "x",
                    "service_id": "x",
                }
            ],
            services_ids=["string"],
            _id="_id",
            brand_id="brandId",
            due_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            due_dates=[parse_datetime("2019-12-27T18:11:19.117Z")],
            employee_ids=["string"],
            metadata={"foo": "bar"},
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            provider_created=True,
            provider_id="providerId",
            quantities={"foo": 1},
            re_captcha_token="reCaptchaToken",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                    "auto_accept": True,
                }
            ],
            token_id="tokenId",
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_3(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.create(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_3(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.create(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderCreateResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_overload_4(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.create(
            employee_ids=["string"],
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_4(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.create(
            employee_ids=["string"],
            employer_id="employerId",
            providers_ids=[
                {
                    "provider_id": "x",
                    "service_id": "x",
                }
            ],
            services_ids=["string"],
            _id="_id",
            brand_id="brandId",
            due_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            due_dates=[parse_datetime("2019-12-27T18:11:19.117Z")],
            employee_id="employeeId",
            metadata={"foo": "bar"},
            payment_method="self-pay",
            person={
                "city": "x",
                "dob": "7321-69-10",
                "email": "email",
                "first_name": "x",
                "last_name": "x",
                "phone": "+)() 92))()1)",
                "state": "xx",
                "street": "x",
                "zipcode": "73216-0225",
                "country": "country",
                "county": "county",
                "street2": "street2",
            },
            provider_created=True,
            provider_id="providerId",
            quantities={"foo": 1},
            re_captcha_token="reCaptchaToken",
            services=[
                {
                    "_id": "x",
                    "quantity": 1,
                    "auto_accept": True,
                }
            ],
            token_id="tokenId",
        )
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_4(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.create(
            employee_ids=["string"],
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderCreateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_4(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.create(
            employee_ids=["string"],
            employer_id="employerId",
            providers_ids=[{"provider_id": "x"}],
            services_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderCreateResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.retrieve(
            "orderId",
        )
        assert_matches_type(OrderRetrieveResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.retrieve(
            "orderId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderRetrieveResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.retrieve(
            "orderId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderRetrieveResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            await async_client.orders.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.update(
            order_id="orderId",
        )
        assert_matches_type(OrderUpdateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.update(
            order_id="orderId",
            metadata={"foo": "bar"},
            services=[
                {
                    "service_id": "x",
                    "due_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "results": {"foo": "bar"},
                    "status": "pending",
                }
            ],
            status="order_sent",
        )
        assert_matches_type(OrderUpdateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.update(
            order_id="orderId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderUpdateResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.update(
            order_id="orderId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderUpdateResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            await async_client.orders.with_raw_response.update(
                order_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_results(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.retrieve_results(
            order_id="orderId",
        )
        assert_matches_type(OrderRetrieveResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_results_with_all_params(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.retrieve_results(
            order_id="orderId",
            page=1,
            page_size=1,
            service_id="serviceId",
            since=parse_datetime("2019-12-27T18:11:19.117Z"),
            status="status",
            until=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(OrderRetrieveResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_results(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.retrieve_results(
            order_id="orderId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderRetrieveResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_results(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.retrieve_results(
            order_id="orderId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderRetrieveResultsResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve_results(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            await async_client.orders.with_raw_response.retrieve_results(
                order_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_schedule_appointment(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.schedule_appointment(
            order_id="orderId",
            appointment={
                "date": "date",
                "date_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "time": "time",
            },
        )
        assert_matches_type(OrderScheduleAppointmentResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_schedule_appointment_with_all_params(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.schedule_appointment(
            order_id="orderId",
            appointment={
                "date": "date",
                "date_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "time": "time",
                "notes": "notes",
                "type": "appointment",
            },
            order_access_code="orderAccessCode",
            provider_id="providerId",
        )
        assert_matches_type(OrderScheduleAppointmentResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_schedule_appointment(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.schedule_appointment(
            order_id="orderId",
            appointment={
                "date": "date",
                "date_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "time": "time",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderScheduleAppointmentResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_schedule_appointment(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.schedule_appointment(
            order_id="orderId",
            appointment={
                "date": "date",
                "date_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "time": "time",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderScheduleAppointmentResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_schedule_appointment(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            await async_client.orders.with_raw_response.schedule_appointment(
                order_id="",
                appointment={
                    "date": "date",
                    "date_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "time": "time",
                },
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_send_for_employee(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.send_for_employee(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "providerId"}],
            services_ids=["string"],
            login_token="login-token",
            user_id="user-id",
        )
        assert_matches_type(OrderSendForEmployeeResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_send_for_employee_with_all_params(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.send_for_employee(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[
                {
                    "provider_id": "providerId",
                    "service_id": "serviceId",
                }
            ],
            services_ids=["string"],
            login_token="login-token",
            user_id="user-id",
            brand_id="brandId",
            due_date="dueDate",
            due_dates=["string"],
            metadata={"foo": "bar"},
            provider_created=True,
            provider_id="providerId",
            quantities={"foo": 1},
        )
        assert_matches_type(OrderSendForEmployeeResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_send_for_employee(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.send_for_employee(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "providerId"}],
            services_ids=["string"],
            login_token="login-token",
            user_id="user-id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderSendForEmployeeResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_send_for_employee(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.send_for_employee(
            employee_id="employeeId",
            employer_id="employerId",
            providers_ids=[{"provider_id": "providerId"}],
            services_ids=["string"],
            login_token="login-token",
            user_id="user-id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderSendForEmployeeResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_status(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.update_status(
            order_id="orderId",
            status="order_sent",
        )
        assert_matches_type(OrderUpdateStatusResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_status_with_all_params(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.update_status(
            order_id="orderId",
            status="order_sent",
            message="message",
        )
        assert_matches_type(OrderUpdateStatusResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update_status(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.update_status(
            order_id="orderId",
            status="order_sent",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderUpdateStatusResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update_status(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.update_status(
            order_id="orderId",
            status="order_sent",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderUpdateStatusResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update_status(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            await async_client.orders.with_raw_response.update_status(
                order_id="",
                status="order_sent",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_upload_results(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.upload_results(
            order_id="orderId",
            captcha_token="x",
            order_access_code="x",
            service_id="x",
        )
        assert_matches_type(OrderUploadResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_upload_results_with_all_params(self, async_client: AsyncBlueHive) -> None:
        order = await async_client.orders.upload_results(
            order_id="orderId",
            captcha_token="x",
            order_access_code="x",
            service_id="x",
            dob="7321-69-10",
            file_ids=["x"],
            files=[
                {
                    "base64": "x",
                    "name": "x",
                    "type": "x",
                }
            ],
            last_name="x",
        )
        assert_matches_type(OrderUploadResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_upload_results(self, async_client: AsyncBlueHive) -> None:
        response = await async_client.orders.with_raw_response.upload_results(
            order_id="orderId",
            captcha_token="x",
            order_access_code="x",
            service_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderUploadResultsResponse, order, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_upload_results(self, async_client: AsyncBlueHive) -> None:
        async with async_client.orders.with_streaming_response.upload_results(
            order_id="orderId",
            captcha_token="x",
            order_access_code="x",
            service_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderUploadResultsResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_upload_results(self, async_client: AsyncBlueHive) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            await async_client.orders.with_raw_response.upload_results(
                order_id="",
                captcha_token="x",
                order_access_code="x",
                service_id="x",
            )
