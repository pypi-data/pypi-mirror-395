# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from tests.utils import assert_matches_type
from fleet.types.sessions import PageGetResponse, PageGetFullResponse, PageGetTextResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPage:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get(self, client: Fleet) -> None:
        page = client.sessions.page.get(
            "session_id",
        )
        assert_matches_type(PageGetResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get(self, client: Fleet) -> None:
        response = client.sessions.page.with_raw_response.get(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        page = response.parse()
        assert_matches_type(PageGetResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get(self, client: Fleet) -> None:
        with client.sessions.page.with_streaming_response.get(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            page = response.parse()
            assert_matches_type(PageGetResponse, page, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.page.with_raw_response.get(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_full(self, client: Fleet) -> None:
        page = client.sessions.page.get_full(
            "session_id",
        )
        assert_matches_type(PageGetFullResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_full(self, client: Fleet) -> None:
        response = client.sessions.page.with_raw_response.get_full(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        page = response.parse()
        assert_matches_type(PageGetFullResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_full(self, client: Fleet) -> None:
        with client.sessions.page.with_streaming_response.get_full(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            page = response.parse()
            assert_matches_type(PageGetFullResponse, page, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_full(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.page.with_raw_response.get_full(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_text(self, client: Fleet) -> None:
        page = client.sessions.page.get_text(
            "session_id",
        )
        assert_matches_type(PageGetTextResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_text(self, client: Fleet) -> None:
        response = client.sessions.page.with_raw_response.get_text(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        page = response.parse()
        assert_matches_type(PageGetTextResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_text(self, client: Fleet) -> None:
        with client.sessions.page.with_streaming_response.get_text(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            page = response.parse()
            assert_matches_type(PageGetTextResponse, page, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_text(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.page.with_raw_response.get_text(
                "",
            )


class TestAsyncPage:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get(self, async_client: AsyncFleet) -> None:
        page = await async_client.sessions.page.get(
            "session_id",
        )
        assert_matches_type(PageGetResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.page.with_raw_response.get(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        page = await response.parse()
        assert_matches_type(PageGetResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.page.with_streaming_response.get(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            page = await response.parse()
            assert_matches_type(PageGetResponse, page, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.page.with_raw_response.get(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_full(self, async_client: AsyncFleet) -> None:
        page = await async_client.sessions.page.get_full(
            "session_id",
        )
        assert_matches_type(PageGetFullResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_full(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.page.with_raw_response.get_full(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        page = await response.parse()
        assert_matches_type(PageGetFullResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_full(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.page.with_streaming_response.get_full(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            page = await response.parse()
            assert_matches_type(PageGetFullResponse, page, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_full(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.page.with_raw_response.get_full(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_text(self, async_client: AsyncFleet) -> None:
        page = await async_client.sessions.page.get_text(
            "session_id",
        )
        assert_matches_type(PageGetTextResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_text(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.page.with_raw_response.get_text(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        page = await response.parse()
        assert_matches_type(PageGetTextResponse, page, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_text(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.page.with_streaming_response.get_text(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            page = await response.parse()
            assert_matches_type(PageGetTextResponse, page, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_text(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.page.with_raw_response.get_text(
                "",
            )
