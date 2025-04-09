# Represents an HTML element in a document tree structure.
# Can represent block-level or inline elements with optional attributes.
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        # The HTML tag name (e.g., "p", "a", "h1").
        self.tag = tag
        # The text content of the HTML element.
        self.value = value
        # List of child HTMLNode objects.
        self.children = children
        # Dictionary of HTML attributes (e.g., {"href": "https://example.com"}).
        self.props = props
    
    # Placeholder HTML conversion method to be implemented by child classes.
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    # Converts the props dictionary to an HTML attribute 
    # string with a space before each attribute.
    def props_to_html(self):
        if self.props is None:
            return ""

        props_html = ""
        for prop_key in self.props:
            props_html = props_html + f' {prop_key}="{self.props[prop_key]}"'
        return props_html

    # Shows the HTMLNode's properties in a readable format.
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
