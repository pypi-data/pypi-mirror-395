```
    ██████╗ ██████╗  ██████╗  ██████╗ ████████╗ ██████╗
    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ╚══██╔══╝██╔════╝
    ██████╔╝██████╔╝██║   ██║██║  ███╗   ██║   ██║     
    ██╔═══╝ ██╔══██╗██║   ██║██║   ██║   ██║   ██║     
    ██║     ██║  ██║╚██████╔╝╚██████╔╝   ██║   ╚██████╗
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝
                                               by capsa
```

**Programmatic Tool Calling** — Let LLM-generated code call your tools, even from inside a sandbox.

---

## The Problem

You want an AI agent to write and execute Python code. Easy enough—spin up an [E2B](https://e2b.dev) sandbox and let it run. But what if that code needs to call your tools?

The code runs inside a sandbox. Your tools live outside. There's no bridge.

## The Solution

**progtc** creates that bridge. It runs a lightweight server inside your sandbox that exposes your tools to the generated code. When the code calls a tool, the request streams back to your client, you execute it locally, and return the result—all transparently.


## Installation

```bash
pip install progtc
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add progtc
```

## Quick Start

### 1. Start the Server (inside your sandbox)

```bash
progtc serve --host 0.0.0.0 --port 8000 --api-key your-secret-key
```

### 2. Execute Code from Your Client

```python
from progtc import AsyncProgtcClient

client = AsyncProgtcClient(
    base_url="https://your-sandbox-url:8000",
    api_key="your-secret-key",
)

# Define your tools as async functions
async def get_weather(city: str, country: str) -> str:
    # Your actual implementation
    return f"Weather in {city}, {country}: Sunny, 22°C"

async def search_database(query: str) -> list[dict]:
    # Your actual implementation
    return [{"id": 1, "name": "Result"}]

# Execute LLM-generated code that uses your tools
code = """
from tools import get_weather

weather = await get_weather("London", "UK")
print(f"The weather is: {weather}")
"""

result = await client.execute_code(
    code=code,
    tool_call_handlers={
        "get_weather": get_weather,
        "search_database": search_database,
    },
)

print(result.stdout)  # "The weather is: Weather in London, UK: Sunny, 22°C"
```

## How It Works

1. **Your client** sends code + a list of available tool names to the progtc server
2. **The server** executes the code in an isolated process, injecting a `tools` module
3. **When code calls a tool**, the server streams the call back to your client via SSE
4. **Your client** executes the tool locally and sends the result back
5. **The server** resumes code execution with the result
6. **Stdout/stderr** are captured and streamed back when execution completes

## Code Requirements

The LLM-generated code must:

- **Import tools from the `tools` module**: `from tools import my_tool`
- **Await all tool calls** (they're async)
- **Use `print()` for output** — stdout/stderr are captured and returned

```python
from tools import get_weather, search_database
import asyncio

# Call tools like regular async functions
weather, results = await asyncio.gather(
    get_weather("Tokyo", "Japan"),
    search_database("hotels"),
)

print(f"Weather: {weather}")
print(f"Results: {results}")
```

> **Note:** The code runs in a top-level async context, so you can use `await` directly without defining an async function.

## CLI Options

```bash
progtc serve [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | `127.0.0.1` | Host to bind to |
| `--port` | `8000` | Port to bind to |
| `--api-key` | (env: `PROGTC_API_KEY`) | API key for authentication |
| `--tool-call-timeout` | `10.0` | Timeout for individual tool calls (seconds) |
| `--code-execution-timeout` | `30.0` | Total timeout for code execution (seconds) |

## Error Handling

The client returns a discriminated union—either success or one of several error types:

```python
from progtc.types import MessageType

result = await client.execute_code(code, tool_call_handlers)

match result.type:
    case MessageType.SUCCESS:
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
    case MessageType.ERROR:
        print(f"Error: {result.message}")
        print(f"Code: {result.code}")  # compilation, runtime, timeout, etc.
```

Error codes:
- `code_compilation_error` — Code failed to compile/exec
- `code_runtime_error` — Exception raised during execution
- `code_timeout_error` — Execution exceeded timeout

## Example: E2B + pydantic-ai

See [`examples/e2b-example/`](examples/e2b-example/) for a complete example using progtc with [E2B](https://e2b.dev) sandboxes and [pydantic-ai](https://ai.pydantic.dev) agents.

The example demonstrates an AI agent that can execute Python code in a secure sandbox while calling tools defined in your application.

## License

MIT

---

<p align="center">
  <b>Building AI agents?</b> We're hiring: <a href="https://capsa.ai/careers">capsa.ai/careers</a>
</p>
