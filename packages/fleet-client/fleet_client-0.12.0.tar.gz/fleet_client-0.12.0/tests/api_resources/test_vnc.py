# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVnc:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_check_health(self, client: Fleet) -> None:
        vnc = client.vnc.check_health()
        assert_matches_type(object, vnc, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_check_health(self, client: Fleet) -> None:
        response = client.vnc.with_raw_response.check_health()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vnc = response.parse()
        assert_matches_type(object, vnc, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_check_health(self, client: Fleet) -> None:
        with client.vnc.with_streaming_response.check_health() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vnc = response.parse()
            assert_matches_type(object, vnc, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncVnc:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_check_health(self, async_client: AsyncFleet) -> None:
        vnc = await async_client.vnc.check_health()
        assert_matches_type(object, vnc, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_check_health(self, async_client: AsyncFleet) -> None:
        response = await async_client.vnc.with_raw_response.check_health()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vnc = await response.parse()
        assert_matches_type(object, vnc, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_check_health(self, async_client: AsyncFleet) -> None:
        async with async_client.vnc.with_streaming_response.check_health() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vnc = await response.parse()
            assert_matches_type(object, vnc, path=["response"])

        assert cast(Any, response.is_closed) is True
