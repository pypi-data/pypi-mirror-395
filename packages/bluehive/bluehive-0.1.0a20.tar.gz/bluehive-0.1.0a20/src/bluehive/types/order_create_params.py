# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = [
    "OrderCreateParams",
    "Variant0",
    "Variant0Person",
    "Variant0Service",
    "Variant0ProvidersID",
    "Variant1",
    "Variant1Service",
    "Variant1Person",
    "Variant1ProvidersID",
    "Variant2",
    "Variant2ProvidersID",
    "Variant2Person",
    "Variant2Service",
    "Variant3",
    "Variant3ProvidersID",
    "Variant3Person",
    "Variant3Service",
]


class Variant0(TypedDict, total=False):
    payment_method: Required[Annotated[Literal["self-pay", "employer-sponsored"], PropertyInfo(alias="paymentMethod")]]

    person: Required[Variant0Person]

    provider_id: Required[Annotated[str, PropertyInfo(alias="providerId")]]

    services: Required[Iterable[Variant0Service]]

    _id: str

    brand_id: Annotated[str, PropertyInfo(alias="brandId")]

    due_date: Annotated[Union[str, datetime], PropertyInfo(alias="dueDate", format="iso8601")]

    due_dates: Annotated[SequenceNotStr[Union[str, datetime]], PropertyInfo(alias="dueDates", format="iso8601")]

    employee_id: Annotated[str, PropertyInfo(alias="employeeId")]

    employee_ids: Annotated[SequenceNotStr[str], PropertyInfo(alias="employeeIds")]

    employer_id: Annotated[str, PropertyInfo(alias="employerId")]

    metadata: Dict[str, object]
    """Optional arbitrary metadata (<=10KB when JSON stringified)"""

    provider_created: Annotated[bool, PropertyInfo(alias="providerCreated")]

    providers_ids: Annotated[Iterable[Variant0ProvidersID], PropertyInfo(alias="providersIds")]

    quantities: Dict[str, int]

    re_captcha_token: Annotated[str, PropertyInfo(alias="reCaptchaToken")]

    services_ids: Annotated[SequenceNotStr[str], PropertyInfo(alias="servicesIds")]

    token_id: Annotated[str, PropertyInfo(alias="tokenId")]


class Variant0Person(TypedDict, total=False):
    city: Required[str]

    dob: Required[str]
    """Date of birth in YYYY-MM-DD format"""

    email: Required[str]

    first_name: Required[Annotated[str, PropertyInfo(alias="firstName")]]

    last_name: Required[Annotated[str, PropertyInfo(alias="lastName")]]

    phone: Required[str]

    state: Required[str]

    street: Required[str]

    zipcode: Required[str]
    """US ZIP code in 12345 or 12345-6789 format"""

    country: str

    county: str

    street2: str


class Variant0Service(TypedDict, total=False):
    _id: Required[str]

    quantity: Required[int]

    auto_accept: Annotated[bool, PropertyInfo(alias="autoAccept")]


class Variant0ProvidersID(TypedDict, total=False):
    provider_id: Required[Annotated[str, PropertyInfo(alias="providerId")]]

    service_id: Annotated[str, PropertyInfo(alias="serviceId")]


class Variant1(TypedDict, total=False):
    employee_id: Required[Annotated[str, PropertyInfo(alias="employeeId")]]

    employer_id: Required[Annotated[str, PropertyInfo(alias="employerId")]]

    services: Required[Iterable[Variant1Service]]

    _id: str

    brand_id: Annotated[str, PropertyInfo(alias="brandId")]

    due_date: Annotated[Union[str, datetime], PropertyInfo(alias="dueDate", format="iso8601")]

    due_dates: Annotated[SequenceNotStr[Union[str, datetime]], PropertyInfo(alias="dueDates", format="iso8601")]

    employee_ids: Annotated[SequenceNotStr[str], PropertyInfo(alias="employeeIds")]

    metadata: Dict[str, object]
    """Optional arbitrary metadata (<=10KB when JSON stringified)"""

    payment_method: Annotated[Literal["self-pay", "employer-sponsored"], PropertyInfo(alias="paymentMethod")]

    person: Variant1Person

    provider_created: Annotated[bool, PropertyInfo(alias="providerCreated")]

    provider_id: Annotated[str, PropertyInfo(alias="providerId")]

    providers_ids: Annotated[Iterable[Variant1ProvidersID], PropertyInfo(alias="providersIds")]

    quantities: Dict[str, int]

    re_captcha_token: Annotated[str, PropertyInfo(alias="reCaptchaToken")]

    services_ids: Annotated[SequenceNotStr[str], PropertyInfo(alias="servicesIds")]

    token_id: Annotated[str, PropertyInfo(alias="tokenId")]


class Variant1Service(TypedDict, total=False):
    _id: Required[str]

    quantity: Required[int]

    auto_accept: Annotated[bool, PropertyInfo(alias="autoAccept")]


class Variant1Person(TypedDict, total=False):
    city: Required[str]

    dob: Required[str]
    """Date of birth in YYYY-MM-DD format"""

    email: Required[str]

    first_name: Required[Annotated[str, PropertyInfo(alias="firstName")]]

    last_name: Required[Annotated[str, PropertyInfo(alias="lastName")]]

    phone: Required[str]

    state: Required[str]

    street: Required[str]

    zipcode: Required[str]
    """US ZIP code in 12345 or 12345-6789 format"""

    country: str

    county: str

    street2: str


