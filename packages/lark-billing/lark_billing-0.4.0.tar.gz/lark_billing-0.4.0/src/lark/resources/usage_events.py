# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from datetime import datetime

import httpx

from ..types import usage_event_create_params
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

__all__ = ["UsageEventsResource", "AsyncUsageEventsResource"]


class UsageEventsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UsageEventsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return UsageEventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsageEventsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return UsageEventsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: Dict[str, Union[str, int]],
        event_name: str,
        idempotency_key: str,
        subject_id: str,
        timestamp: Union[str, datetime, None] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """Create Usage Event

        Args:
          data: The data of the usage event.

        This should contain any data that is needed to
              aggregate the usage event.

          event_name: The name of the event. This is used by pricing metrics to aggregate usage
              events.

          idempotency_key: The idempotency key for the usage event. This ensures that the same event is not
              processed multiple times.

          subject_id: The ID or external ID of the subject that the usage event is for.

          timestamp: The timestamp of the usage event. It is highly recommended to provide a
              timestamp. If not provided, the current timestamp will be used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/usage-events",
            body=maybe_transform(
                {
                    "data": data,
                    "event_name": event_name,
                    "idempotency_key": idempotency_key,
                    "subject_id": subject_id,
                    "timestamp": timestamp,
                },
                usage_event_create_params.UsageEventCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncUsageEventsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUsageEventsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUsageEventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsageEventsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return AsyncUsageEventsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: Dict[str, Union[str, int]],
        event_name: str,
        idempotency_key: str,
        subject_id: str,
        timestamp: Union[str, datetime, None] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """Create Usage Event

        Args:
          data: The data of the usage event.

        This should contain any data that is needed to
              aggregate the usage event.

          event_name: The name of the event. This is used by pricing metrics to aggregate usage
              events.

          idempotency_key: The idempotency key for the usage event. This ensures that the same event is not
              processed multiple times.

          subject_id: The ID or external ID of the subject that the usage event is for.

          timestamp: The timestamp of the usage event. It is highly recommended to provide a
              timestamp. If not provided, the current timestamp will be used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/usage-events",
            body=await async_maybe_transform(
                {
                    "data": data,
                    "event_name": event_name,
                    "idempotency_key": idempotency_key,
                    "subject_id": subject_id,
                    "timestamp": timestamp,
                },
                usage_event_create_params.UsageEventCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class UsageEventsResourceWithRawResponse:
    def __init__(self, usage_events: UsageEventsResource) -> None:
        self._usage_events = usage_events

        self.create = to_raw_response_wrapper(
            usage_events.create,
        )


class AsyncUsageEventsResourceWithRawResponse:
    def __init__(self, usage_events: AsyncUsageEventsResource) -> None:
        self._usage_events = usage_events

        self.create = async_to_raw_response_wrapper(
            usage_events.create,
        )


class UsageEventsResourceWithStreamingResponse:
    def __init__(self, usage_events: UsageEventsResource) -> None:
        self._usage_events = usage_events

        self.create = to_streamed_response_wrapper(
            usage_events.create,
        )


class AsyncUsageEventsResourceWithStreamingResponse:
    def __init__(self, usage_events: AsyncUsageEventsResource) -> None:
        self._usage_events = usage_events

        self.create = async_to_streamed_response_wrapper(
            usage_events.create,
        )
