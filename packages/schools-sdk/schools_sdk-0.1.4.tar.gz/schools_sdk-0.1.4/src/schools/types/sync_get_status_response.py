# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SyncGetStatusResponse"]


class SyncGetStatusResponse(BaseModel):
    is_stale: Optional[bool] = FieldInfo(alias="isStale", default=None)

    last_sync: Optional[datetime] = FieldInfo(alias="lastSync", default=None)

    record_count: Optional[int] = FieldInfo(alias="recordCount", default=None)
