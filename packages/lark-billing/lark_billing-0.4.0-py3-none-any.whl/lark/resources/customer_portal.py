# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import customer_portal_create_session_params
from .._types import Body, Query, Headers, NotGiven, not_given
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
from ..types.customer_portal_create_session_response import CustomerPortalCreateSessionResponse

__all__ = ["CustomerPortalResource", "AsyncCustomerPortalResource"]


class CustomerPortalResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CustomerPortalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return CustomerPortalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CustomerPortalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return CustomerPortalResourceWithStreamingResponse(self)

    def create_session(
        self,
        *,
        return_url: str,
        subject_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CustomerPortalCreateSessionResponse:
        """
        Create Customer Portal Session

        Args:
          return_url: The URL to redirect customers to if they click the back button on the customer
              portal.

          subject_id: The ID or external ID of the subject to create the customer portal session for.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/customer-portal/sessions",
            body=maybe_transform(
                {
                    "return_url": return_url,
                    "subject_id": subject_id,
                },
                customer_portal_create_session_params.CustomerPortalCreateSessionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CustomerPortalCreateSessionResponse,
        )


class AsyncCustomerPortalResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCustomerPortalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCustomerPortalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCustomerPortalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return AsyncCustomerPortalResourceWithStreamingResponse(self)

    async def create_session(
        self,
        *,
        return_url: str,
        subject_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CustomerPortalCreateSessionResponse:
        """
        Create Customer Portal Session

        Args:
          return_url: The URL to redirect customers to if they click the back button on the customer
              portal.

          subject_id: The ID or external ID of the subject to create the customer portal session for.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/customer-portal/sessions",
            body=await async_maybe_transform(
                {
                    "return_url": return_url,
                    "subject_id": subject_id,
                },
                customer_portal_create_session_params.CustomerPortalCreateSessionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CustomerPortalCreateSessionResponse,
        )


class CustomerPortalResourceWithRawResponse:
    def __init__(self, customer_portal: CustomerPortalResource) -> None:
        self._customer_portal = customer_portal

        self.create_session = to_raw_response_wrapper(
            customer_portal.create_session,
        )


class AsyncCustomerPortalResourceWithRawResponse:
    def __init__(self, customer_portal: AsyncCustomerPortalResource) -> None:
        self._customer_portal = customer_portal

        self.create_session = async_to_raw_response_wrapper(
            customer_portal.create_session,
        )


class CustomerPortalResourceWithStreamingResponse:
    def __init__(self, customer_portal: CustomerPortalResource) -> None:
        self._customer_portal = customer_portal

        self.create_session = to_streamed_response_wrapper(
            customer_portal.create_session,
        )


class AsyncCustomerPortalResourceWithStreamingResponse:
    def __init__(self, customer_portal: AsyncCustomerPortalResource) -> None:
        self._customer_portal = customer_portal

        self.create_session = async_to_streamed_response_wrapper(
            customer_portal.create_session,
        )
