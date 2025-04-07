from enum import Enum

# TextType enum defines the different types of inline text
# that our Markdown parser will support. Each type represents
# a different kind of formatting or element.
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


# TextNode class serves as an intermediate representation of text
# between Markdown parsing and HTML generation.
class TextNode:
    # Constructor initializes a TextNode with text content, type, and optional URL.
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    # Equality method to compare TextNodes.
    # Returns True if all properties match between two TextNodes.
    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )
    
    # String representation method for debugging and display.
    # Shows the TextNode's properties in a readable format.
    def __repr__(self):
        return f"TextNode(text: {self.text}, text_type: {self.text_type.value}, url: {self.url})"
