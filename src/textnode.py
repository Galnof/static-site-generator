from enum import Enum

class TextType(Enum):
    """
    Defines the different types of text formatting our Markdown parser will support.
    """
    TEXT = "text"      # Plain text
    BOLD = "bold"      # **Bold text**
    ITALIC = "italic"  # _Italic text_
    CODE = "code"      # `Code text`
    LINK = "link"      # [Link text](url)
    IMAGE = "image"    # ![Image alt text](url)

class TextNode:
    """
    `TextNode` class serves as an intermediate representation 
    of text between Markdown parsing and HTML generation.
    """
    def __init__(self, text, text_type, url=None):
        """
        Create a new `TextNode` representing a segment of text with specific formatting.
    
        Args:
            `text` (str): The text content of the node
            `text_type` (`TextType`): The formatting type from the `TextType` enum
            `url` (str, optional): The URL for link or image nodes. Defaults to `None`.
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """
        Equality method to compare all properties of two `TextNode`s.

        Args:
            `other` (`TextNode`): The `TextNode` you are comparing.
        """
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        """
        Prints a string representation of the `TextNode`'s properties 
        in a readable format for debugging and logging.
        """
        return f"TextNode(text: {self.text}, text_type: {self.text_type.value}, url: {self.url})"
