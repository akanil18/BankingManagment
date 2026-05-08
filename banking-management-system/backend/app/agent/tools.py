import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.uploaded_table import UploadedTable, UploadedRow
from app.models.field_mapping import FieldMapping
from app.config import settings


async def get_user_tables(user_id: uuid.UUID, db: AsyncSession) -> List[Dict]:
    result = await db.execute(
        select(UploadedTable)
        .where(UploadedTable.user_id == user_id)
        .order_by(UploadedTable.created_at.desc())
    )
    tables = result.scalars().all()
    return [{"id": str(t.id), "name": t.table_name, "row_count": t.row_count} for t in tables]


async def get_table_schema(table_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession) -> Dict:
    result = await db.execute(
        select(FieldMapping).where(FieldMapping.table_id == table_id)
    )
    mappings = result.scalars().all()

    row_result = await db.execute(
        select(UploadedRow)
        .where(UploadedRow.table_id == table_id, UploadedRow.user_id == user_id)
        .limit(1)
    )
    sample_row = row_result.scalar_one_or_none()
    columns = list(sample_row.row_data.keys()) if sample_row else []

    return {
        "table_id": str(table_id),
        "columns": columns,
        "field_mappings": [{"original": m.original_column, "mapped": m.mapped_column} for m in mappings],
    }


async def get_top_k_rows(
    table_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession,
    k: int = None,
) -> List[Dict]:
    k = k or settings.AGENT_TOP_K_RESULTS
    result = await db.execute(
        select(UploadedRow)
        .where(UploadedRow.table_id == table_id, UploadedRow.user_id == user_id)
        .limit(k)
    )
    rows = result.scalars().all()
    return [r.row_data for r in rows]
