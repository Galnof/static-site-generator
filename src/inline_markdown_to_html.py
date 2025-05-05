import re
from textnode import TextNode, TextType

def text_to_textnodes(text):
    """
    Converts a raw markdown-flavored string into a list of `TextNode` objects.

    The function processes the input text in sequential steps, splitting it
    into `TextNode` objects based on markdown `delimiter`s. It handles the following formats:
    - Bold (`**`)
    - Italic (`_`)
    - Inline code snippets (`` ` ``)
    - Image nodes (`![alt text](url)`)
    - Hyperlinks (`[text](url)`)

    Args:
        `text` (str): The input markdown-flavored string to be processed.

    Returns:
        list: A list of `TextNode` objects representing the parsed text.

    Example:
        Input: `"This is **bold** and a [link](https://example.com)"`  
        Output: `[`\n
            `TextNode("This is ", TextType.TEXT),`  
            `TextNode("bold", TextType.BOLD),`  
            `TextNode(" and a ", TextType.TEXT),`  
            `TextNode("link", TextType.LINK, "https://example.com"),`
        `]`
    """
    # Start by converting the entire input markdown text into a single TextNode of type TEXT.
    raw_markdown_node = TextNode(text, TextType.TEXT)

    # Split the raw markdown nodes into bold text nodes based on "**" delimiter.
    bold_nodes = split_nodes_delimiter([raw_markdown_node], "**", TextType.BOLD)

    # Further split the bold nodes into italic text nodes based on "_" delimiter.
    italic_bold_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)

    # Further split the italic nodes into code text nodes based on "`" delimiter.
    code_italic_bold_nodes = split_nodes_delimiter(italic_bold_nodes, "`", TextType.CODE)

    # Further handle image nodes in the earlier processed nodes.
    image_code_italic_bold_nodes = split_nodes_image(code_italic_bold_nodes)

    # Finally, handle link nodes in the earlier processed nodes.
    final_nodes = split_nodes_link(image_code_italic_bold_nodes)

    # Return the fully parsed list of nodes.
    return final_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits `TextNode`s based on a `delimiter` and assigns appropriate `text_type`s.
    Return a new list of `TextNode` objects with text split at delimiters.

    Args:
        `old_nodes` (list): List of `TextNode` objects to process.
        `delimiter` (str): The `delimiter` to split text on. (e.g. "**" for bold)
        `text_type` (`TextType`): The `TextType` to assign to text between delimiters.

    Returns:
        list: New list of `TextNode` objects with text split at `delimiter`s.

    Raises:
        `ValueError`: If Markdown syntax `delimiter`s are unbalanced. (odd count)
    """
    new_nodes = []
    for node in old_nodes:
        count = node.text.count(delimiter)

        # Validate the node either has a balanced delimiter.
        if count % 2 != 0:
            raise ValueError("invalid Markdown syntax.")
        
        # If the node is not of type TEXT or contains no delimiter, add it unchanged.
        elif node.text_type != TextType.TEXT or count == 0:
            new_nodes.append(node)
            continue

        # If the node is of type TEXT and contains the delimiter, split it.
        elif node.text_type == TextType.TEXT:
            split_list = node.text.split(delimiter)
            for i, text in enumerate(split_list):
                if text == "":
                    continue
                if i % 2 == 0:
                    # Even-indexed parts are plain text.
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    # Odd-indexed parts are styled with the provided text_type.
                    new_nodes.append(TextNode(text, text_type))

    return new_nodes

def split_nodes_image(old_nodes):
    """
    Split `TextNode`s at image markdown syntax.
    
    Takes a list of `TextNode`s and splits any `TEXT` nodes that contain image markdown
    into separate nodes: text before the image, the image itself, and text after the image.
    
    Args:
        `old_nodes` (list): List of `TextNode` objects to process.
        
    Returns:
        List of `TextNode` objects with images extracted into separate `IMAGE` nodes.
    """
    return split_nodes_by_markdown(
        old_nodes, 
        extract_markdown_images, 
        TextType.IMAGE, 
        "![{}]({})"
    )

def split_nodes_link(old_nodes):
    """
    Split `TextNode`s at link markdown syntax.
    
    Takes a list of `TextNode`s and splits any `TEXT` nodes that contain link markdown
    into separate nodes: text before the link, the link itself, and text after the link.
    
    Args:
        `old_nodes` (list): List of TextNode objects to process.
        
    Returns:
        List of `TextNode` objects with links extracted into separate `LINK` nodes.
    """
    return split_nodes_by_markdown(
        old_nodes, 
        extract_markdown_links, 
        TextType.LINK, 
        "[{}]({})"
    )

def split_nodes_by_markdown(old_nodes, extract_function, text_type, pattern_format):
    """
    Split `TextNode`s based on markdown patterns.
    (images or links)
    
    Args:
        `old_nodes` (list): List of `TextNode` objects to process.

        `extract_function` (function): Function to extract markdown elements.
                                       (`extract_markdown_images` or `extract_markdown_links`)
        `text_type` ('TextType'): `TextType` to assign to new nodes.
                                  (`LINK` or `IMAGE`)
        `pattern_format` (str): String format for the markdown pattern.
                                (`![alt text](url)` or `[anchor text](url)`)
    
    Returns:
        List of `TextNode` objects with markdown elements 
        split and converted into separate nodes.
    """
    new_nodes = []

    for node in old_nodes:
        # Skip non-TEXT nodes preserve them as-is.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        matches = extract_function(remaining_text)
        
        # If no matches found, keep original node unchanged.
        if not matches:
            new_nodes.append(node)
            continue

        cursor = 0 # Track position in the original text.

        for match in matches:
            # Extract components from the match.
            prop_text, url = match
            pattern = pattern_format.format(prop_text, url)
            start_index = remaining_text.find(pattern, cursor)

            # Add text before the pattern if it exists.
            if start_index > cursor:
                before_text = remaining_text[cursor:start_index]
                if before_text:
                    new_nodes.append(TextNode(before_text, TextType.TEXT))
                    
            # Add the markdown element node.
            new_nodes.append(TextNode(prop_text, text_type, url))

            # Move cursor past this match.
            cursor = start_index + len(pattern)

        # Add any remaining text after the last match if it exists.
        if cursor < len(remaining_text):
            after_text = remaining_text[cursor:]
            if after_text:
                new_nodes.append(TextNode(after_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    """
    Extracts markdown image syntax from `text`.
    
    Pattern matches `![alt text](url)` format and returns the alt text and URL.
    
    Args:
        `text` (str): The markdown text to search through.
        
    Returns:
        list: A list of tuples, each containing. (alt_text, url)
    """
    # Regex finds all instances of ![alt text](url)
    # [^\[\]]* matches any character except brackets for the alt text
    # [^\(\)]* matches any character except parentheses for the URL
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    """
    Extracts markdown link syntax from `text`.
    
    Pattern matches `[anchor text](url)` format and returns the anchor text and URL.
    Uses negative lookbehind `(?<!!)` to ensure it doesn't match image tags.
    
    Args:
        `text` (str): The markdown text to search through.
        
    Returns:
        list: A list of tuples, each containing. (anchor_text, url)
    """
    # Regex finds all instances of [anchor text](url) not preceded by !
    # (?<!!) is a negative lookbehind to ensure we don't match images
    # [^\[\]]* matches any character except brackets for the anchor text
    # [^\(\)]* matches any character except parentheses for the URL
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
