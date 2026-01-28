from datetime import datetime
from typing import List
import json
from domain.models.models import AgentExecution, ToolCall
from uuid import UUID

# We want to convert every raw LLM Execution output into Pydantic Model Instances

def build_tool_calls(raw_tool_calls: list[dict], execution_id: UUID) -> List[ToolCall]:
    tool_calls: List[ToolCall] = []

    for idx, raw_call in enumerate(raw_tool_calls or []):
        args = raw_call.get("arguments")

        if isinstance(args, str):
            args = json.loads(args)

        tool_calls.append(
            ToolCall(
                execution_id=execution_id,
                tool_name=raw_call["function_name"],
                arguments=args,
                call_order=idx + 1,
                created_at=datetime.utcnow(),
            )
        )

    return tool_calls

# At the time of creating an execution, we also create the tool_calls, as they're a part of that execution state
def build_execution(
    *,
    query: str,
    response: str,
    agent_name: str,
    model: str | None,
    raw_tool_calls: list[dict],
    ) -> AgentExecution:
    execution = AgentExecution(
        query=query,
        response=response,
        agent_name=agent_name,
        model=model,
        created_at=datetime.utcnow(),
    )
    execution.tool_calls = build_tool_calls(raw_tool_calls,execution_id = execution.id) #tool_calls can't exist without agent execution
    return execution