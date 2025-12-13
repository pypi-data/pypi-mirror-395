# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from ....types.workflows.request import mass_create_company_scrape_params, mass_create_link_extraction_params
from ....types.workflows.request.workflow_result_with_message import WorkflowResultWithMessage

__all__ = ["MassResource", "AsyncMassResource"]


class MassResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MassResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return MassResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MassResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return MassResourceWithStreamingResponse(self)

    def create_company_scrape(
        self,
        *,
        link_prefix: Optional[str] | Omit = omit,
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
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/workflows/request/mass/company-scrape",
            body=maybe_transform(
                {"link_prefix": link_prefix}, mass_create_company_scrape_params.MassCreateCompanyScrapeParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowResultWithMessage,
        )

    def create_link_extraction(
        self,
        *,
        company_name: str,
        n_pages: int | Omit = omit,
        results_per_page: int | Omit = omit,
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
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/workflows/request/mass/link-extraction",
            body=maybe_transform(
                {
                    "company_name": company_name,
                    "n_pages": n_pages,
                    "results_per_page": results_per_page,
                },
                mass_create_link_extraction_params.MassCreateLinkExtractionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowResultWithMessage,
        )


class AsyncMassResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMassResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return AsyncMassResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMassResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return AsyncMassResourceWithStreamingResponse(self)

    async def create_company_scrape(
        self,
        *,
        link_prefix: Optional[str] | Omit = omit,
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
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/workflows/request/mass/company-scrape",
            body=await async_maybe_transform(
                {"link_prefix": link_prefix}, mass_create_company_scrape_params.MassCreateCompanyScrapeParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowResultWithMessage,
        )

    async def create_link_extraction(
        self,
        *,
        company_name: str,
        n_pages: int | Omit = omit,
        results_per_page: int | Omit = omit,
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
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/workflows/request/mass/link-extraction",
            body=await async_maybe_transform(
                {
                    "company_name": company_name,
                    "n_pages": n_pages,
                    "results_per_page": results_per_page,
                },
                mass_create_link_extraction_params.MassCreateLinkExtractionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowResultWithMessage,
        )


class MassResourceWithRawResponse:
    def __init__(self, mass: MassResource) -> None:
        self._mass = mass

        self.create_company_scrape = to_raw_response_wrapper(
            mass.create_company_scrape,
        )
        self.create_link_extraction = to_raw_response_wrapper(
            mass.create_link_extraction,
        )


class AsyncMassResourceWithRawResponse:
    def __init__(self, mass: AsyncMassResource) -> None:
        self._mass = mass

        self.create_company_scrape = async_to_raw_response_wrapper(
            mass.create_company_scrape,
        )
        self.create_link_extraction = async_to_raw_response_wrapper(
            mass.create_link_extraction,
        )


class MassResourceWithStreamingResponse:
    def __init__(self, mass: MassResource) -> None:
        self._mass = mass

        self.create_company_scrape = to_streamed_response_wrapper(
            mass.create_company_scrape,
        )
        self.create_link_extraction = to_streamed_response_wrapper(
            mass.create_link_extraction,
        )


class AsyncMassResourceWithStreamingResponse:
    def __init__(self, mass: AsyncMassResource) -> None:
        self._mass = mass

        self.create_company_scrape = async_to_streamed_response_wrapper(
            mass.create_company_scrape,
        )
        self.create_link_extraction = async_to_streamed_response_wrapper(
            mass.create_link_extraction,
        )
