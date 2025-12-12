# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["InvoiceListParams"]


class InvoiceListParams(TypedDict, total=False):
    subject_id: Required[str]
    """The ID or external ID of the subject to list invoices for."""

    limit: int

    offset: int
