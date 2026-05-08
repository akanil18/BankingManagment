from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
from datetime import datetime


class TableMeta(BaseModel):
    id: uuid.UUID
    table_name: str
    original_filename: str
    row_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class TableListResponse(BaseModel):
    tables: List[TableMeta]


class RowsResponse(BaseModel):
    table_id: uuid.UUID
    table_name: str
    columns: List[str]
    rows: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
