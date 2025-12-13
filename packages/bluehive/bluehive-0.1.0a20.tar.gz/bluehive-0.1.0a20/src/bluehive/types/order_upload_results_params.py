# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["OrderUploadResultsParams", "File"]


class OrderUploadResultsParams(TypedDict, total=False):
    captcha_token: Required[Annotated[str, PropertyInfo(alias="captchaToken")]]

    order_access_code: Required[Annotated[str, PropertyInfo(alias="orderAccessCode")]]

    service_id: Required[Annotated[str, PropertyInfo(alias="serviceId")]]

    dob: str
    """Date of birth in YYYY-MM-DD format"""

    file_ids: Annotated[SequenceNotStr[str], PropertyInfo(alias="fileIds")]

    files: Iterable[File]

    last_name: Annotated[str, PropertyInfo(alias="lastName")]


class File(TypedDict, total=False):
    base64: Required[str]

    name: Required[str]

    type: Required[str]
