class HTMLNode:
    """
    Represents an HTML element in a document tree structure.
    Can represent block-level or inline elements with optional attributes.
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Initialize an HTML node with optional parameters.
        
        Args:
            `tag` (str, optional): String representing the HTML `tag` name.
                                   (e.g., "p", "a", "h1")
            `value` (str, optional): String content inside the HTML element.
            `children` (list, optional): List of child `HTMLNode` objects that 
                                         are nested within this element.
            `props` (dict, optional): Dictionary of HTML attributes as key-value pairs.
                                      (e.g., {"href": "`https://example.com`"})
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Converts the node to HTML string representation.
        This is a placeholder that child classes will override.
        
        Raises:
            NotImplementedError: This base method must be implemented by subclasses.
        """
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        """
        Converts the node's properties (HTML attributes) to a string.
        
        Returns:
            String with HTML attributes formatted as 'key="value"' with leading spaces.
            Empty string if no properties exist.
        """
        if self.props is None:
            return ""

        # Generate props HTML string for HTMLNode.
        props_html = ""
        for prop_key in self.props:
            props_html += f' {prop_key}="{self.props[prop_key]}"'
        return props_html

    def __repr__(self):
        """
        Prints a string representation of the `HTMLNode`'s properties 
        in a readable format for debugging and logging.
        """
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
