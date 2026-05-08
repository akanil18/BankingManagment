from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.agent import QueryRequest, QueryResponse, ConversationHistoryResponse
from app.services.agent_service import AgentService

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query(
    payload: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await AgentService.handle_query(payload, current_user, db)


@router.get("/history", response_model=ConversationHistoryResponse)
async def history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await AgentService.get_history(current_user, db)


@router.delete("/history", status_code=204)
async def clear_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await AgentService.clear_history(current_user, db)
