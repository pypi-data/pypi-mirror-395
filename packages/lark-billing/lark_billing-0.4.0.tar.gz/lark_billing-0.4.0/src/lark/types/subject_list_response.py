# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .subject_resource import SubjectResource

__all__ = ["SubjectListResponse"]


class SubjectListResponse(BaseModel):
    has_more: bool

    subjects: List[SubjectResource]
