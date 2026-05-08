import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from app.models.uploaded_table import UploadedTable, UploadedRow
from app.models.user import User
from app.schemas.data import TableListResponse, TableMeta, RowsResponse
from app.core.exceptions import NotFoundException, ForbiddenException


class DataService:

    @staticmethod
    async def get_user_tables(user: User, db: AsyncSession) -> TableListResponse:
        result = await db.execute(
            select(UploadedTable)
            .where(UploadedTable.user_id == user.id)
            .order_by(UploadedTable.created_at.desc())
        )
        tables = result.scalars().all()
        return TableListResponse(tables=[TableMeta.model_validate(t) for t in tables])

    @staticmethod
    async def get_table_rows(
        table_id: uuid.UUID,
        page: int,
        page_size: int,
        user: User,
        db: AsyncSession,
    ) -> RowsResponse:
        result = await db.execute(
            select(UploadedTable).where(
                UploadedTable.id == table_id,
                UploadedTable.user_id == user.id,
            )
        )
        table = result.scalar_one_or_none()
        if not table:
            raise NotFoundException("Table")

        offset = (page - 1) * page_size
        rows_result = await db.execute(
            select(UploadedRow)
            .where(UploadedRow.table_id == table_id, UploadedRow.user_id == user.id)
            .order_by(UploadedRow.row_index)
            .offset(offset)
            .limit(page_size)
        )
        rows = rows_result.scalars().all()
        row_dicts = [r.row_data for r in rows]
        columns = list(row_dicts[0].keys()) if row_dicts else []

        return RowsResponse(
            table_id=table.id,
            table_name=table.table_name,
            columns=columns,
            rows=row_dicts,
            total=table.row_count,
            page=page,
            page_size=page_size,
        )

    @staticmethod
    async def delete_table(table_id: uuid.UUID, user: User, db: AsyncSession):
        result = await db.execute(
            select(UploadedTable).where(
                UploadedTable.id == table_id,
                UploadedTable.user_id == user.id,
            )
        )
        table = result.scalar_one_or_none()
        if not table:
            raise NotFoundException("Table")

        await db.delete(table)
