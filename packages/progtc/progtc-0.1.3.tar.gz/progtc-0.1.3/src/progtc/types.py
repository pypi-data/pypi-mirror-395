from collections.abc import Awaitable, Callable
from enum import Enum
from typing import Literal, TypeAlias
from uuid import uuid4

from pydantic import BaseModel, Field, JsonValue


class ExecuteCodeRequest(BaseModel):
    tool_names: list[str]
    code: str


class MessageType(str, Enum):
    TOOL_CALL = "tool_call"
    SUCCESS = "success"
    SYNTAX_ERROR = "syntax_error"
    RUNTIME_ERROR = "runtime_error"
    TIMEOUT_ERROR = "timeout_error"


class ToolCall(BaseModel):
    type: Literal[MessageType.TOOL_CALL] = MessageType.TOOL_CALL
    id: str = Field(default_factory=lambda: uuid4().hex)
    execution_id: str
    tool_name: str
    args: tuple[JsonValue, ...]
    kwargs: dict[str, JsonValue]


class ExecuteCodeSuccess(BaseModel):
    type: Literal[MessageType.SUCCESS] = MessageType.SUCCESS
    stdout: str
    stderr: str


class CodeSyntaxError(BaseModel):
    type: Literal[MessageType.SYNTAX_ERROR] = MessageType.SYNTAX_ERROR
    stdout: str
    stderr: str


class CodeRuntimeError(BaseModel):
    type: Literal[MessageType.RUNTIME_ERROR] = MessageType.RUNTIME_ERROR
    stdout: str
    stderr: str


class CodeTimeoutError(BaseModel):
    type: Literal[MessageType.TIMEOUT_ERROR] = MessageType.TIMEOUT_ERROR
    stdout: str
    stderr: str


ExecuteCodeError: TypeAlias = CodeSyntaxError | CodeRuntimeError | CodeTimeoutError


ExecuteCodeMessage: TypeAlias = ToolCall | ExecuteCodeSuccess | ExecuteCodeError


class ToolCallResult(BaseModel):
    execution_id: str
    tool_call_id: str
    result: JsonValue


ToolHandler: TypeAlias = Callable[..., Awaitable[JsonValue]]
