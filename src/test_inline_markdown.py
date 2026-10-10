import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("An _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("An ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_multiple_same_delimiter(self):
        node = TextNode("**one** and **two**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
        )

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`all code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("all code", TextType.CODE)])

    def test_no_delimiter(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("plain text", TextType.TEXT)])

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("a `b` c", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("`d`", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("b", TextType.CODE),
                TextNode(" c", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("d", TextType.CODE),
            ],
        )

    def test_chained_bold_then_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has an **unclosed bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()