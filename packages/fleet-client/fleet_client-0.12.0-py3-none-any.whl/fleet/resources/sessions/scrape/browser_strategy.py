# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import Body, Query, Headers, NotGiven, not_given
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
from ....types.sessions import BrowserSelectionStrategy
from ....types.sessions.scrape import browser_strategy_set_params
from ....types.sessions.scrape.response import Response
from ....types.sessions.browser_selection_strategy import BrowserSelectionStrategy

__all__ = ["BrowserStrategyResource", "AsyncBrowserStrategyResource"]


class BrowserStrategyResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BrowserStrategyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return BrowserStrategyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BrowserStrategyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return BrowserStrategyResourceWithStreamingResponse(self)

    def get(
        self,
        session_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Response:
        """
        Get the current browser selection strategy for async scraping jobs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get(
            f"/sessions/{session_id}/scrape/browser-strategy",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Response,
        )

    def set(
        self,
        session_id: str,
        *,
        strategy: BrowserSelectionStrategy,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Response:
        """
        Set the browser selection strategy for async scraping jobs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._post(
            f"/sessions/{session_id}/scrape/browser-strategy",
            body=maybe_transform({"strategy": strategy}, browser_strategy_set_params.BrowserStrategySetParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Response,
        )


class AsyncBrowserStrategyResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBrowserStrategyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return AsyncBrowserStrategyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBrowserStrategyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return AsyncBrowserStrategyResourceWithStreamingResponse(self)

    async def get(
        self,
        session_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Response:
        """
        Get the current browser selection strategy for async scraping jobs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._get(
            f"/sessions/{session_id}/scrape/browser-strategy",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Response,
        )

    async def set(
        self,
        session_id: str,
        *,
        strategy: BrowserSelectionStrategy,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Response:
        """
        Set the browser selection strategy for async scraping jobs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._post(
            f"/sessions/{session_id}/scrape/browser-strategy",
            body=await async_maybe_transform(
                {"strategy": strategy}, browser_strategy_set_params.BrowserStrategySetParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Response,
        )


class BrowserStrategyResourceWithRawResponse:
    def __init__(self, browser_strategy: BrowserStrategyResource) -> None:
        self._browser_strategy = browser_strategy

        self.get = to_raw_response_wrapper(
            browser_strategy.get,
        )
        self.set = to_raw_response_wrapper(
            browser_strategy.set,
        )


class AsyncBrowserStrategyResourceWithRawResponse:
    def __init__(self, browser_strategy: AsyncBrowserStrategyResource) -> None:
        self._browser_strategy = browser_strategy

        self.get = async_to_raw_response_wrapper(
            browser_strategy.get,
        )
        self.set = async_to_raw_response_wrapper(
            browser_strategy.set,
        )


class BrowserStrategyResourceWithStreamingResponse:
    def __init__(self, browser_strategy: BrowserStrategyResource) -> None:
        self._browser_strategy = browser_strategy

        self.get = to_streamed_response_wrapper(
            browser_strategy.get,
        )
        self.set = to_streamed_response_wrapper(
            browser_strategy.set,
        )


class AsyncBrowserStrategyResourceWithStreamingResponse:
    def __init__(self, browser_strategy: AsyncBrowserStrategyResource) -> None:
        self._browser_strategy = browser_strategy

        self.get = async_to_streamed_response_wrapper(
            browser_strategy.get,
        )
        self.set = async_to_streamed_response_wrapper(
            browser_strategy.set,
        )
