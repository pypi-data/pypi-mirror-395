# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["CustomerPortalCreateSessionParams"]


class CustomerPortalCreateSessionParams(TypedDict, total=False):
    return_url: Required[str]
    """
    The URL to redirect customers to if they click the back button on the customer
    portal.
    """

    subject_id: Required[str]
    """The ID or external ID of the subject to create the customer portal session for."""
