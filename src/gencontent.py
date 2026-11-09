import html
import json
import os
import re

from block_markdown import markdown_to_html_node

DEFAULT_CONFIG = {"name": "", "lang": "en", "nav": [], "url": ""}


def load_config(path):
    """Prebere site.json; manjkajoča datoteka ali polja dobijo privzete vrednosti."""
    config = dict(DEFAULT_CONFIG)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            config.update(json.load(f))
    return config


SITE_PLACEHOLDER = re.compile(r"\{\{ site\.(\w+) \}\}")
DESCRIPTION_COMMENT = re.compile(r"^<!--\s*opis:\s*(.*?)\s*-->\s*$", re.MULTILINE)
SRCSET_ATTR = re.compile(r'srcset="([^"]*)"')


def _same_page(a, b):
    return a.strip("/") == b.strip("/")


def build_nav(nav, current_url=None):
    links = []
    for item in nav:
        current = ""
        if current_url is not None and _same_page(item["url"], current_url):
            current = ' aria-current="page"'
        links.append(
            f'<a href="{html.escape(item["url"])}"{current}>{html.escape(item["label"])}</a>'
        )
    return " ".join(links)


def fill_site_values(text, config):
    """Zamenja {{ site.kljuc }} z vrednostjo iz site.json (v predlogi in vsebini)."""

    def replace(match):
        key = match.group(1)
        if key not in config or not isinstance(config[key], (str, int, float)):
            raise ValueError(f"unknown site value: {{{{ site.{key} }}}}")
        return html.escape(str(config[key]))

    return SITE_PLACEHOLDER.sub(replace, text)


def page_url(site_url, url):
    """Polni naslov strani, npr. https://x.github.io/repo + /storitve -> .../repo/storitve/"""
    if not site_url:
        return ""
    path = url.strip("/")
    return site_url.rstrip("/") + "/" + (path + "/" if path else "")


def find_page_urls(dir_path_content, url="/"):
    """Vrne URL-je vseh strani (map z index.md), urejene po abecedi."""
    urls = []
    for filename in sorted(os.listdir(dir_path_content)):
        path = os.path.join(dir_path_content, filename)
        if filename == "index.md":
            urls.append(url)
        elif os.path.isdir(path):
            urls.extend(find_page_urls(path, url.rstrip("/") + "/" + filename))
    return urls


def build_sitemap(site_url, urls):
    entries = "".join(
        f"  <url><loc>{html.escape(page_url(site_url, u))}</loc></url>\n" for u in urls
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}</urlset>\n"
    )


def build_robots(site_url):
    return f"User-agent: *\nAllow: /\n\nSitemap: {page_url(site_url, '/')}sitemap.xml\n"


def generate_sitemap(dir_path_content, dest_dir_path, config):
    """Zapiše sitemap.xml in robots.txt; brez "url" v site.json ne naredi ničesar."""
    site_url = config.get("url", "")
    if not site_url:
        print("No url in site.json, skipping sitemap.xml and robots.txt")
        return
    urls = find_page_urls(dir_path_content)
    with open(os.path.join(dest_dir_path, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(build_sitemap(site_url, urls))
    with open(os.path.join(dest_dir_path, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(build_robots(site_url))


def extract_description(markdown):
    """Opis strani za Google iz vrstice <!-- opis: ... --> (če je ni, vrne None)."""
    match = DESCRIPTION_COMMENT.search(markdown)
    return match.group(1) if match else None


def fix_srcset(page, basepath):
    """V srcset doda basepath pred vsak URL, ki se začne z "/"."""

    def replace(match):
        parts = [p.strip() for p in match.group(1).split(",")]
        fixed = [basepath + p[1:] if p.startswith("/") else p for p in parts]
        return 'srcset="' + ", ".join(fixed) + '"'

    return SRCSET_ATTR.sub(replace, page)


def render_page(
    template, title, content, basepath="/", config=None, current_url=None, description=None
):
    config = {**DEFAULT_CONFIG, **(config or {})}
    if description is None:
        description = config.get("description", "")
    page = (
        template.replace("{{ Title }}", html.escape(title))
        .replace("{{ Description }}", html.escape(description))
        .replace("{{ SiteName }}", html.escape(config["name"]))
        .replace("{{ Lang }}", html.escape(config["lang"]))
        .replace("{{ Nav }}", build_nav(config["nav"], current_url))
        .replace("{{ PageUrl }}", html.escape(page_url(config["url"], current_url or "/")))
        .replace("{{ Content }}", content)
    )
    page = fill_site_values(page, config)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')
    page = fix_srcset(page, basepath)
    return page


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no h1 header found")


def generate_page(
    from_path, template_path, dest_path, basepath="/", config=None, current_url=None
):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    description = extract_description(markdown)

    page = render_page(
        template, title, html_content, basepath, config, current_url, description
    )

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath="/", config=None, url="/"
):
    for filename in sorted(os.listdir(dir_path_content)):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path = dest_path[:-3] + ".html"
                generate_page(
                    from_path, template_path, dest_path, basepath, config, url
                )
        else:
            generate_pages_recursive(
                from_path, template_path, dest_path, basepath, config,
                url.rstrip("/") + "/" + filename,
            )