from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class ToolCall(BaseModel):
    tool_name:str
    arguments: Dict[str,Any]
    call_order: int
    created_at: datetime

class AgentExecution(BaseModel):
    query: str
    response: str

    agent_name: str
    model: Optional[str] = None

    tool_calls: List[ToolCall] = Field(default_factory=List)
    created_at: datetime 


