# Banking Management System — Project Plan

## Overview
A full-stack banking and transaction management system with AI agent support.
Users upload Excel/CSV files, view data on a dashboard, and interact with an
AI agent (powered by a fine-tuned Qwen2.5 1.5B model) via a chat sidebar.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue.js 2 |
| Backend | FastAPI (Python 3.11) |
| Database | PostgreSQL |
| Auth | JWT (python-jose) |
| File Parsing | pandas, openpyxl |
| AI Agent | LangChain |
| LLM | Qwen2.5 1.5B (fine-tuned via Unsloth QLoRA) |
| LLM Serving | llama-server (llama.cpp) |
| Caching / Rate Limit | Redis |
| Migrations | Alembic |

---

## Project Structure

```
banking-management-system/
├── backend/
├── frontend/
├── ai-training/
├── ai-server/
├── plan.md
└── docker-compose.yml
```

---

## Database Schemas

### users
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR | |
| email | VARCHAR | unique |
| password_hash | VARCHAR | bcrypt |
| created_at | TIMESTAMP | |

### uploaded_tables
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK → users |
| table_name | VARCHAR | user-defined label |
| original_filename | VARCHAR | |
| row_count | INTEGER | |
| created_at | TIMESTAMP | |

### uploaded_rows
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| table_id | UUID | FK → uploaded_tables |
| user_id | UUID | FK → users |
| row_data | JSONB | full row as JSON |
| row_index | INTEGER | |

### field_mappings
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| table_id | UUID | FK → uploaded_tables |
| original_column | VARCHAR | CSV column name |
| mapped_column | VARCHAR | standard field name |

### conversations
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK → users |
| role | VARCHAR | 'user' or 'assistant' |
| message | TEXT | |
| created_at | TIMESTAMP | |

### training_data
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| category | VARCHAR | 'field_mapping', 'query', 'safety' |
| instruction | TEXT | |
| input | TEXT | |
| output | TEXT | |
| created_at | TIMESTAMP | |

---

## Execution Phases

### PHASE 1 — Environment Setup
- [ ] Install CUDA Toolkit 12.4
- [ ] Install Miniconda
- [ ] Create conda env: `banking-ai` (Python 3.11)
- [ ] Install PostgreSQL
- [ ] Install Node.js (v18 LTS)
- [ ] Install Git

### PHASE 2 — Project Scaffold + Git Init
- [ ] Create folder structure
- [ ] Create plan.md (this file)
- [ ] Create all example.env files
- [ ] Git init + first commit

### PHASE 3 — Training Data Generation
- [ ] Generate 200 field mapping pairs
- [ ] Generate 500 query → SQL pairs
- [ ] Generate 100 safety/refusal pairs
- [ ] Create training_data table in PostgreSQL
- [ ] Store all pairs in DB
- [ ] Write export script: DB → JSONL

### PHASE 4 — Backend (FastAPI)
- [ ] Project scaffold (main.py, config, database)
- [ ] Alembic migrations for all schemas
- [ ] Auth routes (register, login, refresh token)
- [ ] File upload routes (Excel/CSV parsing)
- [ ] Field mapping service (LLM assisted)
- [ ] Data routes (fetch tables, rows)
- [ ] Agent routes (query, history)
- [ ] LangChain 3-phase pipeline
- [ ] Conversation memory (PostgreSQL backed)
- [ ] Safety filter
- [ ] Rate limiting (Redis)
- [ ] Concurrency (async SQLAlchemy + connection pool)

### PHASE 5 — Fine-tuning (Qwen2.5 1.5B)
- [ ] Export JSONL from PostgreSQL
- [ ] Validate + split dataset (train/eval)
- [ ] Install Unsloth + dependencies in conda env
- [ ] Run QLoRA training script
- [ ] Evaluate model
- [ ] Export to GGUF format

### PHASE 6 — AI Server (llama-server)
- [ ] Install llama.cpp
- [ ] Load GGUF model
- [ ] Start llama-server (OpenAI-compatible API)
- [ ] Connect LangChain agent to llama-server

### PHASE 7 — Frontend (Vue.js 2)
- [ ] Vue CLI scaffold
- [ ] Vuex store setup (auth, upload, data, agent modules)
- [ ] Vue Router with auth guards
- [ ] Login / Register pages
- [ ] File upload page + field mapping modal
- [ ] Data dashboard (table view, filters)
- [ ] Chat sidebar (messages, result tables, clarify options)

### PHASE 8 — Integration & Testing
- [ ] End-to-end flow test (upload → view → chat)
- [ ] Concurrent user test
- [ ] Security test (JWT, user isolation)
- [ ] Edge cases (empty files, bad queries, illegal questions)

---

## Agent 3-Phase Query Pipeline

```
User sends query
      │
      ▼
PHASE 1: UNDERSTAND
  LLM analyzes query intent
  Determines what data is needed
      │
      ▼
PHASE 2: FETCH
  Tool: get_table_schema(user_id)   → column names + types
  Tool: query_top_k_rows(table, q)  → top 5 relevant rows
  LLM generates SQL from schema
      │
      ▼
PHASE 3: RESOLVE
  If confident  → execute SQL → return table
  If ambiguous  → ask user to pick from top-k options
                → user selects → execute → return table
```

---

## Agent Tools (LangChain)

| Tool | Description |
|---|---|
| get_user_tables | List all tables belonging to current user |
| get_table_schema | Get column names and types for a table |
| query_top_k_rows | Get top K rows relevant to query |
| execute_safe_sql | Run scoped SQL (user_id always in WHERE) |
| get_conversation_history | Load last N messages for context |

---

## Security Rules

- Every DB query is scoped by `user_id` — no cross-user access
- JWT required on all protected routes
- Suspicious/illegal queries → safety filter → generic refusal response
- Rate limit: 10 AI queries per user per minute (Redis)
- Passwords hashed with bcrypt (never stored plain)

---

## Git Commit Strategy

| Commit | Content |
|---|---|
| feat: project scaffold and plan | folder structure, plan.md, example.envs |
| feat: backend auth | register, login, JWT |
| feat: backend file upload | CSV/Excel parsing, field mapping |
| feat: backend data API | tables, rows endpoints |
| feat: backend agent pipeline | LangChain 3-phase agent |
| feat: training data generation | 800 pairs in DB |
| feat: fine-tuning pipeline | Unsloth QLoRA training script |
| feat: llama-server setup | GGUF serving config |
| feat: frontend auth pages | login, register |
| feat: frontend upload page | file upload + mapping UI |
| feat: frontend dashboard | data table view |
| feat: frontend chat sidebar | agent chat UI |
| feat: integration complete | end-to-end working |
