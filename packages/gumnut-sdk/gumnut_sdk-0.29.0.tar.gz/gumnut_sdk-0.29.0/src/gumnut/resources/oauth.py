# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import oauth_auth_url_params, oauth_exchange_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.auth_url_response import AuthURLResponse
from ..types.exchange_response import ExchangeResponse
from ..types.logout_endpoint_response import LogoutEndpointResponse

__all__ = ["OAuthResource", "AsyncOAuthResource"]


class OAuthResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OAuthResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gumnut-ai/photos-sdk-python#accessing-raw-response-data-eg-headers
        """
        return OAuthResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OAuthResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gumnut-ai/photos-sdk-python#with_streaming_response
        """
        return OAuthResourceWithStreamingResponse(self)

    def auth_url(
        self,
        *,
        redirect_uri: str,
        code_challenge: Optional[str] | Omit = omit,
        code_challenge_method: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AuthURLResponse:
        """
        Generate OAuth authorization URL with state and nonce for CSRF and replay attack
        protection. State is stored with TTL for validation.

        Args:
          redirect_uri: The URI to redirect to after OAuth consent. Must match the registered redirect
              URI in OAuth client configuration.

          code_challenge: PKCE code challenge derived from code_verifier. Required for public clients to
              prevent authorization code interception attacks.

          code_challenge_method: PKCE code challenge method, typically 'S256' (SHA-256 hash). Must be provided if
              code_challenge is specified.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/oauth/auth-url",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "redirect_uri": redirect_uri,
                        "code_challenge": code_challenge,
                        "code_challenge_method": code_challenge_method,
                    },
                    oauth_auth_url_params.OAuthAuthURLParams,
                ),
            ),
            cast_to=AuthURLResponse,
        )

    def exchange(
        self,
        *,
        code: Optional[str] | Omit = omit,
        code_verifier: Optional[str] | Omit = omit,
        error: Optional[str] | Omit = omit,
        state: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExchangeResponse:
        """
        Exchange OAuth authorization code for application JWT after validating state,
        nonce, and ID token signature. User is retrieved from or created in the database
        and details added to the JWT.

        Args:
          code: Authorization code returned by the OAuth provider after user consent

          code_verifier: PKCE code verifier that corresponds to the code_challenge sent in the
              authorization request

          error: Error code if OAuth provider returned an error instead of authorization code

          state: State token from the initial auth request, used for CSRF protection

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/oauth/exchange",
            body=maybe_transform(
                {
                    "code": code,
                    "code_verifier": code_verifier,
                    "error": error,
                    "state": state,
                },
                oauth_exchange_params.OAuthExchangeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExchangeResponse,
        )

    def logout_endpoint(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LogoutEndpointResponse:
        """Returns the OAuth provider's logout endpoint URL from OIDC discovery.

        This can
        be used to redirect users to logout from the OAuth provider after logging out
        locally.
        """
        return self._get(
            "/api/oauth/logout-endpoint",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LogoutEndpointResponse,
        )


class AsyncOAuthResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOAuthResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gumnut-ai/photos-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOAuthResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOAuthResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gumnut-ai/photos-sdk-python#with_streaming_response
        """
        return AsyncOAuthResourceWithStreamingResponse(self)

    async def auth_url(
        self,
        *,
        redirect_uri: str,
        code_challenge: Optional[str] | Omit = omit,
        code_challenge_method: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AuthURLResponse:
        """
        Generate OAuth authorization URL with state and nonce for CSRF and replay attack
        protection. State is stored with TTL for validation.

        Args:
          redirect_uri: The URI to redirect to after OAuth consent. Must match the registered redirect
              URI in OAuth client configuration.

          code_challenge: PKCE code challenge derived from code_verifier. Required for public clients to
              prevent authorization code interception attacks.

          code_challenge_method: PKCE code challenge method, typically 'S256' (SHA-256 hash). Must be provided if
              code_challenge is specified.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/oauth/auth-url",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "redirect_uri": redirect_uri,
                        "code_challenge": code_challenge,
                        "code_challenge_method": code_challenge_method,
                    },
                    oauth_auth_url_params.OAuthAuthURLParams,
                ),
            ),
            cast_to=AuthURLResponse,
        )

    async def exchange(
        self,
        *,
        code: Optional[str] | Omit = omit,
        code_verifier: Optional[str] | Omit = omit,
        error: Optional[str] | Omit = omit,
        state: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExchangeResponse:
        """
        Exchange OAuth authorization code for application JWT after validating state,
        nonce, and ID token signature. User is retrieved from or created in the database
        and details added to the JWT.

        Args:
          code: Authorization code returned by the OAuth provider after user consent

          code_verifier: PKCE code verifier that corresponds to the code_challenge sent in the
              authorization request

          error: Error code if OAuth provider returned an error instead of authorization code

          state: State token from the initial auth request, used for CSRF protection

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/oauth/exchange",
            body=await async_maybe_transform(
                {
                    "code": code,
                    "code_verifier": code_verifier,
                    "error": error,
                    "state": state,
                },
                oauth_exchange_params.OAuthExchangeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExchangeResponse,
        )

    async def logout_endpoint(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LogoutEndpointResponse:
        """Returns the OAuth provider's logout endpoint URL from OIDC discovery.

        This can
        be used to redirect users to logout from the OAuth provider after logging out
        locally.
        """
        return await self._get(
            "/api/oauth/logout-endpoint",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LogoutEndpointResponse,
        )


class OAuthResourceWithRawResponse:
    def __init__(self, oauth: OAuthResource) -> None:
        self._oauth = oauth

        self.auth_url = to_raw_response_wrapper(
            oauth.auth_url,
        )
        self.exchange = to_raw_response_wrapper(
            oauth.exchange,
        )
        self.logout_endpoint = to_raw_response_wrapper(
            oauth.logout_endpoint,
        )


class AsyncOAuthResourceWithRawResponse:
    def __init__(self, oauth: AsyncOAuthResource) -> None:
        self._oauth = oauth

        self.auth_url = async_to_raw_response_wrapper(
            oauth.auth_url,
        )
        self.exchange = async_to_raw_response_wrapper(
            oauth.exchange,
        )
        self.logout_endpoint = async_to_raw_response_wrapper(
            oauth.logout_endpoint,
        )


class OAuthResourceWithStreamingResponse:
    def __init__(self, oauth: OAuthResource) -> None:
        self._oauth = oauth

        self.auth_url = to_streamed_response_wrapper(
            oauth.auth_url,
        )
        self.exchange = to_streamed_response_wrapper(
            oauth.exchange,
        )
        self.logout_endpoint = to_streamed_response_wrapper(
            oauth.logout_endpoint,
        )


class AsyncOAuthResourceWithStreamingResponse:
    def __init__(self, oauth: AsyncOAuthResource) -> None:
        self._oauth = oauth

        self.auth_url = async_to_streamed_response_wrapper(
            oauth.auth_url,
        )
        self.exchange = async_to_streamed_response_wrapper(
            oauth.exchange,
        )
        self.logout_endpoint = async_to_streamed_response_wrapper(
            oauth.logout_endpoint,
        )
