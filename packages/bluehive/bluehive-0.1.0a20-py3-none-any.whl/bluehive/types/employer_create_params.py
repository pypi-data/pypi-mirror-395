# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EmployerCreateParams", "Address", "Phone", "Checkr"]


class EmployerCreateParams(TypedDict, total=False):
    address: Required[Address]

    email: Required[str]

    name: Required[str]

    phones: Required[Iterable[Phone]]

    billing_address: Annotated[Dict[str, object], PropertyInfo(alias="billingAddress")]

    checkr: Checkr

    demo: bool

    employee_consent: Annotated[bool, PropertyInfo(alias="employeeConsent")]

    metadata: Dict[str, object]

    onsite_clinic: Annotated[bool, PropertyInfo(alias="onsiteClinic")]

    website: str


class Address(TypedDict, total=False):
    city: Required[str]

    state: Required[str]

    street1: Required[str]

    zip_code: Required[Annotated[str, PropertyInfo(alias="zipCode")]]

    country: str

    street2: str


class Phone(TypedDict, total=False):
    number: Required[str]

    primary: bool

    type: str


class Checkr(TypedDict, total=False):
    id: Required[str]

    status: str
