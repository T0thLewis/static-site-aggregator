from textnode import TextNode, TextType


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
            raise Exception(
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
