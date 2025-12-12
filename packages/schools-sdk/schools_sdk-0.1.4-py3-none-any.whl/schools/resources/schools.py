# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import (
    school_list_params,
    school_search_params,
    school_by_city_params,
    school_by_status_params,
    school_by_suburb_params,
    school_by_authority_params,
)
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.school_list_response import SchoolListResponse
from ..types.school_search_response import SchoolSearchResponse
from ..types.school_retrieve_response import SchoolRetrieveResponse

__all__ = ["SchoolsResource", "AsyncSchoolsResource"]


class SchoolsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SchoolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/et0and/schools-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SchoolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SchoolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/et0and/schools-sdk-python#with_streaming_response
        """
        return SchoolsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        school_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SchoolRetrieveResponse:
        """
        Get school by School ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not school_id:
            raise ValueError(f"Expected a non-empty value for `school_id` but received {school_id!r}")
        return self._get(
            f"/v1/schools/id/{school_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchoolRetrieveResponse,
        )

    def list(
        self,
        *,
        authority: str | Omit = omit,
        city: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        org_type: str | Omit = omit,
        page: int | Omit = omit,
        status: str | Omit = omit,
        suburb: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SchoolListResponse:
        """
        Get all schools with filtering

        Args:
          authority: Filter by education authority

          city: Filter by city (partial match)

          limit: Results per page (default: 20, max: 100)

          name: Filter by school name (partial match)

          org_type: Filter by organization type

          page: Page number (default: 1)

          status: Filter by school status

          suburb: Filter by suburb (partial match)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/schools",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "authority": authority,
                        "city": city,
                        "limit": limit,
                        "name": name,
                        "org_type": org_type,
                        "page": page,
                        "status": status,
                        "suburb": suburb,
                    },
                    school_list_params.SchoolListParams,
                ),
            ),
            cast_to=SchoolListResponse,
        )

    def by_authority(
        self,
        authority: str,
        *,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Get schools by authority

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not authority:
            raise ValueError(f"Expected a non-empty value for `authority` but received {authority!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/v1/schools/authority/{authority}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    school_by_authority_params.SchoolByAuthorityParams,
                ),
            ),
            cast_to=NoneType,
        )

    def by_city(
        self,
        city: str,
        *,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Get schools by city

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not city:
            raise ValueError(f"Expected a non-empty value for `city` but received {city!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/v1/schools/city/{city}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    school_by_city_params.SchoolByCityParams,
                ),
            ),
            cast_to=NoneType,
        )

    def by_status(
        self,
        status: str,
        *,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Get schools by status

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not status:
            raise ValueError(f"Expected a non-empty value for `status` but received {status!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/v1/schools/status/{status}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    school_by_status_params.SchoolByStatusParams,
                ),
            ),
            cast_to=NoneType,
        )

    def by_suburb(
        self,
        suburb: str,
        *,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Get schools by suburb

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not suburb:
            raise ValueError(f"Expected a non-empty value for `suburb` but received {suburb!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/v1/schools/suburb/{suburb}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    school_by_suburb_params.SchoolBySuburbParams,
                ),
            ),
            cast_to=NoneType,
        )

    def search(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SchoolSearchResponse:
        """
        Full-text search schools by name

        Args:
          q: Search query

          limit: Results per page (default: 20, max: 100)

          page: Page number (default: 1)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/schools/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "q": q,
                        "limit": limit,
                        "page": page,
                    },
                    school_search_params.SchoolSearchParams,
                ),
            ),
            cast_to=SchoolSearchResponse,
        )


class AsyncSchoolsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSchoolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/et0and/schools-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSchoolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSchoolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/et0and/schools-sdk-python#with_streaming_response
        """
        return AsyncSchoolsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        school_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SchoolRetrieveResponse:
        """
        Get school by School ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not school_id:
            raise ValueError(f"Expected a non-empty value for `school_id` but received {school_id!r}")
        return await self._get(
            f"/v1/schools/id/{school_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchoolRetrieveResponse,
        )

    async def list(
        self,
        *,
        authority: str | Omit = omit,
        city: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        org_type: str | Omit = omit,
        page: int | Omit = omit,
        status: str | Omit = omit,
        suburb: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SchoolListResponse:
        """
        Get all schools with filtering

        Args:
          authority: Filter by education authority

          city: Filter by city (partial match)

          limit: Results per page (default: 20, max: 100)

          name: Filter by school name (partial match)

          org_type: Filter by organization type

          page: Page number (default: 1)

          status: Filter by school status

          suburb: Filter by suburb (partial match)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/schools",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "authority": authority,
                        "city": city,
                        "limit": limit,
                        "name": name,
                        "org_type": org_type,
                        "page": page,
                        "status": status,
                        "suburb": suburb,
                    },
                    school_list_params.SchoolListParams,
                ),
            ),
            cast_to=SchoolListResponse,
        )

    async def by_authority(
        self,
        authority: str,
        *,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Get schools by authority

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not authority:
            raise ValueError(f"Expected a non-empty value for `authority` but received {authority!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/v1/schools/authority/{authority}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    school_by_authority_params.SchoolByAuthorityParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def by_city(
        self,
        city: str,
        *,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Get schools by city

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not city:
            raise ValueError(f"Expected a non-empty value for `city` but received {city!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/v1/schools/city/{city}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    school_by_city_params.SchoolByCityParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def by_status(
        self,
        status: str,
        *,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Get schools by status

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not status:
            raise ValueError(f"Expected a non-empty value for `status` but received {status!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/v1/schools/status/{status}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    school_by_status_params.SchoolByStatusParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def by_suburb(
        self,
        suburb: str,
        *,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Get schools by suburb

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not suburb:
            raise ValueError(f"Expected a non-empty value for `suburb` but received {suburb!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/v1/schools/suburb/{suburb}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    school_by_suburb_params.SchoolBySuburbParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def search(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SchoolSearchResponse:
        """
        Full-text search schools by name

        Args:
          q: Search query

          limit: Results per page (default: 20, max: 100)

          page: Page number (default: 1)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/schools/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "q": q,
                        "limit": limit,
                        "page": page,
                    },
                    school_search_params.SchoolSearchParams,
                ),
            ),
            cast_to=SchoolSearchResponse,
        )


class SchoolsResourceWithRawResponse:
    def __init__(self, schools: SchoolsResource) -> None:
        self._schools = schools

        self.retrieve = to_raw_response_wrapper(
            schools.retrieve,
        )
        self.list = to_raw_response_wrapper(
            schools.list,
        )
        self.by_authority = to_raw_response_wrapper(
            schools.by_authority,
        )
        self.by_city = to_raw_response_wrapper(
            schools.by_city,
        )
        self.by_status = to_raw_response_wrapper(
            schools.by_status,
        )
        self.by_suburb = to_raw_response_wrapper(
            schools.by_suburb,
        )
        self.search = to_raw_response_wrapper(
            schools.search,
        )


class AsyncSchoolsResourceWithRawResponse:
    def __init__(self, schools: AsyncSchoolsResource) -> None:
        self._schools = schools

        self.retrieve = async_to_raw_response_wrapper(
            schools.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            schools.list,
        )
        self.by_authority = async_to_raw_response_wrapper(
            schools.by_authority,
        )
        self.by_city = async_to_raw_response_wrapper(
            schools.by_city,
        )
        self.by_status = async_to_raw_response_wrapper(
            schools.by_status,
        )
        self.by_suburb = async_to_raw_response_wrapper(
            schools.by_suburb,
        )
        self.search = async_to_raw_response_wrapper(
            schools.search,
        )


class SchoolsResourceWithStreamingResponse:
    def __init__(self, schools: SchoolsResource) -> None:
        self._schools = schools

        self.retrieve = to_streamed_response_wrapper(
            schools.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            schools.list,
        )
        self.by_authority = to_streamed_response_wrapper(
            schools.by_authority,
        )
        self.by_city = to_streamed_response_wrapper(
            schools.by_city,
        )
        self.by_status = to_streamed_response_wrapper(
            schools.by_status,
        )
        self.by_suburb = to_streamed_response_wrapper(
            schools.by_suburb,
        )
        self.search = to_streamed_response_wrapper(
            schools.search,
        )


class AsyncSchoolsResourceWithStreamingResponse:
    def __init__(self, schools: AsyncSchoolsResource) -> None:
        self._schools = schools

        self.retrieve = async_to_streamed_response_wrapper(
            schools.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            schools.list,
        )
        self.by_authority = async_to_streamed_response_wrapper(
            schools.by_authority,
        )
        self.by_city = async_to_streamed_response_wrapper(
            schools.by_city,
        )
        self.by_status = async_to_streamed_response_wrapper(
            schools.by_status,
        )
        self.by_suburb = async_to_streamed_response_wrapper(
            schools.by_suburb,
        )
        self.search = async_to_streamed_response_wrapper(
            schools.search,
        )
