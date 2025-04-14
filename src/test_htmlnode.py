import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    """
    Test suite for the `HTMLNode` class. 
    
    Verifies HTML generation functionality for various HTML attribute scenarios.
    """
    def test_props_to_html_with_href(self):
        """
        Test that `props_to_html` correctly formats a single href attribute.
        Verify the formatted string has a leading space and proper quotes.
        """
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    
    def test_props_to_html_with_multiple_props(self):
        """
        Test that `props_to_html` correctly formats multiple attributes.
        Since dictionary order isn't guaranteed, check against both possible outputs.
        """
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        possible_expected_results = [
            ' href="https://www.google.com" target="_blank"',
            ' target="_blank" href="https://www.google.com"'
        ]
        self.assertIn(result, possible_expected_results)
    
    def test_props_to_html_with_no_props(self):
        """
        Test that `props_to_html` returns an empty string when props is None.
        Verify an empty string is returned when no props are provided.
        """
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_to_html(self):
        """
        Test that `to_html` raises a `NotImplementedError` as required.
        """
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        """
        Test that the string representation of an `HTMLNode` is formatted correctly.
        """
        node = HTMLNode(tag="p", value="This is a paragraph")
        expected = "HTMLNode(tag: p, value: This is a paragraph, children: None, props: None)"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
