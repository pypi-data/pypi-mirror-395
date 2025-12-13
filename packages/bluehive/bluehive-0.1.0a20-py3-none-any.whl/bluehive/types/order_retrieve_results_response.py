# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OrderRetrieveResultsResponse", "Meta", "Service"]


class Meta(BaseModel):
    order_id: str = FieldInfo(alias="orderId")

    page: float

    page_size: float = FieldInfo(alias="pageSize")

    returned: float

    total_services: float = FieldInfo(alias="totalServices")

    employee_id: Optional[str] = FieldInfo(alias="employeeId", default=None)

    order_number: Optional[str] = FieldInfo(alias="orderNumber", default=None)

    provider_id: Optional[str] = FieldInfo(alias="providerId", default=None)


class Service(BaseModel):
    service_id: str = FieldInfo(alias="serviceId")

    status: str

    alt_txt: Optional[str] = FieldInfo(alias="altTxt", default=None)

    completed_datetime: Optional[datetime] = None

    contacts: Optional[List[str]] = None

    drawn_datetime: Optional[datetime] = None

    file_ids: Optional[List[str]] = FieldInfo(alias="fileIds", default=None)

    message: Optional[str] = None

    result: Optional[str] = None

    results_posted: Optional[datetime] = FieldInfo(alias="resultsPosted", default=None)


class OrderRetrieveResultsResponse(BaseModel):
    meta: Meta

    services: List[Service]
