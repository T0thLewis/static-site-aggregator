import unittest

from delimiter import split_nodes_delimiter
from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, TextNode("This is a text node", TextType.ITALIC))
        self.assertNotEqual(
            node, TextNode("This is a different text node", TextType.BOLD)
        )
        self.assertNotEqual(
            node,
            TextNode("This is a text node", TextType.BOLD, "https://www.example.com"),
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode(
            "This is a text node", TextType.IMAGE, "https://www.example.com/image.jpg"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.example.com/image.jpg", "alt": "This is a text node"},
        )

    def test_split_nodes_delimiter(self):
        node = TextNode("This is a text node with a `code block` inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is a text node with a ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " inside")
        node = TextNode(
            "This is a text node with a **bold** text inside", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is a text node with a ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text inside")
        node = TextNode(
            "This is a text node with a _italic_ text inside", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is a text node with a ")
        self.assertEqual(new_nodes[2].text, " text inside")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        node = TextNode("`code` is cool", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " is cool")
        node = TextNode("I am **almighty**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "I am ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        node = TextNode("I am **almighty** and _awesome_ sauce!", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "**", TextType.BOLD)
        second_pass = split_nodes_delimiter(first_pass, "_", TextType.ITALIC)
        self.assertEqual(len(second_pass), 5)
        self.assertEqual(second_pass[0].text, "I am ")
        self.assertEqual(second_pass[1].text_type, TextType.BOLD)
        self.assertEqual(second_pass[2].text, " and ")
        self.assertEqual(second_pass[3].text_type, TextType.ITALIC)
        self.assertEqual(second_pass[4].text, " sauce!")
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        node = TextNode("[This is a link](https://www.example.com)", TextType.LINK)
        new_nodes = split_nodes_delimiter([node], "[", TextType.LINK)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "[This is a link](https://www.example.com)")
        self.assertEqual(new_nodes[0].text_type, TextType.LINK)
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://www.example.com/image.jpg) and ![another](https://www.example.com/another.jpg)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            images,
            [
                ("image", "https://www.example.com/image.jpg"),
                ("another", "https://www.example.com/another.jpg"),
            ],
        )
        text = "This is a text with nothing"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [])
        text = "This is an empty alt text ![](https://www.example.com/image.jpg)"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [("", "https://www.example.com/image.jpg")])
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [])
        text = "This is text with a [link](https://www.example.com) and an image ![image](https://www.example.com/image.jpg)"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [("image", "https://www.example.com/image.jpg")])
        text = "This is text with four images ![image1](https://www.example.com/image1.jpg), the second ![image2](https://www.example.com/image2.jpg), the third ![image3](https://www.example.com/image3.jpg), and the fourth ![image4](https://www.example.com/image4.jpg)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            images,
            [
                ("image1", "https://www.example.com/image1.jpg"),
                ("image2", "https://www.example.com/image2.jpg"),
                ("image3", "https://www.example.com/image3.jpg"),
                ("image4", "https://www.example.com/image4.jpg"),
            ],
        )
        images = extract_markdown_images("")
        self.assertListEqual(images, [])
        text = "This is text with a missing closing parenthesis ![image](https://www.example.com/image.jpg"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [])
        text = "This is text with a missing closing bracket ![image(https://www.example.com/image.jpg"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            links,
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )
        text = "This is text with nothing"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [])
        text = "This is text with an empty anchor text [](https://www.example.com)"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [("", "https://www.example.com")])
        text = "This is text with an image ![image](https://www.example.com/image.jpg)"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [])
        text = "This is text with a [link](https://www.example.com) and an image ![image](https://www.example.com/image.jpg)"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [("link", "https://www.example.com")])
        text = "This is text with four links [link1](https://www.example.com/link1), the second [link2](https://www.example.com/link2), the third [link3](https://www.example.com/link3), and the fourth [link4](https://www.example.com/link4)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            links,
            [
                ("link1", "https://www.example.com/link1"),
                ("link2", "https://www.example.com/link2"),
                ("link3", "https://www.example.com/link3"),
                ("link4", "https://www.example.com/link4"),
            ],
        )
        links = extract_markdown_links("")
        self.assertListEqual(links, [])
        text = "This is text with a missing closing parenthesis [link](https://www.example.com/image.jpg"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [])
        text = "This is text with a missing closing bracket [link(https://www.example.com/image.jpg"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [])

    def test_extract_markdown_images_nested_link(self):
        # Known limitation: nested image-in-link is partially matched
        # only the malformed alt text is returned
        text = "[![image](https://www.example.com/image.jpg)](https://www.example.com)"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [("![image", "https://www.example.com/image.jpg")])


if __name__ == "__main__":
    unittest.main()
