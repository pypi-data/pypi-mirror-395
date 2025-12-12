# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SchoolSearchParams"]


class SchoolSearchParams(TypedDict, total=False):
    q: Required[str]
    """Search query"""

    limit: int
    """Results per page (default: 20, max: 100)"""

    page: int
    """Page number (default: 1)"""
