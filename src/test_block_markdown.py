import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_excessive_newlines(self):
        md = """
# Heading



Paragraph after many blank lines


"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["# Heading", "Paragraph after many blank lines"],
        )

    def test_strips_whitespace(self):
        md = "   first block   \n\n\tsecond block\t"
        self.assertEqual(
            markdown_to_blocks(md),
            ["first block", "second block"],
        )

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("just one block"), ["just one block"])

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_heading_paragraph_list(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Six"), BlockType.HEADING)

    def test_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Seven"), BlockType.PARAGRAPH)

    def test_heading_no_space(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code(self):
        block = "```\nprint('hi')\nx = 1\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_unclosed(self):
        block = "```\nprint('hi')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote(self):
        block = "> line one\n>line two without space"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_broken_line(self):
        block = "> line one\nnot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        block = "- one\n-two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        block = "2. one\n3. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_skips_number(self):
        block = "1. one\n3. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "Just some text\nover two lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading one

### Heading with **bold**
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading one</h1><h3>Heading with <b>bold</b></h3></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with _italic_ text
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <i>italic</i> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- first item
- second with `code`
- third
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second with <code>code</code></li><li>third</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first
2. second with **bold**
3. third
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second with <b>bold</b></li><li>third</li></ol></div>",
        )

    def test_mixed_document(self):
        md = """
# Title

A paragraph with a [link](https://boot.dev).

- item one
- item two
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><h1>Title</h1><p>A paragraph with a <a href="https://boot.dev">link</a>.</p><ul><li>item one</li><li>item two</li></ul></div>',
        )


    
class TestHTMLBlock(unittest.TestCase):
    def test_html_block_type(self):
        self.assertEqual(block_to_block_type('<div class="x">\n<p>a</p>\n</div>'), BlockType.HTML)
        self.assertEqual(block_to_block_type("<!-- opomba -->"), BlockType.HTML)

    def test_angle_bracket_text_is_paragraph(self):
        self.assertEqual(block_to_block_type("< nazaj"), BlockType.PARAGRAPH)

    def test_html_passes_through(self):
        md = "# Naslov\n\n<form action=\"https://x\">\n<input name=\"a\">\n</form>\n\nBesedilo"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><h1>Naslov</h1><form action="https://x">\n<input name="a">\n</form><p>Besedilo</p></div>',
        )


if __name__ == "__main__":
    unittest.main()
