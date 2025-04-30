import unittest
from block_markdown_to_html import (
    markdown_to_html_node, 
    markdown_to_blocks, 
    block_to_block_type, 
    BlockType
)


class TestMarkdownToHTMLNode(unittest.TestCase):
    """
    Test suite for the `markdown_to_html_node` function.

    These tests verify the function converts Markdown text into 
    structured HTML wrapped in an `HTMLNode`. They test each 
    body type element that is supported.
    """
    def test_paragraphs(self):
        """
        Test paragraph conversion to `<p>` tags, including inline Markdown such as bold,
        italic, and code elements.
        """
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(html, expected)

    def test_codeblock(self):
        """
        Test conversion of code blocks into `<pre>` and `<code>` tags, ensuring that
        inline Markdown inside code blocks is not parsed.
        """
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(html, expected)

    def test_lists(self):
        """
        Test unordered and ordered list conversion. Ensure that `<ul>`, `<ol>`, and `<li>`
        tags are created correctly and inline Markdown within list items is parsed.
        """
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>"
        self.assertEqual(html, expected)

    def test_headings(self):
        """
        Test heading conversion to `<h1>` and `<h2>` tags, ensuring that
        heading levels correspond to the number of '#' characters in Markdown.
        """
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>"
        self.assertEqual(html, expected)

    def test_blockquote(self):
        """
        Test blockquote conversion to `<blockquote>` tags, ensuring lines
        prefixed with '>' are wrapped properly, and inline Markdown is parsed.
        """
        markdown = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        expected = "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>"
        self.assertEqual(html, expected)


class TestMarkdownToBlocks(unittest.TestCase):
    """
    Test suite for the `markdown_to_blocks` function.

    Each test case examines a specific aspect of block splitting logic:
    - Regular Markdown with headings, paragraphs, and lists.
    - Handling of empty input or excessive whitespace.
    - Preservation of block structures while removing unnecessary whitespace.
    """

    def test_markdown_text(self):
        """
        Test markdown input with headings, paragraphs, and lists.

        Ensures:
        - Blocks are correctly split by double newlines.
        - List structures retain their inline newlines.
        """
        markdown = """
# This is a heading



This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a second item
- This is a third item
"""
        expected = [
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.", 
            "- This is the first list item in a list block\n- This is a second item\n- This is a third item"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_markdown_text(self):
        """
        Test input with only blank lines.

        Ensures:
        - The function returns an empty list when no meaningful content exists.
        """
        markdown = """

     


"""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_whitespace_markdown_text(self):
        """
        Test input with blocks that have leading, trailing, or excessive internal whitespace.

        Ensures:
        - Whitespace is stripped correctly from each block.
        - Blocks with only meaningful content are retained.
        """
        markdown = """
This text has whitespace in front.

   This text has whitespace on both sides.     

This text has whitespace behind.      
"""
        expected = [
            "This text has whitespace in front.", 
            "This text has whitespace on both sides.", 
            "This text has whitespace behind."
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)        


class TestBlockToBlockType(unittest.TestCase):
    """
    Test suite for the block_to_block_type function.

    Each test verifies that the function correctly identifies the type of a given 
    Markdown block. The tests cover various valid and invalid inputs, ensuring 
    robust classification of Markdown blocks according to the requirements.
    """

    # Heading Tests
    def test_header_1(self):
        """
        Test that a level 1 heading ('#') is identified correctly.
        """
        markdown_block = "# Heading 1"
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_header_6(self):
        """
        Test that a level 6 heading ('######') is identified correctly.
        """
        markdown_block = "###### Heading 6"
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type(markdown_block), expected)
    
    def test_header_7(self):
        """
        Test that a malformed level 7 heading is treated as a paragraph.
        """
        markdown_block = "####### Heading 7"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_whitespace_header(self):
        """
        Test that a heading with leading spaces is treated as a paragraph.
        """
        markdown_block = "    ### Heading 3"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(markdown_block), expected)


    # Code Block Tests
    def test_code(self):
        """
        Test that a valid code block surrounded by triple backticks is identified.
        """
        markdown_block = "```print('Hello, world!')```"
        expected = BlockType.CODE
        self.assertEqual(block_to_block_type(markdown_block), expected)
    
    def test_missing_end_code(self):
        """
        Test that an incomplete code block (missing closing backticks) is treated as a paragraph.
        """
        markdown_block = "```print('Incomplete code block')`"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(markdown_block), expected)


    # Quote Block Tests
    def test_quote(self):
        """
        Test that a valid multi-line quote block, marked with '>', is identified.
        """
        markdown_block = "> This is a quote.\n> This is a second quote.\n> This is a third quote."
        expected = BlockType.QUOTE
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_missing_symbol_quote(self):
        """
        Test that a block with non-quote lines mixed in is treated as a paragraph.
        """
        markdown_block = "> This is a quote.\nThis is an invalid quote."
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_whitespace_quote(self):
        """
        Test that a block with improper whitespace in a quote is treated as a paragraph.
        """
        markdown_block = "> This is a quote.\n     >This is an invalid quote."
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(markdown_block), expected)


    # Unordered List Tests
    def test_unordered_list(self):
        """
        Test that a valid unordered list (lines starting with '- ') is identified.
        """
        markdown_block = "- item 1\n- item 2\n- item 3"
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_whitespace_unordered_list(self):
        """
        Test that an unordered list with improper indentation is treated as a paragraph.
        """
        markdown_block = "    - item 1\n- item 2\n- item 3"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(markdown_block), expected)


    # Ordered List Tests
    def test_ordered_list(self):
        """
        Test that a valid ordered list (sequential numbers like '1., 2., 3.') is identified.
        """
        markdown_block = "1. Step 1\n2. Step 2\n3. Step 3"
        expected = BlockType.ORDERED_LIST
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_wrong_number_ordered_list(self):
        """
        Test that an ordered list with incorrect numbering is treated as a paragraph.
        """
        markdown_block = "1. Step 1\n3. Step 2\n4. Step 3"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_missing_number_ordered_list(self):
        """
        Test that an ordered list missing numbers in some lines is treated as a paragraph.
        """
        markdown_block = "1. Step 1\nStep 2\n3. Step 3"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(markdown_block), expected)


if __name__ == "__main__":
    unittest.main()
