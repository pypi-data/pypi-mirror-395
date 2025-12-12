# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SchoolListParams"]


class SchoolListParams(TypedDict, total=False):
    authority: str
    """Filter by education authority"""

    city: str
    """Filter by city (partial match)"""

    limit: int
    """Results per page (default: 20, max: 100)"""

    name: str
    """Filter by school name (partial match)"""

    org_type: str
    """Filter by organization type"""

    page: int
    """Page number (default: 1)"""

    status: str
    """Filter by school status"""

    suburb: str
    """Filter by suburb (partial match)"""
