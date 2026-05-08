from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.data import TableListResponse, RowsResponse
from app.services.data_service import DataService
import uuid

router = APIRouter()


@router.get("/tables", response_model=TableListResponse)
async def get_tables(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await DataService.get_user_tables(current_user, db)


@router.get("/tables/{table_id}/rows", response_model=RowsResponse)
async def get_rows(
    table_id: uuid.UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await DataService.get_table_rows(table_id, page, page_size, current_user, db)


@router.delete("/tables/{table_id}", status_code=204)
async def delete_table(
    table_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await DataService.delete_table(table_id, current_user, db)
