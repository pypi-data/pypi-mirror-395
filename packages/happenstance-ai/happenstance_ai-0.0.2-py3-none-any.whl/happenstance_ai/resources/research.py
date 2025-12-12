# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import research_create_params
from .._types import Body, Query, Headers, NotGiven, not_given
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
from ..types.research_create_response import ResearchCreateResponse
from ..types.research_retrieve_response import ResearchRetrieveResponse

__all__ = ["ResearchResource", "AsyncResearchResource"]


class ResearchResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ResearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/happenstance-ai/happenstance-ai-api-python#accessing-raw-response-data-eg-headers
        """
        return ResearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/happenstance-ai/happenstance-ai-api-python#with_streaming_response
        """
        return ResearchResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        description: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResearchCreateResponse:
        """
        Start a new person research request.

        Include as many details as possible about the person in the description field
        (full name, company, title, location, social media handles, etc.) for best
        results.

        Requires sufficient credits. Returns 402 Payment Required if not enough credits.

        Args:
          description: Description of the person to research

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/research",
            body=maybe_transform({"description": description}, research_create_params.ResearchCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResearchCreateResponse,
        )

    def retrieve(
        self,
        research_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResearchRetrieveResponse:
        """
        Get the status of a research request.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not research_id:
            raise ValueError(f"Expected a non-empty value for `research_id` but received {research_id!r}")
        return self._get(
            f"/v1/research/{research_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResearchRetrieveResponse,
        )


class AsyncResearchResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncResearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/happenstance-ai/happenstance-ai-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncResearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/happenstance-ai/happenstance-ai-api-python#with_streaming_response
        """
        return AsyncResearchResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        description: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResearchCreateResponse:
        """
        Start a new person research request.

        Include as many details as possible about the person in the description field
        (full name, company, title, location, social media handles, etc.) for best
        results.

        Requires sufficient credits. Returns 402 Payment Required if not enough credits.

        Args:
          description: Description of the person to research

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/research",
            body=await async_maybe_transform({"description": description}, research_create_params.ResearchCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResearchCreateResponse,
        )

    async def retrieve(
        self,
        research_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResearchRetrieveResponse:
        """
        Get the status of a research request.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not research_id:
            raise ValueError(f"Expected a non-empty value for `research_id` but received {research_id!r}")
        return await self._get(
            f"/v1/research/{research_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResearchRetrieveResponse,
        )


class ResearchResourceWithRawResponse:
    def __init__(self, research: ResearchResource) -> None:
        self._research = research

        self.create = to_raw_response_wrapper(
            research.create,
        )
        self.retrieve = to_raw_response_wrapper(
            research.retrieve,
        )


class AsyncResearchResourceWithRawResponse:
    def __init__(self, research: AsyncResearchResource) -> None:
        self._research = research

        self.create = async_to_raw_response_wrapper(
            research.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            research.retrieve,
        )


class ResearchResourceWithStreamingResponse:
    def __init__(self, research: ResearchResource) -> None:
        self._research = research

        self.create = to_streamed_response_wrapper(
            research.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            research.retrieve,
        )


class AsyncResearchResourceWithStreamingResponse:
    def __init__(self, research: AsyncResearchResource) -> None:
        self._research = research

        self.create = async_to_streamed_response_wrapper(
            research.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            research.retrieve,
        )
