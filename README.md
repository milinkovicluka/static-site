# Predloga za spletne strani malih podjetij

Generator statičnih strani v Pythonu (nastal v okviru tečaja
[Build a Static Site Generator](https://www.boot.dev/courses/build-static-site-generator-python)
na Boot.dev) in pripravljena predloga za predstavitveno stran podjetja: Domov,
Storitve, O nas, Kontakt z obrazcem in Politika zasebnosti.

Markdown in HTML bloki iz `content/` se po predlogi `template.html` pretvorijo
v statične HTML strani. Ni baze, ni vtičnikov, ni posodobitev: stran je hitra,
varna in gostovanje je brezplačno.

## Zahteve

- Python 3.10 ali novejši (brez dodatnih knjižnic)
- Bash (na Windows: Git Bash)

## Ukazi

```bash
./test.sh    # požene teste
./main.sh    # zgradi stran v public/ in jo postreže na http://localhost:8888
./build.sh   # produkcijska gradnja v docs/
```

## Nova stranka – kontrolni seznam

1. **Nov repozitorij.** Na GitHubu: Settings → obkljukaj **Template repository**,
   nato **Use this template → Create a new repository** (npr. `mizarstvo-novak`).
2. **`site.json`**: ime, opis, slogan, kontakt, naslov, `company` (pravno ime za nogo
   in zasebnost), `cta_label`/`cta_url` (glavni gumb) in meni (`nav`).
3. **Tema** v `static/index.css`, blok `TEMA` na vrhu: barve, pisava, zaobljenost.
   Isto barvo vpiši v `theme_color` v `site.json`. Preveri kontrast belega
   napisa na `--accent` (≥ 4.5 : 1, npr. na [webaim.org/resources/contrastchecker](https://webaim.org/resources/contrastchecker/)).
4. **Vsebina** v `content/`: besedila, storitve, cene, pogosta vprašanja, mnenja strank.
   Vsaka stran naj ima svoj `<!-- opis: ... -->` za Google.
5. **Fotografije** v `static/images/` (glej spodaj) in slika za deljenje `deljenje.png`.
6. **`favicon.svg`**: črka ali logotip stranke.
7. **Obrazec**: ključ Web3Forms v `web3forms_key` (glej spodaj). Pošlji testno povpraševanje.
8. **Politika zasebnosti** (`content/zasebnost/`): preberi in prilagodi dejanskemu stanju.
9. **Objava** in **domena** (glej spodaj), nato `url` v `site.json` nastavi na pravi naslov.
10. **Preverjanje**: telefon (prava naprava), [PageSpeed Insights](https://pagespeed.web.dev),
    sitemap oddaj v [Google Search Console](https://search.google.com/search-console),
    uredi profil na Google Business Profile.

## Zgradba projekta

| Pot | Vsebina |
| --- | --- |
| `content/` | strani; vsaka mapa z `index.md` postane svoja stran (`content/storitve/index.md` → `/storitve/`) |
| `site.json` | podatki podjetja, glavni gumb, ključ za obrazec in meni |
| `template.html` | glava (znamka, gumb, meni), noga, spodnja vrstica za telefon, meta oznake |
| `static/` | `index.css`, `favicon.svg`, `images/`; skopira se na stran kot je |
| `src/` | generator in testi |
| `.claude/skills/predloga/` | navodila za Claude Code pri delu s to predlogo |

Pri gradnji nastaneta še `sitemap.xml` in `robots.txt` (iz map v `content/` in `url` v `site.json`).

## Oznake v predlogi in vsebini

| Oznaka | Vrednost |
| --- | --- |
| `{{ Title }}` | naslov strani (prva vrstica `# ...` v `index.md`) |
| `{{ Description }}` | opis strani iz `<!-- opis: ... -->`, sicer `description` iz `site.json` |
| `{{ SiteName }}`, `{{ Lang }}` | `name` in `lang` iz `site.json` |
| `{{ Nav }}` | meni iz `nav`; trenutna stran dobi `aria-current="page"` |
| `{{ PageUrl }}` | polni naslov strani (za canonical in deljenje) |
| `{{ Content }}` | vsebina strani |
| `{{ site.kljuc }}` | katerakoli vrednost iz `site.json`, tudi v vsebini (npr. `{{ site.phone_display }}`) |

Kontaktne podatke piši samo v `site.json`, v vsebini vedno prek `{{ site.* }}`.
Neznan ključ (tipkarska napaka) ustavi gradnjo z napako, da ne pride na stran.

## Gradniki (CSS razredi)

Vsebina je Markdown, za postavitve pa uporabiš HTML bloke s temi razredi
(primeri so v `content/`):

| Razred | Uporaba |
| --- | --- |
| `.hero` > `img` + `.hero-text` | naslovni del s sliko, sloganom in gumbi |
| `.features` > `.feature` | tri prednosti v stolpcih |
| `.gallery` > `figure.card` | kartice storitev ali izdelkov (`<strong>` ime, `<span>` cena, `<p>` opis, `<a>` povezava) |
| `.about` | slika + besedilo (O nas) |
| `.cta` | poziv k dejanju na koncu strani |
| `.btn`, `.btn-ghost`, `.btn-whatsapp`, `.btn-viber` | gumbi; več gumbov v `<p class="actions">` |
| `.contact-buttons` | kontaktni gumbi |
| `form.contact-form`, `.form-row`, `.consent` | obrazec |

**HTML blok** je blok, ki se začne z oznako (`<div`, `<section`, `<form`, `<!--` ...).
Gre na stran nespremenjen. V njem ne sme biti prazne vrstice, ker ta konča blok.

**Podprt Markdown:** naslovi (`#`–`######`), odstavki, **krepko**, _ležeče_, `koda`,
kodni bloki, citati, seznami (`- ` in `1. `), povezave in slike.
Ni podprto: tabele, `*ležeče*`, gnezdeni seznami.

## Pisava

Privzeto se uporablja sistemska pisava (hitro, brez zunanjih strežnikov). Za
lastno pisavo stranke:

1. Prenesi datoteke `.woff2` (npr. z [gwfh.mranftl.com](https://gwfh.mranftl.com/fonts),
   z naborom znakov `latin-ext` zaradi č, š, ž) v `static/fonts/`.
2. Na vrh `static/index.css` dodaj:
   ```css
   @font-face {
     font-family: "Moja pisava";
     src: url("fonts/moja-pisava.woff2") format("woff2");
     font-weight: 400 700;
     font-display: swap;
   }
   ```
3. V bloku `TEMA` nastavi npr. `--font-heading: "Moja pisava", Georgia, serif;`.

Pisave raje gosti na svoji strani kot nalagaj z Googlovih strežnikov, ker to
v EU sproža vprašanja glede GDPR.

## Obrazec

Obrazec na strani Kontakt pošilja sporočila prek brezplačne storitve
[Web3Forms](https://web3forms.com): na njihovi strani vpišeš e-pošto stranke, dobiš
ključ (access key) in ga vpišeš v `site.json` pod `web3forms_key`. Dokler je tam
`VSTAVI-SVOJ-KLJUC`, obrazec ne deluje.

## Slike

Vzorčne slike so SVG v `static/images/`. Prave fotografije:

1. Shrani jih v `static/images/` kot `.webp` ali `.jpg`, široke do ~1600 px, pod 300 KB.
2. V `content/` zamenjaj `src` in posodobi `width`/`height`.

Velikosti: naslovna 1200 × 700, kartice 800 × 600 (4 : 3), O nas 600 × 700,
slika za deljenje `deljenje.png` 1200 × 630.

Za telefone pripravi več velikosti in jih poveži s `srcset` (generator pred vse
poti z `/` sam doda basepath):

```html
<img src="/images/foto-800.webp" srcset="/images/foto-800.webp 800w, /images/foto-1600.webp 1600w" sizes="(min-width: 860px) 33vw, 100vw" alt="..." width="800" height="600" loading="lazy">
```

Pretvorba: `cwebp -q 80 -resize 800 0 foto.jpg -o foto-800.webp`
(Mac: `brew install webp`, Linux: `apt install webp`).

## Objava

**Za stranke: Cloudflare Pages ali Netlify** (brezplačno, dovoljena komercialna uporaba).
GitHub Pages po pogojih uporabe ni namenjen spletnim stranem podjetij, zato ga
uporabljaj samo za predogled.

- **Cloudflare Pages**: Workers & Pages → Create → Pages → poveži repozitorij.
  Build command `bash build.sh`, output directory `docs`, okoljska spremenljivka
  `PYTHON_VERSION` = `3.12`.
- **Netlify**: Add new site → Import from Git. Build command `bash build.sh`,
  publish directory `docs`.
- **GitHub Pages** (predogled): Settings → Pages → Source **GitHub Actions**.
  Ob vsakem pushu na `main` `.github/workflows/deploy.yml` požene teste, zgradi
  in objavi stran.

Basepath se nastavi sam: na Cloudflare Pages, Netlify in z lastno domeno
(`static/CNAME`) je `/`, na GitHub Pages `/ime-repozitorija/`.
Ročni preklic: `BASEPATH="/xyz/" ./build.sh`.

Domena (`.si` ~10–15 €/leto) naj bo registrirana na stranko. Ko je povezana,
nastavi `url` v `site.json`.

Mapi `docs/` in `public/` nista v repozitoriju, ker se ustvarita pri gradnji.
