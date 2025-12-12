# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

__all__ = ["SubjectUpdateParams"]


class SubjectUpdateParams(TypedDict, total=False):
    email: Required[Optional[str]]
    """The email of the subject. Must be a valid email address."""

    metadata: Required[Optional[Dict[str, str]]]
    """Additional metadata about the subject.

    You may use this to store any custom data about the subject.
    """

    name: Required[Optional[str]]
    """The name of the subject. Used for display in the dashboard."""
