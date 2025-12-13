# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .async_ import (
    AsyncResource,
    AsyncAsyncResource,
    AsyncResourceWithRawResponse,
    AsyncAsyncResourceWithRawResponse,
    AsyncResourceWithStreamingResponse,
    AsyncAsyncResourceWithStreamingResponse,
)
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
from .browser_strategy import (
    BrowserStrategyResource,
    AsyncBrowserStrategyResource,
    BrowserStrategyResourceWithRawResponse,
    AsyncBrowserStrategyResourceWithRawResponse,
    BrowserStrategyResourceWithStreamingResponse,
    AsyncBrowserStrategyResourceWithStreamingResponse,
)
from ....types.sessions import scrape_page_params, scrape_cleanup_jobs_params
from ....types.workflows import WaitUntil
from ....types.workflows.wait_until import WaitUntil
from ....types.sessions.scrape_cleanup_jobs_response import ScrapeCleanupJobsResponse
from ....types.sessions.scrape_get_browser_stats_response import ScrapeGetBrowserStatsResponse

__all__ = ["ScrapeResource", "AsyncScrapeResource"]


class ScrapeResource(SyncAPIResource):
    @cached_property
    def async_(self) -> AsyncResource:
        return AsyncResource(self._client)

    @cached_property
    def browser_strategy(self) -> BrowserStrategyResource:
        return BrowserStrategyResource(self._client)

    @cached_property
    def with_raw_response(self) -> ScrapeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return ScrapeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ScrapeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return ScrapeResourceWithStreamingResponse(self)

    def cleanup_jobs(
        self,
        session_id: str,
        *,
        max_age_hours: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScrapeCleanupJobsResponse:
        """
        Clean up completed jobs older than the specified age.

        Args:
          max_age_hours: Maximum age in hours for completed jobs

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._post(
            f"/sessions/{session_id}/scrape/cleanup",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"max_age_hours": max_age_hours}, scrape_cleanup_jobs_params.ScrapeCleanupJobsParams
                ),
            ),
            cast_to=ScrapeCleanupJobsResponse,
        )

    def get_browser_stats(
        self,
        session_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScrapeGetBrowserStatsResponse:
        """
        Get browser usage statistics for async scraping jobs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get(
            f"/sessions/{session_id}/scrape/browser-stats",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScrapeGetBrowserStatsResponse,
        )

    def page(
        self,
        session_id: str,
        *,
        url: str,
        wait_until: WaitUntil | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Post Scrape Page

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._post(
            f"/sessions/{session_id}/scrape",
            body=maybe_transform(
                {
                    "url": url,
                    "wait_until": wait_until,
                },
                scrape_page_params.ScrapePageParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncScrapeResource(AsyncAPIResource):
    @cached_property
    def async_(self) -> AsyncAsyncResource:
        return AsyncAsyncResource(self._client)

    @cached_property
    def browser_strategy(self) -> AsyncBrowserStrategyResource:
        return AsyncBrowserStrategyResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncScrapeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return AsyncScrapeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncScrapeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return AsyncScrapeResourceWithStreamingResponse(self)

    async def cleanup_jobs(
        self,
        session_id: str,
        *,
        max_age_hours: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScrapeCleanupJobsResponse:
        """
        Clean up completed jobs older than the specified age.

        Args:
          max_age_hours: Maximum age in hours for completed jobs

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._post(
            f"/sessions/{session_id}/scrape/cleanup",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"max_age_hours": max_age_hours}, scrape_cleanup_jobs_params.ScrapeCleanupJobsParams
                ),
            ),
            cast_to=ScrapeCleanupJobsResponse,
        )

    async def get_browser_stats(
        self,
        session_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScrapeGetBrowserStatsResponse:
        """
        Get browser usage statistics for async scraping jobs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._get(
            f"/sessions/{session_id}/scrape/browser-stats",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScrapeGetBrowserStatsResponse,
        )

    async def page(
        self,
        session_id: str,
        *,
        url: str,
        wait_until: WaitUntil | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Post Scrape Page

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._post(
            f"/sessions/{session_id}/scrape",
            body=await async_maybe_transform(
                {
                    "url": url,
                    "wait_until": wait_until,
                },
                scrape_page_params.ScrapePageParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ScrapeResourceWithRawResponse:
    def __init__(self, scrape: ScrapeResource) -> None:
        self._scrape = scrape

        self.cleanup_jobs = to_raw_response_wrapper(
            scrape.cleanup_jobs,
        )
        self.get_browser_stats = to_raw_response_wrapper(
            scrape.get_browser_stats,
        )
        self.page = to_raw_response_wrapper(
            scrape.page,
        )

    @cached_property
    def async_(self) -> AsyncResourceWithRawResponse:
        return AsyncResourceWithRawResponse(self._scrape.async_)

    @cached_property
    def browser_strategy(self) -> BrowserStrategyResourceWithRawResponse:
        return BrowserStrategyResourceWithRawResponse(self._scrape.browser_strategy)


class AsyncScrapeResourceWithRawResponse:
    def __init__(self, scrape: AsyncScrapeResource) -> None:
        self._scrape = scrape

        self.cleanup_jobs = async_to_raw_response_wrapper(
            scrape.cleanup_jobs,
        )
        self.get_browser_stats = async_to_raw_response_wrapper(
            scrape.get_browser_stats,
        )
        self.page = async_to_raw_response_wrapper(
            scrape.page,
        )

    @cached_property
    def async_(self) -> AsyncAsyncResourceWithRawResponse:
        return AsyncAsyncResourceWithRawResponse(self._scrape.async_)

    @cached_property
    def browser_strategy(self) -> AsyncBrowserStrategyResourceWithRawResponse:
        return AsyncBrowserStrategyResourceWithRawResponse(self._scrape.browser_strategy)


class ScrapeResourceWithStreamingResponse:
    def __init__(self, scrape: ScrapeResource) -> None:
        self._scrape = scrape

        self.cleanup_jobs = to_streamed_response_wrapper(
            scrape.cleanup_jobs,
        )
        self.get_browser_stats = to_streamed_response_wrapper(
            scrape.get_browser_stats,
        )
        self.page = to_streamed_response_wrapper(
            scrape.page,
        )

    @cached_property
    def async_(self) -> AsyncResourceWithStreamingResponse:
        return AsyncResourceWithStreamingResponse(self._scrape.async_)

    @cached_property
    def browser_strategy(self) -> BrowserStrategyResourceWithStreamingResponse:
        return BrowserStrategyResourceWithStreamingResponse(self._scrape.browser_strategy)


class AsyncScrapeResourceWithStreamingResponse:
    def __init__(self, scrape: AsyncScrapeResource) -> None:
        self._scrape = scrape

        self.cleanup_jobs = async_to_streamed_response_wrapper(
            scrape.cleanup_jobs,
        )
        self.get_browser_stats = async_to_streamed_response_wrapper(
            scrape.get_browser_stats,
        )
        self.page = async_to_streamed_response_wrapper(
            scrape.page,
        )

    @cached_property
    def async_(self) -> AsyncAsyncResourceWithStreamingResponse:
        return AsyncAsyncResourceWithStreamingResponse(self._scrape.async_)

    @cached_property
    def browser_strategy(self) -> AsyncBrowserStrategyResourceWithStreamingResponse:
        return AsyncBrowserStrategyResourceWithStreamingResponse(self._scrape.browser_strategy)
