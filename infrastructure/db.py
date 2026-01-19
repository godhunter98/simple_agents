"""
DEPRECATED: This module is kept for backward compatibility.
Use the specific repositories instead:
    - infrastructure.repositories.execution_repo
    - infrastructure.repositories.document_repo
    - infrastructure.connection for get_connection
"""
# Re-export for backward compatibility
from infrastructure.connection import get_connection
from infrastructure.repositories.execution_repo import (
    persist_execution,
    get_execution_by_id,
    get_tool_calls_for_execution,
    list_executions,
    list_recent_executions,
)