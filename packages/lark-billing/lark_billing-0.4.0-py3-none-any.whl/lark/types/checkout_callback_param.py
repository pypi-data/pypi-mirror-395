# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["CheckoutCallbackParam"]


class CheckoutCallbackParam(TypedDict, total=False):
    cancelled_url: Required[str]
    """The URL to redirect to after the checkout is cancelled."""

    success_url: Required[str]
    """The URL to redirect to after the checkout is successful."""
