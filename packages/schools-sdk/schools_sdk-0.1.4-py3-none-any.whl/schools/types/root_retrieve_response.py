# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["RootRetrieveResponse"]


class RootRetrieveResponse(BaseModel):
    docs: Optional[str] = None

    endpoints: Optional[object] = None

    message: Optional[str] = None

    version: Optional[str] = None
