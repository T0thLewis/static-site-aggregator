import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_node(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode("a", "Click me", props={"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me</a>'
        )
        node = LeafNode("div", "Content", props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container">Content</div>')
        node = LeafNode("span", "Inline", props={"style": "color: red;"})
        self.assertEqual(node.to_html(), '<span style="color: red;">Inline</span>')

    def test_to_html_with_children(self):
        child_node = LeafNode("p", "Child content")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><p>Child content</p></div>")
        self.assertEqual(child_node.to_html(), "<p>Child content</p>")
        child_node_2 = LeafNode("p", "Another child")
        parent_node_2 = ParentNode("div", [child_node_2])
        self.assertEqual(parent_node_2.to_html(), "<div><p>Another child</p></div>")
        self.assertEqual(child_node_2.to_html(), "<p>Another child</p>")
        parent_node_3 = ParentNode("div", [parent_node, parent_node_2])
        self.assertEqual(
            parent_node_3.to_html(),
            "<div><div><p>Child content</p></div><div><p>Another child</p></div></div>",
        )
        self.assertEqual(parent_node.to_html(), "<div><p>Child content</p></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("span", "Inline", props={"style": "color: red;"})
        child_node = ParentNode("p", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><p><span style="color: red;">Inline</span></p></div>',
        )
        self.assertEqual(
            child_node.to_html(), '<p><span style="color: red;">Inline</span></p>'
        )
        self.assertEqual(
            grandchild_node.to_html(), '<span style="color: red;">Inline</span>'
        )


if __name__ == "__main__":
    unittest.main()
