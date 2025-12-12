# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["OAuthAuthURLParams"]


class OAuthAuthURLParams(TypedDict, total=False):
    redirect_uri: Required[str]
    """The URI to redirect to after OAuth consent.

    Must match the registered redirect URI in OAuth client configuration.
    """

    code_challenge: Optional[str]
    """PKCE code challenge derived from code_verifier.

    Required for public clients to prevent authorization code interception attacks.
    """

    code_challenge_method: Optional[str]
    """PKCE code challenge method, typically 'S256' (SHA-256 hash).

    Must be provided if code_challenge is specified.
    """
