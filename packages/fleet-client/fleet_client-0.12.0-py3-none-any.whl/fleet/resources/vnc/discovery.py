# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["DiscoveryResource", "AsyncDiscoveryResource"]


class DiscoveryResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DiscoveryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return DiscoveryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DiscoveryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return DiscoveryResourceWithStreamingResponse(self)

    def trigger(
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
        Manually trigger VNC session discovery.

        This forces the VNC aggregator to immediately scan all worker pods for active
        VNC sessions. Useful for testing or immediate updates.
        """
        return self._post(
            "/vnc/discovery/trigger",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncDiscoveryResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDiscoveryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/fleet-client#accessing-raw-response-data-eg-headers
        """
        return AsyncDiscoveryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDiscoveryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/fleet-client#with_streaming_response
        """
        return AsyncDiscoveryResourceWithStreamingResponse(self)

    async def trigger(
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
        Manually trigger VNC session discovery.

        This forces the VNC aggregator to immediately scan all worker pods for active
        VNC sessions. Useful for testing or immediate updates.
        """
        return await self._post(
            "/vnc/discovery/trigger",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class DiscoveryResourceWithRawResponse:
    def __init__(self, discovery: DiscoveryResource) -> None:
        self._discovery = discovery

        self.trigger = to_raw_response_wrapper(
            discovery.trigger,
        )


class AsyncDiscoveryResourceWithRawResponse:
    def __init__(self, discovery: AsyncDiscoveryResource) -> None:
        self._discovery = discovery

        self.trigger = async_to_raw_response_wrapper(
            discovery.trigger,
        )


class DiscoveryResourceWithStreamingResponse:
    def __init__(self, discovery: DiscoveryResource) -> None:
        self._discovery = discovery

        self.trigger = to_streamed_response_wrapper(
            discovery.trigger,
        )


class AsyncDiscoveryResourceWithStreamingResponse:
    def __init__(self, discovery: AsyncDiscoveryResource) -> None:
        self._discovery = discovery

        self.trigger = async_to_streamed_response_wrapper(
            discovery.trigger,
        )
