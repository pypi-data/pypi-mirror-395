from typing import Annotated

import typer
import uvicorn
from rich import print as rprint

from progtc.server.config import server_config

app = typer.Typer(
    name="progtc",
    help="progtc CLI",
    add_completion=True,
)


@app.callback()
def callback() -> None:
    """Progtc - programmatic tool calling"""


ARTWORK = """
[bright_cyan]
    ██████╗ ██████╗  ██████╗  ██████╗ ████████╗ ██████╗
    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ╚══██╔══╝██╔════╝
    ██████╔╝██████╔╝██║   ██║██║  ███╗   ██║   ██║     
    ██╔═══╝ ██╔══██╗██║   ██║██║   ██║   ██║   ██║     
    ██║     ██║  ██║╚██████╔╝╚██████╔╝   ██║   ╚██████╗
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝
                                               by capsa[/bright_cyan]
[dim]───────────────────────────────────────────────────────────[/dim]
    [bright_white]Come build agents with us: https://capsa.ai/careers[/bright_white]
[dim]───────────────────────────────────────────────────────────[/dim]
"""


@app.command()
def serve(
    host: Annotated[str, typer.Option(help="Host to bind to")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Port to bind to")] = 8000,
    api_key: Annotated[
        str | None,
        typer.Option(
            help=(
                "API key for authentication (can also be set via "
                "PROGTC_API_KEY env var)"
            ),
            envvar="PROGTC_API_KEY",
        ),
    ] = None,
    tool_call_timeout: Annotated[
        float,
        typer.Option(help="Timeout for tool calls in seconds"),
    ] = 10.0,
    code_execution_timeout: Annotated[
        float,
        typer.Option(help="Timeout for code execution in seconds"),
    ] = 30.0,
) -> None:
    if api_key:
        server_config.api_key = api_key
    server_config.tool_call_timeout = tool_call_timeout
    server_config.code_execution_timeout = code_execution_timeout

    rprint(ARTWORK)

    uvicorn.run(
        "progtc.server.api:app",
        host=host,
        port=port,
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
