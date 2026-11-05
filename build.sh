#!/bin/bash
# Produkcija: zgradi stran za GitHub Pages v ./docs
set -e
MSYS_NO_PATHCONV=1 python src/main.py "/static-site/" "./docs"