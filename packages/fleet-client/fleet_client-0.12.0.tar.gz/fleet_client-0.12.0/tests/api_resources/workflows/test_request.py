# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from fleet import Fleet, AsyncFleet
from tests.utils import assert_matches_type
from fleet.types.workflows import (
    RequestCreateResponse,
)
from fleet.types.workflows.request import WorkflowResultWithMessage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRequest:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Fleet) -> None:
        request = client.workflows.request.create(
            url="url",
        )
        assert_matches_type(RequestCreateResponse, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Fleet) -> None:
        request = client.workflows.request.create(
            url="url",
            agentic=True,
            camo=True,
            enable_xvfb=True,
            ephemeral_browser=True,
            proxy_password="proxy_password",
            proxy_url="proxy_url",
            proxy_username="proxy_username",
            stealth=True,
            wait_until="load",
        )
        assert_matches_type(RequestCreateResponse, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Fleet) -> None:
        response = client.workflows.request.with_raw_response.create(
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        request = response.parse()
        assert_matches_type(RequestCreateResponse, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Fleet) -> None:
        with client.workflows.request.with_streaming_response.create(
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            request = response.parse()
            assert_matches_type(RequestCreateResponse, request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_business_owner(self, client: Fleet) -> None:
        request = client.workflows.request.create_business_owner(
            company_name="company_name",
        )
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_business_owner_with_all_params(self, client: Fleet) -> None:
        request = client.workflows.request.create_business_owner(
            company_name="company_name",
            addresses=["string"],
            camo=True,
            company_url="company_url",
            emails=["string"],
            max_steps=0,
            n_contact_pages=0,
            n_pages=0,
            n_search_engine_links=0,
            personnel_names=["string"],
            proxy_password="proxy_password",
            proxy_url="proxy_url",
            proxy_username="proxy_username",
            search_engine="duckduckgo",
            workflow_id="workflow_id",
        )
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_business_owner(self, client: Fleet) -> None:
        response = client.workflows.request.with_raw_response.create_business_owner(
            company_name="company_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        request = response.parse()
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_business_owner(self, client: Fleet) -> None:
        with client.workflows.request.with_streaming_response.create_business_owner(
            company_name="company_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            request = response.parse()
            assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_personal_email_request(self, client: Fleet) -> None:
        request = client.workflows.request.create_personal_email_request(
            person_name="person_name",
        )
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_personal_email_request_with_all_params(self, client: Fleet) -> None:
        request = client.workflows.request.create_personal_email_request(
            person_name="person_name",
            additional_context="additional_context",
            camo=True,
            company_name="company_name",
            job_title="job_title",
            known_websites=["string"],
            linkedin_url="linkedin_url",
            location="location",
            max_steps=0,
            n_pages=0,
            n_search_engine_links=0,
            proxy_password="proxy_password",
            proxy_url="proxy_url",
            proxy_username="proxy_username",
            search_engine="duckduckgo",
            workflow_id="workflow_id",
        )
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_personal_email_request(self, client: Fleet) -> None:
        response = client.workflows.request.with_raw_response.create_personal_email_request(
            person_name="person_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        request = response.parse()
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_personal_email_request(self, client: Fleet) -> None:
        with client.workflows.request.with_streaming_response.create_personal_email_request(
            person_name="person_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            request = response.parse()
            assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRequest:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncFleet) -> None:
        request = await async_client.workflows.request.create(
            url="url",
        )
        assert_matches_type(RequestCreateResponse, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncFleet) -> None:
        request = await async_client.workflows.request.create(
            url="url",
            agentic=True,
            camo=True,
            enable_xvfb=True,
            ephemeral_browser=True,
            proxy_password="proxy_password",
            proxy_url="proxy_url",
            proxy_username="proxy_username",
            stealth=True,
            wait_until="load",
        )
        assert_matches_type(RequestCreateResponse, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFleet) -> None:
        response = await async_client.workflows.request.with_raw_response.create(
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        request = await response.parse()
        assert_matches_type(RequestCreateResponse, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFleet) -> None:
        async with async_client.workflows.request.with_streaming_response.create(
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            request = await response.parse()
            assert_matches_type(RequestCreateResponse, request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_business_owner(self, async_client: AsyncFleet) -> None:
        request = await async_client.workflows.request.create_business_owner(
            company_name="company_name",
        )
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_business_owner_with_all_params(self, async_client: AsyncFleet) -> None:
        request = await async_client.workflows.request.create_business_owner(
            company_name="company_name",
            addresses=["string"],
            camo=True,
            company_url="company_url",
            emails=["string"],
            max_steps=0,
            n_contact_pages=0,
            n_pages=0,
            n_search_engine_links=0,
            personnel_names=["string"],
            proxy_password="proxy_password",
            proxy_url="proxy_url",
            proxy_username="proxy_username",
            search_engine="duckduckgo",
            workflow_id="workflow_id",
        )
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_business_owner(self, async_client: AsyncFleet) -> None:
        response = await async_client.workflows.request.with_raw_response.create_business_owner(
            company_name="company_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        request = await response.parse()
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_business_owner(self, async_client: AsyncFleet) -> None:
        async with async_client.workflows.request.with_streaming_response.create_business_owner(
            company_name="company_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            request = await response.parse()
            assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_personal_email_request(self, async_client: AsyncFleet) -> None:
        request = await async_client.workflows.request.create_personal_email_request(
            person_name="person_name",
        )
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_personal_email_request_with_all_params(self, async_client: AsyncFleet) -> None:
        request = await async_client.workflows.request.create_personal_email_request(
            person_name="person_name",
            additional_context="additional_context",
            camo=True,
            company_name="company_name",
            job_title="job_title",
            known_websites=["string"],
            linkedin_url="linkedin_url",
            location="location",
            max_steps=0,
            n_pages=0,
            n_search_engine_links=0,
            proxy_password="proxy_password",
            proxy_url="proxy_url",
            proxy_username="proxy_username",
            search_engine="duckduckgo",
            workflow_id="workflow_id",
        )
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_personal_email_request(self, async_client: AsyncFleet) -> None:
        response = await async_client.workflows.request.with_raw_response.create_personal_email_request(
            person_name="person_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        request = await response.parse()
        assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_personal_email_request(self, async_client: AsyncFleet) -> None:
        async with async_client.workflows.request.with_streaming_response.create_personal_email_request(
            person_name="person_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            request = await response.parse()
            assert_matches_type(WorkflowResultWithMessage, request, path=["response"])

        assert cast(Any, response.is_closed) is True
