from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    """
    A specialized `HTMLNode` that has `children` and cannot contain text content (`value`).
    
    `ParentNodes` have a `tag` and `children`, but no text `value`.
    They render as HTML elements with opening and closing `tag`s
    containing their `children`'s HTML.
    """
    def __init__(self, tag, children, props=None):
        """
        Initialize a new `ParentNode` instance.
        
        Args:
            `tag` (str): The HTML tag name. (e.g., "p", "a", "div")
                         Must not be `None` when rendering.
            `children` (list): List of child HTMLNode objects.
                               Must not be `None` when rendering.
            `props` (dict, optional): HTML attributes as key-value pairs.
                                      For example: {"class": "header", "id": "main"}
                                      Defaults to `None`.
        """
        super().__init__(tag, None, children, props)

    def to_html(self):
        """
        Convert the `ParentNode` and all its `children` to an HTML string.
        
        Raises:
            `ValueError`: If tag is `None` or `children` is `None`.
            
        Returns:
            str: HTML representation of this node and its `children`.
        """
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        
        # Create opening tag with properties.
        parent_html = f"<{self.tag}{self.props_to_html()}>"

        # Add HTML from all children.
        for child in self.children:
            parent_html += child.to_html()
        
        # Add closing tag.
        parent_html += f"</{self.tag}>"
        return parent_html
    
    def __repr__(self):
        """
        Prints a string representation of the `ParentNode`'s properties 
        in a readable format for debugging and logging.
        """
        return f"ParentNode(tag: {self.tag}, children: {self.children}, props: {self.props})"
