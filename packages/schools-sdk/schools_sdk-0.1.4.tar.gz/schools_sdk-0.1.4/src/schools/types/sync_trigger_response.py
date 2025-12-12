# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SyncTriggerResponse"]


class SyncTriggerResponse(BaseModel):
    error: Optional[str] = None

    last_sync: Optional[datetime] = FieldInfo(alias="lastSync", default=None)

    record_count: Optional[int] = FieldInfo(alias="recordCount", default=None)

    success: Optional[bool] = None
