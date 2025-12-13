# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from fleet.types import (
    SessionListResponse,
    SessionCreateResponse,
    SessionDeleteResponse,
    SessionWarmUpResponse,
    SessionRetrieveResponse,
    SessionVisitPageResponse,
)
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSessions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Fleet) -> None:
        session = client.sessions.create(
            browser_configuration={},
        )
        assert_matches_type(SessionCreateResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Fleet) -> None:
        session = client.sessions.create(
            browser_configuration={
                "camo": True,
                "headless": True,
                "stealth": True,
                "track_all_responses": True,
                "wait_until": "wait_until",
            },
            agentic=True,
            enable_xvfb=True,
            n_responses_to_track=0,
            proxy_password="proxy_password",
            proxy_url="proxy_url",
            proxy_username="proxy_username",
            vnc_password="vnc_password",
        )
        assert_matches_type(SessionCreateResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Fleet) -> None:
        response = client.sessions.with_raw_response.create(
            browser_configuration={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionCreateResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Fleet) -> None:
        with client.sessions.with_streaming_response.create(
            browser_configuration={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionCreateResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Fleet) -> None:
        session = client.sessions.retrieve(
            "session_id",
        )
        assert_matches_type(SessionRetrieveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Fleet) -> None:
        response = client.sessions.with_raw_response.retrieve(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionRetrieveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Fleet) -> None:
        with client.sessions.with_streaming_response.retrieve(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionRetrieveResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Fleet) -> None:
        session = client.sessions.list()
        assert_matches_type(SessionListResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Fleet) -> None:
        response = client.sessions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionListResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Fleet) -> None:
        with client.sessions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionListResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: Fleet) -> None:
        session = client.sessions.delete(
            "session_id",
        )
        assert_matches_type(SessionDeleteResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Fleet) -> None:
        response = client.sessions.with_raw_response.delete(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionDeleteResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Fleet) -> None:
        with client.sessions.with_streaming_response.delete(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionDeleteResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_visit_page(self, client: Fleet) -> None:
        session = client.sessions.visit_page(
            session_id="session_id",
            url="url",
        )
        assert_matches_type(SessionVisitPageResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_visit_page_with_all_params(self, client: Fleet) -> None:
        session = client.sessions.visit_page(
            session_id="session_id",
            url="url",
            wait_until="load",
        )
        assert_matches_type(SessionVisitPageResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_visit_page(self, client: Fleet) -> None:
        response = client.sessions.with_raw_response.visit_page(
            session_id="session_id",
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionVisitPageResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_visit_page(self, client: Fleet) -> None:
        with client.sessions.with_streaming_response.visit_page(
            session_id="session_id",
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionVisitPageResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_visit_page(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.visit_page(
                session_id="",
                url="url",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_warm_up(self, client: Fleet) -> None:
        session = client.sessions.warm_up()
        assert_matches_type(SessionWarmUpResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_warm_up(self, client: Fleet) -> None:
        response = client.sessions.with_raw_response.warm_up()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionWarmUpResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_warm_up(self, client: Fleet) -> None:
        with client.sessions.with_streaming_response.warm_up() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionWarmUpResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSessions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncFleet) -> None:
        session = await async_client.sessions.create(
            browser_configuration={},
        )
        assert_matches_type(SessionCreateResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncFleet) -> None:
        session = await async_client.sessions.create(
            browser_configuration={
                "camo": True,
                "headless": True,
                "stealth": True,
                "track_all_responses": True,
                "wait_until": "wait_until",
            },
            agentic=True,
            enable_xvfb=True,
            n_responses_to_track=0,
            proxy_password="proxy_password",
            proxy_url="proxy_url",
            proxy_username="proxy_username",
            vnc_password="vnc_password",
        )
        assert_matches_type(SessionCreateResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.with_raw_response.create(
            browser_configuration={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionCreateResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.with_streaming_response.create(
            browser_configuration={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionCreateResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFleet) -> None:
        session = await async_client.sessions.retrieve(
            "session_id",
        )
        assert_matches_type(SessionRetrieveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.with_raw_response.retrieve(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionRetrieveResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.with_streaming_response.retrieve(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionRetrieveResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncFleet) -> None:
        session = await async_client.sessions.list()
        assert_matches_type(SessionListResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionListResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionListResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncFleet) -> None:
        session = await async_client.sessions.delete(
            "session_id",
        )
        assert_matches_type(SessionDeleteResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.with_raw_response.delete(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionDeleteResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.with_streaming_response.delete(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionDeleteResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_visit_page(self, async_client: AsyncFleet) -> None:
        session = await async_client.sessions.visit_page(
            session_id="session_id",
            url="url",
        )
        assert_matches_type(SessionVisitPageResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_visit_page_with_all_params(self, async_client: AsyncFleet) -> None:
        session = await async_client.sessions.visit_page(
            session_id="session_id",
            url="url",
            wait_until="load",
        )
        assert_matches_type(SessionVisitPageResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_visit_page(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.with_raw_response.visit_page(
            session_id="session_id",
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionVisitPageResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_visit_page(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.with_streaming_response.visit_page(
            session_id="session_id",
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionVisitPageResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_visit_page(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.visit_page(
                session_id="",
                url="url",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_warm_up(self, async_client: AsyncFleet) -> None:
        session = await async_client.sessions.warm_up()
        assert_matches_type(SessionWarmUpResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_warm_up(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.with_raw_response.warm_up()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionWarmUpResponse, session, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_warm_up(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.with_streaming_response.warm_up() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionWarmUpResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True
