# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from tests.utils import assert_matches_type
from fleet.types.sessions import StartNewResponse, StartExistingResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStart:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_existing(self, client: Fleet) -> None:
        start = client.sessions.start.existing(
            session_id="session_id",
        )
        assert_matches_type(StartExistingResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_existing_with_all_params(self, client: Fleet) -> None:
        start = client.sessions.start.existing(
            session_id="session_id",
            url="url",
        )
        assert_matches_type(StartExistingResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_existing(self, client: Fleet) -> None:
        response = client.sessions.start.with_raw_response.existing(
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        start = response.parse()
        assert_matches_type(StartExistingResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_existing(self, client: Fleet) -> None:
        with client.sessions.start.with_streaming_response.existing(
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            start = response.parse()
            assert_matches_type(StartExistingResponse, start, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_existing(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.start.with_raw_response.existing(
                session_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_new(self, client: Fleet) -> None:
        start = client.sessions.start.new(
            browser_configuration={},
        )
        assert_matches_type(StartNewResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_new_with_all_params(self, client: Fleet) -> None:
        start = client.sessions.start.new(
            browser_configuration={
                "camo": True,
                "headless": True,
                "stealth": True,
                "track_all_responses": True,
                "wait_until": "wait_until",
            },
            url="url",
            agentic=True,
            enable_xvfb=True,
            n_responses_to_track=0,
            proxy_password="proxy_password",
            proxy_url="proxy_url",
            proxy_username="proxy_username",
            vnc_password="vnc_password",
        )
        assert_matches_type(StartNewResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_new(self, client: Fleet) -> None:
        response = client.sessions.start.with_raw_response.new(
            browser_configuration={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        start = response.parse()
        assert_matches_type(StartNewResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_new(self, client: Fleet) -> None:
        with client.sessions.start.with_streaming_response.new(
            browser_configuration={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            start = response.parse()
            assert_matches_type(StartNewResponse, start, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncStart:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_existing(self, async_client: AsyncFleet) -> None:
        start = await async_client.sessions.start.existing(
            session_id="session_id",
        )
        assert_matches_type(StartExistingResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_existing_with_all_params(self, async_client: AsyncFleet) -> None:
        start = await async_client.sessions.start.existing(
            session_id="session_id",
            url="url",
        )
        assert_matches_type(StartExistingResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_existing(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.start.with_raw_response.existing(
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        start = await response.parse()
        assert_matches_type(StartExistingResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_existing(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.start.with_streaming_response.existing(
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            start = await response.parse()
            assert_matches_type(StartExistingResponse, start, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_existing(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.start.with_raw_response.existing(
                session_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_new(self, async_client: AsyncFleet) -> None:
        start = await async_client.sessions.start.new(
            browser_configuration={},
        )
        assert_matches_type(StartNewResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_new_with_all_params(self, async_client: AsyncFleet) -> None:
        start = await async_client.sessions.start.new(
            browser_configuration={
                "camo": True,
                "headless": True,
                "stealth": True,
                "track_all_responses": True,
                "wait_until": "wait_until",
            },
            url="url",
            agentic=True,
            enable_xvfb=True,
            n_responses_to_track=0,
            proxy_password="proxy_password",
            proxy_url="proxy_url",
            proxy_username="proxy_username",
            vnc_password="vnc_password",
        )
        assert_matches_type(StartNewResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_new(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.start.with_raw_response.new(
            browser_configuration={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        start = await response.parse()
        assert_matches_type(StartNewResponse, start, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_new(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.start.with_streaming_response.new(
            browser_configuration={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            start = await response.parse()
            assert_matches_type(StartNewResponse, start, path=["response"])

        assert cast(Any, response.is_closed) is True
