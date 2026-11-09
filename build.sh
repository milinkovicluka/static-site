#!/bin/bash
# Produkcija: zgradi stran v ./docs (GitHub Pages, Cloudflare Pages ali Netlify)
# Basepath se nastavi sam, zato ga pri novi strani ni treba popravljati:
#   - Cloudflare Pages, Netlify ali lastna domena (static/CNAME) -> /
#   - GitHub Pages, repozitorij "moja-stran"                     -> /moja-stran/
#   - GitHub Pages, repozitorij "uporabnik.github.io"            -> /
#   - ročni preklic: BASEPATH="/xyz/" ./build.sh
set -e
# Najde delujoč Python: na Linuxu/Macu je to običajno python3, na Windows python.
if python3 -c "" >/dev/null 2>&1; then PY=python3; else PY=python; fi
# Git Bash na Windows bi sicer argumente, kot je "/moja-stran/", pretvoril v Windows poti.
export MSYS_NO_PATHCONV=1

if [ -z "$BASEPATH" ] && { [ -n "$CF_PAGES" ] || [ -n "$NETLIFY" ] || [ -f static/CNAME ]; }; then
    BASEPATH="/"                                  # stran je v korenu domene
fi

if [ -z "$BASEPATH" ]; then
    if [ -n "$GITHUB_REPOSITORY" ]; then
        REPO="${GITHUB_REPOSITORY#*/}"            # v GitHub Actions
    else
        REPO="$(git remote get-url origin 2>/dev/null | sed -E 's#.*/##; s#\.git$##' || true)"  # lokalno
    fi
    case "$REPO" in
        ""|*.github.io) BASEPATH="/" ;;
        *) BASEPATH="/$REPO/" ;;
    esac
fi

echo "Basepath: $BASEPATH"
"$PY" src/main.py "$BASEPATH" "./docs"
