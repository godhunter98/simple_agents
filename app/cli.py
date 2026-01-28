from argparse import ArgumentParser
from uuid import UUID
from infrastructure.db import list_recent_executions, get_execution_by_id
from presentation.cli_renderer import render_response, render_tool_calls


def handle_history():
    executions = list_recent_executions(10)
    for e in executions:
        print(f"{e.id} | {e.agent_name} | {e.query} | {e.created_at} ")


def handle_show(execution_id: str):
    execution = get_execution_by_id(UUID(execution_id))

    if execution is None:
        print("Execution not found.")
        return

    print(f"\nQuery: {execution.query}\n")
    render_response(execution.response)

    if execution.tool_calls:
        render_tool_calls([
            {
                "function_name": tc.tool_name,
                "arguments": tc.arguments,
            }
            for tc in execution.tool_calls
        ])


if __name__ == "__main__":
    parser = ArgumentParser(description="Agent CLI tool")
    subparsers = parser.add_subparsers(dest="command")

    # history subcommand
    subparsers.add_parser("history", help="Show recent execution history")

    # show subcommand
    show_parser = subparsers.add_parser("show", help="Show details of a specific execution")
    show_parser.add_argument("execution_id", help="The UUID of the execution to show")

    args = parser.parse_args()

    if args.command == "history":
        handle_history()
    elif args.command == "show":
        handle_show(args.execution_id)
    else:
        # Default behavior → interactive run
        from app.run_agent import run_interactive
        run_interactive()