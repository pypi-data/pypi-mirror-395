# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["EmployeeLinkUserParams"]


class EmployeeLinkUserParams(TypedDict, total=False):
    employee_id: Required[Annotated[str, PropertyInfo(alias="employeeId")]]

    user_id: Required[Annotated[str, PropertyInfo(alias="userId")]]

    role: SequenceNotStr[str]
