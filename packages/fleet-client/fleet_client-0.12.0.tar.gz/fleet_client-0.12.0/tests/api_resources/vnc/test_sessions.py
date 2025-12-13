# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from tests.utils import assert_matches_type
from fleet.types.vnc import VncSession, SessionListResponse, SessionRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSessions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Fleet) -> None:
        session = client.vnc.sessions.retrieve(
            "browser_id",
        )
        assert_matches_type(SessionRetrieveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Fleet) -> None:
        response = client.vnc.sessions.with_raw_response.retrieve(
            "browser_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionRetrieveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Fleet) -> None:
        with client.vnc.sessions.with_streaming_response.retrieve(
            "browser_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionRetrieveResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `browser_id` but received ''"):
            client.vnc.sessions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Fleet) -> None:
        session = client.vnc.sessions.list()
        assert_matches_type(SessionListResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Fleet) -> None:
        session = client.vnc.sessions.list(
            active_only=True,
        )
        assert_matches_type(SessionListResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Fleet) -> None:
        response = client.vnc.sessions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionListResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Fleet) -> None:
        with client.vnc.sessions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionListResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_raw(self, client: Fleet) -> None:
        session = client.vnc.sessions.retrieve_raw(
            "browser_id",
        )
        assert_matches_type(VncSession, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve_raw(self, client: Fleet) -> None:
        response = client.vnc.sessions.with_raw_response.retrieve_raw(
            "browser_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(VncSession, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_raw(self, client: Fleet) -> None:
        with client.vnc.sessions.with_streaming_response.retrieve_raw(
            "browser_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(VncSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve_raw(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `browser_id` but received ''"):
            client.vnc.sessions.with_raw_response.retrieve_raw(
                "",
            )


class TestAsyncSessions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFleet) -> None:
        session = await async_client.vnc.sessions.retrieve(
            "browser_id",
        )
        assert_matches_type(SessionRetrieveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFleet) -> None:
        response = await async_client.vnc.sessions.with_raw_response.retrieve(
            "browser_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionRetrieveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFleet) -> None:
        async with async_client.vnc.sessions.with_streaming_response.retrieve(
            "browser_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionRetrieveResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `browser_id` but received ''"):
            await async_client.vnc.sessions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncFleet) -> None:
        session = await async_client.vnc.sessions.list()
        assert_matches_type(SessionListResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncFleet) -> None:
        session = await async_client.vnc.sessions.list(
            active_only=True,
        )
        assert_matches_type(SessionListResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFleet) -> None:
        response = await async_client.vnc.sessions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionListResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFleet) -> None:
        async with async_client.vnc.sessions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionListResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_raw(self, async_client: AsyncFleet) -> None:
        session = await async_client.vnc.sessions.retrieve_raw(
            "browser_id",
        )
        assert_matches_type(VncSession, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_raw(self, async_client: AsyncFleet) -> None:
        response = await async_client.vnc.sessions.with_raw_response.retrieve_raw(
            "browser_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(VncSession, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_raw(self, async_client: AsyncFleet) -> None:
        async with async_client.vnc.sessions.with_streaming_response.retrieve_raw(
            "browser_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(VncSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve_raw(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `browser_id` but received ''"):
            await async_client.vnc.sessions.with_raw_response.retrieve_raw(
                "",
            )
