from html import escape

# Prazni (void) HTML elementi nimajo vsebine in zaključne oznake.
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "source", "track", "wbr"}


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(
            f' {key}="{escape(str(value), quote=True)}"'
            for key, value in self.props.items()
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        text = escape(self.value, quote=False)
        if self.tag is None:
            return text
        if self.tag in VOID_TAGS:
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{text}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


class RawNode(HTMLNode):
    """Že pripravljen HTML, ki gre na stran nespremenjen (HTML bloki v Markdownu)."""
    def __init__(self, value):
        super().__init__(None, value, None, None)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        return self.value

    def __repr__(self):
        return f"RawNode({self.value})"
