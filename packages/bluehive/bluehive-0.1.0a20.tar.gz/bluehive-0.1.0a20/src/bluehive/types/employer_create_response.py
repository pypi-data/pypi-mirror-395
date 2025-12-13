# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["EmployerCreateResponse"]


class EmployerCreateResponse(BaseModel):
    api_id: str = FieldInfo(alias="_id")

    address: Dict[str, object]

    email: str

    name: str

    phones: List[Dict[str, object]]

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)

    demo: Optional[bool] = None

    employee_consent: Optional[bool] = FieldInfo(alias="employeeConsent", default=None)

    onsite_clinic: Optional[bool] = FieldInfo(alias="onsiteClinic", default=None)

    website: Optional[str] = None
