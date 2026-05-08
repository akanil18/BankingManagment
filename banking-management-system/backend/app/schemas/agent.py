from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


class QueryRequest(BaseModel):
    query: str
    selected_table_id: Optional[uuid.UUID] = None


class ClarifyChoice(BaseModel):
    label: str
    table_id: uuid.UUID


class QueryResponse(BaseModel):
    response_type: str       # "table" | "text" | "clarify"
    message: str
    columns: Optional[List[str]] = None
    rows: Optional[List[Dict[str, Any]]] = None
    clarify_options: Optional[List[ClarifyChoice]] = None


class ConversationMessage(BaseModel):
    id: uuid.UUID
    role: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationHistoryResponse(BaseModel):
    messages: List[ConversationMessage]
