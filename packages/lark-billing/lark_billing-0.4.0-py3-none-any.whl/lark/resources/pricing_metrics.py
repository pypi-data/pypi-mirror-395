# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import (
    pricing_metric_list_params,
    pricing_metric_create_params,
    pricing_metric_create_summary_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
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
from ..types.period_param import PeriodParam
from ..types.pricing_metric_resource import PricingMetricResource
from ..types.pricing_metric_list_response import PricingMetricListResponse
from ..types.pricing_metric_create_summary_response import PricingMetricCreateSummaryResponse

__all__ = ["PricingMetricsResource", "AsyncPricingMetricsResource"]


class PricingMetricsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PricingMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return PricingMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PricingMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return PricingMetricsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        aggregation: pricing_metric_create_params.Aggregation,
        event_name: str,
        name: str,
        unit: str,
        dimensions: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PricingMetricResource:
        """
        Create Pricing Metric

        Args:
          aggregation: The aggregation function used to compute the value of the pricing metric.

          event_name: The name of the event that the pricing metric is computed on.

          name: The name of the pricing metric.

          unit: Unit of measurement for the pricing metric.

          dimensions: The dimensions by which the events are grouped to compute the pricing metric.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/pricing-metrics",
            body=maybe_transform(
                {
                    "aggregation": aggregation,
                    "event_name": event_name,
                    "name": name,
                    "unit": unit,
                    "dimensions": dimensions,
                },
                pricing_metric_create_params.PricingMetricCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PricingMetricResource,
        )

    def retrieve(
        self,
        pricing_metric_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PricingMetricResource:
        """
        Get Pricing Metric

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pricing_metric_id:
            raise ValueError(f"Expected a non-empty value for `pricing_metric_id` but received {pricing_metric_id!r}")
        return self._get(
            f"/pricing-metrics/{pricing_metric_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PricingMetricResource,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PricingMetricListResponse:
        """
        List Pricing Metrics

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/pricing-metrics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"limit": limit}, pricing_metric_list_params.PricingMetricListParams),
            ),
            cast_to=PricingMetricListResponse,
        )

    def create_summary(
        self,
        pricing_metric_id: str,
        *,
        period: PeriodParam,
        subject_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PricingMetricCreateSummaryResponse:
        """
        Create Pricing Metric Summary

        Args:
          period: The period that the summary should be computed over.

          subject_id: The ID or external ID of the subject that the summary should be computed for.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pricing_metric_id:
            raise ValueError(f"Expected a non-empty value for `pricing_metric_id` but received {pricing_metric_id!r}")
        return self._post(
            f"/pricing-metrics/{pricing_metric_id}/summary",
            body=maybe_transform(
                {
                    "period": period,
                    "subject_id": subject_id,
                },
                pricing_metric_create_summary_params.PricingMetricCreateSummaryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PricingMetricCreateSummaryResponse,
        )


class AsyncPricingMetricsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPricingMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPricingMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPricingMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return AsyncPricingMetricsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        aggregation: pricing_metric_create_params.Aggregation,
        event_name: str,
        name: str,
        unit: str,
        dimensions: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PricingMetricResource:
        """
        Create Pricing Metric

        Args:
          aggregation: The aggregation function used to compute the value of the pricing metric.

          event_name: The name of the event that the pricing metric is computed on.

          name: The name of the pricing metric.

          unit: Unit of measurement for the pricing metric.

          dimensions: The dimensions by which the events are grouped to compute the pricing metric.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/pricing-metrics",
            body=await async_maybe_transform(
                {
                    "aggregation": aggregation,
                    "event_name": event_name,
                    "name": name,
                    "unit": unit,
                    "dimensions": dimensions,
                },
                pricing_metric_create_params.PricingMetricCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PricingMetricResource,
        )

    async def retrieve(
        self,
        pricing_metric_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PricingMetricResource:
        """
        Get Pricing Metric

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pricing_metric_id:
            raise ValueError(f"Expected a non-empty value for `pricing_metric_id` but received {pricing_metric_id!r}")
        return await self._get(
            f"/pricing-metrics/{pricing_metric_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PricingMetricResource,
        )

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PricingMetricListResponse:
        """
        List Pricing Metrics

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/pricing-metrics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"limit": limit}, pricing_metric_list_params.PricingMetricListParams),
            ),
            cast_to=PricingMetricListResponse,
        )

    async def create_summary(
        self,
        pricing_metric_id: str,
        *,
        period: PeriodParam,
        subject_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PricingMetricCreateSummaryResponse:
        """
        Create Pricing Metric Summary

        Args:
          period: The period that the summary should be computed over.

          subject_id: The ID or external ID of the subject that the summary should be computed for.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pricing_metric_id:
            raise ValueError(f"Expected a non-empty value for `pricing_metric_id` but received {pricing_metric_id!r}")
        return await self._post(
            f"/pricing-metrics/{pricing_metric_id}/summary",
            body=await async_maybe_transform(
                {
                    "period": period,
                    "subject_id": subject_id,
                },
                pricing_metric_create_summary_params.PricingMetricCreateSummaryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PricingMetricCreateSummaryResponse,
        )


class PricingMetricsResourceWithRawResponse:
    def __init__(self, pricing_metrics: PricingMetricsResource) -> None:
        self._pricing_metrics = pricing_metrics

        self.create = to_raw_response_wrapper(
            pricing_metrics.create,
        )
        self.retrieve = to_raw_response_wrapper(
            pricing_metrics.retrieve,
        )
        self.list = to_raw_response_wrapper(
            pricing_metrics.list,
        )
        self.create_summary = to_raw_response_wrapper(
            pricing_metrics.create_summary,
        )


class AsyncPricingMetricsResourceWithRawResponse:
    def __init__(self, pricing_metrics: AsyncPricingMetricsResource) -> None:
        self._pricing_metrics = pricing_metrics

        self.create = async_to_raw_response_wrapper(
            pricing_metrics.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            pricing_metrics.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            pricing_metrics.list,
        )
        self.create_summary = async_to_raw_response_wrapper(
            pricing_metrics.create_summary,
        )


class PricingMetricsResourceWithStreamingResponse:
    def __init__(self, pricing_metrics: PricingMetricsResource) -> None:
        self._pricing_metrics = pricing_metrics

        self.create = to_streamed_response_wrapper(
            pricing_metrics.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            pricing_metrics.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            pricing_metrics.list,
        )
        self.create_summary = to_streamed_response_wrapper(
            pricing_metrics.create_summary,
        )


class AsyncPricingMetricsResourceWithStreamingResponse:
    def __init__(self, pricing_metrics: AsyncPricingMetricsResource) -> None:
        self._pricing_metrics = pricing_metrics

        self.create = async_to_streamed_response_wrapper(
            pricing_metrics.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            pricing_metrics.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            pricing_metrics.list,
        )
        self.create_summary = async_to_streamed_response_wrapper(
            pricing_metrics.create_summary,
        )
