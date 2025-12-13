from collections.abc import Generator
from contextlib import contextmanager

from progtc.server.code_execution import CodeExecutionProcess
from progtc.types import ToolCallResult


class CodeExecutionManager:
    """Manages the lifecycle of code execution processes."""

    def __init__(self) -> None:
        self._processes: dict[str, CodeExecutionProcess] = {}

    @contextmanager
    def run(
        self,
        code: str,
        tool_names: list[str],
    ) -> Generator[CodeExecutionProcess, None, None]:
        process = CodeExecutionProcess(code, tool_names)
        self._processes[process.execution_id] = process
        process.start()
        try:
            yield process
        finally:
            process.stop()
            del self._processes[process.execution_id]

    def send_tool_result(self, tool_call_result: ToolCallResult) -> None:
        self._processes[tool_call_result.execution_id].send_tool_result(
            tool_call_result,
        )
