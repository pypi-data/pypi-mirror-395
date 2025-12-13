# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OrderRetrieveResponse"]


class OrderRetrieveResponse(BaseModel):
    order_id: Optional[str] = FieldInfo(alias="orderId", default=None)

    order_number: Optional[str] = FieldInfo(alias="orderNumber", default=None)

    status: Optional[str] = None
