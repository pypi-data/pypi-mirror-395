import secrets
import time
from collections.abc import Generator

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from progtc.server.code_execution_manager import CodeExecutionManager
from progtc.server.config import server_config
from progtc.types import (
    CodeTimeoutError,
    ExecuteCodeRequest,
    ToolCallResult,
)

code_execution_manager = CodeExecutionManager()


def authenticate(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> None:
    if not secrets.compare_digest(credentials.credentials, server_config.api_key):
        raise HTTPException(status_code=401, detail="Unauthorized")


app = FastAPI(dependencies=[Depends(authenticate)])


@app.post("/tool-results")
def add_tool_result(tool_call_result: ToolCallResult) -> None:
    code_execution_manager.send_tool_result(tool_call_result)


@app.post("/execute-code")
def execute_code(body: ExecuteCodeRequest) -> StreamingResponse:
    def stream() -> Generator[str, None, None]:
        with code_execution_manager.run(body.code, body.tool_names) as process:
            t0 = time.monotonic()

            # Yield tool calls to the client until the process
            # is done or the timeout is reached
            while (
                not process.is_done()
                and time.monotonic() - t0 < server_config.code_execution_timeout
            ):
                tool_call = process.next_tool_call()
                if tool_call is None:
                    continue
                yield f"data: {tool_call.model_dump_json()}\n\n"

            # Yield the final result to the client.
            if process.is_done():
                result = process.result()
            else:
                result = CodeTimeoutError(
                    stdout="",
                    stderr="",
                )
            yield f"data: {result.model_dump_json()}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
