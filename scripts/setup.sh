#!/usr/bin/env bash
set -euo pipefail
cp -n .env.example .env || true
python - <<'PY'
import base64, os, pathlib
p=pathlib.Path('.env')
s=p.read_text()
if 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=' in s:
    s=s.replace('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=', base64.b64encode(os.urandom(32)).decode())
    p.write_text(s)
PY
docker compose up --build
