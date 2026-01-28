from uuid import UUID
from pydantic import BaseModel

class RagSource(BaseModel):
    execution_id: UUID
    chunk_id: UUID
    rank: int