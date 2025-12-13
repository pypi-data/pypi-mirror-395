# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EmployeeListParams"]


class EmployeeListParams(TypedDict, total=False):
    employer_id: Required[Annotated[str, PropertyInfo(alias="employerId")]]
    """ID of the employer to list employees for"""

    limit: str
    """Maximum number of employees to return (default: 50)"""

    offset: str
    """Number of employees to skip (default: 0)"""
