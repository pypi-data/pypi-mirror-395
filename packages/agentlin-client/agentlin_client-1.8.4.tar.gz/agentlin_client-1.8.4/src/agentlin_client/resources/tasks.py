# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable

import httpx

from ..types import task_create_params
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
from ..types.task_cancel_response import TaskCancelResponse
from ..types.task_create_response import TaskCreateResponse
from ..types.task_delete_response import TaskDeleteResponse
from ..types.message_content_param import MessageContentParam
from ..types.task_retrieve_response import TaskRetrieveResponse

__all__ = ["TasksResource", "AsyncTasksResource"]


class TasksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LinXueyuanStdio/agentlin-client-python#accessing-raw-response-data-eg-headers
        """
        return TasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LinXueyuanStdio/agentlin-client-python#with_streaming_response
        """
        return TasksResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        stream: bool,
        user_message_content: MessageContentParam,
        agent_config: task_create_params.AgentConfig | Omit = omit,
        allowed_subagents: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        client_id: str | Omit = omit,
        client_tools: Iterable[task_create_params.ClientTool] | Omit = omit,
        disallowed_tools: SequenceNotStr[str] | Omit = omit,
        env: Dict[str, str] | Omit = omit,
        history_messages: Iterable[task_create_params.HistoryMessage] | Omit = omit,
        include_compress_model_rollout: bool | Omit = omit,
        include_subagent_rollout: bool | Omit = omit,
        inference_args: Dict[str, object] | Omit = omit,
        log_dir: str | Omit = omit,
        request_id: str | Omit = omit,
        return_rollout: bool | Omit = omit,
        rollout_save_dir: str | Omit = omit,
        session_id: str | Omit = omit,
        stop_tools: SequenceNotStr[str] | Omit = omit,
        structured_output: Dict[str, object] | Omit = omit,
        task_id: str | Omit = omit,
        thought_messages: Iterable[task_create_params.ThoughtMessage] | Omit = omit,
        user_id: str | Omit = omit,
        workspace_dir: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TaskCreateResponse:
        """Creates a model task.

        Provide [text](https://docs.linxueyuan.online/guides/text)
        or [image](https://docs.linxueyuan.online/guides/images) inputs to generate
        [text](https://docs.linxueyuan.online/guides/text) or
        [JSON](https://docs.linxueyuan.online/guides/structured-outputs) outputs. Have
        the model call your own
        [custom code](https://docs.linxueyuan.online/guides/function-calling) or use
        built-in [tools](https://docs.linxueyuan.online/guides/tools) like
        [web search](https://docs.linxueyuan.online/guides/tools-web-search) or
        [file search](https://docs.linxueyuan.online/guides/tools-file-search) to use
        your own data as input for the model's task.

        Args:
          stream: 是否启用流式（SSE）返回；true 则以 text/event-stream 推送 Task 事件。

          user_message_content: 当前用户输入内容（多模态），按顺序提供给主 Agent。消息内容，字符串或内容项数组，
              工具协议兼容的 message_content（保留字段）。

          agent_config: 指定主 Agent 的配置；为空则按 client_id 推断默认 Agent。

          allowed_subagents: 允许使用的子代理白名单；为 null 允许全部，空数组禁止所有。

          allowed_tools: 允许使用的工具白名单；为 null 允许全部，空数组表示禁止所有。

          client_id: 调用方客户端标识（如 AIME）。

          client_tools: 客户端自带工具定义；命中后会停止由服务端执行，等待客户端完成。

          disallowed_tools: 禁用的工具黑名单；为 null 或空数组不生效。

          env: Agent 的运行时环境变量键值对。

          history_messages: 历史对话消息，用于提供上下文。

          include_compress_model_rollout: 是否包含上下文压缩模型的 rollout 结果。

          include_subagent_rollout: 是否包含子 Agent 的 rollout 结果。

          inference_args: 推理参数覆盖项（如温度、最大 tokens 等），具体字段由后端实现决定。

          log_dir: 日志输出目录。

          request_id: 请求链路唯一 ID；便于将复杂调用串联在一起。

          return_rollout: 是否在最终结果中返回 rollout 事件集合。

          rollout_save_dir: 回溯（rollout）结果保存目录。

          session_id: 会话 ID；用于跨多轮交互复用上下文。

          stop_tools: 命中则停止代理循环的工具名列表；为 null 或空数组不生效。

          structured_output: 期望的结构化输出 JSON Schema；仅非流式模式有效，流式模式下将被忽略。

          task_id: 任务 ID；用于区分主任务与子任务。

          thought_messages: 隐藏的助手思考内容（不可见思考轨迹），如有将并入上下文。

          user_id: 终端用户 ID。

          workspace_dir: 文件系统工作目录；供文件工具与代码解释器使用。

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/tasks",
            body=maybe_transform(
                {
                    "stream": stream,
                    "user_message_content": user_message_content,
                    "agent_config": agent_config,
                    "allowed_subagents": allowed_subagents,
                    "allowed_tools": allowed_tools,
                    "client_id": client_id,
                    "client_tools": client_tools,
                    "disallowed_tools": disallowed_tools,
                    "env": env,
                    "history_messages": history_messages,
                    "include_compress_model_rollout": include_compress_model_rollout,
                    "include_subagent_rollout": include_subagent_rollout,
                    "inference_args": inference_args,
                    "log_dir": log_dir,
                    "request_id": request_id,
                    "return_rollout": return_rollout,
                    "rollout_save_dir": rollout_save_dir,
                    "session_id": session_id,
                    "stop_tools": stop_tools,
                    "structured_output": structured_output,
                    "task_id": task_id,
                    "thought_messages": thought_messages,
                    "user_id": user_id,
                    "workspace_dir": workspace_dir,
                },
                task_create_params.TaskCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskCreateResponse,
        )

    def retrieve(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TaskRetrieveResponse:
        """
        Retrieves a model task with the given ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return self._get(
            f"/tasks/{task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskRetrieveResponse,
        )

    def delete(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TaskDeleteResponse:
        """
        Deletes a model task with the given ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return self._delete(
            f"/tasks/{task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskDeleteResponse,
        )

    def cancel(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TaskCancelResponse:
        """Cancels a model task with the given ID.

        Only tasks created with the `background`
        parameter set to `true` can be cancelled.
        [Learn more](https://docs.linxueyuan.online/guides/background).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return self._post(
            f"/tasks/{task_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskCancelResponse,
        )


class AsyncTasksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LinXueyuanStdio/agentlin-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LinXueyuanStdio/agentlin-client-python#with_streaming_response
        """
        return AsyncTasksResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        stream: bool,
        user_message_content: MessageContentParam,
        agent_config: task_create_params.AgentConfig | Omit = omit,
        allowed_subagents: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        client_id: str | Omit = omit,
        client_tools: Iterable[task_create_params.ClientTool] | Omit = omit,
        disallowed_tools: SequenceNotStr[str] | Omit = omit,
        env: Dict[str, str] | Omit = omit,
        history_messages: Iterable[task_create_params.HistoryMessage] | Omit = omit,
        include_compress_model_rollout: bool | Omit = omit,
        include_subagent_rollout: bool | Omit = omit,
        inference_args: Dict[str, object] | Omit = omit,
        log_dir: str | Omit = omit,
        request_id: str | Omit = omit,
        return_rollout: bool | Omit = omit,
        rollout_save_dir: str | Omit = omit,
        session_id: str | Omit = omit,
        stop_tools: SequenceNotStr[str] | Omit = omit,
        structured_output: Dict[str, object] | Omit = omit,
        task_id: str | Omit = omit,
        thought_messages: Iterable[task_create_params.ThoughtMessage] | Omit = omit,
        user_id: str | Omit = omit,
        workspace_dir: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TaskCreateResponse:
        """Creates a model task.

        Provide [text](https://docs.linxueyuan.online/guides/text)
        or [image](https://docs.linxueyuan.online/guides/images) inputs to generate
        [text](https://docs.linxueyuan.online/guides/text) or
        [JSON](https://docs.linxueyuan.online/guides/structured-outputs) outputs. Have
        the model call your own
        [custom code](https://docs.linxueyuan.online/guides/function-calling) or use
        built-in [tools](https://docs.linxueyuan.online/guides/tools) like
        [web search](https://docs.linxueyuan.online/guides/tools-web-search) or
        [file search](https://docs.linxueyuan.online/guides/tools-file-search) to use
        your own data as input for the model's task.

        Args:
          stream: 是否启用流式（SSE）返回；true 则以 text/event-stream 推送 Task 事件。

          user_message_content: 当前用户输入内容（多模态），按顺序提供给主 Agent。消息内容，字符串或内容项数组，
              工具协议兼容的 message_content（保留字段）。

          agent_config: 指定主 Agent 的配置；为空则按 client_id 推断默认 Agent。

          allowed_subagents: 允许使用的子代理白名单；为 null 允许全部，空数组禁止所有。

          allowed_tools: 允许使用的工具白名单；为 null 允许全部，空数组表示禁止所有。

          client_id: 调用方客户端标识（如 AIME）。

          client_tools: 客户端自带工具定义；命中后会停止由服务端执行，等待客户端完成。

          disallowed_tools: 禁用的工具黑名单；为 null 或空数组不生效。

          env: Agent 的运行时环境变量键值对。

          history_messages: 历史对话消息，用于提供上下文。

          include_compress_model_rollout: 是否包含上下文压缩模型的 rollout 结果。

          include_subagent_rollout: 是否包含子 Agent 的 rollout 结果。

          inference_args: 推理参数覆盖项（如温度、最大 tokens 等），具体字段由后端实现决定。

          log_dir: 日志输出目录。

          request_id: 请求链路唯一 ID；便于将复杂调用串联在一起。

          return_rollout: 是否在最终结果中返回 rollout 事件集合。

          rollout_save_dir: 回溯（rollout）结果保存目录。

          session_id: 会话 ID；用于跨多轮交互复用上下文。

          stop_tools: 命中则停止代理循环的工具名列表；为 null 或空数组不生效。

          structured_output: 期望的结构化输出 JSON Schema；仅非流式模式有效，流式模式下将被忽略。

          task_id: 任务 ID；用于区分主任务与子任务。

          thought_messages: 隐藏的助手思考内容（不可见思考轨迹），如有将并入上下文。

          user_id: 终端用户 ID。

          workspace_dir: 文件系统工作目录；供文件工具与代码解释器使用。

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/tasks",
            body=await async_maybe_transform(
                {
                    "stream": stream,
                    "user_message_content": user_message_content,
                    "agent_config": agent_config,
                    "allowed_subagents": allowed_subagents,
                    "allowed_tools": allowed_tools,
                    "client_id": client_id,
                    "client_tools": client_tools,
                    "disallowed_tools": disallowed_tools,
                    "env": env,
                    "history_messages": history_messages,
                    "include_compress_model_rollout": include_compress_model_rollout,
                    "include_subagent_rollout": include_subagent_rollout,
                    "inference_args": inference_args,
                    "log_dir": log_dir,
                    "request_id": request_id,
                    "return_rollout": return_rollout,
                    "rollout_save_dir": rollout_save_dir,
                    "session_id": session_id,
                    "stop_tools": stop_tools,
                    "structured_output": structured_output,
                    "task_id": task_id,
                    "thought_messages": thought_messages,
                    "user_id": user_id,
                    "workspace_dir": workspace_dir,
                },
                task_create_params.TaskCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskCreateResponse,
        )

    async def retrieve(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TaskRetrieveResponse:
        """
        Retrieves a model task with the given ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return await self._get(
            f"/tasks/{task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskRetrieveResponse,
        )

    async def delete(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TaskDeleteResponse:
        """
        Deletes a model task with the given ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return await self._delete(
            f"/tasks/{task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskDeleteResponse,
        )

    async def cancel(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TaskCancelResponse:
        """Cancels a model task with the given ID.

        Only tasks created with the `background`
        parameter set to `true` can be cancelled.
        [Learn more](https://docs.linxueyuan.online/guides/background).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return await self._post(
            f"/tasks/{task_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskCancelResponse,
        )


class TasksResourceWithRawResponse:
    def __init__(self, tasks: TasksResource) -> None:
        self._tasks = tasks

        self.create = to_raw_response_wrapper(
            tasks.create,
        )
        self.retrieve = to_raw_response_wrapper(
            tasks.retrieve,
        )
        self.delete = to_raw_response_wrapper(
            tasks.delete,
        )
        self.cancel = to_raw_response_wrapper(
            tasks.cancel,
        )


class AsyncTasksResourceWithRawResponse:
    def __init__(self, tasks: AsyncTasksResource) -> None:
        self._tasks = tasks

        self.create = async_to_raw_response_wrapper(
            tasks.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            tasks.retrieve,
        )
        self.delete = async_to_raw_response_wrapper(
            tasks.delete,
        )
        self.cancel = async_to_raw_response_wrapper(
            tasks.cancel,
        )


class TasksResourceWithStreamingResponse:
    def __init__(self, tasks: TasksResource) -> None:
        self._tasks = tasks

        self.create = to_streamed_response_wrapper(
            tasks.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            tasks.retrieve,
        )
        self.delete = to_streamed_response_wrapper(
            tasks.delete,
        )
        self.cancel = to_streamed_response_wrapper(
            tasks.cancel,
        )


class AsyncTasksResourceWithStreamingResponse:
    def __init__(self, tasks: AsyncTasksResource) -> None:
        self._tasks = tasks

        self.create = async_to_streamed_response_wrapper(
            tasks.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            tasks.retrieve,
        )
        self.delete = async_to_streamed_response_wrapper(
            tasks.delete,
        )
        self.cancel = async_to_streamed_response_wrapper(
            tasks.cancel,
        )
