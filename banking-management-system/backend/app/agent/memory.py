import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.conversation import Conversation
from app.config import settings


async def load_history(user_id: uuid.UUID, db: AsyncSession) -> list[dict]:
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.asc())
        .limit(settings.AGENT_MAX_CONVERSATION_HISTORY)
    )
    messages = result.scalars().all()
    return [{"role": m.role, "content": m.message} for m in messages]


async def save_message(user_id: uuid.UUID, role: str, message: str, db: AsyncSession):
    db.add(Conversation(user_id=user_id, role=role, message=message))
    await db.flush()


async def clear_history(user_id: uuid.UUID, db: AsyncSession):
    await db.execute(delete(Conversation).where(Conversation.user_id == user_id))
