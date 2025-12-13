import asyncio
from collections.abc import AsyncGenerator

import pytest_asyncio
import uvicorn
from httpx import AsyncClient

from progtc.server.api import app


@pytest_asyncio.fixture
async def test_server() -> AsyncGenerator[str, None]:
    config = uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning")
    server = uvicorn.Server(config)
    task = asyncio.create_task(server.serve())
    while not server.started:
        await asyncio.sleep(0.01)
    port = server.servers[0].sockets[0].getsockname()[1]
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    await task


@pytest_asyncio.fixture
async def test_client(test_server: str) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        base_url=test_server,
        headers={"Authorization": "Bearer 1234567890"},
    ) as client:
        yield client
