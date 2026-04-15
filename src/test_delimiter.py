import unittest

from delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestDelimiter(unittest.TestCase):
    def test_delimiter_code(self):
        node = TextNode("This is a text node with a `code block` inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is a text node with a ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " inside")
        node = TextNode("`code` is cool", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " is cool")
        node = TextNode("I like `coding`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "I like ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        node = TextNode("I like `writing` multiple `lines` of `code`.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "I like ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " multiple ")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " of ")
        self.assertEqual(new_nodes[5].text_type, TextType.CODE)
        self.assertEqual(new_nodes[6].text, ".")

    def test_delimiter_bold(self):
        node = TextNode(
            "This is a text node with a **bold** text inside", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is a text node with a ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text inside")
        node = TextNode("I am **almighty**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "I am ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        node = TextNode("**The Almighty** have risen", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " have risen")
        node = TextNode("This **text** has a **bold** word inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " has a ")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, " word inside")

    def test_delimiter_italic(self):
        node = TextNode(
            "This is a text node with a _italic_ text inside", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is a text node with a ")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text inside")
        node = TextNode("_italic_ is a very beautiful text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, " is a very beautiful text")
        node = TextNode("I love writing in _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "I love writing in ")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        node = TextNode(
            "I _love_ writing _many_ beautiful _italic_ words!", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "I ")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " writing ")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[4].text, " beautiful ")
        self.assertEqual(new_nodes[5].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[6].text, " words!")

    def test_delimiter_multiple(self):
        node = TextNode("I am **almighty** and _awesome_ sauce!", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "**", TextType.BOLD)
        second_pass = split_nodes_delimiter(first_pass, "_", TextType.ITALIC)
        self.assertEqual(len(second_pass), 5)
        self.assertEqual(second_pass[0].text, "I am ")
        self.assertEqual(second_pass[1].text_type, TextType.BOLD)
        self.assertEqual(second_pass[2].text, " and ")
        self.assertEqual(second_pass[3].text_type, TextType.ITALIC)
        self.assertEqual(second_pass[4].text, " sauce!")
        node = TextNode(
            "I am **almighty** and _awesome_ sauce and I love writing `code` so much",
            TextType.TEXT,
        )
        first_pass = split_nodes_delimiter([node], "**", TextType.BOLD)
        second_pass = split_nodes_delimiter(first_pass, "_", TextType.ITALIC)
        third_pass = split_nodes_delimiter(second_pass, "`", TextType.CODE)
        self.assertEqual(len(third_pass), 7)
        self.assertEqual(third_pass[0].text, "I am ")
        self.assertEqual(third_pass[1].text_type, TextType.BOLD)
        self.assertEqual(third_pass[2].text, " and ")
        self.assertEqual(third_pass[3].text_type, TextType.ITALIC)
        self.assertEqual(third_pass[4].text, " sauce and I love writing ")
        self.assertEqual(third_pass[5].text_type, TextType.CODE)
        self.assertEqual(third_pass[6].text, " so much")
        node = TextNode("**bold** _italic_ `code`", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "**", TextType.BOLD)
        second_pass = split_nodes_delimiter(first_pass, "_", TextType.ITALIC)
        third_pass = split_nodes_delimiter(second_pass, "`", TextType.CODE)
        self.assertEqual(len(third_pass), 5)
        self.assertEqual(third_pass[0].text_type, TextType.BOLD)
        self.assertEqual(third_pass[1].text, " ")
        self.assertEqual(third_pass[2].text_type, TextType.ITALIC)
        self.assertEqual(third_pass[3].text, " ")
        self.assertEqual(third_pass[4].text_type, TextType.CODE)

    def test_delimiter_non_text_node(self):
        node = TextNode("[This is a link](https://www.example.com)", TextType.LINK)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "[This is a link](https://www.example.com)")
        self.assertEqual(new_nodes[0].text_type, TextType.LINK)
        node = TextNode("![alt text](url)", TextType.IMAGE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "![alt text](url)")
        self.assertEqual(new_nodes[0].text_type, TextType.IMAGE)
        node = TextNode("This is code", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is code")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)

    def test_delimiter_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![alt text](https://www.example.com/image.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode(
                    "alt text", TextType.IMAGE, "https://www.example.com/image.jpg"
                ),
            ],
        )
        node = TextNode(
            "This is a text with 3 images ![horse](https://www.example.com/horse.jpg) then ![cat](https://www.example.com/cat.jpg) and ![dog](https://www.example.com/dog.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 6)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a text with 3 images ", TextType.TEXT),
                TextNode("horse", TextType.IMAGE, "https://www.example.com/horse.jpg"),
                TextNode(" then ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://www.example.com/cat.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "https://www.example.com/dog.jpg"),
            ],
        )
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is just plain text", TextType.TEXT),
            ],
        )
        node = TextNode("![alt text](https://www.example.com/horse.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "alt text", TextType.IMAGE, "https://www.example.com/horse.jpg"
                ),
            ],
        )
        node = TextNode(
            "![alt text](https://www.example.com/image.jpg) this is an incredible picture",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "alt text", TextType.IMAGE, "https://www.example.com/image.jpg"
                ),
                TextNode(" this is an incredible picture", TextType.TEXT),
            ],
        )
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
            ],
        )
        node = TextNode(
            "This is a malformed syntax ![alt text(https://www.example.com/image.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is a malformed syntax ![alt text(https://www.example.com/image.jpg)",
                    TextType.TEXT,
                ),
            ],
        )
        node = TextNode(
            "This is plain text but with a different text type", TextType.CODE
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is plain text but with a different text type", TextType.CODE
                ),
            ],
        )
        node = TextNode(
            "This is a link [anchor text](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is a link [anchor text](https://www.example.com)",
                    TextType.TEXT,
                ),
            ],
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is a link [anchor text](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a link ", TextType.TEXT),
                TextNode("anchor text", TextType.LINK, "https://www.example.com"),
            ],
        )
        node = TextNode(
            "This is a malformed syntax [anchor text]https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is a malformed syntax [anchor text]https://www.example.com)",
                    TextType.TEXT,
                ),
            ],
        )
        node = TextNode(
            "This is a text with multiple links [first](https://www.example1.com) then [second](https://www.example2.com) then [third](https://www.example3.com) and finally [fourth](https://www.example4.com) link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 9)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a text with multiple links ", TextType.TEXT),
                TextNode("first", TextType.LINK, "https://www.example1.com"),
                TextNode(" then ", TextType.TEXT),
                TextNode("second", TextType.LINK, "https://www.example2.com"),
                TextNode(" then ", TextType.TEXT),
                TextNode("third", TextType.LINK, "https://www.example3.com"),
                TextNode(" and finally ", TextType.TEXT),
                TextNode("fourth", TextType.LINK, "https://www.example4.com"),
                TextNode(" link", TextType.TEXT),
            ],
        )
        node = TextNode(
            "This is text with an image ![alt text](https.//www.example.com/image.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with an image ![alt text](https.//www.example.com/image.jpg)",
                    TextType.TEXT,
                ),
            ],
        )
        node = TextNode(
            "[anchor text](https://www.example.com) a nice link", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("anchor text", TextType.LINK, "https://www.example.com"),
                TextNode(" a nice link", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
