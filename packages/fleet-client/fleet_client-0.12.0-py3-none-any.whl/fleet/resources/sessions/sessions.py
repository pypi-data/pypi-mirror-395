# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .page import (
    PageResource,
    AsyncPageResource,
    PageResourceWithRawResponse,
    AsyncPageResourceWithRawResponse,
    PageResourceWithStreamingResponse,
    AsyncPageResourceWithStreamingResponse,
)
from .start import (
    StartResource,
    AsyncStartResource,
    StartResourceWithRawResponse,
    AsyncStartResourceWithRawResponse,
    StartResourceWithStreamingResponse,
    AsyncStartResourceWithStreamingResponse,
)
from ...types import session_create_params, session_visit_page_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .responses import (
    ResponsesResource,
    AsyncResponsesResource,
    ResponsesResourceWithRawResponse,
    AsyncResponsesResourceWithRawResponse,
    ResponsesResourceWithStreamingResponse,
    AsyncResponsesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .scrape.scrape import (
    ScrapeResource,
    AsyncScrapeResource,
    ScrapeResourceWithRawResponse,
    AsyncScrapeResourceWithRawResponse,
    ScrapeResourceWithStreamingResponse,
    AsyncScrapeResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from ...types.workflows import WaitUntil
from ...types.workflows.wait_until import WaitUntil
from ...types.session_list_response import SessionListResponse
from ...types.session_create_response import SessionCreateResponse
from ...types.session_delete_response import SessionDeleteResponse
from ...types.session_warm_up_response import SessionWarmUpResponse
from ...types.session_retrieve_response import SessionRetrieveResponse
from ...types.browser_configuration_param import BrowserConfigurationParam
from ...types.session_visit_page_response import SessionVisitPageResponse

__all__ = ["SessionsResource", "AsyncSessionsResource"]


class SessionsResource(SyncAPIResource):
    @cached_property
    def start(self) -> StartResource:
        return StartResource(self._client)

    @cached_property
    def page(self) -> PageResource:
        return PageResource(self._client)

    @cached_property
    def responses(self) -> ResponsesResource:
        return ResponsesResource(self._client)

    @cached_property
    def scrape(self) -> ScrapeResource:
        return ScrapeResource(self._client)

    @cached_property
    def with_raw_response(self) -> SessionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return SessionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return SessionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        browser_configuration: BrowserConfigurationParam,
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
    ) -> SessionCreateResponse:
        """
        Create a new session without starting it.

        Args:
          browser_configuration: Browser configuration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/sessions/",
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
                session_create_params.SessionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCreateResponse,
        )

    def retrieve(
        self,
        session_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionRetrieveResponse:
        """
        Get a specific session's information.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get(
            f"/sessions/{session_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionRetrieveResponse,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionListResponse:
        """List all active sessions."""
        return self._get(
            "/sessions/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionListResponse,
        )

    def delete(
        self,
        session_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionDeleteResponse:
        """
        Delete a session and close its browser.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._delete(
            f"/sessions/{session_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionDeleteResponse,
        )

    def visit_page(
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
    ) -> SessionVisitPageResponse:
        """
        Post Visit Page

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._post(
            f"/sessions/{session_id}/visit",
            body=maybe_transform(
                {
                    "url": url,
                    "wait_until": wait_until,
                },
                session_visit_page_params.SessionVisitPageParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionVisitPageResponse,
        )

    def warm_up(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionWarmUpResponse:
        """Warm up all sessions with initial browser requests."""
        return self._post(
            "/sessions/warm-up",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionWarmUpResponse,
        )


class AsyncSessionsResource(AsyncAPIResource):
    @cached_property
    def start(self) -> AsyncStartResource:
        return AsyncStartResource(self._client)

    @cached_property
    def page(self) -> AsyncPageResource:
        return AsyncPageResource(self._client)

    @cached_property
    def responses(self) -> AsyncResponsesResource:
        return AsyncResponsesResource(self._client)

    @cached_property
    def scrape(self) -> AsyncScrapeResource:
        return AsyncScrapeResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSessionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return AsyncSessionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return AsyncSessionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        browser_configuration: BrowserConfigurationParam,
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
    ) -> SessionCreateResponse:
        """
        Create a new session without starting it.

        Args:
          browser_configuration: Browser configuration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/sessions/",
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
                session_create_params.SessionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCreateResponse,
        )

    async def retrieve(
        self,
        session_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionRetrieveResponse:
        """
        Get a specific session's information.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._get(
            f"/sessions/{session_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionRetrieveResponse,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionListResponse:
        """List all active sessions."""
        return await self._get(
            "/sessions/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionListResponse,
        )

    async def delete(
        self,
        session_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionDeleteResponse:
        """
        Delete a session and close its browser.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._delete(
            f"/sessions/{session_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionDeleteResponse,
        )

    async def visit_page(
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
    ) -> SessionVisitPageResponse:
        """
        Post Visit Page

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._post(
            f"/sessions/{session_id}/visit",
            body=await async_maybe_transform(
                {
                    "url": url,
                    "wait_until": wait_until,
                },
                session_visit_page_params.SessionVisitPageParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionVisitPageResponse,
        )

    async def warm_up(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionWarmUpResponse:
        """Warm up all sessions with initial browser requests."""
        return await self._post(
            "/sessions/warm-up",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionWarmUpResponse,
        )


class SessionsResourceWithRawResponse:
    def __init__(self, sessions: SessionsResource) -> None:
        self._sessions = sessions

        self.create = to_raw_response_wrapper(
            sessions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            sessions.retrieve,
        )
        self.list = to_raw_response_wrapper(
            sessions.list,
        )
        self.delete = to_raw_response_wrapper(
            sessions.delete,
        )
        self.visit_page = to_raw_response_wrapper(
            sessions.visit_page,
        )
        self.warm_up = to_raw_response_wrapper(
            sessions.warm_up,
        )

    @cached_property
    def start(self) -> StartResourceWithRawResponse:
        return StartResourceWithRawResponse(self._sessions.start)

    @cached_property
    def page(self) -> PageResourceWithRawResponse:
        return PageResourceWithRawResponse(self._sessions.page)

    @cached_property
    def responses(self) -> ResponsesResourceWithRawResponse:
        return ResponsesResourceWithRawResponse(self._sessions.responses)

    @cached_property
    def scrape(self) -> ScrapeResourceWithRawResponse:
        return ScrapeResourceWithRawResponse(self._sessions.scrape)


class AsyncSessionsResourceWithRawResponse:
    def __init__(self, sessions: AsyncSessionsResource) -> None:
        self._sessions = sessions

        self.create = async_to_raw_response_wrapper(
            sessions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            sessions.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            sessions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            sessions.delete,
        )
        self.visit_page = async_to_raw_response_wrapper(
            sessions.visit_page,
        )
        self.warm_up = async_to_raw_response_wrapper(
            sessions.warm_up,
        )

    @cached_property
    def start(self) -> AsyncStartResourceWithRawResponse:
        return AsyncStartResourceWithRawResponse(self._sessions.start)

    @cached_property
    def page(self) -> AsyncPageResourceWithRawResponse:
        return AsyncPageResourceWithRawResponse(self._sessions.page)

    @cached_property
    def responses(self) -> AsyncResponsesResourceWithRawResponse:
        return AsyncResponsesResourceWithRawResponse(self._sessions.responses)

    @cached_property
    def scrape(self) -> AsyncScrapeResourceWithRawResponse:
        return AsyncScrapeResourceWithRawResponse(self._sessions.scrape)


class SessionsResourceWithStreamingResponse:
    def __init__(self, sessions: SessionsResource) -> None:
        self._sessions = sessions

        self.create = to_streamed_response_wrapper(
            sessions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            sessions.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            sessions.list,
        )
        self.delete = to_streamed_response_wrapper(
            sessions.delete,
        )
        self.visit_page = to_streamed_response_wrapper(
            sessions.visit_page,
        )
        self.warm_up = to_streamed_response_wrapper(
            sessions.warm_up,
        )

    @cached_property
    def start(self) -> StartResourceWithStreamingResponse:
        return StartResourceWithStreamingResponse(self._sessions.start)

    @cached_property
    def page(self) -> PageResourceWithStreamingResponse:
        return PageResourceWithStreamingResponse(self._sessions.page)

    @cached_property
    def responses(self) -> ResponsesResourceWithStreamingResponse:
        return ResponsesResourceWithStreamingResponse(self._sessions.responses)

    @cached_property
    def scrape(self) -> ScrapeResourceWithStreamingResponse:
        return ScrapeResourceWithStreamingResponse(self._sessions.scrape)


class AsyncSessionsResourceWithStreamingResponse:
    def __init__(self, sessions: AsyncSessionsResource) -> None:
        self._sessions = sessions

        self.create = async_to_streamed_response_wrapper(
            sessions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            sessions.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            sessions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            sessions.delete,
        )
        self.visit_page = async_to_streamed_response_wrapper(
            sessions.visit_page,
        )
        self.warm_up = async_to_streamed_response_wrapper(
            sessions.warm_up,
        )

    @cached_property
    def start(self) -> AsyncStartResourceWithStreamingResponse:
        return AsyncStartResourceWithStreamingResponse(self._sessions.start)

    @cached_property
    def page(self) -> AsyncPageResourceWithStreamingResponse:
        return AsyncPageResourceWithStreamingResponse(self._sessions.page)

    @cached_property
    def responses(self) -> AsyncResponsesResourceWithStreamingResponse:
        return AsyncResponsesResourceWithStreamingResponse(self._sessions.responses)

    @cached_property
    def scrape(self) -> AsyncScrapeResourceWithStreamingResponse:
        return AsyncScrapeResourceWithStreamingResponse(self._sessions.scrape)
