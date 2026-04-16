from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Closing delimiter {delimiter} not found in text {node.text}"
            )
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 != 0:
                new_nodes.append(TextNode(parts[i], text_type))
            else:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        parts = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        if parts[0] != "":
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
        new_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
        if parts[1] != "":
            new_nodes.extend(split_nodes_image([TextNode(parts[1], TextType.TEXT)]))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        parts = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        if parts[0] != "":
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
        new_nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
        if parts[1] != "":
            new_nodes.extend(split_nodes_link([TextNode(parts[1], TextType.TEXT)]))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
