from httpx import AsyncClient
from httpx_sse import aconnect_sse
from pydantic import TypeAdapter

from progtc.types import (
    ExecuteCodeError,
    ExecuteCodeMessage,
    ExecuteCodeSuccess,
    ToolCall,
    ToolHandler,
)

ExecuteCodeMessageAdapter = TypeAdapter[ExecuteCodeMessage](ExecuteCodeMessage)


class AsyncProgtcClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
    ):
        self._base_url = base_url
        self._api_key = api_key

    async def execute_code(
        self,
        code: str,
        tools: dict[str, ToolHandler],
    ) -> ExecuteCodeSuccess | ExecuteCodeError:
        async with (
            AsyncClient(
                base_url=self._base_url,
                headers={"Authorization": f"Bearer {self._api_key}"},
            ) as client,
            aconnect_sse(
                client,
                "POST",
                "/execute-code",
                json={
                    "tool_names": list(tools.keys()),
                    "code": code,
                },
            ) as event_source,
        ):
            async for event in event_source.aiter_sse():
                event_obj = ExecuteCodeMessageAdapter.validate_python(event.json())
                if isinstance(event_obj, ToolCall):
                    handler = tools[event_obj.tool_name]
                    result = await handler(*event_obj.args, **event_obj.kwargs)
                    await client.post(
                        "/tool-results",
                        json={
                            "execution_id": event_obj.execution_id,
                            "tool_call_id": event_obj.id,
                            "result": result,
                        },
                    )
                else:
                    return event_obj

        raise RuntimeError("Stream ended without result")
