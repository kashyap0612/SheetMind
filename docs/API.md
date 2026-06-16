# SheetMind API

Base URL: `http://localhost:8000/api/v1`

All protected routes require `Authorization: Bearer <Clerk JWT>`. In development only, `Bearer dev:<id>` creates or reuses a local user.

## Endpoints

- `GET /health` — service health.
- `GET /users/me` — current user and free query quota.
- `GET /files?search=` — list uploaded files owned by the authenticated user.
- `POST /files` — multipart upload field `upload`; accepts CSV/XLSX up to 50 MB.
- `GET /files/{file_id}` — file metadata, sheets, columns, sample rows.
- `POST /chat/query` — ask a question about a file. Body: `{ "file_id": 1, "question": "Average package for CSE students", "provider": "openai" }`.
- `GET /api-keys` — list provider key hints only.
- `PUT /api-keys` — validate and encrypt a provider key. Body: `{ "provider": "openai", "api_key": "sk-..." }`.
- `DELETE /api-keys/{provider}` — delete stored encrypted key.

The query endpoint returns `answer`, validated structured `action`, `execution_plan`, `result`, and `free_queries_remaining`.
