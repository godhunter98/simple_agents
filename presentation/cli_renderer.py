from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import datetime
import time

console = Console()


def render_tool_calls(tool_calls: list[dict]):
    for tool_call in tool_calls:
        console.print(
            Panel(
                f"[bold blue]Tool Called:[/bold blue] "
                f"[bold magenta]{tool_call['function_name']}[/bold magenta]\n\n"
                f"[bold green]Arguments:[/bold green] {tool_call['arguments']}\n\n"
                f"[bold yellow]Time:[/bold yellow] "
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                title="Tool Execution",
                border_style="bright_blue",
            )
        )
    time.sleep(0.5)


def render_response(response: str):
    console.print(
        Panel(
            Markdown(response),
            title="Assistant Response",
            border_style="bright_magenta",
        )
    )