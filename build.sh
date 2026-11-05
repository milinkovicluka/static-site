#!/bin/bash
# Produkcija: zgradi stran za GitHub Pages v ./docs
set -e
python src/main.py "/static-site/" "./docs"