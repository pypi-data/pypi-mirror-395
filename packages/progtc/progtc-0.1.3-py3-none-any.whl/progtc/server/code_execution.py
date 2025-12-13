from __future__ import annotations

import ast
import asyncio
import multiprocessing as mp
import queue
import sys
import traceback
from collections.abc import Generator
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from functools import partial
from io import StringIO
from multiprocessing import Queue as MPQueue
from multiprocessing.queues import Queue as MPQueueType
from types import ModuleType
from uuid import uuid4

from progtc.server.tool_call_manager import ToolCallManager
from progtc.types import (
    CodeRuntimeError,
    CodeSyntaxError,
    ExecuteCodeError,
    ExecuteCodeSuccess,
    ToolCall,
    ToolCallResult,
)


@contextmanager
def _capture_stdout_stderr() -> Generator[tuple[StringIO, StringIO], None, None]:
    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        yield stdout, stderr


async def execute_code(
    execution_id: str,
    code: str,
    tool_names: list[str],
    tool_call_queue: MPQueueType[ToolCall],
    tool_call_results_queue: MPQueueType[ToolCallResult],
    code_execution_result_queue: MPQueueType[ExecuteCodeSuccess | ExecuteCodeError],
) -> None:
    async with ToolCallManager(
        execution_id=execution_id,
        tool_call_queue=tool_call_queue,
        tool_call_results_queue=tool_call_results_queue,
    ) as tool_call_manager:
        # Create a tools module which the code can import tools from
        # and make it availabl in the sys.modules dictionary.
        tools_module = ModuleType("tools")
        for tool_name in tool_names:
            setattr(
                tools_module,
                tool_name,
                partial(
                    tool_call_manager.call_tool,
                    tool_name,
                ),
            )
        sys.modules["tools"] = tools_module

        # Run the code while capturing stdout and stderr.
        with _capture_stdout_stderr() as (stdout, stderr):
            try:
                compiled = compile(
                    code,
                    "<string>",
                    "exec",
                    flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT,
                )
            except (SyntaxError, ValueError):
                traceback.print_exc()
                code_execution_result_queue.put(
                    CodeSyntaxError(
                        stdout=stdout.getvalue(),
                        stderr=stderr.getvalue(),
                    ),
                )
                return

            try:
                exec_globals = {"__builtins__": __builtins__}
                coro = eval(compiled, exec_globals)
                if asyncio.iscoroutine(coro):
                    await coro
            except Exception:
                traceback.print_exc()
                code_execution_result_queue.put(
                    CodeRuntimeError(
                        stdout=stdout.getvalue(),
                        stderr=stderr.getvalue(),
                    ),
                )
                return

    code_execution_result_queue.put(
        ExecuteCodeSuccess(stdout=stdout.getvalue(), stderr=stderr.getvalue()),
    )


def execute_code_sync(
    execution_id: str,
    code: str,
    tool_names: list[str],
    tool_call_queue: MPQueueType[ToolCall],
    tool_call_results_queue: MPQueueType[ToolCallResult],
    code_execution_result_queue: MPQueueType[ExecuteCodeSuccess | ExecuteCodeError],
) -> None:
    asyncio.run(
        execute_code(
            execution_id=execution_id,
            code=code,
            tool_names=tool_names,
            tool_call_queue=tool_call_queue,
            tool_call_results_queue=tool_call_results_queue,
            code_execution_result_queue=code_execution_result_queue,
        ),
    )


class CodeExecutionProcess:
    def __init__(self, code: str, tool_names: list[str]) -> None:
        self.execution_id = uuid4().hex
        self._tool_call_queue: MPQueueType[ToolCall] = MPQueue()
        self._tool_call_results_queue: MPQueueType[ToolCallResult] = MPQueue()
        self._code_execution_result_queue: MPQueueType[
            ExecuteCodeSuccess | ExecuteCodeError
        ] = MPQueue()
        self._process = mp.Process(
            target=execute_code_sync,
            kwargs=dict(
                execution_id=self.execution_id,
                code=code,
                tool_names=tool_names,
                tool_call_queue=self._tool_call_queue,
                tool_call_results_queue=self._tool_call_results_queue,
                code_execution_result_queue=self._code_execution_result_queue,
            ),
        )

    def start(self) -> None:
        self._process.start()

    def stop(self) -> None:
        if self._process.is_alive():
            self._process.terminate()
        self._process.join()

    def is_done(self) -> bool:
        return self._process.exitcode is not None

    def result(self) -> ExecuteCodeSuccess | ExecuteCodeError:
        if not self.is_done():
            raise RuntimeError("Code execution process not done")
        return self._code_execution_result_queue.get(timeout=0.1)

    def next_tool_call(self, timeout: float = 0.1) -> ToolCall | None:
        try:
            return self._tool_call_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def send_tool_result(self, tool_call_result: ToolCallResult) -> None:
        self._tool_call_results_queue.put(tool_call_result)
