# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["OrderUpdateStatusParams"]


class OrderUpdateStatusParams(TypedDict, total=False):
    status: Required[
        Literal[
            "order_sent", "order_accepted", "order_refused", "employee_confirmed", "order_fulfilled", "order_complete"
        ]
    ]

    message: str
