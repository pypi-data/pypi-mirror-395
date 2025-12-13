# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["LogoutEndpointResponse"]


class LogoutEndpointResponse(BaseModel):
    """Response containing OAuth provider logout endpoint"""

    logout_endpoint: str
