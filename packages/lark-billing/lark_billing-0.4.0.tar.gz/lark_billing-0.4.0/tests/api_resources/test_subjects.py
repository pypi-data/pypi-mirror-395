# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lark import Lark, AsyncLark
from lark.types import (
    SubjectResource,
    SubjectListResponse,
    SubjectCreateResponse,
)
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSubjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Lark) -> None:
        subject = client.subjects.create()
        assert_matches_type(SubjectCreateResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Lark) -> None:
        subject = client.subjects.create(
            email="john.doe@example.com",
            external_id="user_1234567890",
            metadata={},
            name="John Doe",
        )
        assert_matches_type(SubjectCreateResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Lark) -> None:
        response = client.subjects.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = response.parse()
        assert_matches_type(SubjectCreateResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Lark) -> None:
        with client.subjects.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = response.parse()
            assert_matches_type(SubjectCreateResponse, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Lark) -> None:
        subject = client.subjects.retrieve(
            "subject_id",
        )
        assert_matches_type(SubjectResource, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Lark) -> None:
        response = client.subjects.with_raw_response.retrieve(
            "subject_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = response.parse()
        assert_matches_type(SubjectResource, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Lark) -> None:
        with client.subjects.with_streaming_response.retrieve(
            "subject_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = response.parse()
            assert_matches_type(SubjectResource, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Lark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id` but received ''"):
            client.subjects.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update(self, client: Lark) -> None:
        subject = client.subjects.update(
            subject_id="subject_id",
            email="john.doe@example.com",
            metadata={},
            name="John Doe",
        )
        assert_matches_type(SubjectResource, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Lark) -> None:
        response = client.subjects.with_raw_response.update(
            subject_id="subject_id",
            email="john.doe@example.com",
            metadata={},
            name="John Doe",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = response.parse()
        assert_matches_type(SubjectResource, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Lark) -> None:
        with client.subjects.with_streaming_response.update(
            subject_id="subject_id",
            email="john.doe@example.com",
            metadata={},
            name="John Doe",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = response.parse()
            assert_matches_type(SubjectResource, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Lark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id` but received ''"):
            client.subjects.with_raw_response.update(
                subject_id="",
                email="john.doe@example.com",
                metadata={},
                name="John Doe",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Lark) -> None:
        subject = client.subjects.list()
        assert_matches_type(SubjectListResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Lark) -> None:
        subject = client.subjects.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(SubjectListResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Lark) -> None:
        response = client.subjects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = response.parse()
        assert_matches_type(SubjectListResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Lark) -> None:
        with client.subjects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = response.parse()
            assert_matches_type(SubjectListResponse, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: Lark) -> None:
        subject = client.subjects.delete(
            "subject_id",
        )
        assert_matches_type(object, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Lark) -> None:
        response = client.subjects.with_raw_response.delete(
            "subject_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = response.parse()
        assert_matches_type(object, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Lark) -> None:
        with client.subjects.with_streaming_response.delete(
            "subject_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = response.parse()
            assert_matches_type(object, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Lark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id` but received ''"):
            client.subjects.with_raw_response.delete(
                "",
            )


class TestAsyncSubjects:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncLark) -> None:
        subject = await async_client.subjects.create()
        assert_matches_type(SubjectCreateResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLark) -> None:
        subject = await async_client.subjects.create(
            email="john.doe@example.com",
            external_id="user_1234567890",
            metadata={},
            name="John Doe",
        )
        assert_matches_type(SubjectCreateResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLark) -> None:
        response = await async_client.subjects.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = await response.parse()
        assert_matches_type(SubjectCreateResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLark) -> None:
        async with async_client.subjects.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = await response.parse()
            assert_matches_type(SubjectCreateResponse, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLark) -> None:
        subject = await async_client.subjects.retrieve(
            "subject_id",
        )
        assert_matches_type(SubjectResource, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLark) -> None:
        response = await async_client.subjects.with_raw_response.retrieve(
            "subject_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = await response.parse()
        assert_matches_type(SubjectResource, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLark) -> None:
        async with async_client.subjects.with_streaming_response.retrieve(
            "subject_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = await response.parse()
            assert_matches_type(SubjectResource, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncLark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id` but received ''"):
            await async_client.subjects.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncLark) -> None:
        subject = await async_client.subjects.update(
            subject_id="subject_id",
            email="john.doe@example.com",
            metadata={},
            name="John Doe",
        )
        assert_matches_type(SubjectResource, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncLark) -> None:
        response = await async_client.subjects.with_raw_response.update(
            subject_id="subject_id",
            email="john.doe@example.com",
            metadata={},
            name="John Doe",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = await response.parse()
        assert_matches_type(SubjectResource, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncLark) -> None:
        async with async_client.subjects.with_streaming_response.update(
            subject_id="subject_id",
            email="john.doe@example.com",
            metadata={},
            name="John Doe",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = await response.parse()
            assert_matches_type(SubjectResource, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncLark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id` but received ''"):
            await async_client.subjects.with_raw_response.update(
                subject_id="",
                email="john.doe@example.com",
                metadata={},
                name="John Doe",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncLark) -> None:
        subject = await async_client.subjects.list()
        assert_matches_type(SubjectListResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncLark) -> None:
        subject = await async_client.subjects.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(SubjectListResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncLark) -> None:
        response = await async_client.subjects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = await response.parse()
        assert_matches_type(SubjectListResponse, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncLark) -> None:
        async with async_client.subjects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = await response.parse()
            assert_matches_type(SubjectListResponse, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncLark) -> None:
        subject = await async_client.subjects.delete(
            "subject_id",
        )
        assert_matches_type(object, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncLark) -> None:
        response = await async_client.subjects.with_raw_response.delete(
            "subject_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = await response.parse()
        assert_matches_type(object, subject, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncLark) -> None:
        async with async_client.subjects.with_streaming_response.delete(
            "subject_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = await response.parse()
            assert_matches_type(object, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncLark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id` but received ''"):
            await async_client.subjects.with_raw_response.delete(
                "",
            )
