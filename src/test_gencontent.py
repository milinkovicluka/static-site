import unittest

from gencontent import extract_title


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


if __name__ == "__main__":
    unittest.main()