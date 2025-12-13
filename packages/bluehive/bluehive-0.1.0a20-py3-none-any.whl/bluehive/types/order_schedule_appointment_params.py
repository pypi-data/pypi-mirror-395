# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = ["OrderScheduleAppointmentParams", "Appointment", "AppointmentUnionMember0", "AppointmentUnionMember1"]


class OrderScheduleAppointmentParams(TypedDict, total=False):
    appointment: Required[Appointment]

    order_access_code: Annotated[str, PropertyInfo(alias="orderAccessCode")]
    """Order access code for authorization"""

    provider_id: Annotated[str, PropertyInfo(alias="providerId")]
    """Provider ID for authorization"""


class AppointmentUnionMember0(TypedDict, total=False):
    date: Required[str]
    """Required for appointment type"""

    date_time: Required[Annotated[Union[str, datetime], PropertyInfo(alias="dateTime", format="iso8601")]]
    """Required for appointment type"""

    time: Required[str]
    """Required for appointment type"""

    notes: str
    """Optional for walkin type"""

    type: Literal["appointment"]


class AppointmentUnionMember1(TypedDict, total=False):
    date: str
    """Required for appointment type"""

    date_time: Annotated[Union[str, datetime], PropertyInfo(alias="dateTime", format="iso8601")]
    """Required for appointment type"""

    notes: str
    """Optional for walkin type"""

    time: str
    """Required for appointment type"""

    type: Literal["walkin"]


Appointment: TypeAlias = Union[AppointmentUnionMember0, AppointmentUnionMember1]
