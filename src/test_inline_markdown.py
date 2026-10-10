import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            extract_markdown_images(text),
        )

    def test_extract_markdown_links(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            extract_markdown_links(text),
        )

    def test_links_ignore_images(self):
        text = "A [link](https://a.com) and an ![image](https://b.com/x.png)"
        self.assertListEqual(
            [("link", "https://a.com")], extract_markdown_links(text)
        )

    def test_images_ignore_links(self):
        text = "A [link](https://a.com) and an ![image](https://b.com/x.png)"
        self.assertListEqual(
            [("image", "https://b.com/x.png")], extract_markdown_images(text)
        )

    def test_no_matches(self):
        self.assertListEqual([], extract_markdown_images("no images here"))
        self.assertListEqual([], extract_markdown_links("no links here"))

    def test_empty_alt_text(self):
        self.assertListEqual(
            [("", "https://b.com/x.png")],
            extract_markdown_images("![](https://b.com/x.png)"),
        )


class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_only(self):
        node = TextNode("![alone](https://x.com/a.png)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("alone", TextType.IMAGE, "https://x.com/a.png")],
            split_nodes_image([node]),
        )

    def test_split_image_trailing_text(self):
        node = TextNode("![pic](https://x.com/a.png) after", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("pic", TextType.IMAGE, "https://x.com/a.png"),
                TextNode(" after", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_image_no_images(self):
        node = TextNode("no images here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_image_ignores_links(self):
        node = TextNode("a [link](https://a.com) only", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_image_non_text_unchanged(self):
        node = TextNode("bold", TextType.BOLD)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            split_nodes_link([node]),
        )

    def test_split_link_trailing_text(self):
        node = TextNode("[home](https://a.com) is great", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("home", TextType.LINK, "https://a.com"),
                TextNode(" is great", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_link_ignores_images(self):
        node = TextNode("an ![image](https://b.com/x.png) only", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("[a](https://a.com)", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("see [b](https://b.com)", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode("code", TextType.CODE),
                TextNode("see ", TextType.TEXT),
                TextNode("b", TextType.LINK, "https://b.com"),
            ],
            split_nodes_link(nodes),
        )

    def test_split_image_then_link(self):
        node = TextNode(
            "![img](https://b.com/x.png) and [link](https://a.com)", TextType.TEXT
        )
        nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://b.com/x.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://a.com"),
            ],
            nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_plain_text(self):
        self.assertListEqual(
            [TextNode("just plain text", TextType.TEXT)],
            text_to_textnodes("just plain text"),
        )

    def test_only_bold(self):
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            text_to_textnodes("**bold**"),
        )

    def test_underscore_in_url_not_italic(self):
        self.assertListEqual(
            [
                TextNode("see ", TextType.TEXT),
                TextNode("file", TextType.LINK, "https://a.com/my_file_name"),
            ],
            text_to_textnodes("see [file](https://a.com/my_file_name)"),
        )

    def test_markdown_inside_code_stays_literal(self):
        self.assertListEqual(
            [
                TextNode("use ", TextType.TEXT),
                TextNode("**stars**", TextType.CODE),
            ],
            text_to_textnodes("use `**stars**`"),
        )

    def test_unmatched_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("this **is broken")

if __name__ == "__main__":
    unittest.main()