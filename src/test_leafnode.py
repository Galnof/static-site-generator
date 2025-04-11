import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    """
    Test suite for the LeafNode class, verifying HTML generation 
    functionality for various HTML elements.
    """
    def test_leaf_to_html_p(self):
        """Test rendering of paragraph tags."""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        """Test rendering of bold tags."""
        node = LeafNode("b", "THIS IS BOLD")
        self.assertEqual(node.to_html(), "<b>THIS IS BOLD</b>")

    def test_leaf_to_html_i(self):
        """Test rendering of italic tags."""
        node = LeafNode("i", "this is italic")
        self.assertEqual(node.to_html(), "<i>this is italic</i>")

    def test_leaf_to_html_a(self):
        """Test rendering of anchor tags with href attribute."""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        """Test rendering when no tag is provided (raw text output)."""
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        """Test that ValueError is raised when attempting to render a node with no value."""
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
