# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from tests.utils import assert_matches_type
from fleet.types.workflows.request import (
    WorkflowResultWithMessage,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMass:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_company_scrape(self, client: Fleet) -> None:
        mass = client.workflows.request.mass.create_company_scrape()
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_company_scrape_with_all_params(self, client: Fleet) -> None:
        mass = client.workflows.request.mass.create_company_scrape(
            link_prefix="link_prefix",
        )
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_company_scrape(self, client: Fleet) -> None:
        response = client.workflows.request.mass.with_raw_response.create_company_scrape()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mass = response.parse()
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_company_scrape(self, client: Fleet) -> None:
        with client.workflows.request.mass.with_streaming_response.create_company_scrape() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mass = response.parse()
            assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_link_extraction(self, client: Fleet) -> None:
        mass = client.workflows.request.mass.create_link_extraction(
            company_name="company_name",
        )
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_link_extraction_with_all_params(self, client: Fleet) -> None:
        mass = client.workflows.request.mass.create_link_extraction(
            company_name="company_name",
            n_pages=0,
            results_per_page=0,
        )
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_link_extraction(self, client: Fleet) -> None:
        response = client.workflows.request.mass.with_raw_response.create_link_extraction(
            company_name="company_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mass = response.parse()
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_link_extraction(self, client: Fleet) -> None:
        with client.workflows.request.mass.with_streaming_response.create_link_extraction(
            company_name="company_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mass = response.parse()
            assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMass:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_company_scrape(self, async_client: AsyncFleet) -> None:
        mass = await async_client.workflows.request.mass.create_company_scrape()
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_company_scrape_with_all_params(self, async_client: AsyncFleet) -> None:
        mass = await async_client.workflows.request.mass.create_company_scrape(
            link_prefix="link_prefix",
        )
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_company_scrape(self, async_client: AsyncFleet) -> None:
        response = await async_client.workflows.request.mass.with_raw_response.create_company_scrape()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mass = await response.parse()
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_company_scrape(self, async_client: AsyncFleet) -> None:
        async with async_client.workflows.request.mass.with_streaming_response.create_company_scrape() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mass = await response.parse()
            assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_link_extraction(self, async_client: AsyncFleet) -> None:
        mass = await async_client.workflows.request.mass.create_link_extraction(
            company_name="company_name",
        )
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_link_extraction_with_all_params(self, async_client: AsyncFleet) -> None:
        mass = await async_client.workflows.request.mass.create_link_extraction(
            company_name="company_name",
            n_pages=0,
            results_per_page=0,
        )
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_link_extraction(self, async_client: AsyncFleet) -> None:
        response = await async_client.workflows.request.mass.with_raw_response.create_link_extraction(
            company_name="company_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mass = await response.parse()
        assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_link_extraction(self, async_client: AsyncFleet) -> None:
        async with async_client.workflows.request.mass.with_streaming_response.create_link_extraction(
            company_name="company_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mass = await response.parse()
            assert_matches_type(WorkflowResultWithMessage, mass, path=["response"])

        assert cast(Any, response.is_closed) is True
