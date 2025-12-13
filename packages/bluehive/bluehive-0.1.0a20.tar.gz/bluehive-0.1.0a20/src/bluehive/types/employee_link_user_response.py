# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["EmployeeLinkUserResponse"]


class EmployeeLinkUserResponse(BaseModel):
    link_id: str = FieldInfo(alias="linkId")
    """ID of the created link"""

    message: str

    success: bool
