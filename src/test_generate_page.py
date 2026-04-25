import unittest

from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello, World!"
        title = extract_title(markdown)
        self.assertEqual(title, "Hello, World!")

    def test_extract_title_no_hash(self):
        markdown = "Hello, World!"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_leading_and_trailing_whitespace(self):
        markdown = "#     Hello, World!  "
        title = extract_title(markdown)
        self.assertEqual(title, "Hello, World!")

    def test_extract_title_leading_whitespace(self):
        markdown = "  # Hello, World!"
        title = extract_title(markdown)
        self.assertEqual(title, "Hello, World!")

    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_empty_with_hash(self):
        markdown = "# "
        title = extract_title(markdown)
        self.assertEqual(title, "")


if __name__ == "__main__":
    unittest.main()
