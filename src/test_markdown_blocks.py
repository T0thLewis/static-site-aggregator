import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_line(self):
        markdown = "This is a single line"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is a single line"])

    def test_markdown_to_blocks_adjacent_newlines(self):
        markdown = """
This is **bolded** paragraph



This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line



- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_with_spaces(self):
        markdown = "first block\n\n    \n\nsecond block"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["first block", "second block"])

    def test_markdown_to_blocks_with_tabs(self):
        markdown = "first block\n\n\t\n\nsecond block"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["first block", "second block"])

    def test_markdown_to_blocks_with_explicit_spaces(self):
        spaces = "    "
        markdown = f"first block\n\n{spaces}\n\nsecond block"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["first block", "second block"])

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```This is code```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_quote_without_space(self):
        block = ">This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a list item\n- This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a list item\n2. This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_format(self):
        block = "This should be a code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_empty(self):
        block = ""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
