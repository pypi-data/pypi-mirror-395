# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .subscription_resource import SubscriptionResource

__all__ = [
    "SubscriptionCreateResponse",
    "Result",
    "ResultCreateSubscriptionRequiresActionResponse",
    "ResultCreateSubscriptionRequiresActionResponseAction",
    "ResultCreateSubscriptionSuccessResponse",
]


class ResultCreateSubscriptionRequiresActionResponseAction(BaseModel):
    checkout_url: str
    """The URL of the checkout page to redirect to in order to complete the request."""

    requires_action_type: Literal["checkout"]


class ResultCreateSubscriptionRequiresActionResponse(BaseModel):
    action: ResultCreateSubscriptionRequiresActionResponseAction
    """The action to take to complete the request."""

    result_type: Literal["requires_action"]


class ResultCreateSubscriptionSuccessResponse(BaseModel):
    result_type: Literal["success"]

    subscription: SubscriptionResource
    """The created subscription resource."""


Result: TypeAlias = Annotated[
    Union[ResultCreateSubscriptionRequiresActionResponse, ResultCreateSubscriptionSuccessResponse],
    PropertyInfo(discriminator="result_type"),
]


class SubscriptionCreateResponse(BaseModel):
    result: Result
    """The result of the request.

    If the request is successful, the subscription resource will be returned. If the
    request is requires action, the action to take to complete the request will be
    returned.
    """
