#!/bin/bash
# Lokalni razvoj: zgradi stran v ./public in jo postreže na http://localhost:8888
set -e
if python3 -c "" >/dev/null 2>&1; then PY=python3; else PY=python; fi
export MSYS_NO_PATHCONV=1
"$PY" src/main.py "/" "./public"
cd public && "$PY" -m http.server 8888
