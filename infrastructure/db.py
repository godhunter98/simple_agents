import os
import json
import psycopg
from domain.models import AgentExecution, ToolCall

def get_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB", "agents"),
        user=os.getenv("POSTGRES_USER", "agents"),
        password=os.getenv("POSTGRES_PASSWORD", "agents"),
    )

def persist_execution(execution: AgentExecution) -> None:
    """
    Persist an AgentExecution and its ToolCalls atomically.
    """

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            
            # 1. Insert agent execution
            cursor.execute(
                """
                INSERT INTO agent_executions (id, query, response, agent_name, model, created_at)
                VALUES (%s, %s, %s, %s, %s,%s)
                RETURNING id
                """,
                (
                    execution.id,
                    execution.query,
                    execution.response,
                    execution.agent_name,
                    execution.model,
                    execution.created_at,
                ),
            )

            # 2. Insert tool calls
            for tool_call in execution.tool_calls:
                cursor.execute(
                    """
                    INSERT INTO tool_calls (
                    id,
                    execution_id,
                    tool_name,
                    arguments,
                    call_order,
                    created_at
                    )
                    VALUES (%s, %s, %s, %s, %s,%s)
                    """,
                    (
                        tool_call.id,
                        tool_call.execution_id,
                        tool_call.tool_name,
                        psycopg.types.json.Json(tool_call.arguments),
                        tool_call.call_order,
                        tool_call.created_at,
                    ),
                )
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
        