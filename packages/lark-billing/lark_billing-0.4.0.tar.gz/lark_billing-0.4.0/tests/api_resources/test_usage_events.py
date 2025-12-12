# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lark import Lark, AsyncLark
from lark._utils import parse_datetime
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsageEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Lark) -> None:
        usage_event = client.usage_events.create(
            data={
                "compute_hours": "100.5",
                "instance_type": "t2.micro",
                "region": "us-east-1",
            },
            event_name="job_completed",
            idempotency_key="168fbd3a-4d39-4db3-a204-15e014857d10",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )
        assert_matches_type(object, usage_event, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Lark) -> None:
        usage_event = client.usage_events.create(
            data={
                "compute_hours": "100.5",
                "instance_type": "t2.micro",
                "region": "us-east-1",
            },
            event_name="job_completed",
            idempotency_key="168fbd3a-4d39-4db3-a204-15e014857d10",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
            timestamp=parse_datetime("2025-12-03T22:13:28.294419+00:00"),
        )
        assert_matches_type(object, usage_event, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Lark) -> None:
        response = client.usage_events.with_raw_response.create(
            data={
                "compute_hours": "100.5",
                "instance_type": "t2.micro",
                "region": "us-east-1",
            },
            event_name="job_completed",
            idempotency_key="168fbd3a-4d39-4db3-a204-15e014857d10",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage_event = response.parse()
        assert_matches_type(object, usage_event, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Lark) -> None:
        with client.usage_events.with_streaming_response.create(
            data={
                "compute_hours": "100.5",
                "instance_type": "t2.micro",
                "region": "us-east-1",
            },
            event_name="job_completed",
            idempotency_key="168fbd3a-4d39-4db3-a204-15e014857d10",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage_event = response.parse()
            assert_matches_type(object, usage_event, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUsageEvents:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncLark) -> None:
        usage_event = await async_client.usage_events.create(
            data={
                "compute_hours": "100.5",
                "instance_type": "t2.micro",
                "region": "us-east-1",
            },
            event_name="job_completed",
            idempotency_key="168fbd3a-4d39-4db3-a204-15e014857d10",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )
        assert_matches_type(object, usage_event, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLark) -> None:
        usage_event = await async_client.usage_events.create(
            data={
                "compute_hours": "100.5",
                "instance_type": "t2.micro",
                "region": "us-east-1",
            },
            event_name="job_completed",
            idempotency_key="168fbd3a-4d39-4db3-a204-15e014857d10",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
            timestamp=parse_datetime("2025-12-03T22:13:28.294419+00:00"),
        )
        assert_matches_type(object, usage_event, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLark) -> None:
        response = await async_client.usage_events.with_raw_response.create(
            data={
                "compute_hours": "100.5",
                "instance_type": "t2.micro",
                "region": "us-east-1",
            },
            event_name="job_completed",
            idempotency_key="168fbd3a-4d39-4db3-a204-15e014857d10",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage_event = await response.parse()
        assert_matches_type(object, usage_event, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLark) -> None:
        async with async_client.usage_events.with_streaming_response.create(
            data={
                "compute_hours": "100.5",
                "instance_type": "t2.micro",
                "region": "us-east-1",
            },
            event_name="job_completed",
            idempotency_key="168fbd3a-4d39-4db3-a204-15e014857d10",
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage_event = await response.parse()
            assert_matches_type(object, usage_event, path=["response"])

        assert cast(Any, response.is_closed) is True
