import unittest
from textnode import TextNode, TextType
from inline_markdown_to_html import (
    text_to_textnodes, 
    split_nodes_delimiter, 
    split_nodes_image, 
    split_nodes_link, 
    extract_markdown_images, 
    extract_markdown_links
)

class TestTextToTextNode(unittest.TestCase):
    """
    Test suite for the `text_to_textnodes` function.

    These tests verify that the function correctly parses markdown-flavored strings
    into a list of `TextNode` objects for various cases, including:
    - Simple markdown syntax (e.g., bold, italic, code).
    - Complex markdown syntax with links and images.
    - Handling invalid cases, such as unbalanced `delimiter`s.
    """
    def test_single_line_with_simple_markdown_test(self):
        """
        Test a single line of `text` with simple markdown (code and italic).
        """
        text = "This is `code` with an _italic_ word."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_single_line_with_complex_markdown_text(self):
        """
        Test a single line of `text` with complex markdown (bold, italic, code, image, link).
        """
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(text_to_textnodes(text), expected)
    
    def test_unbalanced_delimiter(self):
        """
        Test for unbalanced `delimiter`s (invalid Markdown syntax).

        Verifies that the function raises a `ValueError` when given markdown
        `text` with unbalanced `delimiter`s, such as unclosed code blocks.
        """
        text = "This **bold** and _italic_ is correct but there is unbalanced `code here."
        with self.assertRaises(ValueError):
            text_to_textnodes(text)


class TestSplitNodesDelimiter(unittest.TestCase):
    """
    Test suite for the `split_nodes_delimiter` function.

    These tests verify the function handles splitting a node correctly 
    at the `delimiter` for various markdown element scenarios.
    """
    def test_no_delimiter(self):
        """
        Test for when no `delimiter`s are present in the input.
        """
        node = [TextNode("This is plain text", TextType.TEXT)]
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node, "**", TextType.BOLD), expected)

    def test_balanced_delimiter(self):
        """
        Test for balanced `delimiter`s (start and end present).
        """
        node = [TextNode("Some **bold** words", TextType.TEXT)]
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(node, "**", TextType.BOLD), expected)

    def test_empty_fragments_around_delimiter(self):
        """
        Test for an edge case where `delimiter`s surround the entire text.
        """
        node = [TextNode("**bold**", TextType.TEXT)]
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(node, "**", TextType.BOLD), expected)

    def test_unbalanced_delimiter(self):
        """
        Test for unbalanced `delimiter`s (invalid Markdown syntax).
        """
        node = [TextNode("Unbalanced **bold here", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(node, "**", TextType.BOLD)


class TestSplitNodesImageAndLink(unittest.TestCase):
    """
    Test suite for the `split_nodes_image` and `split_nodes_link` functions.
    
    These tests verify that markdown images and links are correctly extracted from 
    `TextNode`s and converted into separate nodes with the appropriate `TextType`.
    """
    def test_split_multiple_images(self):
        """
        Test splitting a `TextNode` that contains multiple image markdown elements.
        """
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertEqual(split_nodes_image([node]), expected)
    
    def test_no_image(self):
        """
        Test that a `TextNode` without image markdown remains unchanged.
        """
        node = TextNode("This is a text with no image.", TextType.TEXT)
        expected = [TextNode("This is a text with no image.", TextType.TEXT)]
        self.assertEqual(split_nodes_image([node]), expected)
    
    def test_empty_text_with_image(self):
        """
        Test handling a `TextNode` that contains only an image markdown with no surrounding text.
        """
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        expected = [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(split_nodes_image([node]), expected)
    
    def test_bold_node_no_image(self):
        """
        Test that non-`TEXT` nodes are not processed even if they contain image markdown.
        """
        node = TextNode("Bold text", TextType.BOLD)
        expected = [TextNode("Bold text", TextType.BOLD)]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_multiple_links(self):
        """
        Test splitting a `TextNode` that contains multiple link markdown elements.
        """
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", 
            TextType.TEXT
        )
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(split_nodes_link([node]), expected)
    
    def test_no_link(self):
        """
        Test that a `TextNode` without link markdown remains unchanged.
        """
        node = TextNode("This is a text with no link.", TextType.TEXT)
        expected = [TextNode("This is a text with no link.", TextType.TEXT)]
        self.assertEqual(split_nodes_link([node]), expected)
    
    def test_empty_text_with_link(self):
        """
        Test that a `TextNode` without link markdown remains unchanged.
        """
        node = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        expected = [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
        self.assertEqual(split_nodes_link([node]), expected)
    
    def test_bold_node_no_link(self):
        """
        Test that non-`TEXT` nodes are not processed even if they contain link markdown.
        """
        node = TextNode("Bold text", TextType.BOLD)
        expected = [TextNode("Bold text", TextType.BOLD)]
        self.assertEqual(split_nodes_link([node]), expected)


class TestExtractMarkdown(unittest.TestCase):
    """
    Test suite for the `extract_markdown_links` and `extract_markdown_images` functions.

    These tests verify that markdown images (`![alt text](url)`) 
    and links (`[anchor text](url)`) are correctly extracted from `text`.
    """
    def test_extract_markdown_single_image(self):
        """
        Test extraction of a single markdown image from text.
        """
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_multiple_images(self):
        """
        Test extraction of multiple markdown images from text.
        """
        matches = extract_markdown_images(
            "This is text with two images ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_check_image(self):
        """
        Test extraction of images only (not links) when both are present.
        """
        matches = extract_markdown_images(
            "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_single_link(self):
        """
        Test extraction of a single markdown link from text.
        """
        matches = extract_markdown_links(
            "This is text with an [link](https://www.boot.dev)"
        )
        expected = [("link", "https://www.boot.dev")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_multiple_links(self):
        """
        Test extraction of multiple markdown links from text.
        """
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_check_link(self):
        """
        Test extraction of links only (not images) when both are present.
        """
        matches = extract_markdown_links(
            "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)"
        )
        expected = [("link", "https://www.boot.dev")]
        self.assertEqual(matches, expected)


if __name__ == "__main__":
    unittest.main()
