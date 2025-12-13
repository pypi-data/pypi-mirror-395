# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["EmployeeListResponse", "Employee", "EmployeeAddress", "EmployeeExtendedField", "EmployeePhone"]


class EmployeeAddress(BaseModel):
    city: str
    """City"""

    postal_code: str = FieldInfo(alias="postalCode")
    """Postal code"""

    state: str
    """State"""

    street1: str
    """Street address line 1"""

    country: Optional[str] = None
    """Country"""

    county: Optional[str] = None
    """County"""

    street2: Optional[str] = None
    """Street address line 2"""


class EmployeeExtendedField(BaseModel):
    name: str
    """Field name"""

    value: str
    """Field value"""


class EmployeePhone(BaseModel):
    number: str
    """Phone number"""

    type: Literal["Cell", "Home", "Work", "Other"]
    """Type of phone number"""


class Employee(BaseModel):
    api_id: str = FieldInfo(alias="_id")
    """Unique identifier"""

    email: str
    """Email address"""

    employer_id: str
    """ID of associated employer"""

    first_name: str = FieldInfo(alias="firstName")
    """First name"""

    last_name: str = FieldInfo(alias="lastName")
    """Last name"""

    active_account: Optional[Literal["Active", "Inactive"]] = FieldInfo(alias="activeAccount", default=None)
    """Account status"""

    address: Optional[EmployeeAddress] = None
    """Employee address"""

    blurb: Optional[str] = None
    """Brief description or bio"""

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    """Creation timestamp"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """ID of user who created the employee"""

    departments: Optional[List[str]] = None
    """List of department names"""

    dob: Optional[str] = None
    """Date of birth"""

    extended_fields: Optional[List[EmployeeExtendedField]] = FieldInfo(alias="extendedFields", default=None)
    """Additional custom fields"""

    phone: Optional[List[EmployeePhone]] = None
    """Contact phone numbers"""

    title: Optional[str] = None
    """Job title"""

    updated_at: Optional[datetime] = FieldInfo(alias="updatedAt", default=None)
    """Last update timestamp"""

    updated_by: Optional[str] = FieldInfo(alias="updatedBy", default=None)
    """ID of user who last updated the employee"""


class EmployeeListResponse(BaseModel):
    employees: List[Employee]
    """List of employees"""

    message: str

    success: bool

    total: float
    """Total number of employees returned"""
