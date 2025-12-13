# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["ServiceBundleCreateParams"]


class ServiceBundleCreateParams(TypedDict, total=False):
    bundle_name: Required[Annotated[str, PropertyInfo(alias="bundleName")]]

    service_ids: Required[Annotated[SequenceNotStr[str], PropertyInfo(alias="serviceIds")]]

    _id: str

    limit: float

    occurrence: str

    recurring: bool

    roles: Optional[SequenceNotStr[str]]

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
