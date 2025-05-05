from textnode import TextType

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
                                   (e.g., `"p"`, `"a"`, `"h1"`)
            `value` (str, optional): String content inside the HTML element.
            `children` (list, optional): List of child `HTMLNode` objects that 
                                         are nested within this element.
            `props` (dict, optional): Dictionary of HTML attributes as key-value pairs.
                                      For example: `{"href": "https://example.com"}`
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
            `NotImplementedError`: This base method must be implemented by subclasses.
        """
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        """
        Converts the node's properties (HTML attributes) to a string.
        
        Returns:
            String with HTML attributes formatted as `key="value"` with leading spaces.
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
            `tag` (str): The HTML tag name. (e.g., `"p"`, `"a"`, `"div"`)
                         Must not be `None` when rendering.
            `children` (list): List of child HTMLNode objects.
                               Must not be `None` when rendering.
            `props` (dict, optional): HTML attributes as key-value pairs.
                                      For example: `{"class": "header", "id": "main"}`
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
        # Raise error if tag is None or children is None.
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
            `tag` (str): The HTML tag name. (e.g., "b", "i", "code")
                         If `None`, the node will render as raw text.
            `value` (str): The text content of this node.
                           Must not be `None` when rendering.
            `props` (dict, optional): HTML attributes as key-value pairs.
                                      For example: `{"href": "https://example.com"}`
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

        # Raise error if the node has no value.
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

def text_node_to_html_node(text_node):
    """
    Converts a `TextNode` object into a corresponding `HTMLNode`,
    specifically to create children that are a `LeafNode`.

    Args:
        `text_node` (`TextNode`): A `TextNode` object containing the `text`, `text_type`, 
                                  and optional `url` for certain types. (e.g., `LINK`, `IMAGE`)

    Returns:
        `LeafNode`: A `LeafNode` object that represents the 
                    HTML equivalent of the given `TextNode`.

    Raises:
        `ValueError`: If the `text_node`'s `text_type` is not a known `TextType`.
    """
    # Maps each TextType to its corresponding HTML tag and any special properties.
    text_type_map = {
        TextType.TEXT: {"tag": None},
        TextType.BOLD: {"tag": "b"},
        TextType.ITALIC: {"tag": "i"},
        TextType.CODE: {"tag": "code"},
        TextType.LINK: {"tag": "a"},
        TextType.IMAGE: {"tag": "img"}
    }

    # Check if TextType is valid and exists in mapping, 
    # then generates LeafNode arguments as needed for each TextType.
    if text_node.text_type in text_type_map:
        tag_dict = text_type_map[text_node.text_type]
        tag = tag_dict["tag"]
        value = text_node.text
        props = {}

        if text_node.text_type == TextType.LINK:
            props["href"] = text_node.url

        elif text_node.text_type == TextType.IMAGE:
            props["src"] = text_node.url
            props["alt"] = text_node.text
            value = ""

        # Create and return the corresponding LeafNode.    
        return LeafNode(tag, value, props)

    else:
        # Raise an error if the provided TextType is not valid.
        raise ValueError(f"Unknown TextType: {text_node.text_type}")

