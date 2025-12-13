# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from tests.utils import assert_matches_type
from fleet.types.sessions import (
    ResponseListResponse,
    ResponseClearResponse,
    ResponseGetLatestResponse,
    ResponseGetSummaryResponse,
    ResponseGetFilteredResponse,
    ResponseToggleTrackingResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResponses:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Fleet) -> None:
        response = client.sessions.responses.list(
            "session_id",
        )
        assert_matches_type(ResponseListResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Fleet) -> None:
        http_response = client.sessions.responses.with_raw_response.list(
            "session_id",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = http_response.parse()
        assert_matches_type(ResponseListResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Fleet) -> None:
        with client.sessions.responses.with_streaming_response.list(
            "session_id",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = http_response.parse()
            assert_matches_type(ResponseListResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_list(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.responses.with_raw_response.list(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_clear(self, client: Fleet) -> None:
        response = client.sessions.responses.clear(
            "session_id",
        )
        assert_matches_type(ResponseClearResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_clear(self, client: Fleet) -> None:
        http_response = client.sessions.responses.with_raw_response.clear(
            "session_id",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = http_response.parse()
        assert_matches_type(ResponseClearResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_clear(self, client: Fleet) -> None:
        with client.sessions.responses.with_streaming_response.clear(
            "session_id",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = http_response.parse()
            assert_matches_type(ResponseClearResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_clear(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.responses.with_raw_response.clear(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_filtered(self, client: Fleet) -> None:
        response = client.sessions.responses.get_filtered(
            session_id="session_id",
        )
        assert_matches_type(ResponseGetFilteredResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_filtered_with_all_params(self, client: Fleet) -> None:
        response = client.sessions.responses.get_filtered(
            session_id="session_id",
            status_code=0,
            url_pattern="url_pattern",
        )
        assert_matches_type(ResponseGetFilteredResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_filtered(self, client: Fleet) -> None:
        http_response = client.sessions.responses.with_raw_response.get_filtered(
            session_id="session_id",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = http_response.parse()
        assert_matches_type(ResponseGetFilteredResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_filtered(self, client: Fleet) -> None:
        with client.sessions.responses.with_streaming_response.get_filtered(
            session_id="session_id",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = http_response.parse()
            assert_matches_type(ResponseGetFilteredResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_filtered(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.responses.with_raw_response.get_filtered(
                session_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_latest(self, client: Fleet) -> None:
        response = client.sessions.responses.get_latest(
            "session_id",
        )
        assert_matches_type(ResponseGetLatestResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_latest(self, client: Fleet) -> None:
        http_response = client.sessions.responses.with_raw_response.get_latest(
            "session_id",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = http_response.parse()
        assert_matches_type(ResponseGetLatestResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_latest(self, client: Fleet) -> None:
        with client.sessions.responses.with_streaming_response.get_latest(
            "session_id",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = http_response.parse()
            assert_matches_type(ResponseGetLatestResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_latest(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.responses.with_raw_response.get_latest(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_summary(self, client: Fleet) -> None:
        response = client.sessions.responses.get_summary(
            "session_id",
        )
        assert_matches_type(ResponseGetSummaryResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_summary(self, client: Fleet) -> None:
        http_response = client.sessions.responses.with_raw_response.get_summary(
            "session_id",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = http_response.parse()
        assert_matches_type(ResponseGetSummaryResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_summary(self, client: Fleet) -> None:
        with client.sessions.responses.with_streaming_response.get_summary(
            "session_id",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = http_response.parse()
            assert_matches_type(ResponseGetSummaryResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_summary(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.responses.with_raw_response.get_summary(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_toggle_tracking(self, client: Fleet) -> None:
        response = client.sessions.responses.toggle_tracking(
            session_id="session_id",
            enable=True,
        )
        assert_matches_type(ResponseToggleTrackingResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_toggle_tracking(self, client: Fleet) -> None:
        http_response = client.sessions.responses.with_raw_response.toggle_tracking(
            session_id="session_id",
            enable=True,
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = http_response.parse()
        assert_matches_type(ResponseToggleTrackingResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_toggle_tracking(self, client: Fleet) -> None:
        with client.sessions.responses.with_streaming_response.toggle_tracking(
            session_id="session_id",
            enable=True,
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = http_response.parse()
            assert_matches_type(ResponseToggleTrackingResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_toggle_tracking(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.responses.with_raw_response.toggle_tracking(
                session_id="",
                enable=True,
            )


class TestAsyncResponses:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.responses.list(
            "session_id",
        )
        assert_matches_type(ResponseListResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFleet) -> None:
        http_response = await async_client.sessions.responses.with_raw_response.list(
            "session_id",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = await http_response.parse()
        assert_matches_type(ResponseListResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.responses.with_streaming_response.list(
            "session_id",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = await http_response.parse()
            assert_matches_type(ResponseListResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.responses.with_raw_response.list(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_clear(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.responses.clear(
            "session_id",
        )
        assert_matches_type(ResponseClearResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_clear(self, async_client: AsyncFleet) -> None:
        http_response = await async_client.sessions.responses.with_raw_response.clear(
            "session_id",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = await http_response.parse()
        assert_matches_type(ResponseClearResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_clear(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.responses.with_streaming_response.clear(
            "session_id",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = await http_response.parse()
            assert_matches_type(ResponseClearResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_clear(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.responses.with_raw_response.clear(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_filtered(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.responses.get_filtered(
            session_id="session_id",
        )
        assert_matches_type(ResponseGetFilteredResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_filtered_with_all_params(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.responses.get_filtered(
            session_id="session_id",
            status_code=0,
            url_pattern="url_pattern",
        )
        assert_matches_type(ResponseGetFilteredResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_filtered(self, async_client: AsyncFleet) -> None:
        http_response = await async_client.sessions.responses.with_raw_response.get_filtered(
            session_id="session_id",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = await http_response.parse()
        assert_matches_type(ResponseGetFilteredResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_filtered(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.responses.with_streaming_response.get_filtered(
            session_id="session_id",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = await http_response.parse()
            assert_matches_type(ResponseGetFilteredResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_filtered(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.responses.with_raw_response.get_filtered(
                session_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_latest(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.responses.get_latest(
            "session_id",
        )
        assert_matches_type(ResponseGetLatestResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_latest(self, async_client: AsyncFleet) -> None:
        http_response = await async_client.sessions.responses.with_raw_response.get_latest(
            "session_id",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = await http_response.parse()
        assert_matches_type(ResponseGetLatestResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_latest(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.responses.with_streaming_response.get_latest(
            "session_id",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = await http_response.parse()
            assert_matches_type(ResponseGetLatestResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_latest(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.responses.with_raw_response.get_latest(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_summary(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.responses.get_summary(
            "session_id",
        )
        assert_matches_type(ResponseGetSummaryResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_summary(self, async_client: AsyncFleet) -> None:
        http_response = await async_client.sessions.responses.with_raw_response.get_summary(
            "session_id",
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = await http_response.parse()
        assert_matches_type(ResponseGetSummaryResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_summary(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.responses.with_streaming_response.get_summary(
            "session_id",
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = await http_response.parse()
            assert_matches_type(ResponseGetSummaryResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_summary(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.responses.with_raw_response.get_summary(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_toggle_tracking(self, async_client: AsyncFleet) -> None:
        response = await async_client.sessions.responses.toggle_tracking(
            session_id="session_id",
            enable=True,
        )
        assert_matches_type(ResponseToggleTrackingResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_toggle_tracking(self, async_client: AsyncFleet) -> None:
        http_response = await async_client.sessions.responses.with_raw_response.toggle_tracking(
            session_id="session_id",
            enable=True,
        )

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = await http_response.parse()
        assert_matches_type(ResponseToggleTrackingResponse, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_toggle_tracking(self, async_client: AsyncFleet) -> None:
        async with async_client.sessions.responses.with_streaming_response.toggle_tracking(
            session_id="session_id",
            enable=True,
        ) as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = await http_response.parse()
            assert_matches_type(ResponseToggleTrackingResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_toggle_tracking(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.responses.with_raw_response.toggle_tracking(
                session_id="",
                enable=True,
            )
