# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lark import Lark, AsyncLark
from lark.types import RateCardResource, RateCardListResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRateCards:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Lark) -> None:
        rate_card = client.rate_cards.create(
            billing_interval="monthly",
            name="Pro Plan",
        )
        assert_matches_type(RateCardResource, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Lark) -> None:
        rate_card = client.rate_cards.create(
            billing_interval="monthly",
            name="Pro Plan",
            description="For production applicatidddons with moderate usage.",
            fixed_rates=[
                {
                    "name": "Base Rate",
                    "price": {
                        "amount": {
                            "currency_code": "usd",
                            "value": 2500,
                        },
                        "price_type": "flat",
                    },
                    "description": None,
                }
            ],
            metadata={},
            usage_based_rates=[
                {
                    "name": "Compute Hours",
                    "price": {
                        "amount": {
                            "currency_code": "usd",
                            "value": 100,
                        },
                        "price_type": "flat",
                    },
                    "pricing_metric_id": "pmtr_GlX5Tcm2HOn00CoRTFxw2Amw",
                    "usage_based_rate_type": "simple",
                    "description": "description",
                    "included_units": 30,
                }
            ],
        )
        assert_matches_type(RateCardResource, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Lark) -> None:
        response = client.rate_cards.with_raw_response.create(
            billing_interval="monthly",
            name="Pro Plan",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rate_card = response.parse()
        assert_matches_type(RateCardResource, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Lark) -> None:
        with client.rate_cards.with_streaming_response.create(
            billing_interval="monthly",
            name="Pro Plan",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rate_card = response.parse()
            assert_matches_type(RateCardResource, rate_card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Lark) -> None:
        rate_card = client.rate_cards.retrieve(
            "rate_card_id",
        )
        assert_matches_type(RateCardResource, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Lark) -> None:
        response = client.rate_cards.with_raw_response.retrieve(
            "rate_card_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rate_card = response.parse()
        assert_matches_type(RateCardResource, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Lark) -> None:
        with client.rate_cards.with_streaming_response.retrieve(
            "rate_card_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rate_card = response.parse()
            assert_matches_type(RateCardResource, rate_card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Lark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rate_card_id` but received ''"):
            client.rate_cards.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Lark) -> None:
        rate_card = client.rate_cards.list()
        assert_matches_type(RateCardListResponse, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Lark) -> None:
        rate_card = client.rate_cards.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(RateCardListResponse, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Lark) -> None:
        response = client.rate_cards.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rate_card = response.parse()
        assert_matches_type(RateCardListResponse, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Lark) -> None:
        with client.rate_cards.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rate_card = response.parse()
            assert_matches_type(RateCardListResponse, rate_card, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRateCards:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncLark) -> None:
        rate_card = await async_client.rate_cards.create(
            billing_interval="monthly",
            name="Pro Plan",
        )
        assert_matches_type(RateCardResource, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLark) -> None:
        rate_card = await async_client.rate_cards.create(
            billing_interval="monthly",
            name="Pro Plan",
            description="For production applicatidddons with moderate usage.",
            fixed_rates=[
                {
                    "name": "Base Rate",
                    "price": {
                        "amount": {
                            "currency_code": "usd",
                            "value": 2500,
                        },
                        "price_type": "flat",
                    },
                    "description": None,
                }
            ],
            metadata={},
            usage_based_rates=[
                {
                    "name": "Compute Hours",
                    "price": {
                        "amount": {
                            "currency_code": "usd",
                            "value": 100,
                        },
                        "price_type": "flat",
                    },
                    "pricing_metric_id": "pmtr_GlX5Tcm2HOn00CoRTFxw2Amw",
                    "usage_based_rate_type": "simple",
                    "description": "description",
                    "included_units": 30,
                }
            ],
        )
        assert_matches_type(RateCardResource, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLark) -> None:
        response = await async_client.rate_cards.with_raw_response.create(
            billing_interval="monthly",
            name="Pro Plan",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rate_card = await response.parse()
        assert_matches_type(RateCardResource, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLark) -> None:
        async with async_client.rate_cards.with_streaming_response.create(
            billing_interval="monthly",
            name="Pro Plan",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rate_card = await response.parse()
            assert_matches_type(RateCardResource, rate_card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLark) -> None:
        rate_card = await async_client.rate_cards.retrieve(
            "rate_card_id",
        )
        assert_matches_type(RateCardResource, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLark) -> None:
        response = await async_client.rate_cards.with_raw_response.retrieve(
            "rate_card_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rate_card = await response.parse()
        assert_matches_type(RateCardResource, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLark) -> None:
        async with async_client.rate_cards.with_streaming_response.retrieve(
            "rate_card_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rate_card = await response.parse()
            assert_matches_type(RateCardResource, rate_card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncLark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rate_card_id` but received ''"):
            await async_client.rate_cards.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncLark) -> None:
        rate_card = await async_client.rate_cards.list()
        assert_matches_type(RateCardListResponse, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncLark) -> None:
        rate_card = await async_client.rate_cards.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(RateCardListResponse, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncLark) -> None:
        response = await async_client.rate_cards.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rate_card = await response.parse()
        assert_matches_type(RateCardListResponse, rate_card, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncLark) -> None:
        async with async_client.rate_cards.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rate_card = await response.parse()
            assert_matches_type(RateCardListResponse, rate_card, path=["response"])

        assert cast(Any, response.is_closed) is True
