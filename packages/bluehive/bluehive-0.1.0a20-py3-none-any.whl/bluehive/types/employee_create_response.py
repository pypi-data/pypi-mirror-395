# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["EmployeeCreateResponse"]


class EmployeeCreateResponse(BaseModel):
    employee_id: str = FieldInfo(alias="employeeId")
    """ID of the created employee"""

    message: str

    success: bool
