# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ExchangeResponse", "User"]


class User(BaseModel):
    """User information in token exchange response"""

    id: str

    clerk_user_id: Optional[str] = None

    email: Optional[str] = None

    first_name: Optional[str] = None

    is_active: bool

    is_verified: bool

    last_name: Optional[str] = None


class ExchangeResponse(BaseModel):
    """Response containing JWT and user info"""

    access_token: str

    user: User
    """User information in token exchange response"""
