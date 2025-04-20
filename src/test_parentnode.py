import unittest
from html_parent_leaf_node import ParentNode
from html_parent_leaf_node import LeafNode

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

if __name__ == "__main__":
    unittest.main()
