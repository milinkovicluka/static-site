#!/bin/bash
set -e
if python3 -c "" >/dev/null 2>&1; then PY=python3; else PY=python; fi
export MSYS_NO_PATHCONV=1
"$PY" -m unittest discover -s src
