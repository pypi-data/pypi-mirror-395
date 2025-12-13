# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .message_item_param import MessageItemParam
from .reasoning_item_param import ReasoningItemParam
from .tool_call_item_param import ToolCallItemParam
from .message_content_param import MessageContentParam
from .tool_result_item_param import ToolResultItemParam

__all__ = [
    "TaskCreateParams",
    "AgentConfig",
    "AgentConfigBuiltinTool",
    "AgentConfigBuiltinToolFunction",
    "ClientTool",
    "ClientToolFunction",
    "HistoryMessage",
    "ThoughtMessage",
]


class TaskCreateParams(TypedDict, total=False):
    stream: Required[bool]
    """是否启用流式（SSE）返回；true 则以 text/event-stream 推送 Task 事件。"""

    user_message_content: Required[MessageContentParam]
    """
    当前用户输入内容（多模态），按顺序提供给主 Agent。消息内容，字符串或内容项数组，
    工具协议兼容的 message_content（保留字段）。
    """

    agent_config: AgentConfig
    """指定主 Agent 的配置；为空则按 client_id 推断默认 Agent。"""

    allowed_subagents: SequenceNotStr[str]
    """允许使用的子代理白名单；为 null 允许全部，空数组禁止所有。"""

    allowed_tools: SequenceNotStr[str]
    """允许使用的工具白名单；为 null 允许全部，空数组表示禁止所有。"""

    client_id: str
    """调用方客户端标识（如 AIME）。"""

    client_tools: Iterable[ClientTool]
    """客户端自带工具定义；命中后会停止由服务端执行，等待客户端完成。"""

    disallowed_tools: SequenceNotStr[str]
    """禁用的工具黑名单；为 null 或空数组不生效。"""

    env: Dict[str, str]
    """Agent 的运行时环境变量键值对。"""

    history_messages: Iterable[HistoryMessage]
    """历史对话消息，用于提供上下文。"""

    include_compress_model_rollout: bool
    """是否包含上下文压缩模型的 rollout 结果。"""

    include_subagent_rollout: bool
    """是否包含子 Agent 的 rollout 结果。"""

    inference_args: Dict[str, object]
    """推理参数覆盖项（如温度、最大 tokens 等），具体字段由后端实现决定。"""

    log_dir: str
    """日志输出目录。"""

    request_id: str
    """请求链路唯一 ID；便于将复杂调用串联在一起。"""

    return_rollout: bool
    """是否在最终结果中返回 rollout 事件集合。"""

    rollout_save_dir: str
    """回溯（rollout）结果保存目录。"""

    session_id: str
    """会话 ID；用于跨多轮交互复用上下文。"""

    stop_tools: SequenceNotStr[str]
    """命中则停止代理循环的工具名列表；为 null 或空数组不生效。"""

    structured_output: Dict[str, object]
    """期望的结构化输出 JSON Schema；仅非流式模式有效，流式模式下将被忽略。"""

    task_id: str
    """任务 ID；用于区分主任务与子任务。"""

    thought_messages: Iterable[ThoughtMessage]
    """隐藏的助手思考内容（不可见思考轨迹），如有将并入上下文。"""

    user_id: str
    """终端用户 ID。"""

    workspace_dir: str
    """文件系统工作目录；供文件工具与代码解释器使用。"""


class AgentConfigBuiltinToolFunction(TypedDict, total=False):
    name: Required[str]
    """工具/函数名称（唯一标识）。"""

    parameters: Required[Dict[str, object]]
    """JSON Schema for the function parameters."""

    description: str
    """函数的用途说明。"""

    strict: bool
    """是否启用严格参数校验。"""


class AgentConfigBuiltinTool(TypedDict, total=False):
    function: Required[AgentConfigBuiltinToolFunction]
    """函数工具定义（名称/参数/描述）。"""

    type: Required[Literal["function"]]
    """工具类型，此处固定为 function。"""


class AgentConfig(TypedDict, total=False):
    agent_id: Required[str]
    """Agent 唯一标识（目录名）。"""

    code_for_agent: Required[str]
    """注入到 Agent 侧的代码片段。"""

    code_for_interpreter: Required[str]
    """注入到代码解释器侧的代码片段。"""

    description: Required[str]
    """Agent 描述。"""

    developer_prompt: Required[str]
    """主系统提示词（开发者指令）。"""

    max_model_length: Required[int]
    """模型上下文最大 tokens。"""

    max_response_length: Required[int]
    """模型生成的最大 tokens。"""

    model: Required[str]
    """主模型名称。"""

    name: Required[str]
    """Agent 名称。"""

    allowed_tools: SequenceNotStr[str]
    """默认允许使用的工具。"""

    builtin_subagents: Iterable[object]
    """内置子代理列表（名称/工具/提示词等）。"""

    builtin_tools: Iterable[AgentConfigBuiltinTool]
    """内置工具集合（含 CodeInterpreter/Task 等）。"""

    code_interpreter_config: Dict[str, object]
    """代码解释器连接配置（Jupyter）。"""

    compress_model: str
    """用于压缩上下文的模型名称。"""

    compress_prompt: str
    """上下文压缩时使用的系统提示词。"""

    compress_threshold_token_ratio: float
    """触发上下文压缩的 token 比例阈值。"""

    inference_args: Dict[str, object]
    """默认推理参数覆盖项。"""

    tool_mcp_config: Dict[str, object]
    """MCP 服务器配置（工具来源）。"""


class ClientToolFunction(TypedDict, total=False):
    name: Required[str]
    """工具/函数名称（唯一标识）。"""

    parameters: Required[Dict[str, object]]
    """JSON Schema for the function parameters."""

    description: str
    """函数的用途说明。"""

    strict: bool
    """是否启用严格参数校验。"""


class ClientTool(TypedDict, total=False):
    function: Required[ClientToolFunction]
    """函数工具定义（名称/参数/描述）。"""

    type: Required[Literal["function"]]
    """工具类型，此处固定为 function。"""


HistoryMessage: TypeAlias = Union[ReasoningItemParam, MessageItemParam, ToolCallItemParam, ToolResultItemParam]

ThoughtMessage: TypeAlias = Union[ReasoningItemParam, MessageItemParam, ToolCallItemParam, ToolResultItemParam]
