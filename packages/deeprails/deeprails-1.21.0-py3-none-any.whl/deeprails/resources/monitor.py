# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import monitor_create_params, monitor_update_params, monitor_retrieve_params, monitor_submit_event_params
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
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
from ..types.monitor_event_response import MonitorEventResponse
from ..types.monitor_create_response import MonitorCreateResponse
from ..types.monitor_detail_response import MonitorDetailResponse
from ..types.monitor_update_response import MonitorUpdateResponse
from ..types.monitor_event_detail_response import MonitorEventDetailResponse

__all__ = ["MonitorResource", "AsyncMonitorResource"]


class MonitorResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MonitorResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/deeprails/deeprails-sdk-python#accessing-raw-response-data-eg-headers
        """
        return MonitorResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MonitorResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/deeprails/deeprails-sdk-python#with_streaming_response
        """
        return MonitorResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        guardrail_metrics: List[
            Literal[
                "correctness",
                "completeness",
                "instruction_adherence",
                "context_adherence",
                "ground_truth_adherence",
                "comprehensive_safety",
            ]
        ],
        name: str,
        context_awareness: bool | Omit = omit,
        description: str | Omit = omit,
        file_search: SequenceNotStr[str] | Omit = omit,
        web_search: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MonitorCreateResponse:
        """
        Use this endpoint to create a new monitor to evaluate model inputs and outputs
        using guardrails

        Args:
          guardrail_metrics: An array of guardrail metrics that the model input and output pair will be
              evaluated on. For non-enterprise users, these will be limited to `correctness`,
              `completeness`, `instruction_adherence`, `context_adherence`,
              `ground_truth_adherence`, and/or `comprehensive_safety`.

          name: Name of the new monitor.

          context_awareness: Whether to enable context for this workflow's evaluations. Defaults to false.

          description: Description of the new monitor.

          file_search: An array of file IDs to search in the monitor's evaluations. Files must be
              uploaded via the DeepRails API first.

          web_search: Whether to enable web search for this monitor's evaluations. Defaults to false.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/monitor",
            body=maybe_transform(
                {
                    "guardrail_metrics": guardrail_metrics,
                    "name": name,
                    "context_awareness": context_awareness,
                    "description": description,
                    "file_search": file_search,
                    "web_search": web_search,
                },
                monitor_create_params.MonitorCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MonitorCreateResponse,
        )

    def retrieve(
        self,
        monitor_id: str,
        *,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MonitorDetailResponse:
        """
        Use this endpoint to retrieve the details and evaluations associated with a
        specific monitor

        Args:
          limit: Limit the number of returned evaluations associated with this monitor. Defaults
              to 10.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not monitor_id:
            raise ValueError(f"Expected a non-empty value for `monitor_id` but received {monitor_id!r}")
        return self._get(
            f"/monitor/{monitor_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"limit": limit}, monitor_retrieve_params.MonitorRetrieveParams),
            ),
            cast_to=MonitorDetailResponse,
        )

    def update(
        self,
        monitor_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        status: Literal["active", "inactive"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MonitorUpdateResponse:
        """
        Use this endpoint to update the name, description, or status of an existing
        monitor

        Args:
          description: Description of the monitor.

          name: Name of the monitor.

          status: Status of the monitor. Can be `active` or `inactive`. Inactive monitors no
              longer record and evaluate events.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not monitor_id:
            raise ValueError(f"Expected a non-empty value for `monitor_id` but received {monitor_id!r}")
        return self._put(
            f"/monitor/{monitor_id}",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "status": status,
                },
                monitor_update_params.MonitorUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MonitorUpdateResponse,
        )

    def retrieve_event(
        self,
        event_id: str,
        *,
        monitor_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MonitorEventDetailResponse:
        """
        Use this endpoint to retrieve the details of a specific monitor event

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not monitor_id:
            raise ValueError(f"Expected a non-empty value for `monitor_id` but received {monitor_id!r}")
        if not event_id:
            raise ValueError(f"Expected a non-empty value for `event_id` but received {event_id!r}")
        return self._get(
            f"/monitor/{monitor_id}/events/{event_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MonitorEventDetailResponse,
        )

    def submit_event(
        self,
        monitor_id: str,
        *,
        model_input: monitor_submit_event_params.ModelInput,
        model_output: str,
        nametag: str | Omit = omit,
        run_mode: Literal["precision_plus", "precision", "smart", "economy"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MonitorEventResponse:
        """
        Use this endpoint to submit a model input and output pair to a monitor for
        evaluation

        Args:
          model_input: A dictionary of inputs sent to the LLM to generate output. The dictionary must
              contain at least a `user_prompt` field or a `system_prompt` field. For
              ground_truth_adherence guardrail metric, `ground_truth` should be provided.

          model_output: Output generated by the LLM to be evaluated.

          nametag: An optional, user-defined tag for the event.

          run_mode: Run mode for the monitor event. The run mode allows the user to optimize for
              speed, accuracy, and cost by determining which models are used to evaluate the
              event. Available run modes include `precision_plus`, `precision`, `smart`, and
              `economy`. Defaults to `smart`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not monitor_id:
            raise ValueError(f"Expected a non-empty value for `monitor_id` but received {monitor_id!r}")
        return self._post(
            f"/monitor/{monitor_id}/events",
            body=maybe_transform(
                {
                    "model_input": model_input,
                    "model_output": model_output,
                    "nametag": nametag,
                    "run_mode": run_mode,
                },
                monitor_submit_event_params.MonitorSubmitEventParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MonitorEventResponse,
        )


class AsyncMonitorResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMonitorResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/deeprails/deeprails-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMonitorResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMonitorResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/deeprails/deeprails-sdk-python#with_streaming_response
        """
        return AsyncMonitorResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        guardrail_metrics: List[
            Literal[
                "correctness",
                "completeness",
                "instruction_adherence",
                "context_adherence",
                "ground_truth_adherence",
                "comprehensive_safety",
            ]
        ],
        name: str,
        context_awareness: bool | Omit = omit,
        description: str | Omit = omit,
        file_search: SequenceNotStr[str] | Omit = omit,
        web_search: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MonitorCreateResponse:
        """
        Use this endpoint to create a new monitor to evaluate model inputs and outputs
        using guardrails

        Args:
          guardrail_metrics: An array of guardrail metrics that the model input and output pair will be
              evaluated on. For non-enterprise users, these will be limited to `correctness`,
              `completeness`, `instruction_adherence`, `context_adherence`,
              `ground_truth_adherence`, and/or `comprehensive_safety`.

          name: Name of the new monitor.

          context_awareness: Whether to enable context for this workflow's evaluations. Defaults to false.

          description: Description of the new monitor.

          file_search: An array of file IDs to search in the monitor's evaluations. Files must be
              uploaded via the DeepRails API first.

          web_search: Whether to enable web search for this monitor's evaluations. Defaults to false.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/monitor",
            body=await async_maybe_transform(
                {
                    "guardrail_metrics": guardrail_metrics,
                    "name": name,
                    "context_awareness": context_awareness,
                    "description": description,
                    "file_search": file_search,
                    "web_search": web_search,
                },
                monitor_create_params.MonitorCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MonitorCreateResponse,
        )

    async def retrieve(
        self,
        monitor_id: str,
        *,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MonitorDetailResponse:
        """
        Use this endpoint to retrieve the details and evaluations associated with a
        specific monitor

        Args:
          limit: Limit the number of returned evaluations associated with this monitor. Defaults
              to 10.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not monitor_id:
            raise ValueError(f"Expected a non-empty value for `monitor_id` but received {monitor_id!r}")
        return await self._get(
            f"/monitor/{monitor_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"limit": limit}, monitor_retrieve_params.MonitorRetrieveParams),
            ),
            cast_to=MonitorDetailResponse,
        )

    async def update(
        self,
        monitor_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        status: Literal["active", "inactive"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MonitorUpdateResponse:
        """
        Use this endpoint to update the name, description, or status of an existing
        monitor

        Args:
          description: Description of the monitor.

          name: Name of the monitor.

          status: Status of the monitor. Can be `active` or `inactive`. Inactive monitors no
              longer record and evaluate events.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not monitor_id:
            raise ValueError(f"Expected a non-empty value for `monitor_id` but received {monitor_id!r}")
        return await self._put(
            f"/monitor/{monitor_id}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "status": status,
                },
                monitor_update_params.MonitorUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MonitorUpdateResponse,
        )

    async def retrieve_event(
        self,
        event_id: str,
        *,
        monitor_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MonitorEventDetailResponse:
        """
        Use this endpoint to retrieve the details of a specific monitor event

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not monitor_id:
            raise ValueError(f"Expected a non-empty value for `monitor_id` but received {monitor_id!r}")
        if not event_id:
            raise ValueError(f"Expected a non-empty value for `event_id` but received {event_id!r}")
        return await self._get(
            f"/monitor/{monitor_id}/events/{event_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MonitorEventDetailResponse,
        )

    async def submit_event(
        self,
        monitor_id: str,
        *,
        model_input: monitor_submit_event_params.ModelInput,
        model_output: str,
        nametag: str | Omit = omit,
        run_mode: Literal["precision_plus", "precision", "smart", "economy"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MonitorEventResponse:
        """
        Use this endpoint to submit a model input and output pair to a monitor for
        evaluation

        Args:
          model_input: A dictionary of inputs sent to the LLM to generate output. The dictionary must
              contain at least a `user_prompt` field or a `system_prompt` field. For
              ground_truth_adherence guardrail metric, `ground_truth` should be provided.

          model_output: Output generated by the LLM to be evaluated.

          nametag: An optional, user-defined tag for the event.

          run_mode: Run mode for the monitor event. The run mode allows the user to optimize for
              speed, accuracy, and cost by determining which models are used to evaluate the
              event. Available run modes include `precision_plus`, `precision`, `smart`, and
              `economy`. Defaults to `smart`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not monitor_id:
            raise ValueError(f"Expected a non-empty value for `monitor_id` but received {monitor_id!r}")
        return await self._post(
            f"/monitor/{monitor_id}/events",
            body=await async_maybe_transform(
                {
                    "model_input": model_input,
                    "model_output": model_output,
                    "nametag": nametag,
                    "run_mode": run_mode,
                },
                monitor_submit_event_params.MonitorSubmitEventParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MonitorEventResponse,
        )


class MonitorResourceWithRawResponse:
    def __init__(self, monitor: MonitorResource) -> None:
        self._monitor = monitor

        self.create = to_raw_response_wrapper(
            monitor.create,
        )
        self.retrieve = to_raw_response_wrapper(
            monitor.retrieve,
        )
        self.update = to_raw_response_wrapper(
            monitor.update,
        )
        self.retrieve_event = to_raw_response_wrapper(
            monitor.retrieve_event,
        )
        self.submit_event = to_raw_response_wrapper(
            monitor.submit_event,
        )


class AsyncMonitorResourceWithRawResponse:
    def __init__(self, monitor: AsyncMonitorResource) -> None:
        self._monitor = monitor

        self.create = async_to_raw_response_wrapper(
            monitor.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            monitor.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            monitor.update,
        )
        self.retrieve_event = async_to_raw_response_wrapper(
            monitor.retrieve_event,
        )
        self.submit_event = async_to_raw_response_wrapper(
            monitor.submit_event,
        )


class MonitorResourceWithStreamingResponse:
    def __init__(self, monitor: MonitorResource) -> None:
        self._monitor = monitor

        self.create = to_streamed_response_wrapper(
            monitor.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            monitor.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            monitor.update,
        )
        self.retrieve_event = to_streamed_response_wrapper(
            monitor.retrieve_event,
        )
        self.submit_event = to_streamed_response_wrapper(
            monitor.submit_event,
        )


class AsyncMonitorResourceWithStreamingResponse:
    def __init__(self, monitor: AsyncMonitorResource) -> None:
        self._monitor = monitor

        self.create = async_to_streamed_response_wrapper(
            monitor.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            monitor.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            monitor.update,
        )
        self.retrieve_event = async_to_streamed_response_wrapper(
            monitor.retrieve_event,
        )
        self.submit_event = async_to_streamed_response_wrapper(
            monitor.submit_event,
        )
