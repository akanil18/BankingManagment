from pydantic import BaseModel
from typing import List, Dict, Any
import uuid


class FieldMappingItem(BaseModel):
    original_column: str
    mapped_column: str


class ConfirmMappingRequest(BaseModel):
    table_id: uuid.UUID
    mappings: List[FieldMappingItem]


class UploadResponse(BaseModel):
    table_id: uuid.UUID
    table_name: str
    original_filename: str
    detected_columns: List[str]
    suggested_mappings: List[FieldMappingItem]
    row_count: int


class MappingConfirmedResponse(BaseModel):
    table_id: uuid.UUID
    message: str
    row_count: int
