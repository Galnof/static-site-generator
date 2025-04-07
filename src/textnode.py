from enum import Enum

# Defines the different types of text formatting our Markdown parser will support.
class TextType(Enum):
    TEXT = "text"      # Plain text
    BOLD = "bold"      # **Bold text**
    ITALIC = "italic"  # _Italic text_
    CODE = "code"      # `Code text`
    LINK = "link"      # [Link text](url)
    IMAGE = "image"    # ![Image alt text](url)


# TextNode class serves as an intermediate representation of text
# between Markdown parsing and HTML generation.
class TextNode:
    # Constructor initializes a TextNode with text content, type, and optional URL.
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    # Equality method to compare TextNodes.
    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )
    
    # Shows the TextNode's properties in a readable format.
    def __repr__(self):
        return f"TextNode(text: {self.text}, text_type: {self.text_type.value}, url: {self.url})"
