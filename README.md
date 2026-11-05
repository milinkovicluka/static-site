# Tolkien Fan Club – generator statičnih strani

Preprost generator statičnih strani v Pythonu, narejen v okviru tečaja
[Build a Static Site Generator](https://www.boot.dev/courses/build-static-site-generator-python)
na Boot.dev. Markdown datoteke iz `content/` pretvori v HTML strani po predlogi
`template.html` in jim doda datoteke iz `static/`.

Objavljena stran: https://milinkovicluka.github.io/static-site/

## Zahteve

- Python 3.10 ali novejši (brez dodatnih knjižnic)
- Bash (na Windows: Git Bash)

## Uporaba

```bash
./test.sh    # požene teste
./main.sh    # zgradi stran v public/ in jo postreže na http://localhost:8888
./build.sh   # zgradi stran za GitHub Pages v docs/
```

Skripte delujejo na Linuxu, macOS in Windows (Git Bash).

## Objava

Ob vsakem pushu na `main` GitHub Actions (`.github/workflows/deploy.yml`) požene
teste, zgradi stran in jo objavi na GitHub Pages. Mapi `docs/` in `public/` nista
v repozitoriju, ker se ustvarita pri gradnji.

## Podprt Markdown

Naslovi (`#`–`######`), odstavki, **krepko**, _ležeče_, `koda`, kodni bloki,
citati, neoštevilčeni (`- `) in oštevilčeni (`1. `) seznami, povezave in slike.
