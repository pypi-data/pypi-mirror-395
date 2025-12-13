# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from agentlin_client import Client, AsyncClient
from agentlin_client.types import (
    TaskCancelResponse,
    TaskCreateResponse,
    TaskDeleteResponse,
    TaskRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTasks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Client) -> None:
        task = client.tasks.create(
            stream=True,
            user_message_content="string",
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Client) -> None:
        task = client.tasks.create(
            stream=True,
            user_message_content="string",
            agent_config={
                "agent_id": "agent_id",
                "code_for_agent": "code_for_agent",
                "code_for_interpreter": "code_for_interpreter",
                "description": "description",
                "developer_prompt": "developer_prompt",
                "max_model_length": 0,
                "max_response_length": 0,
                "model": "model",
                "name": "name",
                "allowed_tools": ["string"],
                "builtin_subagents": [{}],
                "builtin_tools": [
                    {
                        "function": {
                            "name": "name",
                            "parameters": {"foo": "bar"},
                            "description": "description",
                            "strict": True,
                        },
                        "type": "function",
                    }
                ],
                "code_interpreter_config": {"foo": "bar"},
                "compress_model": "compress_model",
                "compress_prompt": "compress_prompt",
                "compress_threshold_token_ratio": 0,
                "inference_args": {"foo": "bar"},
                "tool_mcp_config": {"foo": "bar"},
            },
            allowed_subagents=["string"],
            allowed_tools=["string"],
            client_id="client_id",
            client_tools=[
                {
                    "function": {
                        "name": "name",
                        "parameters": {"foo": "bar"},
                        "description": "description",
                        "strict": True,
                    },
                    "type": "function",
                }
            ],
            disallowed_tools=["string"],
            env={"foo": "string"},
            history_messages=[
                {
                    "id": "id",
                    "summary": [
                        {
                            "text": "text",
                            "type": "text",
                            "id": 0,
                            "annotations": [
                                {
                                    "file_id": "file_id",
                                    "filename": "filename",
                                    "index": 0,
                                    "type": "file_citation",
                                }
                            ],
                            "logprobs": [
                                {
                                    "token": "token",
                                    "bytes": [0],
                                    "logprob": 0,
                                    "top_logprobs": [
                                        {
                                            "token": "token",
                                            "bytes": [0],
                                            "logprob": 0,
                                        }
                                    ],
                                }
                            ],
                            "tags": ["string"],
                        }
                    ],
                    "type": "reasoning",
                    "content": [
                        {
                            "text": "text",
                            "type": "text",
                            "id": 0,
                            "annotations": [
                                {
                                    "file_id": "file_id",
                                    "filename": "filename",
                                    "index": 0,
                                    "type": "file_citation",
                                }
                            ],
                            "logprobs": [
                                {
                                    "token": "token",
                                    "bytes": [0],
                                    "logprob": 0,
                                    "top_logprobs": [
                                        {
                                            "token": "token",
                                            "bytes": [0],
                                            "logprob": 0,
                                        }
                                    ],
                                }
                            ],
                            "tags": ["string"],
                        }
                    ],
                    "status": "in_progress",
                }
            ],
            include_compress_model_rollout=True,
            include_subagent_rollout=True,
            inference_args={"foo": "bar"},
            log_dir="log_dir",
            request_id="request_id",
            return_rollout=True,
            rollout_save_dir="rollout_save_dir",
            session_id="session_id",
            stop_tools=["string"],
            structured_output={"foo": "bar"},
            task_id="task_id",
            thought_messages=[
                {
                    "id": "id",
                    "summary": [
                        {
                            "text": "text",
                            "type": "text",
                            "id": 0,
                            "annotations": [
                                {
                                    "file_id": "file_id",
                                    "filename": "filename",
                                    "index": 0,
                                    "type": "file_citation",
                                }
                            ],
                            "logprobs": [
                                {
                                    "token": "token",
                                    "bytes": [0],
                                    "logprob": 0,
                                    "top_logprobs": [
                                        {
                                            "token": "token",
                                            "bytes": [0],
                                            "logprob": 0,
                                        }
                                    ],
                                }
                            ],
                            "tags": ["string"],
                        }
                    ],
                    "type": "reasoning",
                    "content": [
                        {
                            "text": "text",
                            "type": "text",
                            "id": 0,
                            "annotations": [
                                {
                                    "file_id": "file_id",
                                    "filename": "filename",
                                    "index": 0,
                                    "type": "file_citation",
                                }
                            ],
                            "logprobs": [
                                {
                                    "token": "token",
                                    "bytes": [0],
                                    "logprob": 0,
                                    "top_logprobs": [
                                        {
                                            "token": "token",
                                            "bytes": [0],
                                            "logprob": 0,
                                        }
                                    ],
                                }
                            ],
                            "tags": ["string"],
                        }
                    ],
                    "status": "in_progress",
                }
            ],
            user_id="user_id",
            workspace_dir="workspace_dir",
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Client) -> None:
        response = client.tasks.with_raw_response.create(
            stream=True,
            user_message_content="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Client) -> None:
        with client.tasks.with_streaming_response.create(
            stream=True,
            user_message_content="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskCreateResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Client) -> None:
        task = client.tasks.retrieve(
            "task_677efb5139a88190b512bc3fef8e535d",
        )
        assert_matches_type(TaskRetrieveResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Client) -> None:
        response = client.tasks.with_raw_response.retrieve(
            "task_677efb5139a88190b512bc3fef8e535d",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskRetrieveResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Client) -> None:
        with client.tasks.with_streaming_response.retrieve(
            "task_677efb5139a88190b512bc3fef8e535d",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskRetrieveResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.tasks.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: Client) -> None:
        task = client.tasks.delete(
            "task_677efb5139a88190b512bc3fef8e535d",
        )
        assert_matches_type(TaskDeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Client) -> None:
        response = client.tasks.with_raw_response.delete(
            "task_677efb5139a88190b512bc3fef8e535d",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskDeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Client) -> None:
        with client.tasks.with_streaming_response.delete(
            "task_677efb5139a88190b512bc3fef8e535d",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskDeleteResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.tasks.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_cancel(self, client: Client) -> None:
        task = client.tasks.cancel(
            "task_677efb5139a88190b512bc3fef8e535d",
        )
        assert_matches_type(TaskCancelResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_cancel(self, client: Client) -> None:
        response = client.tasks.with_raw_response.cancel(
            "task_677efb5139a88190b512bc3fef8e535d",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskCancelResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_cancel(self, client: Client) -> None:
        with client.tasks.with_streaming_response.cancel(
            "task_677efb5139a88190b512bc3fef8e535d",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskCancelResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_cancel(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.tasks.with_raw_response.cancel(
                "",
            )


class TestAsyncTasks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncClient) -> None:
        task = await async_client.tasks.create(
            stream=True,
            user_message_content="string",
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncClient) -> None:
        task = await async_client.tasks.create(
            stream=True,
            user_message_content="string",
            agent_config={
                "agent_id": "agent_id",
                "code_for_agent": "code_for_agent",
                "code_for_interpreter": "code_for_interpreter",
                "description": "description",
                "developer_prompt": "developer_prompt",
                "max_model_length": 0,
                "max_response_length": 0,
                "model": "model",
                "name": "name",
                "allowed_tools": ["string"],
                "builtin_subagents": [{}],
                "builtin_tools": [
                    {
                        "function": {
                            "name": "name",
                            "parameters": {"foo": "bar"},
                            "description": "description",
                            "strict": True,
                        },
                        "type": "function",
                    }
                ],
                "code_interpreter_config": {"foo": "bar"},
                "compress_model": "compress_model",
                "compress_prompt": "compress_prompt",
                "compress_threshold_token_ratio": 0,
                "inference_args": {"foo": "bar"},
                "tool_mcp_config": {"foo": "bar"},
            },
            allowed_subagents=["string"],
            allowed_tools=["string"],
            client_id="client_id",
            client_tools=[
                {
                    "function": {
                        "name": "name",
                        "parameters": {"foo": "bar"},
                        "description": "description",
                        "strict": True,
                    },
                    "type": "function",
                }
            ],
            disallowed_tools=["string"],
            env={"foo": "string"},
            history_messages=[
                {
                    "id": "id",
                    "summary": [
                        {
                            "text": "text",
                            "type": "text",
                            "id": 0,
                            "annotations": [
                                {
                                    "file_id": "file_id",
                                    "filename": "filename",
                                    "index": 0,
                                    "type": "file_citation",
                                }
                            ],
                            "logprobs": [
                                {
                                    "token": "token",
                                    "bytes": [0],
                                    "logprob": 0,
                                    "top_logprobs": [
                                        {
                                            "token": "token",
                                            "bytes": [0],
                                            "logprob": 0,
                                        }
                                    ],
                                }
                            ],
                            "tags": ["string"],
                        }
                    ],
                    "type": "reasoning",
                    "content": [
                        {
                            "text": "text",
                            "type": "text",
                            "id": 0,
                            "annotations": [
                                {
                                    "file_id": "file_id",
                                    "filename": "filename",
                                    "index": 0,
                                    "type": "file_citation",
                                }
                            ],
                            "logprobs": [
                                {
                                    "token": "token",
                                    "bytes": [0],
                                    "logprob": 0,
                                    "top_logprobs": [
                                        {
                                            "token": "token",
                                            "bytes": [0],
                                            "logprob": 0,
                                        }
                                    ],
                                }
                            ],
                            "tags": ["string"],
                        }
                    ],
                    "status": "in_progress",
                }
            ],
            include_compress_model_rollout=True,
            include_subagent_rollout=True,
            inference_args={"foo": "bar"},
            log_dir="log_dir",
            request_id="request_id",
            return_rollout=True,
            rollout_save_dir="rollout_save_dir",
            session_id="session_id",
            stop_tools=["string"],
            structured_output={"foo": "bar"},
            task_id="task_id",
            thought_messages=[
                {
                    "id": "id",
                    "summary": [
                        {
                            "text": "text",
                            "type": "text",
                            "id": 0,
                            "annotations": [
                                {
                                    "file_id": "file_id",
                                    "filename": "filename",
                                    "index": 0,
                                    "type": "file_citation",
                                }
                            ],
                            "logprobs": [
                                {
                                    "token": "token",
                                    "bytes": [0],
                                    "logprob": 0,
                                    "top_logprobs": [
                                        {
                                            "token": "token",
                                            "bytes": [0],
                                            "logprob": 0,
                                        }
                                    ],
                                }
                            ],
                            "tags": ["string"],
                        }
                    ],
                    "type": "reasoning",
                    "content": [
                        {
                            "text": "text",
                            "type": "text",
                            "id": 0,
                            "annotations": [
                                {
                                    "file_id": "file_id",
                                    "filename": "filename",
                                    "index": 0,
                                    "type": "file_citation",
                                }
                            ],
                            "logprobs": [
                                {
                                    "token": "token",
                                    "bytes": [0],
                                    "logprob": 0,
                                    "top_logprobs": [
                                        {
                                            "token": "token",
                                            "bytes": [0],
                                            "logprob": 0,
                                        }
                                    ],
                                }
                            ],
                            "tags": ["string"],
                        }
                    ],
                    "status": "in_progress",
                }
            ],
            user_id="user_id",
            workspace_dir="workspace_dir",
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncClient) -> None:
        response = await async_client.tasks.with_raw_response.create(
            stream=True,
            user_message_content="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncClient) -> None:
        async with async_client.tasks.with_streaming_response.create(
            stream=True,
            user_message_content="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskCreateResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncClient) -> None:
        task = await async_client.tasks.retrieve(
            "task_677efb5139a88190b512bc3fef8e535d",
        )
        assert_matches_type(TaskRetrieveResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncClient) -> None:
        response = await async_client.tasks.with_raw_response.retrieve(
            "task_677efb5139a88190b512bc3fef8e535d",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskRetrieveResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncClient) -> None:
        async with async_client.tasks.with_streaming_response.retrieve(
            "task_677efb5139a88190b512bc3fef8e535d",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskRetrieveResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.tasks.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncClient) -> None:
        task = await async_client.tasks.delete(
            "task_677efb5139a88190b512bc3fef8e535d",
        )
        assert_matches_type(TaskDeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncClient) -> None:
        response = await async_client.tasks.with_raw_response.delete(
            "task_677efb5139a88190b512bc3fef8e535d",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskDeleteResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncClient) -> None:
        async with async_client.tasks.with_streaming_response.delete(
            "task_677efb5139a88190b512bc3fef8e535d",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskDeleteResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.tasks.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_cancel(self, async_client: AsyncClient) -> None:
        task = await async_client.tasks.cancel(
            "task_677efb5139a88190b512bc3fef8e535d",
        )
        assert_matches_type(TaskCancelResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncClient) -> None:
        response = await async_client.tasks.with_raw_response.cancel(
            "task_677efb5139a88190b512bc3fef8e535d",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskCancelResponse, task, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncClient) -> None:
        async with async_client.tasks.with_streaming_response.cancel(
            "task_677efb5139a88190b512bc3fef8e535d",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskCancelResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.tasks.with_raw_response.cancel(
                "",
            )
