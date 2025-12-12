# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lark import Lark, AsyncLark
from lark.types import (
    PricingMetricResource,
    PricingMetricListResponse,
    PricingMetricCreateSummaryResponse,
)
from lark._utils import parse_datetime
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPricingMetrics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Lark) -> None:
        pricing_metric = client.pricing_metrics.create(
            aggregation={
                "aggregation_type": "sum",
                "value_field": "compute_hours",
            },
            event_name="job_completed",
            name="Compute Hours",
            unit="hours",
        )
        assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Lark) -> None:
        pricing_metric = client.pricing_metrics.create(
            aggregation={
                "aggregation_type": "sum",
                "value_field": "compute_hours",
            },
            event_name="job_completed",
            name="Compute Hours",
            unit="hours",
            dimensions=["string"],
        )
        assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Lark) -> None:
        response = client.pricing_metrics.with_raw_response.create(
            aggregation={
                "aggregation_type": "sum",
                "value_field": "compute_hours",
            },
            event_name="job_completed",
            name="Compute Hours",
            unit="hours",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pricing_metric = response.parse()
        assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Lark) -> None:
        with client.pricing_metrics.with_streaming_response.create(
            aggregation={
                "aggregation_type": "sum",
                "value_field": "compute_hours",
            },
            event_name="job_completed",
            name="Compute Hours",
            unit="hours",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pricing_metric = response.parse()
            assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Lark) -> None:
        pricing_metric = client.pricing_metrics.retrieve(
            "pricing_metric_id",
        )
        assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Lark) -> None:
        response = client.pricing_metrics.with_raw_response.retrieve(
            "pricing_metric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pricing_metric = response.parse()
        assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Lark) -> None:
        with client.pricing_metrics.with_streaming_response.retrieve(
            "pricing_metric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pricing_metric = response.parse()
            assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Lark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pricing_metric_id` but received ''"):
            client.pricing_metrics.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Lark) -> None:
        pricing_metric = client.pricing_metrics.list()
        assert_matches_type(PricingMetricListResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Lark) -> None:
        pricing_metric = client.pricing_metrics.list(
            limit=1,
        )
        assert_matches_type(PricingMetricListResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Lark) -> None:
        response = client.pricing_metrics.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pricing_metric = response.parse()
        assert_matches_type(PricingMetricListResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Lark) -> None:
        with client.pricing_metrics.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pricing_metric = response.parse()
            assert_matches_type(PricingMetricListResponse, pricing_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_summary(self, client: Lark) -> None:
        pricing_metric = client.pricing_metrics.create_summary(
            pricing_metric_id="pmtr_GlX5Tcm2HOn00CoRTFxw2Amw",
            period={
                "end": parse_datetime("2025-11-01T00:00:00Z"),
                "start": parse_datetime("2025-10-01T00:00:00Z"),
            },
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )
        assert_matches_type(PricingMetricCreateSummaryResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_summary_with_all_params(self, client: Lark) -> None:
        pricing_metric = client.pricing_metrics.create_summary(
            pricing_metric_id="pmtr_GlX5Tcm2HOn00CoRTFxw2Amw",
            period={
                "end": parse_datetime("2025-11-01T00:00:00Z"),
                "start": parse_datetime("2025-10-01T00:00:00Z"),
                "inclusive_end": True,
                "inclusive_start": True,
            },
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )
        assert_matches_type(PricingMetricCreateSummaryResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_summary(self, client: Lark) -> None:
        response = client.pricing_metrics.with_raw_response.create_summary(
            pricing_metric_id="pmtr_GlX5Tcm2HOn00CoRTFxw2Amw",
            period={
                "end": parse_datetime("2025-11-01T00:00:00Z"),
                "start": parse_datetime("2025-10-01T00:00:00Z"),
            },
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pricing_metric = response.parse()
        assert_matches_type(PricingMetricCreateSummaryResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_summary(self, client: Lark) -> None:
        with client.pricing_metrics.with_streaming_response.create_summary(
            pricing_metric_id="pmtr_GlX5Tcm2HOn00CoRTFxw2Amw",
            period={
                "end": parse_datetime("2025-11-01T00:00:00Z"),
                "start": parse_datetime("2025-10-01T00:00:00Z"),
            },
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pricing_metric = response.parse()
            assert_matches_type(PricingMetricCreateSummaryResponse, pricing_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_create_summary(self, client: Lark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pricing_metric_id` but received ''"):
            client.pricing_metrics.with_raw_response.create_summary(
                pricing_metric_id="",
                period={
                    "end": parse_datetime("2025-11-01T00:00:00Z"),
                    "start": parse_datetime("2025-10-01T00:00:00Z"),
                },
                subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
            )


class TestAsyncPricingMetrics:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncLark) -> None:
        pricing_metric = await async_client.pricing_metrics.create(
            aggregation={
                "aggregation_type": "sum",
                "value_field": "compute_hours",
            },
            event_name="job_completed",
            name="Compute Hours",
            unit="hours",
        )
        assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLark) -> None:
        pricing_metric = await async_client.pricing_metrics.create(
            aggregation={
                "aggregation_type": "sum",
                "value_field": "compute_hours",
            },
            event_name="job_completed",
            name="Compute Hours",
            unit="hours",
            dimensions=["string"],
        )
        assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLark) -> None:
        response = await async_client.pricing_metrics.with_raw_response.create(
            aggregation={
                "aggregation_type": "sum",
                "value_field": "compute_hours",
            },
            event_name="job_completed",
            name="Compute Hours",
            unit="hours",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pricing_metric = await response.parse()
        assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLark) -> None:
        async with async_client.pricing_metrics.with_streaming_response.create(
            aggregation={
                "aggregation_type": "sum",
                "value_field": "compute_hours",
            },
            event_name="job_completed",
            name="Compute Hours",
            unit="hours",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pricing_metric = await response.parse()
            assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLark) -> None:
        pricing_metric = await async_client.pricing_metrics.retrieve(
            "pricing_metric_id",
        )
        assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLark) -> None:
        response = await async_client.pricing_metrics.with_raw_response.retrieve(
            "pricing_metric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pricing_metric = await response.parse()
        assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLark) -> None:
        async with async_client.pricing_metrics.with_streaming_response.retrieve(
            "pricing_metric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pricing_metric = await response.parse()
            assert_matches_type(PricingMetricResource, pricing_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncLark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pricing_metric_id` but received ''"):
            await async_client.pricing_metrics.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncLark) -> None:
        pricing_metric = await async_client.pricing_metrics.list()
        assert_matches_type(PricingMetricListResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncLark) -> None:
        pricing_metric = await async_client.pricing_metrics.list(
            limit=1,
        )
        assert_matches_type(PricingMetricListResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncLark) -> None:
        response = await async_client.pricing_metrics.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pricing_metric = await response.parse()
        assert_matches_type(PricingMetricListResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncLark) -> None:
        async with async_client.pricing_metrics.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pricing_metric = await response.parse()
            assert_matches_type(PricingMetricListResponse, pricing_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_summary(self, async_client: AsyncLark) -> None:
        pricing_metric = await async_client.pricing_metrics.create_summary(
            pricing_metric_id="pmtr_GlX5Tcm2HOn00CoRTFxw2Amw",
            period={
                "end": parse_datetime("2025-11-01T00:00:00Z"),
                "start": parse_datetime("2025-10-01T00:00:00Z"),
            },
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )
        assert_matches_type(PricingMetricCreateSummaryResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_summary_with_all_params(self, async_client: AsyncLark) -> None:
        pricing_metric = await async_client.pricing_metrics.create_summary(
            pricing_metric_id="pmtr_GlX5Tcm2HOn00CoRTFxw2Amw",
            period={
                "end": parse_datetime("2025-11-01T00:00:00Z"),
                "start": parse_datetime("2025-10-01T00:00:00Z"),
                "inclusive_end": True,
                "inclusive_start": True,
            },
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )
        assert_matches_type(PricingMetricCreateSummaryResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_summary(self, async_client: AsyncLark) -> None:
        response = await async_client.pricing_metrics.with_raw_response.create_summary(
            pricing_metric_id="pmtr_GlX5Tcm2HOn00CoRTFxw2Amw",
            period={
                "end": parse_datetime("2025-11-01T00:00:00Z"),
                "start": parse_datetime("2025-10-01T00:00:00Z"),
            },
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pricing_metric = await response.parse()
        assert_matches_type(PricingMetricCreateSummaryResponse, pricing_metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_summary(self, async_client: AsyncLark) -> None:
        async with async_client.pricing_metrics.with_streaming_response.create_summary(
            pricing_metric_id="pmtr_GlX5Tcm2HOn00CoRTFxw2Amw",
            period={
                "end": parse_datetime("2025-11-01T00:00:00Z"),
                "start": parse_datetime("2025-10-01T00:00:00Z"),
            },
            subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pricing_metric = await response.parse()
            assert_matches_type(PricingMetricCreateSummaryResponse, pricing_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_create_summary(self, async_client: AsyncLark) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pricing_metric_id` but received ''"):
            await async_client.pricing_metrics.with_raw_response.create_summary(
                pricing_metric_id="",
                period={
                    "end": parse_datetime("2025-11-01T00:00:00Z"),
                    "start": parse_datetime("2025-10-01T00:00:00Z"),
                },
                subject_id="subj_VyX6Q96h5avMho8O7QWlKeXE",
            )
