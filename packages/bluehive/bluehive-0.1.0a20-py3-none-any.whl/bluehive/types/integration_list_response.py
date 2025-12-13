# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["IntegrationListResponse", "Integrations"]


class Integrations(BaseModel):
    active: bool

    display_name: str = FieldInfo(alias="displayName")

    config: Optional[Dict[str, object]] = None


class IntegrationListResponse(BaseModel):
    integrations: Dict[str, Integrations]
