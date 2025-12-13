# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDiscovery:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_trigger(self, client: Fleet) -> None:
        discovery = client.vnc.discovery.trigger()
        assert_matches_type(object, discovery, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_trigger(self, client: Fleet) -> None:
        response = client.vnc.discovery.with_raw_response.trigger()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        discovery = response.parse()
        assert_matches_type(object, discovery, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_trigger(self, client: Fleet) -> None:
        with client.vnc.discovery.with_streaming_response.trigger() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            discovery = response.parse()
            assert_matches_type(object, discovery, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDiscovery:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_trigger(self, async_client: AsyncFleet) -> None:
        discovery = await async_client.vnc.discovery.trigger()
        assert_matches_type(object, discovery, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_trigger(self, async_client: AsyncFleet) -> None:
        response = await async_client.vnc.discovery.with_raw_response.trigger()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        discovery = await response.parse()
        assert_matches_type(object, discovery, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_trigger(self, async_client: AsyncFleet) -> None:
        async with async_client.vnc.discovery.with_streaming_response.trigger() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            discovery = await response.parse()
            assert_matches_type(object, discovery, path=["response"])

        assert cast(Any, response.is_closed) is True
