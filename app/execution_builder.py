from datetime import datetime
from typing import List
import json

from domain.models import AgentExecution, ToolCall


def build_tool_calls(raw_tool_calls: list[dict]) -> List[ToolCall]:
    tool_calls: List[ToolCall] = []

    for idx, raw_call in enumerate(raw_tool_calls or []):
        args = raw_call.get("arguments")

        if isinstance(args, str):
            args = json.loads(args)

        tool_calls.append(
            ToolCall(
                tool_name=raw_call["function_name"],
                arguments=args,
                call_order=idx + 1,
                created_at=datetime.utcnow(),
            )
        )

    return tool_calls


def build_execution(
    *,
    query: str,
    response: str,
    agent_name: str,
    model: str | None,
    raw_tool_calls: list[dict],
) -> AgentExecution:
    return AgentExecution(
        query=query,
        response=response,
        agent_name=agent_name,
        model=model,
        tool_calls=build_tool_calls(raw_tool_calls),
        created_at=datetime.utcnow(),
    )