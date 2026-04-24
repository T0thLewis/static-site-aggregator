from delimiter import text_to_textnodes
from htmlnode import ParentNode
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return header_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Invalid block type: {block_type}")


def paragraph_to_html_node(block):
    children = text_to_children(block.replace("\n", " "))
    return ParentNode("p", children)


def header_to_html_node(block):
    level = len(block) - len(block.lstrip("#"))
    if level < 1 or level > 6:
        raise ValueError(f"Invalid heading block: {block}")

    stripped = block[level + 1 :]
    children = text_to_children(stripped)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    content = block[4:-3]
    text_node = TextNode(content, TextType.CODE)
    html_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [html_node])


def quote_to_html_node(block):
    stripped_lines = []
    for line in block.split("\n"):
        if not line.startswith(">"):
            raise ValueError(f"Invalid quote line: {line}")
        stripped_lines.append(line[2:] if line.startswith("> ") else line[1:])
    children = text_to_children(" ".join(stripped_lines))
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        text = line.split(" ", 1)[1]
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_nodes)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
