# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal

import httpx

from ..types import (
    subscription_list_params,
    subscription_cancel_params,
    subscription_create_params,
    subscription_change_rate_card_params,
)
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
from ..types.subscription_resource import SubscriptionResource
from ..types.checkout_callback_param import CheckoutCallbackParam
from ..types.subscription_list_response import SubscriptionListResponse
from ..types.subscription_create_response import SubscriptionCreateResponse
from ..types.subscription_change_rate_card_response import SubscriptionChangeRateCardResponse

__all__ = ["SubscriptionsResource", "AsyncSubscriptionsResource"]


class SubscriptionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SubscriptionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return SubscriptionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SubscriptionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return SubscriptionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        checkout_callback_urls: CheckoutCallbackParam,
        rate_card_id: str,
        subject_id: str,
        create_checkout_session: Literal["when_required", "always"] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionCreateResponse:
        """
        Create Subscription

        Args:
          checkout_callback_urls: The URLs to redirect to after the checkout is completed or cancelled, if a
              checkout is required.

          rate_card_id: The ID of the rate card to use for the subscription.

          subject_id: The ID or external ID of the subject to create the subscription for.

          create_checkout_session: Determines whether a checkout session is always required even if the subject has
              a payment method on file. By default, if the subject has a payment method on
              file or the subscription is for a free plan, the subscription will be created
              and billed for immediately (if for a paid plan).

          metadata: Additional metadata about the subscription. You may use this to store any custom
              data about the subscription.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/subscriptions",
            body=maybe_transform(
                {
                    "checkout_callback_urls": checkout_callback_urls,
                    "rate_card_id": rate_card_id,
                    "subject_id": subject_id,
                    "create_checkout_session": create_checkout_session,
                    "metadata": metadata,
                },
                subscription_create_params.SubscriptionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionCreateResponse,
        )

    def retrieve(
        self,
        subscription_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionResource:
        """
        Get Subscription

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subscription_id:
            raise ValueError(f"Expected a non-empty value for `subscription_id` but received {subscription_id!r}")
        return self._get(
            f"/subscriptions/{subscription_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionResource,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        rate_card_id: Optional[str] | Omit = omit,
        subject_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionListResponse:
        """
        List Subscriptions

        Args:
          rate_card_id: The ID of the rate card to list subscriptions for. Cannot be used with
              subject_id.

          subject_id: The ID or external ID of the subject to list subscriptions for. Cannot be used
              with rate_card_id.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/subscriptions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "rate_card_id": rate_card_id,
                        "subject_id": subject_id,
                    },
                    subscription_list_params.SubscriptionListParams,
                ),
            ),
            cast_to=SubscriptionListResponse,
        )

    def cancel(
        self,
        subscription_id: str,
        *,
        cancel_at_end_of_cycle: Literal[True] | Omit = omit,
        reason: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionResource:
        """
        Cancel Subscription

        Args:
          cancel_at_end_of_cycle: Whether to cancel the subscription at end of cycle.

          reason: The reason for cancelling the subscription.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subscription_id:
            raise ValueError(f"Expected a non-empty value for `subscription_id` but received {subscription_id!r}")
        return self._post(
            f"/subscriptions/{subscription_id}/cancel",
            body=maybe_transform(
                {
                    "cancel_at_end_of_cycle": cancel_at_end_of_cycle,
                    "reason": reason,
                },
                subscription_cancel_params.SubscriptionCancelParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionResource,
        )

    def change_rate_card(
        self,
        subscription_id: str,
        *,
        checkout_callback_urls: CheckoutCallbackParam,
        rate_card_id: str,
        upgrade_behavior: Literal["prorate", "rate_difference"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionChangeRateCardResponse:
        """
        Change Subscription Rate Card

        Args:
          checkout_callback_urls: The URLs to redirect to after the checkout is completed or cancelled, if a
              checkout is required.

          rate_card_id: The ID of the rate card to change the subscription to.

          upgrade_behavior: The behavior to use when upgrading the subscription. If 'prorate', the customer
              will be charged for the prorated difference. If 'rate_difference', the customer
              will be charged for the difference in the rate cards without respect to time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subscription_id:
            raise ValueError(f"Expected a non-empty value for `subscription_id` but received {subscription_id!r}")
        return self._post(
            f"/subscriptions/{subscription_id}/change-rate-card",
            body=maybe_transform(
                {
                    "checkout_callback_urls": checkout_callback_urls,
                    "rate_card_id": rate_card_id,
                    "upgrade_behavior": upgrade_behavior,
                },
                subscription_change_rate_card_params.SubscriptionChangeRateCardParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionChangeRateCardResponse,
        )


class AsyncSubscriptionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSubscriptionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSubscriptionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSubscriptionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return AsyncSubscriptionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        checkout_callback_urls: CheckoutCallbackParam,
        rate_card_id: str,
        subject_id: str,
        create_checkout_session: Literal["when_required", "always"] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionCreateResponse:
        """
        Create Subscription

        Args:
          checkout_callback_urls: The URLs to redirect to after the checkout is completed or cancelled, if a
              checkout is required.

          rate_card_id: The ID of the rate card to use for the subscription.

          subject_id: The ID or external ID of the subject to create the subscription for.

          create_checkout_session: Determines whether a checkout session is always required even if the subject has
              a payment method on file. By default, if the subject has a payment method on
              file or the subscription is for a free plan, the subscription will be created
              and billed for immediately (if for a paid plan).

          metadata: Additional metadata about the subscription. You may use this to store any custom
              data about the subscription.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/subscriptions",
            body=await async_maybe_transform(
                {
                    "checkout_callback_urls": checkout_callback_urls,
                    "rate_card_id": rate_card_id,
                    "subject_id": subject_id,
                    "create_checkout_session": create_checkout_session,
                    "metadata": metadata,
                },
                subscription_create_params.SubscriptionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionCreateResponse,
        )

    async def retrieve(
        self,
        subscription_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionResource:
        """
        Get Subscription

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subscription_id:
            raise ValueError(f"Expected a non-empty value for `subscription_id` but received {subscription_id!r}")
        return await self._get(
            f"/subscriptions/{subscription_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionResource,
        )

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        rate_card_id: Optional[str] | Omit = omit,
        subject_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionListResponse:
        """
        List Subscriptions

        Args:
          rate_card_id: The ID of the rate card to list subscriptions for. Cannot be used with
              subject_id.

          subject_id: The ID or external ID of the subject to list subscriptions for. Cannot be used
              with rate_card_id.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/subscriptions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "rate_card_id": rate_card_id,
                        "subject_id": subject_id,
                    },
                    subscription_list_params.SubscriptionListParams,
                ),
            ),
            cast_to=SubscriptionListResponse,
        )

    async def cancel(
        self,
        subscription_id: str,
        *,
        cancel_at_end_of_cycle: Literal[True] | Omit = omit,
        reason: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionResource:
        """
        Cancel Subscription

        Args:
          cancel_at_end_of_cycle: Whether to cancel the subscription at end of cycle.

          reason: The reason for cancelling the subscription.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subscription_id:
            raise ValueError(f"Expected a non-empty value for `subscription_id` but received {subscription_id!r}")
        return await self._post(
            f"/subscriptions/{subscription_id}/cancel",
            body=await async_maybe_transform(
                {
                    "cancel_at_end_of_cycle": cancel_at_end_of_cycle,
                    "reason": reason,
                },
                subscription_cancel_params.SubscriptionCancelParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionResource,
        )

    async def change_rate_card(
        self,
        subscription_id: str,
        *,
        checkout_callback_urls: CheckoutCallbackParam,
        rate_card_id: str,
        upgrade_behavior: Literal["prorate", "rate_difference"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubscriptionChangeRateCardResponse:
        """
        Change Subscription Rate Card

        Args:
          checkout_callback_urls: The URLs to redirect to after the checkout is completed or cancelled, if a
              checkout is required.

          rate_card_id: The ID of the rate card to change the subscription to.

          upgrade_behavior: The behavior to use when upgrading the subscription. If 'prorate', the customer
              will be charged for the prorated difference. If 'rate_difference', the customer
              will be charged for the difference in the rate cards without respect to time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subscription_id:
            raise ValueError(f"Expected a non-empty value for `subscription_id` but received {subscription_id!r}")
        return await self._post(
            f"/subscriptions/{subscription_id}/change-rate-card",
            body=await async_maybe_transform(
                {
                    "checkout_callback_urls": checkout_callback_urls,
                    "rate_card_id": rate_card_id,
                    "upgrade_behavior": upgrade_behavior,
                },
                subscription_change_rate_card_params.SubscriptionChangeRateCardParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionChangeRateCardResponse,
        )


class SubscriptionsResourceWithRawResponse:
    def __init__(self, subscriptions: SubscriptionsResource) -> None:
        self._subscriptions = subscriptions

        self.create = to_raw_response_wrapper(
            subscriptions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            subscriptions.retrieve,
        )
        self.list = to_raw_response_wrapper(
            subscriptions.list,
        )
        self.cancel = to_raw_response_wrapper(
            subscriptions.cancel,
        )
        self.change_rate_card = to_raw_response_wrapper(
            subscriptions.change_rate_card,
        )


class AsyncSubscriptionsResourceWithRawResponse:
    def __init__(self, subscriptions: AsyncSubscriptionsResource) -> None:
        self._subscriptions = subscriptions

        self.create = async_to_raw_response_wrapper(
            subscriptions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            subscriptions.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            subscriptions.list,
        )
        self.cancel = async_to_raw_response_wrapper(
            subscriptions.cancel,
        )
        self.change_rate_card = async_to_raw_response_wrapper(
            subscriptions.change_rate_card,
        )


class SubscriptionsResourceWithStreamingResponse:
    def __init__(self, subscriptions: SubscriptionsResource) -> None:
        self._subscriptions = subscriptions

        self.create = to_streamed_response_wrapper(
            subscriptions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            subscriptions.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            subscriptions.list,
        )
        self.cancel = to_streamed_response_wrapper(
            subscriptions.cancel,
        )
        self.change_rate_card = to_streamed_response_wrapper(
            subscriptions.change_rate_card,
        )


class AsyncSubscriptionsResourceWithStreamingResponse:
    def __init__(self, subscriptions: AsyncSubscriptionsResource) -> None:
        self._subscriptions = subscriptions

        self.create = async_to_streamed_response_wrapper(
            subscriptions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            subscriptions.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            subscriptions.list,
        )
        self.cancel = async_to_streamed_response_wrapper(
            subscriptions.cancel,
        )
        self.change_rate_card = async_to_streamed_response_wrapper(
            subscriptions.change_rate_card,
        )
