# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from happenstance_ai import HappenstanceAI, AsyncHappenstanceAI
from happenstance_ai.types import ResearchCreateResponse, ResearchRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResearch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: HappenstanceAI) -> None:
        research = client.research.create(
            description="description",
        )
        assert_matches_type(ResearchCreateResponse, research, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: HappenstanceAI) -> None:
        response = client.research.with_raw_response.create(
            description="description",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        research = response.parse()
        assert_matches_type(ResearchCreateResponse, research, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: HappenstanceAI) -> None:
        with client.research.with_streaming_response.create(
            description="description",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            research = response.parse()
            assert_matches_type(ResearchCreateResponse, research, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: HappenstanceAI) -> None:
        research = client.research.retrieve(
            "research_id",
        )
        assert_matches_type(ResearchRetrieveResponse, research, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: HappenstanceAI) -> None:
        response = client.research.with_raw_response.retrieve(
            "research_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        research = response.parse()
        assert_matches_type(ResearchRetrieveResponse, research, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: HappenstanceAI) -> None:
        with client.research.with_streaming_response.retrieve(
            "research_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            research = response.parse()
            assert_matches_type(ResearchRetrieveResponse, research, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: HappenstanceAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `research_id` but received ''"):
            client.research.with_raw_response.retrieve(
                "",
            )


class TestAsyncResearch:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncHappenstanceAI) -> None:
        research = await async_client.research.create(
            description="description",
        )
        assert_matches_type(ResearchCreateResponse, research, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncHappenstanceAI) -> None:
        response = await async_client.research.with_raw_response.create(
            description="description",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        research = await response.parse()
        assert_matches_type(ResearchCreateResponse, research, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncHappenstanceAI) -> None:
        async with async_client.research.with_streaming_response.create(
            description="description",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            research = await response.parse()
            assert_matches_type(ResearchCreateResponse, research, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncHappenstanceAI) -> None:
        research = await async_client.research.retrieve(
            "research_id",
        )
        assert_matches_type(ResearchRetrieveResponse, research, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncHappenstanceAI) -> None:
        response = await async_client.research.with_raw_response.retrieve(
            "research_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        research = await response.parse()
        assert_matches_type(ResearchRetrieveResponse, research, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncHappenstanceAI) -> None:
        async with async_client.research.with_streaming_response.retrieve(
            "research_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            research = await response.parse()
            assert_matches_type(ResearchRetrieveResponse, research, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncHappenstanceAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `research_id` but received ''"):
            await async_client.research.with_raw_response.retrieve(
                "",
            )
