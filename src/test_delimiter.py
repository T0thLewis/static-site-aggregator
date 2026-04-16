import unittest

from typing_extensions import Text

from delimiter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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

    def test_text_to_textnodes_basic(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )
        text = "This is a basic text node"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is a basic text node", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_mixed(self):
        text = "I found _this cool link_ take a look [link](https://boot.dev), isn't it **awesome**? It does contain some **code** in `italic` though, so **you** might want to _snap_ a _picture_ of it. Here is the link for that `image` ![absolute cinema](https://i.imgur.com/absolute-cinema.jpg)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("I found ", TextType.TEXT),
                TextNode("this cool link", TextType.ITALIC),
                TextNode(" take a look ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(", isn't it ", TextType.TEXT),
                TextNode("awesome", TextType.BOLD),
                TextNode("? It does contain some ", TextType.TEXT),
                TextNode("code", TextType.BOLD),
                TextNode(" in ", TextType.TEXT),
                TextNode("italic", TextType.CODE),
                TextNode(" though, so ", TextType.TEXT),
                TextNode("you", TextType.BOLD),
                TextNode(" might want to ", TextType.TEXT),
                TextNode("snap", TextType.ITALIC),
                TextNode(" a ", TextType.TEXT),
                TextNode("picture", TextType.ITALIC),
                TextNode(" of it. Here is the link for that ", TextType.TEXT),
                TextNode("image", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode(
                    "absolute cinema",
                    TextType.IMAGE,
                    "https://i.imgur.com/absolute-cinema.jpg",
                ),
            ],
        )

    def test_text_to_textnodes_adjacent_formats(self):
        text = "**bold****bold**_italic_`code`_italic__italic_[link](https://boot.dev)![image](https://i.imgur.com/image.jpg)[another link](https://boot.dev)_italic_**bold**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
                TextNode("italic", TextType.ITALIC),
                TextNode("italic", TextType.ITALIC),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/image.jpg"),
                TextNode("another link", TextType.LINK, "https://boot.dev"),
                TextNode("italic", TextType.ITALIC),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_text_to_textnodes_invalid_markdown(self):
        text = "This text contains **invalid' _markdown_"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

        text = "This text contains **invalid** _markdown**"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

        text = "This text contains **invalid** _markdown_`code'"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_text_to_textnodes_repetition(self):
        text = "This **bold** text **contains** **only** **bold****text** and **nothing else**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text ", TextType.TEXT),
                TextNode("contains", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("only", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("text", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("nothing else", TextType.BOLD),
            ],
        )


if __name__ == "__main__":
    unittest.main()
