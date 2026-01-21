import sys
import openai
import os
from dotenv import load_dotenv, find_dotenv
from core.tools import fetch_security_data_args, fetch_security_data
from core.agent import Agent
from rich.console import Console
import time
from app.execution_builder import build_execution
from presentation.cli_renderer import render_tool_calls, render_response
from infrastructure.db import persist_execution

# load env variables
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
                "parameters": fetch_security_data_args.model_json_schema(),
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
    # Ensure stdin is ready for interactive input
    if not sys.stdin.isatty():
        console.print("[bold red]Error:[/bold red] This app requires an interactive terminal.")
        console.print("Run with: [bold cyan]docker compose run --rm app[/bold cyan]")
        sys.exit(1)
    
    user_query = console.input("\n[bold blue]Query:[/bold blue] ")
    print("\n")
    with console.status("[bold green]Agent is working...", spinner="dots"):
        response = agent(message=user_query)

    if agent.last_tool_calls:
        render_tool_calls(agent.last_tool_calls)
    

    with console.status("[bold cyan]Generating response...", spinner="dots") as status:
        time.sleep(1) 

    # for logging to db
    execution = build_execution(
        query=user_query,
        response=response,
        agent_name="finance_agent",
        model=agent.model,
        raw_tool_calls=agent.last_tool_calls,
    )

    persist_execution(execution)    

    render_response(response)

    # For debugging
    print(execution)
    print(render_tool_calls(agent.last_tool_calls))
    
