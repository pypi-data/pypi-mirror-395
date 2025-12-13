# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["OAuthExchangeParams"]


class OAuthExchangeParams(TypedDict, total=False):
    code: Optional[str]
    """Authorization code returned by the OAuth provider after user consent"""

    code_verifier: Optional[str]
    """
    PKCE code verifier that corresponds to the code_challenge sent in the
    authorization request
    """

    error: Optional[str]
    """Error code if OAuth provider returned an error instead of authorization code"""

    state: Optional[str]
    """State token from the initial auth request, used for CSRF protection"""
