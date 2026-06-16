# SheetMind

SheetMind is a production-oriented MVP for AI-powered spreadsheet analytics. It combines a Next.js 15 App Router frontend with a FastAPI backend, PostgreSQL metadata storage, Cloudflare R2 file storage, and a structured action engine powered by Pandas/DuckDB-compatible dataframes.

## Features

- Clerk Google sign-in, protected dashboard/profile/settings routes, and logout via Clerk `UserButton`.
- CSV/XLSX uploads with 50 MB limit, MIME and extension validation.
- Original file storage in Cloudflare R2; local disk fallback for development.
- Metadata extraction: sheets, columns, dtypes, row/column counts, sample rows.
- Natural-language spreadsheet questions converted into validated structured actions, not SQL.
- Operations: count, average, sum, min, max, filter, sort, groupby, top_n, unique, null_analysis.
- Free tier with 10 included queries and encrypted bring-your-own API key support for OpenAI, Gemini, and Anthropic.
- AES-256-GCM key encryption, Pydantic validation, route ownership checks, JWT verification, rate limiting, service/repository layering, Alembic migrations.

## Local development

```bash
./scripts/setup.sh
```

Then open:

- Frontend: http://localhost:3000
- Backend health: http://localhost:8000/api/v1/health
- OpenAPI: http://localhost:8000/api/v1/openapi.json

For backend-only development:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Environment variables

See `.env.example` for all variables. Important values:

- `ENCRYPTION_KEY`: base64 encoded 32-byte key for AES-256-GCM.
- `DATABASE_URL`: SQLAlchemy PostgreSQL connection string.
- `CLERK_ISSUER`, `CLERK_JWKS_URL`: Clerk JWT verification settings.
- `R2_ENDPOINT_URL`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`: Cloudflare R2 storage.
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY`: Clerk frontend/server credentials.
- `NEXT_PUBLIC_API_URL`: frontend-to-backend API base URL.

## Project structure

```text
backend/app/api/routes   FastAPI route modules
backend/app/models       SQLAlchemy models
backend/app/services     storage, spreadsheet parsing, LLM planning, action execution
backend/alembic          migrations
frontend/app             Next.js App Router pages
frontend/components      SaaS dashboard and reusable UI
frontend/lib             API client and utilities
docs                     API and deployment docs
```
