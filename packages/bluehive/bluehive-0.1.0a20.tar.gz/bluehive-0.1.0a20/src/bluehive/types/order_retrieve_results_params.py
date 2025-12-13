# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["OrderRetrieveResultsParams"]


class OrderRetrieveResultsParams(TypedDict, total=False):
    page: int

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]

    service_id: Annotated[str, PropertyInfo(alias="serviceId")]

    since: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    status: str

    until: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
