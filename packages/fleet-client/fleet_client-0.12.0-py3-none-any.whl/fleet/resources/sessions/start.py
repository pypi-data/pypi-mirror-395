# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.sessions import start_new_params, start_existing_params
from ...types.browser_configuration_param import BrowserConfigurationParam
from ...types.sessions.start_new_response import StartNewResponse
from ...types.sessions.start_existing_response import StartExistingResponse

__all__ = ["StartResource", "AsyncStartResource"]


class StartResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StartResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return StartResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StartResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return StartResourceWithStreamingResponse(self)

    def existing(
        self,
        session_id: str,
        *,
        url: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StartExistingResponse:
        """
        Start an existing session that was previously created.

        Args:
          url: Initial URL to navigate to

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._post(
            f"/sessions/{session_id}/start",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"url": url}, start_existing_params.StartExistingParams),
            ),
            cast_to=StartExistingResponse,
        )

    def new(
        self,
        *,
        browser_configuration: BrowserConfigurationParam,
        url: str | Omit = omit,
        agentic: bool | Omit = omit,
        enable_xvfb: bool | Omit = omit,
        n_responses_to_track: int | Omit = omit,
        proxy_password: str | Omit = omit,
        proxy_url: str | Omit = omit,
        proxy_username: str | Omit = omit,
        vnc_password: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StartNewResponse:
        """
        Create and immediately start a new session with a browser.

        Args:
          browser_configuration: Browser configuration.

          url: Initial URL to navigate to

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/sessions/start",
            body=maybe_transform(
                {
                    "browser_configuration": browser_configuration,
                    "agentic": agentic,
                    "enable_xvfb": enable_xvfb,
                    "n_responses_to_track": n_responses_to_track,
                    "proxy_password": proxy_password,
                    "proxy_url": proxy_url,
                    "proxy_username": proxy_username,
                    "vnc_password": vnc_password,
                },
                start_new_params.StartNewParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"url": url}, start_new_params.StartNewParams),
            ),
            cast_to=StartNewResponse,
        )


class AsyncStartResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStartResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return AsyncStartResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStartResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return AsyncStartResourceWithStreamingResponse(self)

    async def existing(
        self,
        session_id: str,
        *,
        url: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StartExistingResponse:
        """
        Start an existing session that was previously created.

        Args:
          url: Initial URL to navigate to

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._post(
            f"/sessions/{session_id}/start",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"url": url}, start_existing_params.StartExistingParams),
            ),
            cast_to=StartExistingResponse,
        )

    async def new(
        self,
        *,
        browser_configuration: BrowserConfigurationParam,
        url: str | Omit = omit,
        agentic: bool | Omit = omit,
        enable_xvfb: bool | Omit = omit,
        n_responses_to_track: int | Omit = omit,
        proxy_password: str | Omit = omit,
        proxy_url: str | Omit = omit,
        proxy_username: str | Omit = omit,
        vnc_password: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StartNewResponse:
        """
        Create and immediately start a new session with a browser.

        Args:
          browser_configuration: Browser configuration.

          url: Initial URL to navigate to

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/sessions/start",
            body=await async_maybe_transform(
                {
                    "browser_configuration": browser_configuration,
                    "agentic": agentic,
                    "enable_xvfb": enable_xvfb,
                    "n_responses_to_track": n_responses_to_track,
                    "proxy_password": proxy_password,
                    "proxy_url": proxy_url,
                    "proxy_username": proxy_username,
                    "vnc_password": vnc_password,
                },
                start_new_params.StartNewParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"url": url}, start_new_params.StartNewParams),
            ),
            cast_to=StartNewResponse,
        )


class StartResourceWithRawResponse:
    def __init__(self, start: StartResource) -> None:
        self._start = start

        self.existing = to_raw_response_wrapper(
            start.existing,
        )
        self.new = to_raw_response_wrapper(
            start.new,
        )


class AsyncStartResourceWithRawResponse:
    def __init__(self, start: AsyncStartResource) -> None:
        self._start = start

        self.existing = async_to_raw_response_wrapper(
            start.existing,
        )
        self.new = async_to_raw_response_wrapper(
            start.new,
        )


class StartResourceWithStreamingResponse:
    def __init__(self, start: StartResource) -> None:
        self._start = start

        self.existing = to_streamed_response_wrapper(
            start.existing,
        )
        self.new = to_streamed_response_wrapper(
            start.new,
        )


class AsyncStartResourceWithStreamingResponse:
    def __init__(self, start: AsyncStartResource) -> None:
        self._start = start

        self.existing = async_to_streamed_response_wrapper(
            start.existing,
        )
        self.new = async_to_streamed_response_wrapper(
            start.new,
        )
