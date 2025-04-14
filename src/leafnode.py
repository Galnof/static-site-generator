from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    """
    A specialized `HTMLNode` that can only contain 
    text content (`value`) and cannot have child elements.
    
    `LeafNode` represents HTML elements that are "leaves" in the DOM tree, 
    meaning they don't contain other HTML elements, only text content.
    
    Examples include text in paragraphs, anchors, and formatted text. (e.g., bold, italic)
    """
    def __init__(self, tag, value, props=None):
        """
        Initialize a `LeafNode` object which represents an HTML element without `children`.
    
        Args:
            `tag` (str): The HTML tag name. (e.g., "p", "a", "div")
                         If `None`, the node will render as raw text.
            `value` (str): The text content of this node.
                           Must not be `None` when rendering.
            `props` (dict, optional): HTML attributes as key-value pairs.
                                      For example: {"class": "header", "id": "main"}
                                      Defaults to `None`.
        """
        super().__init__(tag, value, None, props)

    def to_html(self):
        """
        Converts the `LeafNode` to an HTML string representation of this node.
        
        Returns:
            str: HTML representation of this node
            
        Raises:
            `ValueError`: If the node has no `value`
        """
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        
        if self.tag is None:
            return self.value
        
        # Generate HTML string for LeafNode.
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        """
        Prints a string representation of the `LeafNode`'s properties 
        in a readable format for debugging and logging.
        """
        return f"LeafNode(tag: {self.tag}, value: {self.value}, props: {self.props})"
