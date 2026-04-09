import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode("a", "Click me", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
        node = HTMLNode("div", "Content", props={"class": "container"})
        self.assertEqual(node.props_to_html(), ' class="container"')
        node = HTMLNode("span", "Inline", props={"style": "color: red;"})
        self.assertEqual(node.props_to_html(), ' style="color: red;"')


if __name__ == "__main__":
    unittest.main()
