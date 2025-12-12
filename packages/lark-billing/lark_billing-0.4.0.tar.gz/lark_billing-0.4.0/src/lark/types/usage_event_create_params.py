# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["UsageEventCreateParams"]


class UsageEventCreateParams(TypedDict, total=False):
    data: Required[Dict[str, Union[str, int]]]
    """The data of the usage event.

    This should contain any data that is needed to aggregate the usage event.
    """

    event_name: Required[str]
    """The name of the event.

    This is used by pricing metrics to aggregate usage events.
    """

    idempotency_key: Required[str]
    """The idempotency key for the usage event.

    This ensures that the same event is not processed multiple times.
    """

    subject_id: Required[str]
    """The ID or external ID of the subject that the usage event is for."""

    timestamp: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """The timestamp of the usage event.

    It is highly recommended to provide a timestamp. If not provided, the current
    timestamp will be used.
    """
