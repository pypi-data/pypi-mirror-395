# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["Hl7SendResultsParams", "File"]


class Hl7SendResultsParams(TypedDict, total=False):
    employee_id: Required[Annotated[str, PropertyInfo(alias="employeeId")]]
    """Employee ID to send results for"""

    file: Required[File]
    """File containing the results"""


class File(TypedDict, total=False):
    base64: Required[str]
    """Base64 encoded file content"""

    name: Required[str]
    """File name"""

    type: Required[str]
    """MIME type of the file"""
