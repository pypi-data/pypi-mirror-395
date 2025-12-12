# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Literal

import httpx

from ..types import rate_card_list_params, rate_card_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.rate_card_resource import RateCardResource
from ..types.rate_card_list_response import RateCardListResponse

__all__ = ["RateCardsResource", "AsyncRateCardsResource"]


class RateCardsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RateCardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return RateCardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RateCardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return RateCardsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        billing_interval: Literal["monthly", "yearly"],
        name: str,
        description: Optional[str] | Omit = omit,
        fixed_rates: Iterable[rate_card_create_params.FixedRate] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        usage_based_rates: Iterable[rate_card_create_params.UsageBasedRate] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RateCardResource:
        """
        Create Rate Card

        Args:
          billing_interval: How often the customer will be billed for this rate card.

          name: The name of the rate card displayed to the customer.

          description: The description of the rate card displayed to the customer.

          fixed_rates: The fixed rates of the rate card. These are billed at the start of each billing
              cycle.

          usage_based_rates: The usage based rates of the rate card. These are billed at the end of each
              billing cycle.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/rate-cards",
            body=maybe_transform(
                {
                    "billing_interval": billing_interval,
                    "name": name,
                    "description": description,
                    "fixed_rates": fixed_rates,
                    "metadata": metadata,
                    "usage_based_rates": usage_based_rates,
                },
                rate_card_create_params.RateCardCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RateCardResource,
        )

    def retrieve(
        self,
        rate_card_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RateCardResource:
        """
        Get Rate Card

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rate_card_id:
            raise ValueError(f"Expected a non-empty value for `rate_card_id` but received {rate_card_id!r}")
        return self._get(
            f"/rate-cards/{rate_card_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RateCardResource,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RateCardListResponse:
        """
        List Rate Cards

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/rate-cards",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    rate_card_list_params.RateCardListParams,
                ),
            ),
            cast_to=RateCardListResponse,
        )


class AsyncRateCardsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRateCardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRateCardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRateCardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return AsyncRateCardsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        billing_interval: Literal["monthly", "yearly"],
        name: str,
        description: Optional[str] | Omit = omit,
        fixed_rates: Iterable[rate_card_create_params.FixedRate] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        usage_based_rates: Iterable[rate_card_create_params.UsageBasedRate] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RateCardResource:
        """
        Create Rate Card

        Args:
          billing_interval: How often the customer will be billed for this rate card.

          name: The name of the rate card displayed to the customer.

          description: The description of the rate card displayed to the customer.

          fixed_rates: The fixed rates of the rate card. These are billed at the start of each billing
              cycle.

          usage_based_rates: The usage based rates of the rate card. These are billed at the end of each
              billing cycle.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/rate-cards",
            body=await async_maybe_transform(
                {
                    "billing_interval": billing_interval,
                    "name": name,
                    "description": description,
                    "fixed_rates": fixed_rates,
                    "metadata": metadata,
                    "usage_based_rates": usage_based_rates,
                },
                rate_card_create_params.RateCardCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RateCardResource,
        )

    async def retrieve(
        self,
        rate_card_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RateCardResource:
        """
        Get Rate Card

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rate_card_id:
            raise ValueError(f"Expected a non-empty value for `rate_card_id` but received {rate_card_id!r}")
        return await self._get(
            f"/rate-cards/{rate_card_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RateCardResource,
        )

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RateCardListResponse:
        """
        List Rate Cards

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/rate-cards",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    rate_card_list_params.RateCardListParams,
                ),
            ),
            cast_to=RateCardListResponse,
        )


class RateCardsResourceWithRawResponse:
    def __init__(self, rate_cards: RateCardsResource) -> None:
        self._rate_cards = rate_cards

        self.create = to_raw_response_wrapper(
            rate_cards.create,
        )
        self.retrieve = to_raw_response_wrapper(
            rate_cards.retrieve,
        )
        self.list = to_raw_response_wrapper(
            rate_cards.list,
        )


class AsyncRateCardsResourceWithRawResponse:
    def __init__(self, rate_cards: AsyncRateCardsResource) -> None:
        self._rate_cards = rate_cards

        self.create = async_to_raw_response_wrapper(
            rate_cards.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            rate_cards.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            rate_cards.list,
        )


class RateCardsResourceWithStreamingResponse:
    def __init__(self, rate_cards: RateCardsResource) -> None:
        self._rate_cards = rate_cards

        self.create = to_streamed_response_wrapper(
            rate_cards.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            rate_cards.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            rate_cards.list,
        )


class AsyncRateCardsResourceWithStreamingResponse:
    def __init__(self, rate_cards: AsyncRateCardsResource) -> None:
        self._rate_cards = rate_cards

        self.create = async_to_streamed_response_wrapper(
            rate_cards.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            rate_cards.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            rate_cards.list,
        )
