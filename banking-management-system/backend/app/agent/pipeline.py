import uuid
import json
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.agent.llm_client import chat
from app.agent.tools import get_user_tables, get_table_schema, get_top_k_rows
from app.agent.memory import load_history
from app.schemas.agent import QueryResponse, ClarifyChoice


SYSTEM_PROMPT = """You are a banking data assistant. You ONLY have access to the current user's uploaded transaction and banking data.
You help users query, analyze, and understand their own financial data.
Always respond based on the data context provided. Format data results as structured JSON when returning rows.
Never access or mention other users' data. Never discuss sensitive personal information."""


class AgentPipeline:

    @staticmethod
    async def run(
        query: str,
        user_id: uuid.UUID,
        db: AsyncSession,
        selected_table_id: Optional[uuid.UUID] = None,
    ) -> QueryResponse:
        # Phase 1: Understand the query
        tables = await get_user_tables(user_id, db)
        if not tables:
            return QueryResponse(
                response_type="text",
                message="You have no uploaded data yet. Please upload an Excel or CSV file first.",
            )

        history = await load_history(user_id, db)

        table_context = json.dumps(tables, indent=2)
        phase1_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history[-10:],
            {
                "role": "user",
                "content": (
                    f"User has these tables:\n{table_context}\n\n"
                    f"User query: {query}\n\n"
                    f"Which table(s) are most relevant? Reply with a JSON object: "
                    f'{{"table_ids": ["<id>", ...], "confident": true/false, "intent": "<brief intent>"}}'
                ),
            },
        ]
        phase1_raw = await chat(phase1_messages, temperature=0.1)

        try:
            phase1 = json.loads(phase1_raw)
        except Exception:
            phase1 = {"table_ids": [tables[0]["id"]], "confident": True, "intent": query}

        relevant_ids = phase1.get("table_ids", [tables[0]["id"]])
        confident = phase1.get("confident", True)

        # If user pre-selected a table, use that
        if selected_table_id:
            relevant_ids = [str(selected_table_id)]
            confident = True

        # Phase 2: Get schema + top-k rows
        schemas = []
        sample_rows = []
        for tid_str in relevant_ids[:3]:
            try:
                tid = uuid.UUID(tid_str)
                schema = await get_table_schema(tid, user_id, db)
                rows = await get_top_k_rows(tid, user_id, db)
                schemas.append(schema)
                sample_rows.extend(rows[:3])
            except Exception:
                continue

        # Not confident → ask user to clarify
        if not confident and len(relevant_ids) > 1:
            options = []
            for t in tables:
                if t["id"] in relevant_ids:
                    options.append(ClarifyChoice(label=t["name"], table_id=uuid.UUID(t["id"])))
            return QueryResponse(
                response_type="clarify",
                message="I found multiple relevant data sections. Which one would you like to query?",
                clarify_options=options,
            )

        # Phase 3: Generate answer
        schema_context = json.dumps(schemas, indent=2)
        sample_context = json.dumps(sample_rows, indent=2)

        phase3_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history[-10:],
            {
                "role": "user",
                "content": (
                    f"Table schemas:\n{schema_context}\n\n"
                    f"Sample rows:\n{sample_context}\n\n"
                    f"User query: {query}\n\n"
                    f"Answer the query. If returning data rows, format as JSON: "
                    f'{{"type": "table", "columns": [...], "rows": [[...], ...], "summary": "..."}} '
                    f'Otherwise: {{"type": "text", "message": "..."}}'
                ),
            },
        ]
        answer_raw = await chat(phase3_messages, temperature=0.2)

        try:
            answer = json.loads(answer_raw)
            if answer.get("type") == "table":
                return QueryResponse(
                    response_type="table",
                    message=answer.get("summary", "Here are the results:"),
                    columns=answer.get("columns", []),
                    rows=[dict(zip(answer["columns"], r)) for r in answer.get("rows", [])],
                )
        except Exception:
            pass

        return QueryResponse(response_type="text", message=answer_raw)
