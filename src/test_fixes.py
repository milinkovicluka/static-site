import unittest

from htmlnode import LeafNode
from inline_markdown import text_to_textnodes
from block_markdown import markdown_to_blocks, markdown_to_html_node
from textnode import TextNode, TextType


class TestFixes(unittest.TestCase):
    def test_text_is_escaped(self):
        self.assertEqual(LeafNode(None, "< Back & Home").to_html(), "&lt; Back &amp; Home")

    def test_attribute_is_escaped(self):
        node = LeafNode("a", "x", {"href": 'a"b'})
        self.assertEqual(node.to_html(), '<a href="a&quot;b">x</a>')

    def test_img_has_no_closing_tag(self):
        node = LeafNode("img", "", {"src": "a.png", "alt": "A"})
        self.assertEqual(node.to_html(), '<img src="a.png" alt="A">')

    def test_blank_line_inside_code(self):
        md = "Intro\n\n```\nline one\n\nline two\n```\n\nOutro"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Intro", "```\nline one\n\nline two\n```", "Outro"],
        )

    def test_quote_paragraphs(self):
        md = '> "Quote."\n>\n> -- Author'
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            '<div><blockquote><p>"Quote."</p><p>-- Author</p></blockquote></div>',
        )

    def test_snake_case_is_not_italic(self):
        self.assertEqual(
            text_to_textnodes("use my_var_name here"),
            [TextNode("use my_var_name here", TextType.TEXT)],
        )


if __name__ == "__main__":
    unittest.main()