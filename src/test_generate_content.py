import unittest
from generate_content import extract_title

class TestExtractTitle(unittest.TestCase):
    """
    Test suite for the `extract_title` function.

    These tests verify the function returns the h1 header from 
    markdown and handles a missing h1 header correctly.
    """
    def test_extract_title(self):
        """
        Test that the function correctly extracts an h1 header from markdown.
        """
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""
        expected = "this is an h1"
        self.assertEqual(extract_title(md), expected)

    def test_extract_title_error(self):
        """
        Test that the function raises ValueError when no h1 header is present.
        """
        md = """
this is an error

this is paragraph text

## this is an h2
"""
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
