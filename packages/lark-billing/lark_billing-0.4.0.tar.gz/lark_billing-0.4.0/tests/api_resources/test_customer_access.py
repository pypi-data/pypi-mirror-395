# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lark import Lark, AsyncLark
from lark.types import CustomerAccessRetrieveBillingStateResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCustomerAccess:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_billing_state(self, client: Lark) -> None:
        customer_access = client.customer_access.retrieve_billing_state(
            "user_1234567890",
        )
        assert_matches_type(CustomerAccessRetrieveBillingStateResponse, customer_access, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve_billing_state(self, client: Lark) -> None:
        response = client.customer_access.with_raw_response.retrieve_billing_state(
            "user_1234567890",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        customer_access = response.parse()
        assert_matches_type(CustomerAccessRetrieveBillingStateResponse, customer_access, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_billing_state(self, client: Lark) -> None:
        with client.customer_access.with_streaming_response.retrieve_billing_state(
            "user_1234567890",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            customer_access = response.parse()
            assert_matches_type(CustomerAccessRetrieveBillingStateResponse, customer_access, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve_billing_state(self, client: Lark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id` but received ''"):
            client.customer_access.with_raw_response.retrieve_billing_state(
                "",
            )


class TestAsyncCustomerAccess:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_billing_state(self, async_client: AsyncLark) -> None:
        customer_access = await async_client.customer_access.retrieve_billing_state(
            "user_1234567890",
        )
        assert_matches_type(CustomerAccessRetrieveBillingStateResponse, customer_access, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_billing_state(self, async_client: AsyncLark) -> None:
        response = await async_client.customer_access.with_raw_response.retrieve_billing_state(
            "user_1234567890",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        customer_access = await response.parse()
        assert_matches_type(CustomerAccessRetrieveBillingStateResponse, customer_access, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_billing_state(self, async_client: AsyncLark) -> None:
        async with async_client.customer_access.with_streaming_response.retrieve_billing_state(
            "user_1234567890",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            customer_access = await response.parse()
            assert_matches_type(CustomerAccessRetrieveBillingStateResponse, customer_access, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve_billing_state(self, async_client: AsyncLark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id` but received ''"):
            await async_client.customer_access.with_raw_response.retrieve_billing_state(
                "",
            )
