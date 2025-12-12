# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gumnut import Gumnut, AsyncGumnut
from tests.utils import assert_matches_type
from gumnut.types import (
    AuthURLResponse,
    ExchangeResponse,
    LogoutEndpointResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOAuth:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_auth_url(self, client: Gumnut) -> None:
        oauth = client.oauth.auth_url(
            redirect_uri="redirect_uri",
        )
        assert_matches_type(AuthURLResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_auth_url_with_all_params(self, client: Gumnut) -> None:
        oauth = client.oauth.auth_url(
            redirect_uri="redirect_uri",
            code_challenge="code_challenge",
            code_challenge_method="code_challenge_method",
        )
        assert_matches_type(AuthURLResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_auth_url(self, client: Gumnut) -> None:
        response = client.oauth.with_raw_response.auth_url(
            redirect_uri="redirect_uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = response.parse()
        assert_matches_type(AuthURLResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_auth_url(self, client: Gumnut) -> None:
        with client.oauth.with_streaming_response.auth_url(
            redirect_uri="redirect_uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = response.parse()
            assert_matches_type(AuthURLResponse, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_exchange(self, client: Gumnut) -> None:
        oauth = client.oauth.exchange()
        assert_matches_type(ExchangeResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_exchange_with_all_params(self, client: Gumnut) -> None:
        oauth = client.oauth.exchange(
            code="code",
            code_verifier="code_verifier",
            error="error",
            state="state",
        )
        assert_matches_type(ExchangeResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_exchange(self, client: Gumnut) -> None:
        response = client.oauth.with_raw_response.exchange()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = response.parse()
        assert_matches_type(ExchangeResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_exchange(self, client: Gumnut) -> None:
        with client.oauth.with_streaming_response.exchange() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = response.parse()
            assert_matches_type(ExchangeResponse, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_logout_endpoint(self, client: Gumnut) -> None:
        oauth = client.oauth.logout_endpoint()
        assert_matches_type(LogoutEndpointResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_logout_endpoint(self, client: Gumnut) -> None:
        response = client.oauth.with_raw_response.logout_endpoint()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = response.parse()
        assert_matches_type(LogoutEndpointResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_logout_endpoint(self, client: Gumnut) -> None:
        with client.oauth.with_streaming_response.logout_endpoint() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = response.parse()
            assert_matches_type(LogoutEndpointResponse, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOAuth:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_auth_url(self, async_client: AsyncGumnut) -> None:
        oauth = await async_client.oauth.auth_url(
            redirect_uri="redirect_uri",
        )
        assert_matches_type(AuthURLResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_auth_url_with_all_params(self, async_client: AsyncGumnut) -> None:
        oauth = await async_client.oauth.auth_url(
            redirect_uri="redirect_uri",
            code_challenge="code_challenge",
            code_challenge_method="code_challenge_method",
        )
        assert_matches_type(AuthURLResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_auth_url(self, async_client: AsyncGumnut) -> None:
        response = await async_client.oauth.with_raw_response.auth_url(
            redirect_uri="redirect_uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = await response.parse()
        assert_matches_type(AuthURLResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_auth_url(self, async_client: AsyncGumnut) -> None:
        async with async_client.oauth.with_streaming_response.auth_url(
            redirect_uri="redirect_uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = await response.parse()
            assert_matches_type(AuthURLResponse, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_exchange(self, async_client: AsyncGumnut) -> None:
        oauth = await async_client.oauth.exchange()
        assert_matches_type(ExchangeResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_exchange_with_all_params(self, async_client: AsyncGumnut) -> None:
        oauth = await async_client.oauth.exchange(
            code="code",
            code_verifier="code_verifier",
            error="error",
            state="state",
        )
        assert_matches_type(ExchangeResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_exchange(self, async_client: AsyncGumnut) -> None:
        response = await async_client.oauth.with_raw_response.exchange()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = await response.parse()
        assert_matches_type(ExchangeResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_exchange(self, async_client: AsyncGumnut) -> None:
        async with async_client.oauth.with_streaming_response.exchange() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = await response.parse()
            assert_matches_type(ExchangeResponse, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_logout_endpoint(self, async_client: AsyncGumnut) -> None:
        oauth = await async_client.oauth.logout_endpoint()
        assert_matches_type(LogoutEndpointResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_logout_endpoint(self, async_client: AsyncGumnut) -> None:
        response = await async_client.oauth.with_raw_response.logout_endpoint()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = await response.parse()
        assert_matches_type(LogoutEndpointResponse, oauth, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_logout_endpoint(self, async_client: AsyncGumnut) -> None:
        async with async_client.oauth.with_streaming_response.logout_endpoint() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = await response.parse()
            assert_matches_type(LogoutEndpointResponse, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True
