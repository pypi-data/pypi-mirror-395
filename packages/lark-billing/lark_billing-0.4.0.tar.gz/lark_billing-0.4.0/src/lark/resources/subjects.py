# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional

import httpx

from ..types import subject_list_params, subject_create_params, subject_update_params
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
from ..types.subject_resource import SubjectResource
from ..types.subject_list_response import SubjectListResponse
from ..types.subject_create_response import SubjectCreateResponse

__all__ = ["SubjectsResource", "AsyncSubjectsResource"]


class SubjectsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SubjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return SubjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SubjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return SubjectsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        email: Optional[str] | Omit = omit,
        external_id: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubjectCreateResponse:
        """Create Subject

        Args:
          email: The email of the subject.

        Must be a valid email address.

          external_id: The ID of the subject in your system. If provided, you may use pass it to the
              API in place of the subject ID. Must be unique.

          metadata: Additional metadata about the subject. You may use this to store any custom data
              about the subject.

          name: The name of the subject. Used for display in the dashboard.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/subjects",
            body=maybe_transform(
                {
                    "email": email,
                    "external_id": external_id,
                    "metadata": metadata,
                    "name": name,
                },
                subject_create_params.SubjectCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectCreateResponse,
        )

    def retrieve(
        self,
        subject_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubjectResource:
        """
        Get Subject

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id:
            raise ValueError(f"Expected a non-empty value for `subject_id` but received {subject_id!r}")
        return self._get(
            f"/subjects/{subject_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectResource,
        )

    def update(
        self,
        subject_id: str,
        *,
        email: Optional[str],
        metadata: Optional[Dict[str, str]],
        name: Optional[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubjectResource:
        """Update Subject

        Args:
          email: The email of the subject.

        Must be a valid email address.

          metadata: Additional metadata about the subject. You may use this to store any custom data
              about the subject.

          name: The name of the subject. Used for display in the dashboard.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id:
            raise ValueError(f"Expected a non-empty value for `subject_id` but received {subject_id!r}")
        return self._put(
            f"/subjects/{subject_id}",
            body=maybe_transform(
                {
                    "email": email,
                    "metadata": metadata,
                    "name": name,
                },
                subject_update_params.SubjectUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectResource,
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
    ) -> SubjectListResponse:
        """
        List Subjects

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/subjects",
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
                    subject_list_params.SubjectListParams,
                ),
            ),
            cast_to=SubjectListResponse,
        )

    def delete(
        self,
        subject_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Delete Subject

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id:
            raise ValueError(f"Expected a non-empty value for `subject_id` but received {subject_id!r}")
        return self._delete(
            f"/subjects/{subject_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncSubjectsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSubjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/uselark/lark-billing-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSubjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSubjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/uselark/lark-billing-python#with_streaming_response
        """
        return AsyncSubjectsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        email: Optional[str] | Omit = omit,
        external_id: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubjectCreateResponse:
        """Create Subject

        Args:
          email: The email of the subject.

        Must be a valid email address.

          external_id: The ID of the subject in your system. If provided, you may use pass it to the
              API in place of the subject ID. Must be unique.

          metadata: Additional metadata about the subject. You may use this to store any custom data
              about the subject.

          name: The name of the subject. Used for display in the dashboard.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/subjects",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "external_id": external_id,
                    "metadata": metadata,
                    "name": name,
                },
                subject_create_params.SubjectCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectCreateResponse,
        )

    async def retrieve(
        self,
        subject_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubjectResource:
        """
        Get Subject

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id:
            raise ValueError(f"Expected a non-empty value for `subject_id` but received {subject_id!r}")
        return await self._get(
            f"/subjects/{subject_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectResource,
        )

    async def update(
        self,
        subject_id: str,
        *,
        email: Optional[str],
        metadata: Optional[Dict[str, str]],
        name: Optional[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubjectResource:
        """Update Subject

        Args:
          email: The email of the subject.

        Must be a valid email address.

          metadata: Additional metadata about the subject. You may use this to store any custom data
              about the subject.

          name: The name of the subject. Used for display in the dashboard.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id:
            raise ValueError(f"Expected a non-empty value for `subject_id` but received {subject_id!r}")
        return await self._put(
            f"/subjects/{subject_id}",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "metadata": metadata,
                    "name": name,
                },
                subject_update_params.SubjectUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectResource,
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
    ) -> SubjectListResponse:
        """
        List Subjects

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/subjects",
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
                    subject_list_params.SubjectListParams,
                ),
            ),
            cast_to=SubjectListResponse,
        )

    async def delete(
        self,
        subject_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Delete Subject

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id:
            raise ValueError(f"Expected a non-empty value for `subject_id` but received {subject_id!r}")
        return await self._delete(
            f"/subjects/{subject_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class SubjectsResourceWithRawResponse:
    def __init__(self, subjects: SubjectsResource) -> None:
        self._subjects = subjects

        self.create = to_raw_response_wrapper(
            subjects.create,
        )
        self.retrieve = to_raw_response_wrapper(
            subjects.retrieve,
        )
        self.update = to_raw_response_wrapper(
            subjects.update,
        )
        self.list = to_raw_response_wrapper(
            subjects.list,
        )
        self.delete = to_raw_response_wrapper(
            subjects.delete,
        )


class AsyncSubjectsResourceWithRawResponse:
    def __init__(self, subjects: AsyncSubjectsResource) -> None:
        self._subjects = subjects

        self.create = async_to_raw_response_wrapper(
            subjects.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            subjects.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            subjects.update,
        )
        self.list = async_to_raw_response_wrapper(
            subjects.list,
        )
        self.delete = async_to_raw_response_wrapper(
            subjects.delete,
        )


class SubjectsResourceWithStreamingResponse:
    def __init__(self, subjects: SubjectsResource) -> None:
        self._subjects = subjects

        self.create = to_streamed_response_wrapper(
            subjects.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            subjects.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            subjects.update,
        )
        self.list = to_streamed_response_wrapper(
            subjects.list,
        )
        self.delete = to_streamed_response_wrapper(
            subjects.delete,
        )


class AsyncSubjectsResourceWithStreamingResponse:
    def __init__(self, subjects: AsyncSubjectsResource) -> None:
        self._subjects = subjects

        self.create = async_to_streamed_response_wrapper(
            subjects.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            subjects.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            subjects.update,
        )
        self.list = async_to_streamed_response_wrapper(
            subjects.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            subjects.delete,
        )
