from __future__ import annotations

import asyncio
import queue
from multiprocessing.queues import Queue as MPQueueType
from types import TracebackType

from pydantic import JsonValue

from progtc.server.config import server_config
from progtc.types import (
    ToolCall,
    ToolCallResult,
)


class ToolCallManager:
    def __init__(
        self,
        execution_id: str,
        tool_call_queue: MPQueueType[ToolCall],
        tool_call_results_queue: MPQueueType[ToolCallResult],
    ) -> None:
        self._execution_id = execution_id
        self._tool_call_queue = tool_call_queue
        self._tool_call_results_queue = tool_call_results_queue
        self._tool_call_results_split_queue: dict[
            str,
            asyncio.Queue[ToolCallResult],
        ] = {}
        self._handle_results_task: asyncio.Task[None] | None = None
        self._shutdown_event = asyncio.Event()

    async def _handle_results_queue(self) -> None:
        while not self._shutdown_event.is_set():
            try:
                tool_call_result = self._tool_call_results_queue.get_nowait()
                await self._tool_call_results_split_queue[
                    tool_call_result.tool_call_id
                ].put(tool_call_result)
            except queue.Empty:
                await asyncio.sleep(0.1)

    async def __aenter__(self) -> ToolCallManager:
        self._handle_results_task = asyncio.create_task(self._handle_results_queue())
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._shutdown_event.set()
        if self._handle_results_task is not None:
            await self._handle_results_task

    async def call_tool(
        self,
        tool_name: str,
        *args: JsonValue,
        **kwargs: JsonValue,
    ) -> JsonValue:
        tool_call = ToolCall(
            execution_id=self._execution_id,
            tool_name=tool_name,
            args=args,
            kwargs=kwargs,
        )
        self._tool_call_results_split_queue[tool_call.id] = asyncio.Queue[
            ToolCallResult
        ]()
        self._tool_call_queue.put(tool_call)
        try:
            result = await asyncio.wait_for(
                self._tool_call_results_split_queue[tool_call.id].get(),
                timeout=server_config.tool_call_timeout,
            )
            return result.result
        finally:
            del self._tool_call_results_split_queue[tool_call.id]
