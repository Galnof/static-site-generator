import unittest
from node_conversions import text_node_to_html_node
from textnode import TextNode, TextType

class TestTextNodeToHTMLNode(unittest.TestCase):
    """
    Test suite for the `text_node_to_html_node` function.

    These tests verify that the function correctly converts `TextNode` objects to 
    `LeafNode` objects with a proper `tag`, `value`, and if provided `prop`.
    """
    def test_text(self):
        """
        Test conversion of a plain text node (`TextType.TEXT`) to a `LeafNode` with no `tag`.
        """
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        """
        Test conversion of a bold text node (`TextType.BOLD`) to a `LeafNode` with `<b>` `tag`.
        """
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        """
        Test conversion of an italic text node (`TextType.ITALIC`) to a LeafNode with `<i>` `tag`.
        """
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
    
    def test_code(self):
        """
        Test conversion of a code text node (`TextType.CODE`) to a `LeafNode` with `<code>` `tag`.
        """
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        """
        Test conversion of a link text node (`TextType.LINK`) to a `LeafNode` with `<a>` `tag`
        and an href property for the `url`.
        """
        node = TextNode("Click Me!", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click Me!")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
    
    def test_image(self):
        """
        Test conversion of an image text node (`TextType.IMAGE`) to a `LeafNode` with `<img>` `tag`.
        Ensure it properly sets 'src' to the `url` and 'alt' to the descriptive `text`.
        """
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://www.google.com")
        self.assertEqual(html_node.props["alt"], "This is an image node")
    
    def test_error(self):
        """
        Test that an unsupported `TextType` raises a `ValueError`.
        """
        class TextType:
            ERROR = "error"
        node = TextNode("This is a error node", TextType.ERROR)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
