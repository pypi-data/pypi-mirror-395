import asyncio
import json
import secrets

from dotenv import load_dotenv
from e2b_code_interpreter import AsyncSandbox
from pydantic_ai import Agent
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from progtc import AsyncProgtcClient

load_dotenv()

PROGTC_API_KEY = secrets.token_urlsafe(32)
PROGTC_PORT = 8000


async def get_weather(city: str, country: str) -> str:
    """Get the weather for a city."""
    return f"Weather in {city}, {country}: Rainy"


async def get_reviews(city: str, country: str) -> str:
    """Get reviews for a city."""
    return f"Reviews in {city}, {country}: 4.5 stars"


async def execute_code_with_tools(code: str) -> dict[str, str]:
    """Execute python code in a sandboxed environment and return the stdout and stderr.

    You have the following available tools:
    - async def get_weather(city: str, country: str) -> str:
    - async def get_reviews(city: str, country: str) -> str:

    Guidelines:
    - All tools are async and must be awaited.
    - You must import the tools from the tools module.
    - Try to consolidate your requests into a single script for efficiency.
    - The code runs in a top-level async context.
    - You can use `await` directly without defining an async function.
    - Print the data you want to be returned in stdout.

    Example Code:
    ```python
    from tools import get_weather
    weather = await get_weather("London", "UK")
    print(f"The weather in London, UK is {weather}")
    ````

    """
    try:
        # Start e2b sandbox
        sandbox = await AsyncSandbox.create()

        # Install progtc server in the sandbox
        await sandbox.commands.run("pip install 'progtc[server]'")

        # Start the progtc server in the sandbox and get url
        await sandbox.commands.run(
            f"progtc serve --host 0.0.0.0 --port {PROGTC_PORT} "
            f"--api-key {PROGTC_API_KEY}",
            background=True,
        )
        host = sandbox.get_host(PROGTC_PORT)

        # Create client and execute code
        client = AsyncProgtcClient(
            base_url=f"https://{host}",
            api_key=PROGTC_API_KEY,
        )
        result = await client.execute_code(
            code=code,
            tools={
                "get_weather": get_weather,
                "get_reviews": get_reviews,
            },
        )

        return {"stdout": result.stdout, "stderr": result.stderr}

    finally:
        await sandbox.kill()


async def main() -> None:
    agent = Agent(
        "openai:gpt-5.1",
        system_prompt=(
            "You are a helpful assistant that can execute python code "
            "to answer questions."
        ),
        tools=[execute_code_with_tools],
    )

    result = await agent.run(
        "Can you get the weather and reviews score for "
        "London, Tokyo and Paris using your code execution tools?"
    )

    # Print the conversation
    console = Console()
    for msg in result.new_messages():
        if isinstance(msg, ModelRequest):
            for request_part in msg.parts:
                if isinstance(request_part, SystemPromptPart):
                    console.print(
                        Panel(request_part.content, title="System", border_style="dim")
                    )
                elif isinstance(request_part, UserPromptPart):
                    console.print(
                        Panel(
                            str(request_part.content), title="User", border_style="blue"
                        )
                    )
                elif isinstance(request_part, ToolReturnPart):
                    content = (
                        request_part.content
                        if isinstance(request_part.content, dict)
                        else json.loads(request_part.content)
                    )
                    console.print(
                        Panel(
                            f"stdout:\n\n{content['stdout']}\n\nstderr:\n\n{content['stderr']}",
                            title=f"Tool Return: {request_part.tool_name}",
                            border_style="green",
                        )
                    )
        elif isinstance(msg, ModelResponse):
            for response_part in msg.parts:
                if isinstance(response_part, TextPart):
                    console.print(
                        Panel(
                            response_part.content,
                            title="Assistant",
                            border_style="magenta",
                        )
                    )
                elif isinstance(response_part, ToolCallPart):
                    args = (
                        response_part.args
                        if isinstance(response_part.args, dict)
                        else json.loads(response_part.args or '{"code": ""}')
                    )
                    code = Syntax(
                        args["code"], "python", theme="monokai", line_numbers=True
                    )
                    console.print(
                        Panel(
                            code,
                            title=f"Tool Call: {response_part.tool_name}",
                            border_style="yellow",
                        )
                    )


if __name__ == "__main__":
    asyncio.run(main())
