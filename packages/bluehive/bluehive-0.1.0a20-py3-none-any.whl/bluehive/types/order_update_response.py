# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OrderUpdateResponse"]


class OrderUpdateResponse(BaseModel):
    message: str

    order_id: str = FieldInfo(alias="orderId")

    order_number: str = FieldInfo(alias="orderNumber")

    success: Literal[True]

    updated_fields: Optional[List[str]] = FieldInfo(alias="updatedFields", default=None)
