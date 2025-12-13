# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["OrderUpdateParams", "Service"]


class OrderUpdateParams(TypedDict, total=False):
    metadata: Dict[str, object]
    """
    Arbitrary metadata to update on the order (non-indexed passthrough, <=10KB when
    JSON stringified)
    """

    services: Iterable[Service]

    status: Literal[
        "order_sent", "order_accepted", "order_refused", "employee_confirmed", "order_fulfilled", "order_complete"
    ]


class Service(TypedDict, total=False):
    service_id: Required[Annotated[str, PropertyInfo(alias="serviceId")]]

    due_date: Annotated[Union[str, datetime], PropertyInfo(alias="dueDate", format="iso8601")]

    results: Dict[str, object]

    status: Literal["pending", "in_progress", "completed", "cancelled", "rejected"]
