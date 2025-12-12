# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lark import Lark, AsyncLark
from lark.types import (
    SubscriptionResource,
    SubscriptionListResponse,
    SubscriptionCreateResponse,
    SubscriptionChangeRateCardResponse,
)
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSubscriptions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Lark) -> None:
        subscription = client.subscriptions.create(
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/welcome",
            },
            rate_card_id="rc_AJWMxR81jxoRlli6p13uf3JB",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )
        assert_matches_type(SubscriptionCreateResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Lark) -> None:
        subscription = client.subscriptions.create(
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/welcome",
            },
            rate_card_id="rc_AJWMxR81jxoRlli6p13uf3JB",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
            create_checkout_session="when_required",
            metadata={},
        )
        assert_matches_type(SubscriptionCreateResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Lark) -> None:
        response = client.subscriptions.with_raw_response.create(
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/welcome",
            },
            rate_card_id="rc_AJWMxR81jxoRlli6p13uf3JB",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionCreateResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Lark) -> None:
        with client.subscriptions.with_streaming_response.create(
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/welcome",
            },
            rate_card_id="rc_AJWMxR81jxoRlli6p13uf3JB",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionCreateResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Lark) -> None:
        subscription = client.subscriptions.retrieve(
            "subscription_id",
        )
        assert_matches_type(SubscriptionResource, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Lark) -> None:
        response = client.subscriptions.with_raw_response.retrieve(
            "subscription_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionResource, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Lark) -> None:
        with client.subscriptions.with_streaming_response.retrieve(
            "subscription_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionResource, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Lark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subscription_id` but received ''"):
            client.subscriptions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Lark) -> None:
        subscription = client.subscriptions.list()
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Lark) -> None:
        subscription = client.subscriptions.list(
            limit=1,
            offset=0,
            rate_card_id="rate_card_id",
            subject_id="subject_id",
        )
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Lark) -> None:
        response = client.subscriptions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Lark) -> None:
        with client.subscriptions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_cancel(self, client: Lark) -> None:
        subscription = client.subscriptions.cancel(
            subscription_id="subscription_id",
        )
        assert_matches_type(SubscriptionResource, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_cancel_with_all_params(self, client: Lark) -> None:
        subscription = client.subscriptions.cancel(
            subscription_id="subscription_id",
            cancel_at_end_of_cycle=True,
            reason="user_requested",
        )
        assert_matches_type(SubscriptionResource, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_cancel(self, client: Lark) -> None:
        response = client.subscriptions.with_raw_response.cancel(
            subscription_id="subscription_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionResource, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_cancel(self, client: Lark) -> None:
        with client.subscriptions.with_streaming_response.cancel(
            subscription_id="subscription_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionResource, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_cancel(self, client: Lark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subscription_id` but received ''"):
            client.subscriptions.with_raw_response.cancel(
                subscription_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_change_rate_card(self, client: Lark) -> None:
        subscription = client.subscriptions.change_rate_card(
            subscription_id="subscription_id",
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/completed",
            },
            rate_card_id="rc_jQK2n0wutCj6bBcAIrL6o07g",
        )
        assert_matches_type(SubscriptionChangeRateCardResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_change_rate_card_with_all_params(self, client: Lark) -> None:
        subscription = client.subscriptions.change_rate_card(
            subscription_id="subscription_id",
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/completed",
            },
            rate_card_id="rc_jQK2n0wutCj6bBcAIrL6o07g",
            upgrade_behavior="prorate",
        )
        assert_matches_type(SubscriptionChangeRateCardResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_change_rate_card(self, client: Lark) -> None:
        response = client.subscriptions.with_raw_response.change_rate_card(
            subscription_id="subscription_id",
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/completed",
            },
            rate_card_id="rc_jQK2n0wutCj6bBcAIrL6o07g",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionChangeRateCardResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_change_rate_card(self, client: Lark) -> None:
        with client.subscriptions.with_streaming_response.change_rate_card(
            subscription_id="subscription_id",
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/completed",
            },
            rate_card_id="rc_jQK2n0wutCj6bBcAIrL6o07g",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionChangeRateCardResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_change_rate_card(self, client: Lark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subscription_id` but received ''"):
            client.subscriptions.with_raw_response.change_rate_card(
                subscription_id="",
                checkout_callback_urls={
                    "cancelled_url": "https://example.com/try-again",
                    "success_url": "https://example.com/completed",
                },
                rate_card_id="rc_jQK2n0wutCj6bBcAIrL6o07g",
            )


class TestAsyncSubscriptions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncLark) -> None:
        subscription = await async_client.subscriptions.create(
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/welcome",
            },
            rate_card_id="rc_AJWMxR81jxoRlli6p13uf3JB",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )
        assert_matches_type(SubscriptionCreateResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLark) -> None:
        subscription = await async_client.subscriptions.create(
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/welcome",
            },
            rate_card_id="rc_AJWMxR81jxoRlli6p13uf3JB",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
            create_checkout_session="when_required",
            metadata={},
        )
        assert_matches_type(SubscriptionCreateResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLark) -> None:
        response = await async_client.subscriptions.with_raw_response.create(
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/welcome",
            },
            rate_card_id="rc_AJWMxR81jxoRlli6p13uf3JB",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionCreateResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLark) -> None:
        async with async_client.subscriptions.with_streaming_response.create(
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/welcome",
            },
            rate_card_id="rc_AJWMxR81jxoRlli6p13uf3JB",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionCreateResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLark) -> None:
        subscription = await async_client.subscriptions.retrieve(
            "subscription_id",
        )
        assert_matches_type(SubscriptionResource, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLark) -> None:
        response = await async_client.subscriptions.with_raw_response.retrieve(
            "subscription_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionResource, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLark) -> None:
        async with async_client.subscriptions.with_streaming_response.retrieve(
            "subscription_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionResource, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncLark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subscription_id` but received ''"):
            await async_client.subscriptions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncLark) -> None:
        subscription = await async_client.subscriptions.list()
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncLark) -> None:
        subscription = await async_client.subscriptions.list(
            limit=1,
            offset=0,
            rate_card_id="rate_card_id",
            subject_id="subject_id",
        )
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncLark) -> None:
        response = await async_client.subscriptions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncLark) -> None:
        async with async_client.subscriptions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_cancel(self, async_client: AsyncLark) -> None:
        subscription = await async_client.subscriptions.cancel(
            subscription_id="subscription_id",
        )
        assert_matches_type(SubscriptionResource, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_cancel_with_all_params(self, async_client: AsyncLark) -> None:
        subscription = await async_client.subscriptions.cancel(
            subscription_id="subscription_id",
            cancel_at_end_of_cycle=True,
            reason="user_requested",
        )
        assert_matches_type(SubscriptionResource, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncLark) -> None:
        response = await async_client.subscriptions.with_raw_response.cancel(
            subscription_id="subscription_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionResource, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncLark) -> None:
        async with async_client.subscriptions.with_streaming_response.cancel(
            subscription_id="subscription_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionResource, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncLark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subscription_id` but received ''"):
            await async_client.subscriptions.with_raw_response.cancel(
                subscription_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_change_rate_card(self, async_client: AsyncLark) -> None:
        subscription = await async_client.subscriptions.change_rate_card(
            subscription_id="subscription_id",
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/completed",
            },
            rate_card_id="rc_jQK2n0wutCj6bBcAIrL6o07g",
        )
        assert_matches_type(SubscriptionChangeRateCardResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_change_rate_card_with_all_params(self, async_client: AsyncLark) -> None:
        subscription = await async_client.subscriptions.change_rate_card(
            subscription_id="subscription_id",
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/completed",
            },
            rate_card_id="rc_jQK2n0wutCj6bBcAIrL6o07g",
            upgrade_behavior="prorate",
        )
        assert_matches_type(SubscriptionChangeRateCardResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_change_rate_card(self, async_client: AsyncLark) -> None:
        response = await async_client.subscriptions.with_raw_response.change_rate_card(
            subscription_id="subscription_id",
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/completed",
            },
            rate_card_id="rc_jQK2n0wutCj6bBcAIrL6o07g",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionChangeRateCardResponse, subscription, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_change_rate_card(self, async_client: AsyncLark) -> None:
        async with async_client.subscriptions.with_streaming_response.change_rate_card(
            subscription_id="subscription_id",
            checkout_callback_urls={
                "cancelled_url": "https://example.com/try-again",
                "success_url": "https://example.com/completed",
            },
            rate_card_id="rc_jQK2n0wutCj6bBcAIrL6o07g",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionChangeRateCardResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_change_rate_card(self, async_client: AsyncLark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subscription_id` but received ''"):
            await async_client.subscriptions.with_raw_response.change_rate_card(
                subscription_id="",
                checkout_callback_urls={
                    "cancelled_url": "https://example.com/try-again",
                    "success_url": "https://example.com/completed",
                },
                rate_card_id="rc_jQK2n0wutCj6bBcAIrL6o07g",
            )
