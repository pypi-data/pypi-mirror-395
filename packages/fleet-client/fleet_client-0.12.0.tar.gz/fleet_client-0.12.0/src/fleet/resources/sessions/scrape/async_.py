# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

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
from ....types.workflows import WaitUntil
from ....types.sessions.scrape import async_create_job_params
from ....types.workflows.wait_until import WaitUntil
from ....types.sessions.scrape.async_list_jobs_response import AsyncListJobsResponse
from ....types.sessions.scrape.async_create_job_response import AsyncCreateJobResponse
from ....types.sessions.scrape.async_delete_job_response import AsyncDeleteJobResponse
from ....types.sessions.scrape.async_get_job_status_response import AsyncGetJobStatusResponse

__all__ = ["AsyncResource", "AsyncAsyncResource"]


class AsyncResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return AsyncResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return AsyncResourceWithStreamingResponse(self)

    def create_job(
        self,
        session_id: str,
        *,
        url: str,
        stealth: bool | Omit = omit,
        wait_until: WaitUntil | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncCreateJobResponse:
        """
        Create an async scraping job and return a job ID immediately.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._post(
            f"/sessions/{session_id}/scrape/async",
            body=maybe_transform(
                {
                    "url": url,
                    "stealth": stealth,
                    "wait_until": wait_until,
                },
                async_create_job_params.AsyncCreateJobParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncCreateJobResponse,
        )

    def delete_job(
        self,
        job_id: str,
        *,
        session_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncDeleteJobResponse:
        """
        Delete a specific async scraping job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return self._delete(
            f"/sessions/{session_id}/scrape/async/{job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncDeleteJobResponse,
        )

    def get_job_status(
        self,
        job_id: str,
        *,
        session_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncGetJobStatusResponse:
        """
        Get the status and results of an async scraping job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return self._get(
            f"/sessions/{session_id}/scrape/async/{job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncGetJobStatusResponse,
        )

    def list_jobs(
        self,
        session_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncListJobsResponse:
        """
        List all async scraping jobs with their statuses.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get(
            f"/sessions/{session_id}/scrape/async",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncListJobsResponse,
        )


class AsyncAsyncResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAsyncResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return AsyncAsyncResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAsyncResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return AsyncAsyncResourceWithStreamingResponse(self)

    async def create_job(
        self,
        session_id: str,
        *,
        url: str,
        stealth: bool | Omit = omit,
        wait_until: WaitUntil | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncCreateJobResponse:
        """
        Create an async scraping job and return a job ID immediately.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._post(
            f"/sessions/{session_id}/scrape/async",
            body=await async_maybe_transform(
                {
                    "url": url,
                    "stealth": stealth,
                    "wait_until": wait_until,
                },
                async_create_job_params.AsyncCreateJobParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncCreateJobResponse,
        )

    async def delete_job(
        self,
        job_id: str,
        *,
        session_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncDeleteJobResponse:
        """
        Delete a specific async scraping job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return await self._delete(
            f"/sessions/{session_id}/scrape/async/{job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncDeleteJobResponse,
        )

    async def get_job_status(
        self,
        job_id: str,
        *,
        session_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncGetJobStatusResponse:
        """
        Get the status and results of an async scraping job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return await self._get(
            f"/sessions/{session_id}/scrape/async/{job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncGetJobStatusResponse,
        )

    async def list_jobs(
        self,
        session_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncListJobsResponse:
        """
        List all async scraping jobs with their statuses.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._get(
            f"/sessions/{session_id}/scrape/async",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncListJobsResponse,
        )


class AsyncResourceWithRawResponse:
    def __init__(self, async_: AsyncResource) -> None:
        self._async_ = async_

        self.create_job = to_raw_response_wrapper(
            async_.create_job,
        )
        self.delete_job = to_raw_response_wrapper(
            async_.delete_job,
        )
        self.get_job_status = to_raw_response_wrapper(
            async_.get_job_status,
        )
        self.list_jobs = to_raw_response_wrapper(
            async_.list_jobs,
        )


class AsyncAsyncResourceWithRawResponse:
    def __init__(self, async_: AsyncAsyncResource) -> None:
        self._async_ = async_

        self.create_job = async_to_raw_response_wrapper(
            async_.create_job,
        )
        self.delete_job = async_to_raw_response_wrapper(
            async_.delete_job,
        )
        self.get_job_status = async_to_raw_response_wrapper(
            async_.get_job_status,
        )
        self.list_jobs = async_to_raw_response_wrapper(
            async_.list_jobs,
        )


class AsyncResourceWithStreamingResponse:
    def __init__(self, async_: AsyncResource) -> None:
        self._async_ = async_

        self.create_job = to_streamed_response_wrapper(
            async_.create_job,
        )
        self.delete_job = to_streamed_response_wrapper(
            async_.delete_job,
        )
        self.get_job_status = to_streamed_response_wrapper(
            async_.get_job_status,
        )
        self.list_jobs = to_streamed_response_wrapper(
            async_.list_jobs,
        )


class AsyncAsyncResourceWithStreamingResponse:
    def __init__(self, async_: AsyncAsyncResource) -> None:
        self._async_ = async_

        self.create_job = async_to_streamed_response_wrapper(
            async_.create_job,
        )
        self.delete_job = async_to_streamed_response_wrapper(
            async_.delete_job,
        )
        self.get_job_status = async_to_streamed_response_wrapper(
            async_.get_job_status,
        )
        self.list_jobs = async_to_streamed_response_wrapper(
            async_.list_jobs,
        )
