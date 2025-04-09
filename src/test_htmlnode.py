import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    # Test that props_to_html correctly formats a single href attribute.
    # Verify the formatted string has a leading space and proper quotes.
    def test_props_to_html_with_href(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    
    # Test that props_to_html correctly formats multiple attributes.
    # Since dictionary order isn't guaranteed, check against both possible outputs.
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        possible_expected_results = [
            ' href="https://www.google.com" target="_blank"',
            ' target="_blank" href="https://www.google.com"'
        ]
        self.assertIn(result, possible_expected_results)
    
    # Test that props_to_html returns an empty string when props is None.
    # Verify an empty string is returned when no props are provided.
    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    # Test that to_html raises a NotImplementedError as required.
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # Test that the string representation of a HTMLNode is formatted correctly.
    def test_repr(self):
        node = HTMLNode(tag="p", value="This is a paragraph")
        expected = "HTMLNode(tag: p, value: This is a paragraph, children: None, props: None)"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
