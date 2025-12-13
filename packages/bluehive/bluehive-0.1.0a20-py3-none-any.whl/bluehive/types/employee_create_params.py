# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["EmployeeCreateParams", "Address", "ExtendedField", "Phone"]


class EmployeeCreateParams(TypedDict, total=False):
    email: Required[str]

    first_name: Required[Annotated[str, PropertyInfo(alias="firstName")]]

    last_name: Required[Annotated[str, PropertyInfo(alias="lastName")]]

    active_account: Annotated[Literal["Active", "Inactive"], PropertyInfo(alias="activeAccount")]

    address: Address

    blurb: str

    departments: SequenceNotStr[str]

    dob: str

    employer_id: str

    extended_fields: Annotated[Iterable[ExtendedField], PropertyInfo(alias="extendedFields")]

    phone: Iterable[Phone]

    title: str


class Address(TypedDict, total=False):
    city: Required[str]

    postal_code: Required[Annotated[str, PropertyInfo(alias="postalCode")]]

    state: Required[str]

    street1: Required[str]

    country: str

    county: str

    street2: str


class ExtendedField(TypedDict, total=False):
    name: Required[str]

    value: Required[str]


class Phone(TypedDict, total=False):
    number: Required[str]

    type: Required[Literal["Cell", "Home", "Work", "Other"]]
