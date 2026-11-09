import re
from enum import Enum

from htmlnode import ParentNode, RawNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    HTML = "html"


def markdown_to_blocks(markdown):
    # Bloke ločujejo prazne vrstice, razen znotraj kodnega bloka (```),
    # kjer prazne vrstice ostanejo del kode.
    blocks = []
    current = []
    in_code = False
    for line in markdown.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
        if line.strip() == "" and not in_code:
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            continue
        current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return [block for block in blocks if block != ""]


def block_to_block_type(block):
    lines = block.split("\n")

    # Blok, ki se začne s HTML oznako (npr. "<div", "<form", "<!--"), gre na stran nespremenjen.
    if re.match(r"^<[a-zA-Z!/]", block):
        return BlockType.HTML

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.HTML:
        return RawNode(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode("p", text_to_children(paragraph))


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level < 1 or level > 6 or len(block) <= level + 1:
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    if not block.startswith("```\n") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    code = text_node_to_html_node(TextNode(text, TextType.TEXT))
    code_node = ParentNode("code", [code])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    # Prazna vrstica ">" loči odstavke znotraj citata.
    paragraphs = [[]]
    for line in block.split("\n"):
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        text = line[1:].strip()
        if text == "":
            if paragraphs[-1]:
                paragraphs.append([])
            continue
        paragraphs[-1].append(text)
    paragraphs = [" ".join(p) for p in paragraphs if p]
    if len(paragraphs) == 1:
        return ParentNode("blockquote", text_to_children(paragraphs[0]))
    children = [ParentNode("p", text_to_children(p)) for p in paragraphs]
    return ParentNode("blockquote", children)


def ulist_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line[2:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def olist_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line.split(". ", 1)[1]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)