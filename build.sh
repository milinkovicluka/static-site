#!/bin/bash
# Produkcija: zgradi stran za GitHub Pages v ./docs
set -e
# Najde delujoč Python: na Linuxu/Macu je to običajno python3, na Windows python.
if python3 -c "" >/dev/null 2>&1; then PY=python3; else PY=python; fi
# Git Bash na Windows bi sicer argumente, kot je "/static-site/", pretvoril v Windows poti.
export MSYS_NO_PATHCONV=1
"$PY" src/main.py "/static-site/" "./docs"
