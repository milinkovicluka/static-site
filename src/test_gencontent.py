import unittest

from gencontent import build_nav, extract_title, load_config, render_page


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


class TestConfig(unittest.TestCase):
    def test_empty_nav(self):
        self.assertEqual(build_nav([]), "")

    def test_missing_file_gives_defaults(self):
        self.assertEqual(load_config("/nonexistent/site.json")["lang"], "en")


if __name__ == "__main__":
    unittest.main()