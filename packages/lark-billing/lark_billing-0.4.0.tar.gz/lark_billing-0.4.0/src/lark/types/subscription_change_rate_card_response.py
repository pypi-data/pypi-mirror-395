# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .subscription_resource import SubscriptionResource

__all__ = [
    "SubscriptionChangeRateCardResponse",
    "Result",
    "ResultChangeSubscriptionRateCardRequiresActionResponse",
    "ResultChangeSubscriptionRateCardRequiresActionResponseAction",
    "ResultChangeSubscriptionRateCardSuccessResponse",
]


class ResultChangeSubscriptionRateCardRequiresActionResponseAction(BaseModel):
    checkout_url: str
    """The URL of the checkout page to redirect to in order to complete the request."""

    type: Literal["checkout"]


class ResultChangeSubscriptionRateCardRequiresActionResponse(BaseModel):
    action: ResultChangeSubscriptionRateCardRequiresActionResponseAction
    """The action to take to complete the request."""

    type: Literal["requires_action"]


class ResultChangeSubscriptionRateCardSuccessResponse(BaseModel):
    subscription: SubscriptionResource
    """The updated subscription resource."""

    type: Literal["success"]


Result: TypeAlias = Annotated[
    Union[ResultChangeSubscriptionRateCardRequiresActionResponse, ResultChangeSubscriptionRateCardSuccessResponse],
    PropertyInfo(discriminator="type"),
]


class SubscriptionChangeRateCardResponse(BaseModel):
    result: Result
    """The result of the request.

    If the request is successful, the subscription resource will be returned. If the
    request is requires action, the action to take to complete the request will be
    returned.
    """
