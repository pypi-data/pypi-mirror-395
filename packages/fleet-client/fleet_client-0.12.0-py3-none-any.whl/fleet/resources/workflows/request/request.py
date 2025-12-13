# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .mass import (
    MassResource,
    AsyncMassResource,
    MassResourceWithRawResponse,
    AsyncMassResourceWithRawResponse,
    MassResourceWithStreamingResponse,
    AsyncMassResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.workflows import (
    WaitUntil,
    SearchEngine,
    request_create_params,
    request_create_business_owner_params,
    request_create_personal_email_request_params,
)
from ....types.workflows.wait_until import WaitUntil
from ....types.workflows.search_engine import SearchEngine
from ....types.workflows.request_create_response import RequestCreateResponse
from ....types.workflows.request.workflow_result_with_message import WorkflowResultWithMessage

__all__ = ["RequestResource", "AsyncRequestResource"]


class RequestResource(SyncAPIResource):
    @cached_property
    def mass(self) -> MassResource:
        return MassResource(self._client)

    @cached_property
    def with_raw_response(self) -> RequestResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return RequestResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RequestResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return RequestResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        url: str,
        agentic: bool | Omit = omit,
        camo: bool | Omit = omit,
        enable_xvfb: bool | Omit = omit,
        ephemeral_browser: bool | Omit = omit,
        proxy_password: Optional[str] | Omit = omit,
        proxy_url: Optional[str] | Omit = omit,
        proxy_username: Optional[str] | Omit = omit,
        stealth: bool | Omit = omit,
        wait_until: WaitUntil | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RequestCreateResponse:
        """
        Make a request to temporal worker

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/workflows/request/scrape",
            body=maybe_transform(
                {
                    "url": url,
                    "agentic": agentic,
                    "camo": camo,
                    "enable_xvfb": enable_xvfb,
                    "ephemeral_browser": ephemeral_browser,
                    "proxy_password": proxy_password,
                    "proxy_url": proxy_url,
                    "proxy_username": proxy_username,
                    "stealth": stealth,
                    "wait_until": wait_until,
                },
                request_create_params.RequestCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RequestCreateResponse,
        )

    def create_business_owner(
        self,
        *,
        company_name: str,
        addresses: Optional[SequenceNotStr[str]] | Omit = omit,
        camo: bool | Omit = omit,
        company_url: Optional[str] | Omit = omit,
        emails: Optional[SequenceNotStr[str]] | Omit = omit,
        max_steps: Optional[int] | Omit = omit,
        n_contact_pages: int | Omit = omit,
        n_pages: int | Omit = omit,
        n_search_engine_links: int | Omit = omit,
        personnel_names: Optional[SequenceNotStr[str]] | Omit = omit,
        proxy_password: Optional[str] | Omit = omit,
        proxy_url: Optional[str] | Omit = omit,
        proxy_username: Optional[str] | Omit = omit,
        search_engine: SearchEngine | Omit = omit,
        workflow_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkflowResultWithMessage:
        """
        Make a request to temporal worker

        Args:
          company_name: The name of the business

          addresses: Optional list of addresses associated with the business

          camo: Whether to use CAMO for scraping (if available)

          company_url: The URL of the business to find the owner for

          emails: Optional list of emails associated with the business

          max_steps: Maximum number of steps the agent can take

          n_contact_pages: Number of additional pages to visit to find contact info after identifying the
              owner

          n_pages: Number of pages to scrape for owner information

          n_search_engine_links: Number of search engine links to consider if needed

          personnel_names: List of people associated with the business

          proxy_password: Optional proxy password

          proxy_url: Optional proxy URL to use for web requests

          proxy_username: Optional proxy username

          search_engine: Search engine to use for finding links

          workflow_id: Optional workflow ID for tracking

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/workflows/request/business-owner",
            body=maybe_transform(
                {
                    "company_name": company_name,
                    "addresses": addresses,
                    "camo": camo,
                    "company_url": company_url,
                    "emails": emails,
                    "max_steps": max_steps,
                    "n_contact_pages": n_contact_pages,
                    "n_pages": n_pages,
                    "n_search_engine_links": n_search_engine_links,
                    "personnel_names": personnel_names,
                    "proxy_password": proxy_password,
                    "proxy_url": proxy_url,
                    "proxy_username": proxy_username,
                    "search_engine": search_engine,
                    "workflow_id": workflow_id,
                },
                request_create_business_owner_params.RequestCreateBusinessOwnerParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowResultWithMessage,
        )

    def create_personal_email_request(
        self,
        *,
        person_name: str,
        additional_context: Optional[str] | Omit = omit,
        camo: bool | Omit = omit,
        company_name: Optional[str] | Omit = omit,
        job_title: Optional[str] | Omit = omit,
        known_websites: Optional[SequenceNotStr[str]] | Omit = omit,
        linkedin_url: Optional[str] | Omit = omit,
        location: Optional[str] | Omit = omit,
        max_steps: Optional[int] | Omit = omit,
        n_pages: int | Omit = omit,
        n_search_engine_links: int | Omit = omit,
        proxy_password: Optional[str] | Omit = omit,
        proxy_url: Optional[str] | Omit = omit,
        proxy_username: Optional[str] | Omit = omit,
        search_engine: SearchEngine | Omit = omit,
        workflow_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkflowResultWithMessage:
        """
        Make a request to temporal worker

        Args:
          person_name: The name of the person to find email for

          additional_context: Any additional context that might help find the person's email

          camo: Whether to use CAMO for scraping

          company_name: Optional company name associated with the person

          job_title: Optional job title of the person

          known_websites: Optional list of websites associated with the person

          linkedin_url: Optional LinkedIn URL of the person

          location: Optional location (city, state) of the person

          max_steps: Maximum number of steps the agent can take

          n_pages: Number of pages to visit while searching for email

          n_search_engine_links: Number of search engine results to explore

          proxy_password: Optional proxy password

          proxy_url: Optional proxy URL to use for web requests

          proxy_username: Optional proxy username

          search_engine: Search engine to use for finding email

          workflow_id: Optional workflow ID for tracking

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/workflows/request/personal-email",
            body=maybe_transform(
                {
                    "person_name": person_name,
                    "additional_context": additional_context,
                    "camo": camo,
                    "company_name": company_name,
                    "job_title": job_title,
                    "known_websites": known_websites,
                    "linkedin_url": linkedin_url,
                    "location": location,
                    "max_steps": max_steps,
                    "n_pages": n_pages,
                    "n_search_engine_links": n_search_engine_links,
                    "proxy_password": proxy_password,
                    "proxy_url": proxy_url,
                    "proxy_username": proxy_username,
                    "search_engine": search_engine,
                    "workflow_id": workflow_id,
                },
                request_create_personal_email_request_params.RequestCreatePersonalEmailRequestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowResultWithMessage,
        )


class AsyncRequestResource(AsyncAPIResource):
    @cached_property
    def mass(self) -> AsyncMassResource:
        return AsyncMassResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncRequestResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return AsyncRequestResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRequestResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return AsyncRequestResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        url: str,
        agentic: bool | Omit = omit,
        camo: bool | Omit = omit,
        enable_xvfb: bool | Omit = omit,
        ephemeral_browser: bool | Omit = omit,
        proxy_password: Optional[str] | Omit = omit,
        proxy_url: Optional[str] | Omit = omit,
        proxy_username: Optional[str] | Omit = omit,
        stealth: bool | Omit = omit,
        wait_until: WaitUntil | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RequestCreateResponse:
        """
        Make a request to temporal worker

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/workflows/request/scrape",
            body=await async_maybe_transform(
                {
                    "url": url,
                    "agentic": agentic,
                    "camo": camo,
                    "enable_xvfb": enable_xvfb,
                    "ephemeral_browser": ephemeral_browser,
                    "proxy_password": proxy_password,
                    "proxy_url": proxy_url,
                    "proxy_username": proxy_username,
                    "stealth": stealth,
                    "wait_until": wait_until,
                },
                request_create_params.RequestCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RequestCreateResponse,
        )

    async def create_business_owner(
        self,
        *,
        company_name: str,
        addresses: Optional[SequenceNotStr[str]] | Omit = omit,
        camo: bool | Omit = omit,
        company_url: Optional[str] | Omit = omit,
        emails: Optional[SequenceNotStr[str]] | Omit = omit,
        max_steps: Optional[int] | Omit = omit,
        n_contact_pages: int | Omit = omit,
        n_pages: int | Omit = omit,
        n_search_engine_links: int | Omit = omit,
        personnel_names: Optional[SequenceNotStr[str]] | Omit = omit,
        proxy_password: Optional[str] | Omit = omit,
        proxy_url: Optional[str] | Omit = omit,
        proxy_username: Optional[str] | Omit = omit,
        search_engine: SearchEngine | Omit = omit,
        workflow_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkflowResultWithMessage:
        """
        Make a request to temporal worker

        Args:
          company_name: The name of the business

          addresses: Optional list of addresses associated with the business

          camo: Whether to use CAMO for scraping (if available)

          company_url: The URL of the business to find the owner for

          emails: Optional list of emails associated with the business

          max_steps: Maximum number of steps the agent can take

          n_contact_pages: Number of additional pages to visit to find contact info after identifying the
              owner

          n_pages: Number of pages to scrape for owner information

          n_search_engine_links: Number of search engine links to consider if needed

          personnel_names: List of people associated with the business

          proxy_password: Optional proxy password

          proxy_url: Optional proxy URL to use for web requests

          proxy_username: Optional proxy username

          search_engine: Search engine to use for finding links

          workflow_id: Optional workflow ID for tracking

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/workflows/request/business-owner",
            body=await async_maybe_transform(
                {
                    "company_name": company_name,
                    "addresses": addresses,
                    "camo": camo,
                    "company_url": company_url,
                    "emails": emails,
                    "max_steps": max_steps,
                    "n_contact_pages": n_contact_pages,
                    "n_pages": n_pages,
                    "n_search_engine_links": n_search_engine_links,
                    "personnel_names": personnel_names,
                    "proxy_password": proxy_password,
                    "proxy_url": proxy_url,
                    "proxy_username": proxy_username,
                    "search_engine": search_engine,
                    "workflow_id": workflow_id,
                },
                request_create_business_owner_params.RequestCreateBusinessOwnerParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowResultWithMessage,
        )

    async def create_personal_email_request(
        self,
        *,
        person_name: str,
        additional_context: Optional[str] | Omit = omit,
        camo: bool | Omit = omit,
        company_name: Optional[str] | Omit = omit,
        job_title: Optional[str] | Omit = omit,
        known_websites: Optional[SequenceNotStr[str]] | Omit = omit,
        linkedin_url: Optional[str] | Omit = omit,
        location: Optional[str] | Omit = omit,
        max_steps: Optional[int] | Omit = omit,
        n_pages: int | Omit = omit,
        n_search_engine_links: int | Omit = omit,
        proxy_password: Optional[str] | Omit = omit,
        proxy_url: Optional[str] | Omit = omit,
        proxy_username: Optional[str] | Omit = omit,
        search_engine: SearchEngine | Omit = omit,
        workflow_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkflowResultWithMessage:
        """
        Make a request to temporal worker

        Args:
          person_name: The name of the person to find email for

          additional_context: Any additional context that might help find the person's email

          camo: Whether to use CAMO for scraping

          company_name: Optional company name associated with the person

          job_title: Optional job title of the person

          known_websites: Optional list of websites associated with the person

          linkedin_url: Optional LinkedIn URL of the person

          location: Optional location (city, state) of the person

          max_steps: Maximum number of steps the agent can take

          n_pages: Number of pages to visit while searching for email

          n_search_engine_links: Number of search engine results to explore

          proxy_password: Optional proxy password

          proxy_url: Optional proxy URL to use for web requests

          proxy_username: Optional proxy username

          search_engine: Search engine to use for finding email

          workflow_id: Optional workflow ID for tracking

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/workflows/request/personal-email",
            body=await async_maybe_transform(
                {
                    "person_name": person_name,
                    "additional_context": additional_context,
                    "camo": camo,
                    "company_name": company_name,
                    "job_title": job_title,
                    "known_websites": known_websites,
                    "linkedin_url": linkedin_url,
                    "location": location,
                    "max_steps": max_steps,
                    "n_pages": n_pages,
                    "n_search_engine_links": n_search_engine_links,
                    "proxy_password": proxy_password,
                    "proxy_url": proxy_url,
                    "proxy_username": proxy_username,
                    "search_engine": search_engine,
                    "workflow_id": workflow_id,
                },
                request_create_personal_email_request_params.RequestCreatePersonalEmailRequestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowResultWithMessage,
        )


class RequestResourceWithRawResponse:
    def __init__(self, request: RequestResource) -> None:
        self._request = request

        self.create = to_raw_response_wrapper(
            request.create,
        )
        self.create_business_owner = to_raw_response_wrapper(
            request.create_business_owner,
        )
        self.create_personal_email_request = to_raw_response_wrapper(
            request.create_personal_email_request,
        )

    @cached_property
    def mass(self) -> MassResourceWithRawResponse:
        return MassResourceWithRawResponse(self._request.mass)


class AsyncRequestResourceWithRawResponse:
    def __init__(self, request: AsyncRequestResource) -> None:
        self._request = request

        self.create = async_to_raw_response_wrapper(
            request.create,
        )
        self.create_business_owner = async_to_raw_response_wrapper(
            request.create_business_owner,
        )
        self.create_personal_email_request = async_to_raw_response_wrapper(
            request.create_personal_email_request,
        )

    @cached_property
    def mass(self) -> AsyncMassResourceWithRawResponse:
        return AsyncMassResourceWithRawResponse(self._request.mass)


class RequestResourceWithStreamingResponse:
    def __init__(self, request: RequestResource) -> None:
        self._request = request

        self.create = to_streamed_response_wrapper(
            request.create,
        )
        self.create_business_owner = to_streamed_response_wrapper(
            request.create_business_owner,
        )
        self.create_personal_email_request = to_streamed_response_wrapper(
            request.create_personal_email_request,
        )

    @cached_property
    def mass(self) -> MassResourceWithStreamingResponse:
        return MassResourceWithStreamingResponse(self._request.mass)


class AsyncRequestResourceWithStreamingResponse:
    def __init__(self, request: AsyncRequestResource) -> None:
        self._request = request

        self.create = async_to_streamed_response_wrapper(
            request.create,
        )
        self.create_business_owner = async_to_streamed_response_wrapper(
            request.create_business_owner,
        )
        self.create_personal_email_request = async_to_streamed_response_wrapper(
            request.create_personal_email_request,
        )

    @cached_property
    def mass(self) -> AsyncMassResourceWithStreamingResponse:
        return AsyncMassResourceWithStreamingResponse(self._request.mass)
