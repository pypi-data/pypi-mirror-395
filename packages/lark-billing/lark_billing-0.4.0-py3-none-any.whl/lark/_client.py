# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import (
    invoices,
    subjects,
    rate_cards,
    usage_events,
    subscriptions,
    customer_access,
    customer_portal,
    pricing_metrics,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import LarkError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Lark", "AsyncLark", "Client", "AsyncClient"]


class Lark(SyncAPIClient):
    customer_portal: customer_portal.CustomerPortalResource
    rate_cards: rate_cards.RateCardsResource
    usage_events: usage_events.UsageEventsResource
    subscriptions: subscriptions.SubscriptionsResource
    subjects: subjects.SubjectsResource
    pricing_metrics: pricing_metrics.PricingMetricsResource
    customer_access: customer_access.CustomerAccessResource
    invoices: invoices.InvoicesResource
    with_raw_response: LarkWithRawResponse
    with_streaming_response: LarkWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Lark client instance.

        This automatically infers the `api_key` argument from the `LARK_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("LARK_API_KEY")
        if api_key is None:
            raise LarkError(
                "The api_key client option must be set either by passing api_key to the client or by setting the LARK_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("LARK_BASE_URL")
        if base_url is None:
            base_url = f"https://api.uselark.ai"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.customer_portal = customer_portal.CustomerPortalResource(self)
        self.rate_cards = rate_cards.RateCardsResource(self)
        self.usage_events = usage_events.UsageEventsResource(self)
        self.subscriptions = subscriptions.SubscriptionsResource(self)
        self.subjects = subjects.SubjectsResource(self)
        self.pricing_metrics = pricing_metrics.PricingMetricsResource(self)
        self.customer_access = customer_access.CustomerAccessResource(self)
        self.invoices = invoices.InvoicesResource(self)
        self.with_raw_response = LarkWithRawResponse(self)
        self.with_streaming_response = LarkWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"X-API-Key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncLark(AsyncAPIClient):
    customer_portal: customer_portal.AsyncCustomerPortalResource
    rate_cards: rate_cards.AsyncRateCardsResource
    usage_events: usage_events.AsyncUsageEventsResource
    subscriptions: subscriptions.AsyncSubscriptionsResource
    subjects: subjects.AsyncSubjectsResource
    pricing_metrics: pricing_metrics.AsyncPricingMetricsResource
    customer_access: customer_access.AsyncCustomerAccessResource
    invoices: invoices.AsyncInvoicesResource
    with_raw_response: AsyncLarkWithRawResponse
    with_streaming_response: AsyncLarkWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncLark client instance.

        This automatically infers the `api_key` argument from the `LARK_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("LARK_API_KEY")
        if api_key is None:
            raise LarkError(
                "The api_key client option must be set either by passing api_key to the client or by setting the LARK_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("LARK_BASE_URL")
        if base_url is None:
            base_url = f"https://api.uselark.ai"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.customer_portal = customer_portal.AsyncCustomerPortalResource(self)
        self.rate_cards = rate_cards.AsyncRateCardsResource(self)
        self.usage_events = usage_events.AsyncUsageEventsResource(self)
        self.subscriptions = subscriptions.AsyncSubscriptionsResource(self)
        self.subjects = subjects.AsyncSubjectsResource(self)
        self.pricing_metrics = pricing_metrics.AsyncPricingMetricsResource(self)
        self.customer_access = customer_access.AsyncCustomerAccessResource(self)
        self.invoices = invoices.AsyncInvoicesResource(self)
        self.with_raw_response = AsyncLarkWithRawResponse(self)
        self.with_streaming_response = AsyncLarkWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"X-API-Key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class LarkWithRawResponse:
    def __init__(self, client: Lark) -> None:
        self.customer_portal = customer_portal.CustomerPortalResourceWithRawResponse(client.customer_portal)
        self.rate_cards = rate_cards.RateCardsResourceWithRawResponse(client.rate_cards)
        self.usage_events = usage_events.UsageEventsResourceWithRawResponse(client.usage_events)
        self.subscriptions = subscriptions.SubscriptionsResourceWithRawResponse(client.subscriptions)
        self.subjects = subjects.SubjectsResourceWithRawResponse(client.subjects)
        self.pricing_metrics = pricing_metrics.PricingMetricsResourceWithRawResponse(client.pricing_metrics)
        self.customer_access = customer_access.CustomerAccessResourceWithRawResponse(client.customer_access)
        self.invoices = invoices.InvoicesResourceWithRawResponse(client.invoices)


class AsyncLarkWithRawResponse:
    def __init__(self, client: AsyncLark) -> None:
        self.customer_portal = customer_portal.AsyncCustomerPortalResourceWithRawResponse(client.customer_portal)
        self.rate_cards = rate_cards.AsyncRateCardsResourceWithRawResponse(client.rate_cards)
        self.usage_events = usage_events.AsyncUsageEventsResourceWithRawResponse(client.usage_events)
        self.subscriptions = subscriptions.AsyncSubscriptionsResourceWithRawResponse(client.subscriptions)
        self.subjects = subjects.AsyncSubjectsResourceWithRawResponse(client.subjects)
        self.pricing_metrics = pricing_metrics.AsyncPricingMetricsResourceWithRawResponse(client.pricing_metrics)
        self.customer_access = customer_access.AsyncCustomerAccessResourceWithRawResponse(client.customer_access)
        self.invoices = invoices.AsyncInvoicesResourceWithRawResponse(client.invoices)


class LarkWithStreamedResponse:
    def __init__(self, client: Lark) -> None:
        self.customer_portal = customer_portal.CustomerPortalResourceWithStreamingResponse(client.customer_portal)
        self.rate_cards = rate_cards.RateCardsResourceWithStreamingResponse(client.rate_cards)
        self.usage_events = usage_events.UsageEventsResourceWithStreamingResponse(client.usage_events)
        self.subscriptions = subscriptions.SubscriptionsResourceWithStreamingResponse(client.subscriptions)
        self.subjects = subjects.SubjectsResourceWithStreamingResponse(client.subjects)
        self.pricing_metrics = pricing_metrics.PricingMetricsResourceWithStreamingResponse(client.pricing_metrics)
        self.customer_access = customer_access.CustomerAccessResourceWithStreamingResponse(client.customer_access)
        self.invoices = invoices.InvoicesResourceWithStreamingResponse(client.invoices)


class AsyncLarkWithStreamedResponse:
    def __init__(self, client: AsyncLark) -> None:
        self.customer_portal = customer_portal.AsyncCustomerPortalResourceWithStreamingResponse(client.customer_portal)
        self.rate_cards = rate_cards.AsyncRateCardsResourceWithStreamingResponse(client.rate_cards)
        self.usage_events = usage_events.AsyncUsageEventsResourceWithStreamingResponse(client.usage_events)
        self.subscriptions = subscriptions.AsyncSubscriptionsResourceWithStreamingResponse(client.subscriptions)
        self.subjects = subjects.AsyncSubjectsResourceWithStreamingResponse(client.subjects)
        self.pricing_metrics = pricing_metrics.AsyncPricingMetricsResourceWithStreamingResponse(client.pricing_metrics)
        self.customer_access = customer_access.AsyncCustomerAccessResourceWithStreamingResponse(client.customer_access)
        self.invoices = invoices.AsyncInvoicesResourceWithStreamingResponse(client.invoices)


Client = Lark

AsyncClient = AsyncLark
