from textnode import TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    """
    Converts a `TextNode` object into a corresponding `HTMLNode` (specifically a `LeafNode`).

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
        props_dict = text_type_map[text_node.text_type]
        tag = props_dict["tag"]
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
