import openai
import os
from dotenv import load_dotenv, find_dotenv
from tools import GetFetchPriceArgs, fetch_security_data
from agent import Agent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import datetime
import time


load_dotenv(find_dotenv())

console = Console()


base_url = "https://api.mistral.ai/v1"
# base_url = "https://generativelanguage.googleapis.com/v1beta/openai/" ##Comment out if using gemini API

TOOLS = [
    {
        "schema": {
            "type": "function",
            "function": {
                "name": "fetch_security_data",
                "description": "Get the price, percent_change, pe_ratio and industry for a security, just pass in the ticker symbol.",
                "parameters": GetFetchPriceArgs.model_json_schema(),
            },
        },
        "function": fetch_security_data,
    }
]

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=base_url)
system = "You are helpful AI assistant made by Harsh, who can answer questions about security prices and financial data. Use the tools that I've provided to you to complete the users request. Keep your responses well structured."
tools = TOOLS
agent = Agent(client, system, tools)


if __name__ == "__main__":
    user_query = console.input("\n[bold blue]Query:[/bold blue] ")
    print("\n")
    with console.status("[bold green]Agent is working...", spinner="dots"):
        response = agent(message=user_query)

    if agent.last_tool_calls:
        for tool_call in agent.last_tool_calls:
            console.print(
                Panel(
                    f"[bold blue]Tool Called:[/bold blue] [bold magenta]{tool_call['function_name']}[/bold magenta]\n\n"
                    f"[bold green]Arguments:[/bold green] {tool_call['arguments']}\n\n"
                    f"[bold yellow]Time:[/bold yellow] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    title="Tool Execution",
                    border_style="bright_blue",
                )
            )
        time.sleep(0.5)

    with console.status("[bold cyan]Generating response...", spinner="dots") as status:
        time.sleep(1) 

    console.print(
        Panel(
            Markdown(response),
            title="Assistant Response",
            border_style="bright_magenta",
        )
    )
