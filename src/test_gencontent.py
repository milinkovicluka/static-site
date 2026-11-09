import unittest

import os
import tempfile

from gencontent import (
    extract_description,
    fix_srcset,
    build_nav,
    build_robots,
    build_sitemap,
    extract_title,
    find_page_urls,
    load_config,
    page_url,
    render_page,
)


class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello world   "), "Hello world")

    def test_h1_not_first_line(self):
        md = "Some intro\n\n# The Title\n\nMore text"
        self.assertEqual(extract_title(md), "The Title")

    def test_ignores_h2(self):
        md = "## Not this\n\n# This one"
        self.assertEqual(extract_title(md), "This one")

    def test_no_title_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Only an h2\n\nand a paragraph")


class TestRenderPage(unittest.TestCase):
    TEMPLATE = (
        '<html lang="{{ Lang }}"><title>{{ Title }} | {{ SiteName }}</title>'
        '<nav>{{ Nav }}</nav><img src="/a.png">{{ Content }}</html>'
    )
    CONFIG = {"name": "Moja", "lang": "sl", "nav": [{"label": "Domov", "url": "/"}]}

    def test_fills_placeholders(self):
        page = render_page(self.TEMPLATE, "Naslov", "<p>x</p>", "/", self.CONFIG)
        self.assertIn('lang="sl"', page)
        self.assertIn("<title>Naslov | Moja</title>", page)
        self.assertIn("<p>x</p>", page)

    def test_basepath_applies_to_nav_and_assets(self):
        page = render_page(self.TEMPLATE, "T", "", "/moja-stran/", self.CONFIG)
        self.assertIn('<a href="/moja-stran/">Domov</a>', page)
        self.assertIn('src="/moja-stran/a.png"', page)

    def test_escapes_title(self):
        page = render_page(self.TEMPLATE, "A & B", "", "/", self.CONFIG)
        self.assertIn("A &amp; B", page)

    def test_works_without_config(self):
        page = render_page(self.TEMPLATE, "T", "c")
        self.assertIn('lang="en"', page)
        self.assertIn("<nav></nav>", page)


    def test_site_values_in_template_and_content(self):
        config = {**self.CONFIG, "phone": "+386 1 234"}
        template = "<p>{{ site.phone }}</p>{{ Content }}"
        page = render_page(template, "T", "<a href=\"tel:{{ site.phone }}\">x</a>", "/", config)
        self.assertEqual(page, '<p>+386 1 234</p><a href="tel:+386 1 234">x</a>')

    def test_site_values_are_escaped(self):
        page = render_page("{{ site.name }}", "T", "", "/", {"name": "A & B"})
        self.assertEqual(page, "A &amp; B")

    def test_unknown_site_value_raises(self):
        with self.assertRaises(ValueError):
            render_page("{{ site.nope }}", "T", "", "/", self.CONFIG)

    def test_current_page_marked_in_nav(self):
        nav = [{"label": "Domov", "url": "/"}, {"label": "Storitve", "url": "/storitve"}]
        out = build_nav(nav, "/storitve")
        self.assertIn('<a href="/storitve" aria-current="page">Storitve</a>', out)
        self.assertIn('<a href="/">Domov</a>', out)
        self.assertIn('aria-current="page">Domov', build_nav(nav, "/"))


class TestSitemap(unittest.TestCase):
    SITE = "https://x.github.io/repo"

    def test_page_url(self):
        self.assertEqual(page_url(self.SITE, "/"), "https://x.github.io/repo/")
        self.assertEqual(page_url(self.SITE + "/", "/storitve"), "https://x.github.io/repo/storitve/")
        self.assertEqual(page_url("", "/storitve"), "")

    def test_find_page_urls(self):
        with tempfile.TemporaryDirectory() as d:
            for sub in ["", "storitve", "o-nas", "prazna"]:
                os.makedirs(os.path.join(d, sub), exist_ok=True)
                if sub != "prazna":
                    open(os.path.join(d, sub, "index.md"), "w").close()
            self.assertEqual(find_page_urls(d), ["/", "/o-nas", "/storitve"])

    def test_build_sitemap(self):
        xml = build_sitemap(self.SITE, ["/", "/storitve"])
        self.assertIn("<loc>https://x.github.io/repo/</loc>", xml)
        self.assertIn("<loc>https://x.github.io/repo/storitve/</loc>", xml)
        self.assertTrue(xml.startswith('<?xml version="1.0"'))

    def test_build_robots(self):
        self.assertIn("Sitemap: https://x.github.io/repo/sitemap.xml", build_robots(self.SITE))

    def test_page_url_placeholder(self):
        config = {**TestRenderPage.CONFIG, "url": self.SITE}
        page = render_page("{{ PageUrl }}", "T", "", "/", config, "/storitve")
        self.assertEqual(page, "https://x.github.io/repo/storitve/")


class TestConfig(unittest.TestCase):
    def test_empty_nav(self):
        self.assertEqual(build_nav([]), "")

    def test_missing_file_gives_defaults(self):
        self.assertEqual(load_config("/nonexistent/site.json")["lang"], "en")


class TestDescription(unittest.TestCase):
    def test_extract(self):
        md = "# Naslov\n\n<!-- opis: Kratek opis strani. -->\n\nBesedilo"
        self.assertEqual(extract_description(md), "Kratek opis strani.")

    def test_missing(self):
        self.assertIsNone(extract_description("# Naslov\n\nBesedilo"))

    def test_page_description_overrides_site(self):
        config = {"description": "Opis podjetja"}
        page = render_page("{{ Description }}", "T", "", "/", config, "/", "Moj & opis")
        self.assertEqual(page, "Moj &amp; opis")

    def test_falls_back_to_site_description(self):
        config = {"description": "Opis podjetja"}
        self.assertEqual(render_page("{{ Description }}", "T", "", "/", config), "Opis podjetja")


class TestSrcset(unittest.TestCase):
    def test_every_url_gets_basepath(self):
        page = '<img src="/a.webp" srcset="/a-800.webp 800w, /a-1600.webp 1600w">'
        out = render_page("{{ Content }}", "T", page, "/repo/")
        self.assertIn('src="/repo/a.webp"', out)
        self.assertIn('srcset="/repo/a-800.webp 800w, /repo/a-1600.webp 1600w"', out)

    def test_external_urls_unchanged(self):
        out = fix_srcset('srcset="https://x.si/a.webp 1x"', "/repo/")
        self.assertEqual(out, 'srcset="https://x.si/a.webp 1x"')


if __name__ == "__main__":
    unittest.main()