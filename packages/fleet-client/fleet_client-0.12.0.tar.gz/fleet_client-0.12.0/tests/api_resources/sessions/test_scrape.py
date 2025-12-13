# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from tests.utils import assert_matches_type
from fleet.types.sessions import (
    ScrapeCleanupJobsResponse,
    ScrapeGetBrowserStatsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestScrape:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_cleanup_jobs(self, client: Fleet) -> None:
        scrape = client.sessions.scrape.cleanup_jobs(
            session_id="session_id",
        )
        assert_matches_type(ScrapeCleanupJobsResponse, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_cleanup_jobs_with_all_params(self, client: Fleet) -> None:
        scrape = client.sessions.scrape.cleanup_jobs(
            session_id="session_id",
            max_age_hours=0,
        )
        assert_matches_type(ScrapeCleanupJobsResponse, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_cleanup_jobs(self, client: Fleet) -> None:
        response = client.sessions.scrape.with_raw_response.cleanup_jobs(
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scrape = response.parse()
        assert_matches_type(ScrapeCleanupJobsResponse, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_cleanup_jobs(self, client: Fleet) -> None:
        with client.sessions.scrape.with_streaming_response.cleanup_jobs(
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scrape = response.parse()
            assert_matches_type(ScrapeCleanupJobsResponse, scrape, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_cleanup_jobs(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.scrape.with_raw_response.cleanup_jobs(
                session_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_browser_stats(self, client: Fleet) -> None:
        scrape = client.sessions.scrape.get_browser_stats(
            "session_id",
        )
        assert_matches_type(ScrapeGetBrowserStatsResponse, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_browser_stats(self, client: Fleet) -> None:
        response = client.sessions.scrape.with_raw_response.get_browser_stats(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scrape = response.parse()
        assert_matches_type(ScrapeGetBrowserStatsResponse, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_browser_stats(self, client: Fleet) -> None:
        with client.sessions.scrape.with_streaming_response.get_browser_stats(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scrape = response.parse()
            assert_matches_type(ScrapeGetBrowserStatsResponse, scrape, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_browser_stats(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.scrape.with_raw_response.get_browser_stats(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_page(self, client: Fleet) -> None:
        scrape = client.sessions.scrape.page(
            session_id="session_id",
            url="url",
        )
        assert_matches_type(object, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_page_with_all_params(self, client: Fleet) -> None:
        scrape = client.sessions.scrape.page(
            session_id="session_id",
            url="url",
            wait_until="load",
        )
        assert_matches_type(object, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_page(self, client: Fleet) -> None:
        response = client.sessions.scrape.with_raw_response.page(
            session_id="session_id",
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scrape = response.parse()
        assert_matches_type(object, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_page(self, client: Fleet) -> None:
        with client.sessions.scrape.with_streaming_response.page(
            session_id="session_id",
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scrape = response.parse()
            assert_matches_type(object, scrape, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_page(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.scrape.with_raw_response.page(
                session_id="",
                url="url",
            )


class TestAsyncScrape:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_cleanup_jobs(self, async_client: AsyncFleet) -> None:
        scrape = await async_client.sessions.scrape.cleanup_jobs(
            session_id="session_id",
        )
        assert_matches_type(ScrapeCleanupJobsResponse, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_cleanup_jobs_with_all_params(self, async_client: AsyncFleet) -> None:
        scrape = await async_client.sessions.scrape.cleanup_jobs(
            session_id="session_id",
            max_age_hours=0,
        )
        assert_matches_type(ScrapeCleanupJobsResponse, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_cleanup_jobs(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.scrape.with_raw_response.cleanup_jobs(
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scrape = await response.parse()
        assert_matches_type(ScrapeCleanupJobsResponse, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_cleanup_jobs(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.scrape.with_streaming_response.cleanup_jobs(
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scrape = await response.parse()
            assert_matches_type(ScrapeCleanupJobsResponse, scrape, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_cleanup_jobs(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.scrape.with_raw_response.cleanup_jobs(
                session_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_browser_stats(self, async_client: AsyncFleet) -> None:
        scrape = await async_client.sessions.scrape.get_browser_stats(
            "session_id",
        )
        assert_matches_type(ScrapeGetBrowserStatsResponse, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_browser_stats(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.scrape.with_raw_response.get_browser_stats(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scrape = await response.parse()
        assert_matches_type(ScrapeGetBrowserStatsResponse, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_browser_stats(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.scrape.with_streaming_response.get_browser_stats(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scrape = await response.parse()
            assert_matches_type(ScrapeGetBrowserStatsResponse, scrape, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_browser_stats(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.scrape.with_raw_response.get_browser_stats(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_page(self, async_client: AsyncFleet) -> None:
        scrape = await async_client.sessions.scrape.page(
            session_id="session_id",
            url="url",
        )
        assert_matches_type(object, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_page_with_all_params(self, async_client: AsyncFleet) -> None:
        scrape = await async_client.sessions.scrape.page(
            session_id="session_id",
            url="url",
            wait_until="load",
        )
        assert_matches_type(object, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_page(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.scrape.with_raw_response.page(
            session_id="session_id",
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scrape = await response.parse()
        assert_matches_type(object, scrape, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_page(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.scrape.with_streaming_response.page(
            session_id="session_id",
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scrape = await response.parse()
            assert_matches_type(object, scrape, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_page(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.scrape.with_raw_response.page(
                session_id="",
                url="url",
            )
