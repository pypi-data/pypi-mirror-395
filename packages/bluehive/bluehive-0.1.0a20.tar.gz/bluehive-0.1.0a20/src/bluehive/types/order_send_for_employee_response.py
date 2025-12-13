# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "OrderSendForEmployeeResponse",
    "UnionMember0",
    "UnionMember0UnavailableService",
    "UnionMember1",
    "UnionMember1OrderResult",
    "UnionMember1UnavailableService",
]


class UnionMember0UnavailableService(BaseModel):
    reason: str
    """Why the service was unavailable"""

    service_id: str = FieldInfo(alias="serviceId")

    service_name: Optional[str] = FieldInfo(alias="serviceName", default=None)


class UnionMember0(BaseModel):
    order_id: str = FieldInfo(alias="orderId")

    order_number: str = FieldInfo(alias="orderNumber")

    success: Literal[True]

    message: Optional[str] = None

    partial_success: Optional[bool] = FieldInfo(alias="partialSuccess", default=None)
    """True when some services were unavailable but order was still created"""

    unavailable_services: Optional[List[UnionMember0UnavailableService]] = FieldInfo(
        alias="unavailableServices", default=None
    )
    """Services that could not be included in the order"""


class UnionMember1OrderResult(BaseModel):
    order_id: str = FieldInfo(alias="orderId")

    order_number: str = FieldInfo(alias="orderNumber")

    provider_id: str = FieldInfo(alias="providerId")


class UnionMember1UnavailableService(BaseModel):
    reason: str
    """Why the service was unavailable"""

    service_id: str = FieldInfo(alias="serviceId")

    service_name: Optional[str] = FieldInfo(alias="serviceName", default=None)


class UnionMember1(BaseModel):
    order_results: List[UnionMember1OrderResult] = FieldInfo(alias="orderResults")

    status: Literal["split"]

    success: Literal[True]

    message: Optional[str] = None

    partial_success: Optional[bool] = FieldInfo(alias="partialSuccess", default=None)
    """True when some services were unavailable but orders were still created"""

    unavailable_services: Optional[List[UnionMember1UnavailableService]] = FieldInfo(
        alias="unavailableServices", default=None
    )
    """Services that could not be included in any order"""


OrderSendForEmployeeResponse: TypeAlias = Union[UnionMember0, UnionMember1]
