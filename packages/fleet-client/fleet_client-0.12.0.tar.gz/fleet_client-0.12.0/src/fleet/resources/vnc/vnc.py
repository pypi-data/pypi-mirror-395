# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from .sessions import (
    SessionsResource,
    AsyncSessionsResource,
    SessionsResourceWithRawResponse,
    AsyncSessionsResourceWithRawResponse,
    SessionsResourceWithStreamingResponse,
    AsyncSessionsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .discovery import (
    DiscoveryResource,
    AsyncDiscoveryResource,
    DiscoveryResourceWithRawResponse,
    AsyncDiscoveryResourceWithRawResponse,
    DiscoveryResourceWithStreamingResponse,
    AsyncDiscoveryResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["VncResource", "AsyncVncResource"]


class VncResource(SyncAPIResource):
    @cached_property
    def sessions(self) -> SessionsResource:
        return SessionsResource(self._client)

    @cached_property
    def discovery(self) -> DiscoveryResource:
        return DiscoveryResource(self._client)

    @cached_property
    def with_raw_response(self) -> VncResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return VncResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VncResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return VncResourceWithStreamingResponse(self)

    def check_health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Health check for VNC proxy functionality.

        Tests connectivity to the VNC aggregator service.
        """
        return self._get(
            "/vnc/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncVncResource(AsyncAPIResource):
    @cached_property
    def sessions(self) -> AsyncSessionsResource:
        return AsyncSessionsResource(self._client)

    @cached_property
    def discovery(self) -> AsyncDiscoveryResource:
        return AsyncDiscoveryResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncVncResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return AsyncVncResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVncResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return AsyncVncResourceWithStreamingResponse(self)

    async def check_health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Health check for VNC proxy functionality.

        Tests connectivity to the VNC aggregator service.
        """
        return await self._get(
            "/vnc/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class VncResourceWithRawResponse:
    def __init__(self, vnc: VncResource) -> None:
        self._vnc = vnc

        self.check_health = to_raw_response_wrapper(
            vnc.check_health,
        )

    @cached_property
    def sessions(self) -> SessionsResourceWithRawResponse:
        return SessionsResourceWithRawResponse(self._vnc.sessions)

    @cached_property
    def discovery(self) -> DiscoveryResourceWithRawResponse:
        return DiscoveryResourceWithRawResponse(self._vnc.discovery)


class AsyncVncResourceWithRawResponse:
    def __init__(self, vnc: AsyncVncResource) -> None:
        self._vnc = vnc

        self.check_health = async_to_raw_response_wrapper(
            vnc.check_health,
        )

    @cached_property
    def sessions(self) -> AsyncSessionsResourceWithRawResponse:
        return AsyncSessionsResourceWithRawResponse(self._vnc.sessions)

    @cached_property
    def discovery(self) -> AsyncDiscoveryResourceWithRawResponse:
        return AsyncDiscoveryResourceWithRawResponse(self._vnc.discovery)


class VncResourceWithStreamingResponse:
    def __init__(self, vnc: VncResource) -> None:
        self._vnc = vnc

        self.check_health = to_streamed_response_wrapper(
            vnc.check_health,
        )

    @cached_property
    def sessions(self) -> SessionsResourceWithStreamingResponse:
        return SessionsResourceWithStreamingResponse(self._vnc.sessions)

    @cached_property
    def discovery(self) -> DiscoveryResourceWithStreamingResponse:
        return DiscoveryResourceWithStreamingResponse(self._vnc.discovery)


class AsyncVncResourceWithStreamingResponse:
    def __init__(self, vnc: AsyncVncResource) -> None:
        self._vnc = vnc

        self.check_health = async_to_streamed_response_wrapper(
            vnc.check_health,
        )

    @cached_property
    def sessions(self) -> AsyncSessionsResourceWithStreamingResponse:
        return AsyncSessionsResourceWithStreamingResponse(self._vnc.sessions)

    @cached_property
    def discovery(self) -> AsyncDiscoveryResourceWithStreamingResponse:
        return AsyncDiscoveryResourceWithStreamingResponse(self._vnc.discovery)
