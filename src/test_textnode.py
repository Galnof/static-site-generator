import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    """
    Test suite for the `TextNode` class.
    
    These tests verify that two nodes with identical properties 
    are considered equal by the `__eq__` method.
    """
    def test_eq_true(self):
        """
        Test that two `TextNode`s with the same `text` and `text_type` are equal.
        """
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_false_texttype(self):
        """
        Test that two `TextNode`s with the same `text` but different `text_type`s are not equal.
        """
        node1 = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_eq_false_text(self):
        """
        Test that two `TextNode`s with different `text` but the same `text_type` are not equal.
        """
        node1 = TextNode("This text node doesn't match", TextType.TEXT)
        node2 = TextNode("This is a text node that doesn't match", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        """
        Test that two `TextNode`s with the same `text`, `text_type`, and `url` are equal.
        """
        node1 = TextNode("This is a link text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node1, node2)

    def test_repr(self):
        """
        Test that the string representation of a `TextNode` is formatted correctly.
        """
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        expected = "TextNode(text: This is a text node, text_type: text, url: https://www.boot.dev)"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
