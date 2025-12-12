# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from schools import Schools, AsyncSchools
from tests.utils import assert_matches_type
from schools.types import (
    SchoolListResponse,
    SchoolSearchResponse,
    SchoolRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSchools:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Schools) -> None:
        school = client.schools.retrieve(
            "schoolId",
        )
        assert_matches_type(SchoolRetrieveResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Schools) -> None:
        response = client.schools.with_raw_response.retrieve(
            "schoolId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = response.parse()
        assert_matches_type(SchoolRetrieveResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Schools) -> None:
        with client.schools.with_streaming_response.retrieve(
            "schoolId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = response.parse()
            assert_matches_type(SchoolRetrieveResponse, school, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Schools) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `school_id` but received ''"):
            client.schools.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Schools) -> None:
        school = client.schools.list()
        assert_matches_type(SchoolListResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Schools) -> None:
        school = client.schools.list(
            authority="authority",
            city="city",
            limit=1,
            name="name",
            org_type="org_type",
            page=1,
            status="status",
            suburb="suburb",
        )
        assert_matches_type(SchoolListResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Schools) -> None:
        response = client.schools.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = response.parse()
        assert_matches_type(SchoolListResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Schools) -> None:
        with client.schools.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = response.parse()
            assert_matches_type(SchoolListResponse, school, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_by_authority(self, client: Schools) -> None:
        school = client.schools.by_authority(
            authority="authority",
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_by_authority_with_all_params(self, client: Schools) -> None:
        school = client.schools.by_authority(
            authority="authority",
            limit=1,
            page=1,
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_by_authority(self, client: Schools) -> None:
        response = client.schools.with_raw_response.by_authority(
            authority="authority",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = response.parse()
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_by_authority(self, client: Schools) -> None:
        with client.schools.with_streaming_response.by_authority(
            authority="authority",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = response.parse()
            assert school is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_by_authority(self, client: Schools) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `authority` but received ''"):
            client.schools.with_raw_response.by_authority(
                authority="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_by_city(self, client: Schools) -> None:
        school = client.schools.by_city(
            city="city",
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_by_city_with_all_params(self, client: Schools) -> None:
        school = client.schools.by_city(
            city="city",
            limit=1,
            page=1,
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_by_city(self, client: Schools) -> None:
        response = client.schools.with_raw_response.by_city(
            city="city",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = response.parse()
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_by_city(self, client: Schools) -> None:
        with client.schools.with_streaming_response.by_city(
            city="city",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = response.parse()
            assert school is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_by_city(self, client: Schools) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `city` but received ''"):
            client.schools.with_raw_response.by_city(
                city="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_by_status(self, client: Schools) -> None:
        school = client.schools.by_status(
            status="status",
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_by_status_with_all_params(self, client: Schools) -> None:
        school = client.schools.by_status(
            status="status",
            limit=1,
            page=1,
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_by_status(self, client: Schools) -> None:
        response = client.schools.with_raw_response.by_status(
            status="status",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = response.parse()
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_by_status(self, client: Schools) -> None:
        with client.schools.with_streaming_response.by_status(
            status="status",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = response.parse()
            assert school is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_by_status(self, client: Schools) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `status` but received ''"):
            client.schools.with_raw_response.by_status(
                status="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_by_suburb(self, client: Schools) -> None:
        school = client.schools.by_suburb(
            suburb="suburb",
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_by_suburb_with_all_params(self, client: Schools) -> None:
        school = client.schools.by_suburb(
            suburb="suburb",
            limit=1,
            page=1,
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_by_suburb(self, client: Schools) -> None:
        response = client.schools.with_raw_response.by_suburb(
            suburb="suburb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = response.parse()
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_by_suburb(self, client: Schools) -> None:
        with client.schools.with_streaming_response.by_suburb(
            suburb="suburb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = response.parse()
            assert school is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_by_suburb(self, client: Schools) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `suburb` but received ''"):
            client.schools.with_raw_response.by_suburb(
                suburb="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search(self, client: Schools) -> None:
        school = client.schools.search(
            q="x",
        )
        assert_matches_type(SchoolSearchResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_with_all_params(self, client: Schools) -> None:
        school = client.schools.search(
            q="x",
            limit=1,
            page=1,
        )
        assert_matches_type(SchoolSearchResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search(self, client: Schools) -> None:
        response = client.schools.with_raw_response.search(
            q="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = response.parse()
        assert_matches_type(SchoolSearchResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search(self, client: Schools) -> None:
        with client.schools.with_streaming_response.search(
            q="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = response.parse()
            assert_matches_type(SchoolSearchResponse, school, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSchools:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.retrieve(
            "schoolId",
        )
        assert_matches_type(SchoolRetrieveResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSchools) -> None:
        response = await async_client.schools.with_raw_response.retrieve(
            "schoolId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = await response.parse()
        assert_matches_type(SchoolRetrieveResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSchools) -> None:
        async with async_client.schools.with_streaming_response.retrieve(
            "schoolId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = await response.parse()
            assert_matches_type(SchoolRetrieveResponse, school, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSchools) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `school_id` but received ''"):
            await async_client.schools.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.list()
        assert_matches_type(SchoolListResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.list(
            authority="authority",
            city="city",
            limit=1,
            name="name",
            org_type="org_type",
            page=1,
            status="status",
            suburb="suburb",
        )
        assert_matches_type(SchoolListResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSchools) -> None:
        response = await async_client.schools.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = await response.parse()
        assert_matches_type(SchoolListResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSchools) -> None:
        async with async_client.schools.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = await response.parse()
            assert_matches_type(SchoolListResponse, school, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_by_authority(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.by_authority(
            authority="authority",
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_by_authority_with_all_params(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.by_authority(
            authority="authority",
            limit=1,
            page=1,
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_by_authority(self, async_client: AsyncSchools) -> None:
        response = await async_client.schools.with_raw_response.by_authority(
            authority="authority",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = await response.parse()
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_by_authority(self, async_client: AsyncSchools) -> None:
        async with async_client.schools.with_streaming_response.by_authority(
            authority="authority",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = await response.parse()
            assert school is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_by_authority(self, async_client: AsyncSchools) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `authority` but received ''"):
            await async_client.schools.with_raw_response.by_authority(
                authority="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_by_city(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.by_city(
            city="city",
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_by_city_with_all_params(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.by_city(
            city="city",
            limit=1,
            page=1,
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_by_city(self, async_client: AsyncSchools) -> None:
        response = await async_client.schools.with_raw_response.by_city(
            city="city",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = await response.parse()
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_by_city(self, async_client: AsyncSchools) -> None:
        async with async_client.schools.with_streaming_response.by_city(
            city="city",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = await response.parse()
            assert school is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_by_city(self, async_client: AsyncSchools) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `city` but received ''"):
            await async_client.schools.with_raw_response.by_city(
                city="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_by_status(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.by_status(
            status="status",
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_by_status_with_all_params(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.by_status(
            status="status",
            limit=1,
            page=1,
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_by_status(self, async_client: AsyncSchools) -> None:
        response = await async_client.schools.with_raw_response.by_status(
            status="status",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = await response.parse()
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_by_status(self, async_client: AsyncSchools) -> None:
        async with async_client.schools.with_streaming_response.by_status(
            status="status",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = await response.parse()
            assert school is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_by_status(self, async_client: AsyncSchools) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `status` but received ''"):
            await async_client.schools.with_raw_response.by_status(
                status="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_by_suburb(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.by_suburb(
            suburb="suburb",
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_by_suburb_with_all_params(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.by_suburb(
            suburb="suburb",
            limit=1,
            page=1,
        )
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_by_suburb(self, async_client: AsyncSchools) -> None:
        response = await async_client.schools.with_raw_response.by_suburb(
            suburb="suburb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = await response.parse()
        assert school is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_by_suburb(self, async_client: AsyncSchools) -> None:
        async with async_client.schools.with_streaming_response.by_suburb(
            suburb="suburb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = await response.parse()
            assert school is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_by_suburb(self, async_client: AsyncSchools) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `suburb` but received ''"):
            await async_client.schools.with_raw_response.by_suburb(
                suburb="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.search(
            q="x",
        )
        assert_matches_type(SchoolSearchResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncSchools) -> None:
        school = await async_client.schools.search(
            q="x",
            limit=1,
            page=1,
        )
        assert_matches_type(SchoolSearchResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search(self, async_client: AsyncSchools) -> None:
        response = await async_client.schools.with_raw_response.search(
            q="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        school = await response.parse()
        assert_matches_type(SchoolSearchResponse, school, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncSchools) -> None:
        async with async_client.schools.with_streaming_response.search(
            q="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            school = await response.parse()
            assert_matches_type(SchoolSearchResponse, school, path=["response"])

        assert cast(Any, response.is_closed) is True
