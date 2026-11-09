---
name: predloga
description: Kako graditi in urejati predstavitveno stran podjetja s to predlogo (statični generator v Pythonu, vsebina v Markdownu + HTML blokih, site.json, tema v CSS). Uporabi pred vsakim dodajanjem ali urejanjem strani, menija, kontaktnih podatkov, slik, obrazca, videza ali generatorja v tem projektu.
---

# Predloga za strani podjetij – kako delati

Jezik strani in dela z uporabnikom: **slovenščina**, vikanje, preprost in topel ton.
Večina obiskovalcev je na **telefonu**: vsako spremembo preveri tudi pri širini 375 px.

## Zgradba

- `content/**/index.md` → vsaka mapa je ena stran. Vsaka `.md` **mora** imeti naslov `# ...`
  (sicer `no h1 header found`). Pod naslovom naj bo `<!-- opis: ... -->` (opis za Google, do ~155 znakov).
- `site.json` → `name`, `lang`, `locale`, `url` (brez `/` na koncu), `description`, `tagline`,
  `theme_color`, `company`, `address`, `area`, `phone`, `phone_display`, `whatsapp`, `email`,
  `instagram`, `cta_label`, `cta_url`, `web3forms_key`, `nav`.
- `template.html` → `{{ Title }}`, `{{ Description }}`, `{{ SiteName }}`, `{{ Lang }}`, `{{ Nav }}`,
  `{{ PageUrl }}`, `{{ Content }}` in poljubni `{{ site.kljuc }}`.
- `static/` → `index.css`, `favicon.svg`, `images/`; skopira se kot je.
- `src/` → generator in testi `test_*.py` (unittest).

## Generator

- `{{ site.kljuc }}` se zamenja v predlogi **in vsebini** z escapano vrednostjo iz `site.json`.
  Neznan ključ → `ValueError: unknown site value`. Kontaktnih podatkov nikoli ne piši ročno v vsebino.
  Če dodaš nov ključ v predlogo, ga dodaj tudi v `site.json`.
- HTML bloki: blok, ki se začne z `<` + črka/`!`/`/`, gre na stran nespremenjen (`RawNode`).
  **Brez praznih vrstic** znotraj bloka; Markdown se v njem ne obdela.
- Basepath: `href="/`, `src="/` in vsi URL-ji v `srcset` z `/` dobijo basepath.
  Notranje povezave in slike vedno piši z začetnim `/`. Drugi atributi (`action`, `content`) se ne popravljajo.
- `sitemap.xml` in `robots.txt` iz map z `index.md` in `url` (brez `url` se preskočita).

## Ukazi

- `./test.sh` – testi (vedno po spremembi v `src/`).
- `./main.sh` – gradnja v `public/` + strežnik na http://localhost:8888.
- `./build.sh` – produkcija v `docs/`; basepath `/` na Cloudflare Pages (`CF_PAGES`), Netlify (`NETLIFY`)
  ali s `static/CNAME`, sicer `/ime-repozitorija/`.

## Markdown

Podprto: naslovi, odstavki, `**krepko**`, `_ležeče_`, `` `koda` ``, kodni bloki, citati `>`,
seznami `- ` in `1. `, povezave, slike. **Ni podprto:** tabele (cene kot seznam), `*ležeče*`,
gnezdeni seznami. Neparni `**` ali `` ` `` → `invalid markdown: unmatched ...`.

## Videz

- Tema je **samo** v bloku `TEMA` na `:root` v `static/index.css` (barve, `--font-body`,
  `--font-heading`, `--heading-weight`, `--radius`, `--btn-radius`). Za novo stranko spreminjaj tam.
- Gradniki: `.hero` (+ `.hero-text`, `.hero-tagline`), `.features` > `.feature`, `.gallery` > `figure.card`,
  `.about`, `.cta`, `.btn` / `.btn-ghost` / `.btn-whatsapp` / `.btn-viber` v `<p class="actions">`,
  `.contact-buttons`, `form.contact-form` (`id="povprasevanje"`), `.form-row`, `.consent`.
- Kontrast besedila ≥ 4.5 : 1. Na `--accent-soft` piši z `--accent-dark`; bel napis samo na temnih barvah.
- CSS je mobile-first: osnova za telefon, `@media (min-width: 560px)` in `(min-width: 860px)`.
  Polja obrazca `font-size` ≥ 16px, gumbi ≥ 46px visoki.
- Pisave gosti lokalno v `static/fonts/` (`@font-face`, `latin-ext`), ne z Google Fonts.

## Obrazec

Web3Forms (`https://api.web3forms.com/submit`), ključ v `site.json` → `web3forms_key`.
Obrazec ima obvezno soglasje in povezavo na `/zasebnost`. Ob spremembi polj posodobi tudi
`content/zasebnost/index.md`.

## Slike

`.webp`/`.jpg`, do ~1600 px, pod 300 KB; naslovna 1200×700, kartice 800×600, O nas 600×700,
`deljenje.png` 1200×630. Vedno `alt`, `width`, `height`, pod pregibom `loading="lazy"`.
