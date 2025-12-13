# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from fleet.types import WorkflowResultsResponse, WorkflowDescribeResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWorkflows:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_describe(self, client: Fleet) -> None:
        workflow = client.workflows.describe(
            "workflow_id",
        )
        assert_matches_type(WorkflowDescribeResponse, workflow, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_describe(self, client: Fleet) -> None:
        response = client.workflows.with_raw_response.describe(
            "workflow_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow = response.parse()
        assert_matches_type(WorkflowDescribeResponse, workflow, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_describe(self, client: Fleet) -> None:
        with client.workflows.with_streaming_response.describe(
            "workflow_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow = response.parse()
            assert_matches_type(WorkflowDescribeResponse, workflow, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_describe(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workflow_id` but received ''"):
            client.workflows.with_raw_response.describe(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_results(self, client: Fleet) -> None:
        workflow = client.workflows.results(
            "workflow_id",
        )
        assert_matches_type(WorkflowResultsResponse, workflow, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_results(self, client: Fleet) -> None:
        response = client.workflows.with_raw_response.results(
            "workflow_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow = response.parse()
        assert_matches_type(WorkflowResultsResponse, workflow, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_results(self, client: Fleet) -> None:
        with client.workflows.with_streaming_response.results(
            "workflow_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow = response.parse()
            assert_matches_type(WorkflowResultsResponse, workflow, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_results(self, client: Fleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workflow_id` but received ''"):
            client.workflows.with_raw_response.results(
                "",
            )


class TestAsyncWorkflows:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_describe(self, async_client: AsyncFleet) -> None:
        workflow = await async_client.workflows.describe(
            "workflow_id",
        )
        assert_matches_type(WorkflowDescribeResponse, workflow, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_describe(self, async_client: AsyncFleet) -> None:
        response = await async_client.workflows.with_raw_response.describe(
            "workflow_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow = await response.parse()
        assert_matches_type(WorkflowDescribeResponse, workflow, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_describe(self, async_client: AsyncFleet) -> None:
        async with async_client.workflows.with_streaming_response.describe(
            "workflow_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow = await response.parse()
            assert_matches_type(WorkflowDescribeResponse, workflow, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_describe(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workflow_id` but received ''"):
            await async_client.workflows.with_raw_response.describe(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_results(self, async_client: AsyncFleet) -> None:
        workflow = await async_client.workflows.results(
            "workflow_id",
        )
        assert_matches_type(WorkflowResultsResponse, workflow, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_results(self, async_client: AsyncFleet) -> None:
        response = await async_client.workflows.with_raw_response.results(
            "workflow_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow = await response.parse()
        assert_matches_type(WorkflowResultsResponse, workflow, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_results(self, async_client: AsyncFleet) -> None:
        async with async_client.workflows.with_streaming_response.results(
            "workflow_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow = await response.parse()
            assert_matches_type(WorkflowResultsResponse, workflow, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_results(self, async_client: AsyncFleet) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workflow_id` but received ''"):
            await async_client.workflows.with_raw_response.results(
                "",
            )
