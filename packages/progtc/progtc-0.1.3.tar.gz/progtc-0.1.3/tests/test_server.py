import textwrap

import pytest
from httpx import AsyncClient
from httpx_sse import aconnect_sse

from progtc.types import MessageType


@pytest.mark.asyncio
async def test_execute_code_basic(test_client: AsyncClient) -> None:
    code = textwrap.dedent(
        """\
        async def main():
            print("main function called")
        await main()
        """,
    )
    messages = []
    async with aconnect_sse(
        test_client,
        "POST",
        "/execute-code",
        json={"tool_names": [], "code": code},
    ) as event_source:
        async for event in event_source.aiter_sse():
            messages.append(event.json())
    assert messages[0]["type"] == MessageType.SUCCESS
    assert messages[0]["stdout"] == "main function called\n"


@pytest.mark.asyncio
async def test_execute_code_with_func_call(test_client: AsyncClient) -> None:
    code = textwrap.dedent(
        """\
        async def say_hello():
            print("say_hello function called")
        async def main():
            print("main function called")
            await say_hello()
        await main()
        """,
    )
    messages = []
    async with aconnect_sse(
        test_client,
        "POST",
        "/execute-code",
        json={"tool_names": [], "code": code},
    ) as event_source:
        async for event in event_source.aiter_sse():
            messages.append(event.json())
    assert messages[0]["type"] == MessageType.SUCCESS
    assert messages[0]["stdout"] == "main function called\nsay_hello function called\n"


@pytest.mark.asyncio
async def test_execute_code_with_tool_call(test_client: AsyncClient) -> None:
    code = textwrap.dedent(
        """\
        from tools import get_weather
        async def main():
            print("main function called")
            return await get_weather()
        print(await main())
        """,
    )
    messages = []
    async with aconnect_sse(
        test_client,
        "POST",
        "/execute-code",
        json={"tool_names": ["get_weather"], "code": code},
        timeout=10,
    ) as event_source:
        async for event in event_source.aiter_sse():
            message = event.json()
            messages.append(message)
            if (
                message["type"] == MessageType.TOOL_CALL
                and message["tool_name"] == "get_weather"
            ):
                await test_client.post(
                    "/tool-results",
                    json={
                        "execution_id": message["execution_id"],
                        "tool_call_id": message["id"],
                        "result": "Sunny",
                    },
                )
    assert messages[0]["type"] == MessageType.TOOL_CALL, messages[0]
    assert messages[0]["tool_name"] == "get_weather"
    assert messages[0]["args"] == []
    assert messages[0]["kwargs"] == {}
    assert messages[1]["type"] == MessageType.SUCCESS
    assert messages[1]["stdout"] == "main function called\nSunny\n"


@pytest.mark.asyncio
async def test_execute_code_with_tool_call_with_args(test_client: AsyncClient) -> None:
    code = textwrap.dedent(
        """\
        from tools import get_weather
        async def main():
            from tools import get_weather
            print("main function called")
            return await get_weather("UK", city="London")
        print(await main())
        """,
    )
    messages = []
    async with aconnect_sse(
        test_client,
        "POST",
        "/execute-code",
        json={"tool_names": ["get_weather"], "code": code},
        timeout=10,
    ) as event_source:
        async for event in event_source.aiter_sse():
            message = event.json()
            messages.append(message)
            if (
                message["type"] == MessageType.TOOL_CALL
                and message["tool_name"] == "get_weather"
            ):
                await test_client.post(
                    "/tool-results",
                    json={
                        "execution_id": message["execution_id"],
                        "tool_call_id": message["id"],
                        "result": "Sunny",
                    },
                )
    assert messages[0]["type"] == MessageType.TOOL_CALL, messages[0]
    assert messages[0]["tool_name"] == "get_weather"
    assert messages[0]["args"] == ["UK"]
    assert messages[0]["kwargs"] == {"city": "London"}
    assert messages[1]["type"] == MessageType.SUCCESS
    assert messages[1]["stdout"] == "main function called\nSunny\n"
