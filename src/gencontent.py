import html
import json
import os

from block_markdown import markdown_to_html_node

DEFAULT_CONFIG = {"name": "", "lang": "en", "nav": []}


def load_config(path):
    """Prebere site.json; manjkajoča datoteka ali polja dobijo privzete vrednosti."""
    config = dict(DEFAULT_CONFIG)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            config.update(json.load(f))
    return config


def build_nav(nav):
    links = [
        f'<a href="{html.escape(item["url"])}">{html.escape(item["label"])}</a>'
        for item in nav
    ]
    return " ".join(links)


def render_page(template, title, content, basepath="/", config=None):
    config = {**DEFAULT_CONFIG, **(config or {})}
    page = (
        template.replace("{{ Title }}", html.escape(title))
        .replace("{{ SiteName }}", html.escape(config["name"]))
        .replace("{{ Lang }}", html.escape(config["lang"]))
        .replace("{{ Nav }}", build_nav(config["nav"]))
        .replace("{{ Content }}", content)
    )
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')
    return page


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no h1 header found")


def generate_page(from_path, template_path, dest_path, basepath="/", config=None):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = render_page(template, title, html_content, basepath, config)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath="/", config=None
):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path = dest_path[:-3] + ".html"
                generate_page(from_path, template_path, dest_path, basepath, config)
        else:
            generate_pages_recursive(
                from_path, template_path, dest_path, basepath, config
            )