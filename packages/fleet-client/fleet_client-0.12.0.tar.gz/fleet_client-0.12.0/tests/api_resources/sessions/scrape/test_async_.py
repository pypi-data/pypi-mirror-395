# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from tests.utils import assert_matches_type
from fleet.types.sessions.scrape import (
    AsyncListJobsResponse,
    AsyncCreateJobResponse,
    AsyncDeleteJobResponse,
    AsyncGetJobStatusResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAsync:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_job(self, client: Fleet) -> None:
        async_ = client.sessions.scrape.async_.create_job(
            session_id="session_id",
            url="url",
        )
        assert_matches_type(AsyncCreateJobResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_job_with_all_params(self, client: Fleet) -> None:
        async_ = client.sessions.scrape.async_.create_job(
            session_id="session_id",
            url="url",
            stealth=True,
            wait_until="load",
        )
        assert_matches_type(AsyncCreateJobResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_job(self, client: Fleet) -> None:
        response = client.sessions.scrape.async_.with_raw_response.create_job(
            session_id="session_id",
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncCreateJobResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_job(self, client: Fleet) -> None:
        with client.sessions.scrape.async_.with_streaming_response.create_job(
            session_id="session_id",
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncCreateJobResponse, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_create_job(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.scrape.async_.with_raw_response.create_job(
                session_id="",
                url="url",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete_job(self, client: Fleet) -> None:
        async_ = client.sessions.scrape.async_.delete_job(
            job_id="job_id",
            session_id="session_id",
        )
        assert_matches_type(AsyncDeleteJobResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete_job(self, client: Fleet) -> None:
        response = client.sessions.scrape.async_.with_raw_response.delete_job(
            job_id="job_id",
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncDeleteJobResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete_job(self, client: Fleet) -> None:
        with client.sessions.scrape.async_.with_streaming_response.delete_job(
            job_id="job_id",
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncDeleteJobResponse, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete_job(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.scrape.async_.with_raw_response.delete_job(
                job_id="job_id",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.sessions.scrape.async_.with_raw_response.delete_job(
                job_id="",
                session_id="session_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_job_status(self, client: Fleet) -> None:
        async_ = client.sessions.scrape.async_.get_job_status(
            job_id="job_id",
            session_id="session_id",
        )
        assert_matches_type(AsyncGetJobStatusResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_job_status(self, client: Fleet) -> None:
        response = client.sessions.scrape.async_.with_raw_response.get_job_status(
            job_id="job_id",
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncGetJobStatusResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_job_status(self, client: Fleet) -> None:
        with client.sessions.scrape.async_.with_streaming_response.get_job_status(
            job_id="job_id",
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncGetJobStatusResponse, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_job_status(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.scrape.async_.with_raw_response.get_job_status(
                job_id="job_id",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.sessions.scrape.async_.with_raw_response.get_job_status(
                job_id="",
                session_id="session_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_jobs(self, client: Fleet) -> None:
        async_ = client.sessions.scrape.async_.list_jobs(
            "session_id",
        )
        assert_matches_type(AsyncListJobsResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_jobs(self, client: Fleet) -> None:
        response = client.sessions.scrape.async_.with_raw_response.list_jobs(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncListJobsResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_jobs(self, client: Fleet) -> None:
        with client.sessions.scrape.async_.with_streaming_response.list_jobs(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncListJobsResponse, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_list_jobs(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.scrape.async_.with_raw_response.list_jobs(
                "",
            )


class TestAsyncAsync:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_job(self, async_client: AsyncFleet) -> None:
        async_ = await async_client.sessions.scrape.async_.create_job(
            session_id="session_id",
            url="url",
        )
        assert_matches_type(AsyncCreateJobResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_job_with_all_params(self, async_client: AsyncFleet) -> None:
        async_ = await async_client.sessions.scrape.async_.create_job(
            session_id="session_id",
            url="url",
            stealth=True,
            wait_until="load",
        )
        assert_matches_type(AsyncCreateJobResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_job(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.scrape.async_.with_raw_response.create_job(
            session_id="session_id",
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncCreateJobResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_job(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.scrape.async_.with_streaming_response.create_job(
            session_id="session_id",
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncCreateJobResponse, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_create_job(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.scrape.async_.with_raw_response.create_job(
                session_id="",
                url="url",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete_job(self, async_client: AsyncFleet) -> None:
        async_ = await async_client.sessions.scrape.async_.delete_job(
            job_id="job_id",
            session_id="session_id",
        )
        assert_matches_type(AsyncDeleteJobResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete_job(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.scrape.async_.with_raw_response.delete_job(
            job_id="job_id",
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncDeleteJobResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete_job(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.scrape.async_.with_streaming_response.delete_job(
            job_id="job_id",
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncDeleteJobResponse, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete_job(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.scrape.async_.with_raw_response.delete_job(
                job_id="job_id",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.sessions.scrape.async_.with_raw_response.delete_job(
                job_id="",
                session_id="session_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_job_status(self, async_client: AsyncFleet) -> None:
        async_ = await async_client.sessions.scrape.async_.get_job_status(
            job_id="job_id",
            session_id="session_id",
        )
        assert_matches_type(AsyncGetJobStatusResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_job_status(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.scrape.async_.with_raw_response.get_job_status(
            job_id="job_id",
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncGetJobStatusResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_job_status(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.scrape.async_.with_streaming_response.get_job_status(
            job_id="job_id",
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncGetJobStatusResponse, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_job_status(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.scrape.async_.with_raw_response.get_job_status(
                job_id="job_id",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.sessions.scrape.async_.with_raw_response.get_job_status(
                job_id="",
                session_id="session_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_jobs(self, async_client: AsyncFleet) -> None:
        async_ = await async_client.sessions.scrape.async_.list_jobs(
            "session_id",
        )
        assert_matches_type(AsyncListJobsResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_jobs(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.scrape.async_.with_raw_response.list_jobs(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncListJobsResponse, async_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_jobs(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.scrape.async_.with_streaming_response.list_jobs(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncListJobsResponse, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_list_jobs(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.scrape.async_.with_raw_response.list_jobs(
                "",
            )
