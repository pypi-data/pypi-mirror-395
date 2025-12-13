# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["ServiceBundleListResponse", "ServiceBundleListResponseItem"]


class ServiceBundleListResponseItem(BaseModel):
    api_id: str = FieldInfo(alias="_id")

    bundle_name: str = FieldInfo(alias="bundleName")

    employer_id: str = FieldInfo(alias="employerId")

    service_ids: List[str] = FieldInfo(alias="serviceIds")

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)

    limit: Optional[float] = None

    occurrence: Optional[str] = None

    recurring: Optional[bool] = None

    roles: Optional[List[str]] = None

    start_date: Optional[str] = FieldInfo(alias="startDate", default=None)

    updated_at: Optional[str] = FieldInfo(alias="updatedAt", default=None)

    updated_by: Optional[str] = FieldInfo(alias="updatedBy", default=None)


ServiceBundleListResponse: TypeAlias = List[ServiceBundleListResponseItem]
