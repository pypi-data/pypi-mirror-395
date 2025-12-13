# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EmployeeUnlinkUserParams"]


class EmployeeUnlinkUserParams(TypedDict, total=False):
    employee_id: Required[Annotated[str, PropertyInfo(alias="employeeId")]]
    """ID of the employee to unlink"""

    user_id: Required[Annotated[str, PropertyInfo(alias="userId")]]
    """ID of the user to unlink from"""
