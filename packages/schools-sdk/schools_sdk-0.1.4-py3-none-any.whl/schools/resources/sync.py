# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.sync_trigger_response import SyncTriggerResponse
from ..types.sync_get_status_response import SyncGetStatusResponse

__all__ = ["SyncResource", "AsyncSyncResource"]


class SyncResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SyncResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/et0and/schools-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SyncResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SyncResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/et0and/schools-sdk-python#with_streaming_response
        """
        return SyncResourceWithStreamingResponse(self)

    def get_status(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncGetStatusResponse:
        """Get sync status"""
        return self._get(
            "/v1/sync/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SyncGetStatusResponse,
        )

    def trigger(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncTriggerResponse:
        """Trigger manual data sync"""
        return self._post(
            "/v1/sync",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SyncTriggerResponse,
        )


class AsyncSyncResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSyncResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/et0and/schools-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSyncResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSyncResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/et0and/schools-sdk-python#with_streaming_response
        """
        return AsyncSyncResourceWithStreamingResponse(self)

    async def get_status(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncGetStatusResponse:
        """Get sync status"""
        return await self._get(
            "/v1/sync/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SyncGetStatusResponse,
        )

    async def trigger(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncTriggerResponse:
        """Trigger manual data sync"""
        return await self._post(
            "/v1/sync",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SyncTriggerResponse,
        )


class SyncResourceWithRawResponse:
    def __init__(self, sync: SyncResource) -> None:
        self._sync = sync

        self.get_status = to_raw_response_wrapper(
            sync.get_status,
        )
        self.trigger = to_raw_response_wrapper(
            sync.trigger,
        )


class AsyncSyncResourceWithRawResponse:
    def __init__(self, sync: AsyncSyncResource) -> None:
        self._sync = sync

        self.get_status = async_to_raw_response_wrapper(
            sync.get_status,
        )
        self.trigger = async_to_raw_response_wrapper(
            sync.trigger,
        )


class SyncResourceWithStreamingResponse:
    def __init__(self, sync: SyncResource) -> None:
        self._sync = sync

        self.get_status = to_streamed_response_wrapper(
            sync.get_status,
        )
        self.trigger = to_streamed_response_wrapper(
            sync.trigger,
        )


class AsyncSyncResourceWithStreamingResponse:
    def __init__(self, sync: AsyncSyncResource) -> None:
        self._sync = sync

        self.get_status = async_to_streamed_response_wrapper(
            sync.get_status,
        )
        self.trigger = async_to_streamed_response_wrapper(
            sync.trigger,
        )
