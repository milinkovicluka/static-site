from textnode import TextNode, TextType

def main():
    node = TextNode("This is an anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

main()