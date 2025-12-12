# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lark import Lark, AsyncLark
from lark.types import CustomerPortalCreateSessionResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCustomerPortal:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_session(self, client: Lark) -> None:
        customer_portal = client.customer_portal.create_session(
            return_url="https://example.com/dashboard",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )
        assert_matches_type(CustomerPortalCreateSessionResponse, customer_portal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_session(self, client: Lark) -> None:
        response = client.customer_portal.with_raw_response.create_session(
            return_url="https://example.com/dashboard",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        customer_portal = response.parse()
        assert_matches_type(CustomerPortalCreateSessionResponse, customer_portal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_session(self, client: Lark) -> None:
        with client.customer_portal.with_streaming_response.create_session(
            return_url="https://example.com/dashboard",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            customer_portal = response.parse()
            assert_matches_type(CustomerPortalCreateSessionResponse, customer_portal, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCustomerPortal:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_session(self, async_client: AsyncLark) -> None:
        customer_portal = await async_client.customer_portal.create_session(
            return_url="https://example.com/dashboard",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )
        assert_matches_type(CustomerPortalCreateSessionResponse, customer_portal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_session(self, async_client: AsyncLark) -> None:
        response = await async_client.customer_portal.with_raw_response.create_session(
            return_url="https://example.com/dashboard",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        customer_portal = await response.parse()
        assert_matches_type(CustomerPortalCreateSessionResponse, customer_portal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_session(self, async_client: AsyncLark) -> None:
        async with async_client.customer_portal.with_streaming_response.create_session(
            return_url="https://example.com/dashboard",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            customer_portal = await response.parse()
            assert_matches_type(CustomerPortalCreateSessionResponse, customer_portal, path=["response"])

        assert cast(Any, response.is_closed) is True
