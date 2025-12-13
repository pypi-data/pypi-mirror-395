# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["UserResponse"]


class UserResponse(BaseModel):
    """Represents a user account with profile information."""

    id: str
    """Unique user identifier with 'intuser\\__' prefix"""

    created_at: datetime
    """When this user account was created"""

    is_active: bool
    """Whether this user account is currently active"""

    is_superuser: bool
    """Whether this user has superuser/admin privileges"""

    is_verified: bool
    """Whether this user's email is verified"""

    updated_at: datetime
    """When this user account was last updated"""

    email: Optional[str] = None
    """User's email address"""

    first_name: Optional[str] = None
    """User's first name"""

    last_name: Optional[str] = None
    """User's last name"""
