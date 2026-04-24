import unittest
from textwrap import dedent

from markdown_to_html import header_to_html_node, markdown_to_html_node


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraph(self):
        md = dedent("""
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = dedent("""
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_header(self):
        md = dedent("""
            # This is a header
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a header</h1></div>",
        )

    def test_nested_header(self):
        md = dedent("""
            # This is a header

            ## This is a nested header
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a header</h1><h2>This is a nested header</h2></div>",
        )

    def test_all_headers(self):
        md = dedent("""
            # This is a header

            ## This is a nested header

            ### This is a nested header

            #### This is a nested header

            ##### This is a nested header

            ###### This is a nested header
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a header</h1><h2>This is a nested header</h2><h3>This is a nested header</h3><h4>This is a nested header</h4><h5>This is a nested header</h5><h6>This is a nested header</h6></div>",
        )

    def test_invalid_header_direct(self):
        with self.assertRaises(ValueError):
            header_to_html_node("####### This is an invalid header")

    def test_quote_block(self):
        md = dedent("""
            > This is a quote
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote></div>",
        )

    def test_multiline_quote_block(self):
        md = dedent("""
            > This is a quote
            > that spans multiple lines
            > in the same block
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote that spans multiple lines in the same block</blockquote></div>",
        )

    def test_multiple_separate_quote_blocks(self):
        md = dedent("""
            > This is the first quote

            > This is the second quote
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is the first quote</blockquote><blockquote>This is the second quote</blockquote></div>",
        )

    def test_unordered_list(self):
        md = dedent("""
            - Item 1
            - Item 2
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>",
        )

    def test_multiple_separate_unordered_lists(self):
        md = dedent("""
            - Item 1
            - Item 2

            - Item 3
            - Item 4
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li></ul><ul><li>Item 3</li><li>Item 4</li></ul></div>",
        )

    def test_ordered_list(self):
        md = dedent("""
            1. Item 1
            2. Item 2
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li></ol></div>",
        )

    def test_multiple_separate_ordered_lists(self):
        md = dedent("""
            1. Item 1
            2. Item 2

            1. Item 3
            2. Item 4
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li></ol><ol><li>Item 3</li><li>Item 4</li></ol></div>",
        )

    def test_large_ordered_list(self):
        md = dedent("""
            1. Item 1
            2. Item 2
            3. Item 3
            4. Item 4
            5. Item 5
            6. Item 6
            7. Item 7
            8. Item 8
            9. Item 9
            10. Item 10
            11. Item 11
            100. Item 100
            2000. Item 2000
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li><li>Item 5</li><li>Item 6</li><li>Item 7</li><li>Item 8</li><li>Item 9</li><li>Item 10</li><li>Item 11</li><li>Item 100</li><li>Item 2000</li></ol></div>",
        )

        def test_ordered_list_bad_numbering_becomes_paragraph(self):
            md = "3. Item 3\n4. Item 4"
            node = markdown_to_html_node(md)
            html = node.to_html()
            # Expect a <p> tag, not <ol>
            self.assertIn("<p>", html)

        def test_mixed_everything(self):
            md = dedent("""
                # Main Heading

                This is an introductory paragraph with **bold** text,
                _italic_ words, and some `inline code` mixed in.

                ## A Subheading

                Here is another paragraph that spans
                multiple lines but should become one
                flowing sentence in the output.

                ### Code Example

                ```
                def hello():
                    print("world")
                ```

                > This is a quote with **bold**
                > across multiple lines

                #### Unordered Stuff

                - First bullet with _italic_
                - Second bullet with `code`
                - Third bullet plain

                ##### Ordered Stuff

                1. First numbered item
                2. Second with **bold**
                3. Third item

                ###### Final Heading

                A closing paragraph.
                """)

            node = markdown_to_html_node(md)
            html = node.to_html()
            expected = (
                "<div>"
                "<h1>Main Heading</h1>"
                "<p>This is an introductory paragraph with <b>bold</b> text, <i>italic</i> words, and some <code>inline code</code> mixed in.</p>"
                "<h2>A Subheading</h2>"
                "<p>Here is another paragraph that spans multiple lines but should become one flowing sentence in the output.</p>"
                "<h3>Code Example</h3>"
                '<pre><code>def hello():\n    print("world")\n</code></pre>'
                "<blockquote>This is a quote with <b>bold</b> across multiple lines</blockquote>"
                "<h4>Unordered Stuff</h4>"
                "<ul>"
                "<li>First bullet with <i>italic</i></li>"
                "<li>Second bullet with <code>code</code></li>"
                "<li>Third bullet plain</li>"
                "</ul>"
                "<h5>Ordered Stuff</h5>"
                "<ol>"
                "<li>First numbered item</li>"
                "<li>Second with <b>bold</b></li>"
                "<li>Third item</li>"
                "</ol>"
                "<h6>Final Heading</h6>"
                "<p>A closing paragraph.</p>"
                "</div>"
            )
            self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
