from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4,UUID

class ToolCall(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    execution_id: UUID
    tool_name:str
    arguments: Dict[str,Any]
    call_order: int
    created_at: datetime

class AgentExecution(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    query: str
    response: str

    agent_name: str
    model: Optional[str] = None

    tool_calls: List[ToolCall] = Field(default_factory=list)
    created_at: datetime 

class DocumentChunk(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    document_id : UUID = Field(default_factory=uuid4)
    content: str
    embedding: Optional[list[float]] = None
    
