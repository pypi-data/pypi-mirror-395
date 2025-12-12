# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.customer_access_retrieve_billing_state_response import CustomerAccessRetrieveBillingStateResponse

__all__ = ["CustomerAccessResource", "AsyncCustomerAccessResource"]


class CustomerAccessResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CustomerAccessResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return CustomerAccessResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CustomerAccessResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return CustomerAccessResourceWithStreamingResponse(self)

    def retrieve_billing_state(
        self,
        subject_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CustomerAccessRetrieveBillingStateResponse:
        """
        Get Billing State

        Args:
          subject_id: The ID or external ID of the subject to get billing state for.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id:
            raise ValueError(f"Expected a non-empty value for `subject_id` but received {subject_id!r}")
        return self._get(
            f"/customer-access/{subject_id}/billing-state",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CustomerAccessRetrieveBillingStateResponse,
        )


class AsyncCustomerAccessResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCustomerAccessResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCustomerAccessResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCustomerAccessResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return AsyncCustomerAccessResourceWithStreamingResponse(self)

    async def retrieve_billing_state(
        self,
        subject_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CustomerAccessRetrieveBillingStateResponse:
        """
        Get Billing State

        Args:
          subject_id: The ID or external ID of the subject to get billing state for.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id:
            raise ValueError(f"Expected a non-empty value for `subject_id` but received {subject_id!r}")
        return await self._get(
            f"/customer-access/{subject_id}/billing-state",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CustomerAccessRetrieveBillingStateResponse,
        )


class CustomerAccessResourceWithRawResponse:
    def __init__(self, customer_access: CustomerAccessResource) -> None:
        self._customer_access = customer_access

        self.retrieve_billing_state = to_raw_response_wrapper(
            customer_access.retrieve_billing_state,
        )


class AsyncCustomerAccessResourceWithRawResponse:
    def __init__(self, customer_access: AsyncCustomerAccessResource) -> None:
        self._customer_access = customer_access

        self.retrieve_billing_state = async_to_raw_response_wrapper(
            customer_access.retrieve_billing_state,
        )


class CustomerAccessResourceWithStreamingResponse:
    def __init__(self, customer_access: CustomerAccessResource) -> None:
        self._customer_access = customer_access

        self.retrieve_billing_state = to_streamed_response_wrapper(
            customer_access.retrieve_billing_state,
        )


class AsyncCustomerAccessResourceWithStreamingResponse:
    def __init__(self, customer_access: AsyncCustomerAccessResource) -> None:
        self._customer_access = customer_access

        self.retrieve_billing_state = async_to_streamed_response_wrapper(
            customer_access.retrieve_billing_state,
        )
