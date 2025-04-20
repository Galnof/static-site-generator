import unittest
from html_parent_leaf_node import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType

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
        possible_expected_results = [
            ' href="https://www.google.com" target="_blank"',
            ' target="_blank" href="https://www.google.com"'
        ]
        self.assertIn(node.props_to_html(), possible_expected_results)
    
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

class TestParentNode(unittest.TestCase):
    """
    Test suite for the `ParentNode` class.

    Verifies HTML generation functionality for various 
    parent/child node scenarios and HTML elements.
    """
    def test_to_html_with_children(self):
        """
        Test that a `ParentNode` with a single child renders correctly.
        """
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span>child</span></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_grandchildren(self):
        """
        Test nested `ParentNode`s render correctly (two levels of nesting).
        """
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_multiple_children(self):
        """
        Test a `ParentNode` with multiple `children` renders correctly.
        
        Tests a paragraph with mixed content including plain text,
        **bold** text, and _italic_ text.
        """
        child_node1 = LeafNode(None, "This paragraph has ")
        child_node2 = LeafNode("b", "BOLD TEXT")
        child_node3 = LeafNode(None, " mixed with ")
        child_node4 = LeafNode("i", "italic text")
        child_node5 = LeafNode(None, ".")
        parent_node = ParentNode("p", [
            child_node1, 
            child_node2, 
            child_node3, 
            child_node4, 
            child_node5
        ])
        expected = "<p>This paragraph has <b>BOLD TEXT</b> mixed with <i>italic text</i>.</p>"
        self.assertEqual(parent_node.to_html(), expected)
        
    def test_to_html_complex_children_tree(self):
        """
        Test complex nested structure resembling a full HTML document.
        
        Creates a structure with multiple levels of nesting, including:
        - html
          - head
            - title
          - body
            - h1
            - p (with mixed text and formatting)
        """
        grandchild_node1 = LeafNode("title", "THIS IS A TITLE")
        child_node1 = ParentNode("head", [grandchild_node1])

        grandchild_node2 = LeafNode("h1", "This is a heading")

        # Create a paragraph with mixed formatting.
        great_grandchild_node1 = LeafNode(None, "This paragraph has ")
        great_grandchild_node2 = LeafNode("b", "BOLD TEXT")
        great_grandchild_node3 = LeafNode(None, " mixed with ")
        great_grandchild_node4 = LeafNode("i", "italic text")
        great_grandchild_node5 = LeafNode(None, ".")
        grandchild_node3 = ParentNode("p", [
            great_grandchild_node1, 
            great_grandchild_node2, 
            great_grandchild_node3, 
            great_grandchild_node4, 
            great_grandchild_node5
        ])

        child_node2 = ParentNode("body", [grandchild_node2, grandchild_node3])
        parent_node = ParentNode("html", [child_node1, child_node2])

        expected = "<html><head><title>THIS IS A TITLE</title></head><body><h1>This is a heading</h1><p>This paragraph has <b>BOLD TEXT</b> mixed with <i>italic text</i>.</p></body></html>"
        self.assertEqual(parent_node.to_html(), expected)
    
    def test_to_html_no_tag(self):
        """
        Test that a `ValueError` is raised when a `ParentNode` has no `tag`.
        """
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_no_children(self):
        """
        Test that a `ValueError` is raised when a `ParentNode` has no `children`.
        """
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

class TestLeafNode(unittest.TestCase):
    """
    Test suite for the `LeafNode` class.

    Verifies HTML generation functionality for various HTML elements.
    """
    def test_leaf_to_html_p(self):
        """
        Test rendering of paragraph `tag`s.
        """
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        """
        Test rendering of bold `tag`s.
        """
        node = LeafNode("b", "THIS IS BOLD")
        self.assertEqual(node.to_html(), "<b>THIS IS BOLD</b>")

    def test_leaf_to_html_i(self):
        """
        Test rendering of italic `tag`s.
        """
        node = LeafNode("i", "this is italic")
        self.assertEqual(node.to_html(), "<i>this is italic</i>")

    def test_leaf_to_html_a(self):
        """
        Test rendering of anchor tags with href attribute.
        """
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        """
        Test rendering when no `tag` is provided (raw text output).
        """
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        """
        Test that `ValueError` is raised when attempting to render a node with no `value`.
        """
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

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
