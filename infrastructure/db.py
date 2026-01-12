from typing import List
import os
import psycopg
import psycopg.rows
from domain.models import AgentExecution, ToolCall
from uuid import UUID

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
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            
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

def get_tool_calls_for_execution(execution_id:UUID) -> List[ToolCall]:
    conn = get_connection()

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:

            cursor.execute(
                '''
                SELECT 
                    id,
                    execution_id,
                    tool_name,
                    arguments,
                    call_order,
                    created_at
                    FROM tool_calls WHERE execution_id = %s
                    ORDER BY call_order ASC
                ''',
                (execution_id,)
            )

            rows = cursor.fetchall()

            if rows is None:
                return []

            tool_calls = []

            for row in rows:
                tool_calls.append(
                    ToolCall(
                        id=row["id"],
                        execution_id=row["execution_id"],
                        tool_name=row["tool_name"],
                        arguments=row["arguments"],
                        call_order=row["call_order"],
                        created_at=row["created_at"],
                    )
                )

            return tool_calls

    finally:
        conn.close()

def get_execution_by_id(execution_id:UUID) -> AgentExecution | None:
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute(
                '''
                SELECT 
                    id, 
                    query, 
                    response, 
                    agent_name, 
                    model, 
                    created_at
                FROM agent_executions WHERE ID = %s
                ''',
                (execution_id,)
            )

            row = cursor.fetchone()         

            if row is None:
                return None
            
            execution = AgentExecution(
                id=row["id"],
                query=row["query"],
                response=row["response"],
                agent_name=row["agent_name"],
                model=row["model"],
                created_at=row["created_at"],
                tool_calls=[],
            )

            execution.tool_calls = get_tool_calls_for_execution(execution.id)

            return execution

    finally:
        conn.close()

print(get_execution_by_id(UUID('7ee90d67-43bd-4ae4-86b8-04fd3f42958d')))