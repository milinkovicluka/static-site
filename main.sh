#!/bin/bash
# Lokalni razvoj: zgradi stran v ./public (ni v gitu) in jo postreže na http://localhost:8888
set -e
MSYS_NO_PATHCONV=1 python src/main.py "/" "./public"
cd public && python -m http.server 8888