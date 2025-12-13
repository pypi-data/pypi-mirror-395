import textwrap

import pytest

from progtc.client import AsyncProgtcClient
from progtc.types import ExecuteCodeSuccess, MessageType


@pytest.fixture
def progtc_client(test_server: str) -> AsyncProgtcClient:
    return AsyncProgtcClient(
        base_url=test_server,
        api_key="1234567890",
    )


@pytest.mark.asyncio
async def test_client_execute_code_basic(progtc_client: AsyncProgtcClient) -> None:
    code = textwrap.dedent(
        """\
        print("Hello, world!")
        """,
    )
    result = await progtc_client.execute_code(code, tools={})

    assert isinstance(result, ExecuteCodeSuccess)
    assert result.stdout == "Hello, world!\n"


@pytest.mark.asyncio
async def test_client_execute_code_with_tool_call(
    progtc_client: AsyncProgtcClient,
) -> None:
    async def get_weather() -> str:
        return "Sunny"

    code = textwrap.dedent(
        """\
        from tools import get_weather
        print(await get_weather())
        """,
    )
    result = await progtc_client.execute_code(
        code,
        tools={"get_weather": get_weather},
    )

    assert isinstance(result, ExecuteCodeSuccess)
    assert result.stdout == "Sunny\n"


@pytest.mark.asyncio
async def test_client_execute_code_with_tool_call_args(
    progtc_client: AsyncProgtcClient,
) -> None:
    async def get_weather(city: str, country: str) -> str:
        return f"Weather in {city}, {country}: Rainy"

    code = textwrap.dedent(
        """\
        from tools import get_weather
        print(await get_weather("London", country="UK"))
        """,
    )
    result = await progtc_client.execute_code(
        code,
        tools={"get_weather": get_weather},
    )

    assert isinstance(result, ExecuteCodeSuccess)
    assert result.stdout == "Weather in London, UK: Rainy\n"


@pytest.mark.asyncio
async def test_client_execute_code_multiple_tool_calls(
    progtc_client: AsyncProgtcClient,
) -> None:
    async def increment(n: int) -> int:
        return n + 1

    code = textwrap.dedent(
        """\
        from tools import increment
        async def main():
            a = await increment(0)
            b = await increment(a)
            c = await increment(b)
            return [a, b, c]
        print(await main())
        """,
    )
    result = await progtc_client.execute_code(
        code,
        tools={"increment": increment},
    )

    assert isinstance(result, ExecuteCodeSuccess)
    assert result.stdout == "[1, 2, 3]\n"


@pytest.mark.asyncio
async def test_client_syntax_error(progtc_client: AsyncProgtcClient) -> None:
    code = "def main( invalid syntax"
    result = await progtc_client.execute_code(code, tools={})
    assert result.type == MessageType.SYNTAX_ERROR


@pytest.mark.asyncio
async def test_client_execution_error(progtc_client: AsyncProgtcClient) -> None:
    code = textwrap.dedent(
        """\
        async def main():
            raise ValueError("Something went wrong")
        print(await main())
        """,
    )
    result = await progtc_client.execute_code(code, tools={})
    assert result.type == MessageType.RUNTIME_ERROR
    assert "Something went wrong" in result.stderr
