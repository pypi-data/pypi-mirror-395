# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["UsageRetrieveResponse", "Purchase", "Usage"]


class Purchase(BaseModel):
    id: str
    """Unique identifier for the purchase"""

    credits: int
    """Number of credits purchased"""

    purchased_at: str
    """When the purchase was made (ISO 8601 format)"""


class Usage(BaseModel):
    id: str
    """Unique identifier for the usage"""

    created_at: str
    """When the usage was recorded (ISO 8601 format)"""

    credit_used: int
    """Number of credits consumed"""

    research_id: Optional[str] = None
    """Research ID that consumed the credits"""


class UsageRetrieveResponse(BaseModel):
    balance_credits: int
    """
    Current credit balance (can be negative if credits consumed without sufficient
    balance)
    """

    has_credits: bool
    """Whether the user has credits available (balance > 0)"""

    purchases: List[Purchase]
    """List of credit purchases, most recent first"""

    usage: List[Usage]
    """List of credit usage records, most recent first"""
