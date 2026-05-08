from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.conversation import Conversation
from app.schemas.agent import QueryRequest, QueryResponse, ConversationHistoryResponse, ConversationMessage
from app.agent.pipeline import AgentPipeline
from app.agent.memory import save_message, clear_history as _clear_history, load_history
from app.agent.safety import is_suspicious, SAFE_REFUSAL


class AgentService:

    @staticmethod
    async def handle_query(payload: QueryRequest, user: User, db: AsyncSession) -> QueryResponse:
        if is_suspicious(payload.query):
            await save_message(user.id, "user", payload.query, db)
            await save_message(user.id, "assistant", SAFE_REFUSAL, db)
            return QueryResponse(response_type="text", message=SAFE_REFUSAL)

        await save_message(user.id, "user", payload.query, db)

        response = await AgentPipeline.run(
            query=payload.query,
            user_id=user.id,
            db=db,
            selected_table_id=payload.selected_table_id,
        )

        await save_message(user.id, "assistant", response.message, db)
        return response

    @staticmethod
    async def get_history(user: User, db: AsyncSession) -> ConversationHistoryResponse:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user.id)
            .order_by(Conversation.created_at.asc())
        )
        messages = result.scalars().all()
        return ConversationHistoryResponse(
            messages=[ConversationMessage.model_validate(m) for m in messages]
        )

    @staticmethod
    async def clear_history(user: User, db: AsyncSession):
        await _clear_history(user.id, db)