class Variant1ProvidersID(TypedDict, total=False):
    provider_id: Required[Annotated[str, PropertyInfo(alias="providerId")]]

    service_id: Annotated[str, PropertyInfo(alias="serviceId")]


class Variant2(TypedDict, total=False):
    employee_id: Required[Annotated[str, PropertyInfo(alias="employeeId")]]

    employer_id: Required[Annotated[str, PropertyInfo(alias="employerId")]]

    providers_ids: Required[Annotated[Iterable[Variant2ProvidersID], PropertyInfo(alias="providersIds")]]

    services_ids: Required[Annotated[SequenceNotStr[str], PropertyInfo(alias="servicesIds")]]

    _id: str

    brand_id: Annotated[str, PropertyInfo(alias="brandId")]

    due_date: Annotated[Union[str, datetime], PropertyInfo(alias="dueDate", format="iso8601")]

    due_dates: Annotated[SequenceNotStr[Union[str, datetime]], PropertyInfo(alias="dueDates", format="iso8601")]

    employee_ids: Annotated[SequenceNotStr[str], PropertyInfo(alias="employeeIds")]

    metadata: Dict[str, object]
    """Optional arbitrary metadata (<=10KB when JSON stringified)"""

    payment_method: Annotated[Literal["self-pay", "employer-sponsored"], PropertyInfo(alias="paymentMethod")]

    person: Variant2Person

    provider_created: Annotated[bool, PropertyInfo(alias="providerCreated")]

    provider_id: Annotated[str, PropertyInfo(alias="providerId")]

    quantities: Dict[str, int]

    re_captcha_token: Annotated[str, PropertyInfo(alias="reCaptchaToken")]

    services: Iterable[Variant2Service]

    token_id: Annotated[str, PropertyInfo(alias="tokenId")]


class Variant2ProvidersID(TypedDict, total=False):
    provider_id: Required[Annotated[str, PropertyInfo(alias="providerId")]]

    service_id: Annotated[str, PropertyInfo(alias="serviceId")]


class Variant2Person(TypedDict, total=False):
    city: Required[str]

    dob: Required[str]
    """Date of birth in YYYY-MM-DD format"""

    email: Required[str]

    first_name: Required[Annotated[str, PropertyInfo(alias="firstName")]]

    last_name: Required[Annotated[str, PropertyInfo(alias="lastName")]]

    phone: Required[str]

    state: Required[str]

    street: Required[str]

    zipcode: Required[str]
    """US ZIP code in 12345 or 12345-6789 format"""

    country: str

    county: str

    street2: str


class Variant2Service(TypedDict, total=False):
    _id: Required[str]

    quantity: Required[int]

    auto_accept: Annotated[bool, PropertyInfo(alias="autoAccept")]


class Variant3(TypedDict, total=False):
    employee_ids: Required[Annotated[SequenceNotStr[str], PropertyInfo(alias="employeeIds")]]

    employer_id: Required[Annotated[str, PropertyInfo(alias="employerId")]]

    providers_ids: Required[Annotated[Iterable[Variant3ProvidersID], PropertyInfo(alias="providersIds")]]

    services_ids: Required[Annotated[SequenceNotStr[str], PropertyInfo(alias="servicesIds")]]

    _id: str

    brand_id: Annotated[str, PropertyInfo(alias="brandId")]

    due_date: Annotated[Union[str, datetime], PropertyInfo(alias="dueDate", format="iso8601")]

    due_dates: Annotated[SequenceNotStr[Union[str, datetime]], PropertyInfo(alias="dueDates", format="iso8601")]

    employee_id: Annotated[str, PropertyInfo(alias="employeeId")]

    metadata: Dict[str, object]
    """Optional arbitrary metadata (<=10KB when JSON stringified)"""

    payment_method: Annotated[Literal["self-pay", "employer-sponsored"], PropertyInfo(alias="paymentMethod")]

    person: Variant3Person

    provider_created: Annotated[bool, PropertyInfo(alias="providerCreated")]

    provider_id: Annotated[str, PropertyInfo(alias="providerId")]

    quantities: Dict[str, int]

    re_captcha_token: Annotated[str, PropertyInfo(alias="reCaptchaToken")]

    services: Iterable[Variant3Service]

    token_id: Annotated[str, PropertyInfo(alias="tokenId")]


class Variant3ProvidersID(TypedDict, total=False):
    provider_id: Required[Annotated[str, PropertyInfo(alias="providerId")]]

    service_id: Annotated[str, PropertyInfo(alias="serviceId")]


class Variant3Person(TypedDict, total=False):
    city: Required[str]

    dob: Required[str]
    """Date of birth in YYYY-MM-DD format"""

    email: Required[str]

    first_name: Required[Annotated[str, PropertyInfo(alias="firstName")]]

    last_name: Required[Annotated[str, PropertyInfo(alias="lastName")]]

    phone: Required[str]

    state: Required[str]

    street: Required[str]

    zipcode: Required[str]
    """US ZIP code in 12345 or 12345-6789 format"""

    country: str

    county: str

    street2: str


class Variant3Service(TypedDict, total=False):
    _id: Required[str]

    quantity: Required[int]

    auto_accept: Annotated[bool, PropertyInfo(alias="autoAccept")]


OrderCreateParams: TypeAlias = Union[Variant0, Variant1, Variant2, Variant3]
