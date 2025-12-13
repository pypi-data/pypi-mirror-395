from collections.abc import Awaitable, Callable
from enum import StrEnum
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, JsonValue


class ExecuteCodeRequest(BaseModel):
    tool_names: list[str]
    code: str


class MessageType(StrEnum):
    TOOL_CALL = "tool_call"
    SUCCESS = "success"
    ERROR = "error"


class ErrorCode(StrEnum):
    CODE_COMPILATION_ERROR = "code_compilation_error"
    CODE_RUNTIME_ERROR = "code_runtime_error"
    CODE_TIMEOUT_ERROR = "code_timeout_error"


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


class CodeCompilationError(BaseModel):
    type: Literal[MessageType.ERROR] = MessageType.ERROR
    code: Literal[ErrorCode.CODE_COMPILATION_ERROR] = ErrorCode.CODE_COMPILATION_ERROR
    message: str
    stdout: str
    stderr: str


class CodeRuntimeError(BaseModel):
    type: Literal[MessageType.ERROR] = MessageType.ERROR
    code: Literal[ErrorCode.CODE_RUNTIME_ERROR] = ErrorCode.CODE_RUNTIME_ERROR
    message: str
    stdout: str
    stderr: str


class CodeTimeoutError(BaseModel):
    type: Literal[MessageType.ERROR] = MessageType.ERROR
    code: Literal[ErrorCode.CODE_TIMEOUT_ERROR] = ErrorCode.CODE_TIMEOUT_ERROR
    message: str
    stdout: str
    stderr: str


type ExecuteCodeError = CodeCompilationError | CodeRuntimeError | CodeTimeoutError


type ExecuteCodeMessage = ToolCall | ExecuteCodeSuccess | ExecuteCodeError


class ToolCallResult(BaseModel):
    execution_id: str
    tool_call_id: str
    result: JsonValue


type ToolHandler = Callable[..., Awaitable[JsonValue]]
