# Deployment Guide

1. Provision PostgreSQL and Cloudflare R2.
2. Configure Clerk Google OAuth and copy issuer/JWKS URLs.
3. Generate a 32-byte AES key: `python -c "import os,base64; print(base64.b64encode(os.urandom(32)).decode())"`.
4. Set environment variables from `.env.example` in your host or secrets manager.
5. Run backend migrations: `cd backend && alembic upgrade head`.
6. Deploy `backend` as a FastAPI service and `frontend` as a Next.js standalone app.
7. Restrict CORS to the production frontend URL and enable HTTPS everywhere.

Cloudflare R2 credentials are optional for local development because the backend falls back to `/tmp/sheetmind-storage`, but production should always set R2 credentials.
