# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["OrderSendForEmployeeParams", "ProvidersID"]


class OrderSendForEmployeeParams(TypedDict, total=False):
    employee_id: Required[Annotated[str, PropertyInfo(alias="employeeId")]]
    """Employee ID to send order to"""

    employer_id: Required[Annotated[str, PropertyInfo(alias="employerId")]]
    """Employer ID sending the order"""

    providers_ids: Required[Annotated[Iterable[ProvidersID], PropertyInfo(alias="providersIds")]]
    """Array mapping each service (by index) to a provider; serviceId optional"""

    services_ids: Required[Annotated[SequenceNotStr[str], PropertyInfo(alias="servicesIds")]]
    """Array of service IDs to include in the order"""

    login_token: Required[Annotated[str, PropertyInfo(alias="login-token")]]

    user_id: Required[Annotated[str, PropertyInfo(alias="user-id")]]

    brand_id: Annotated[str, PropertyInfo(alias="brandId")]
    """Brand ID for branded orders"""

    due_date: Annotated[str, PropertyInfo(alias="dueDate")]
    """Due date for the order (date or date-time ISO string)"""

    due_dates: Annotated[SequenceNotStr[str], PropertyInfo(alias="dueDates")]
    """Array of due dates per service"""

    metadata: Dict[str, object]
    """
    Optional arbitrary metadata to store on the order (non-indexed passthrough,
    <=10KB when JSON stringified)
    """

    provider_created: Annotated[bool, PropertyInfo(alias="providerCreated")]
    """Whether this order is being created by a provider (affects permission checking)"""

    provider_id: Annotated[str, PropertyInfo(alias="providerId")]
    """Single provider ID (shortcut when all services map to one provider)"""

    quantities: Dict[str, int]
    """Service ID to quantity mapping"""


class ProvidersID(TypedDict, total=False):
    provider_id: Required[Annotated[str, PropertyInfo(alias="providerId")]]

    service_id: Annotated[str, PropertyInfo(alias="serviceId")]
