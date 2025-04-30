from enum import Enum
from html_parent_leaf_node import ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from inline_markdown_to_html import text_to_textnodes

class BlockType(Enum):
    """
    Enum representing different types of Markdown blocks 
    out Markdown parser will support.

    `BlockType`s supported:
    `PARAGRAPH` `HEADING` `CODE` `QUOTE` `UNORDERED_LIST` `ORDERED_LIST`
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_html_node(markdown_document):
    """
    Converts an entire Markdown document into a single parent `HTMLNode`.

    Each block within the Markdown document is converted into a corresponding
    child `HTMLNode` and nested under a single `<div>` parent.

    Args:
        `markdown_document` (str): Full Markdown text to parse.

    Returns:
        `ParentNode`: The HTML structure with all blocks and their inner content converted.
    """
    # Split the Markdown document into individual blocks.
    markdown_blocks = markdown_to_blocks(markdown_document)
    children = []

    # Convert each block to an HTMLNode and add it as a child.
    for markdown_block in markdown_blocks:
        html_node = block_to_html_node(markdown_block)
        children.append(html_node)
    
    # Wrap all child nodes within a parent `<div>` node.
    return ParentNode("div", children)

def markdown_to_blocks(markdown_document):
    """
    Splits a Markdown document into a list of block-level Markdown elements.

    A block is defined as a section of Markdown separated by a blank line.
    Blank lines (denoted by two consecutive newline characters, '\n\n') divide blocks,
    but any leading or trailing whitespace within a block is stripped. Empty blocks
    caused by excessive newlines are ignored.

    Args:
        `markdown_document` (str): The raw Markdown string to process.

    Returns:
        list: A list of strings, each representing a block of Markdown. Inline 
              newlines within a block (e.g., for lists) are preserved.
    """
    # Split the Markdown document into potential blocks using double newline as a delimiter.
    blocks = markdown_document.split("\n\n")
    processed_blocks = []
    
    # Process blocks by stripping whitespace and ignoring empty blocks.
    for block in blocks:
        processed_block = block.strip()
        if processed_block:
            processed_blocks.append(processed_block)

    return processed_blocks

def block_to_block_type(markdown_block):
    """
    Determine the type of a Markdown block.

    This function inspects a block of Markdown text and returns its corresponding
    `BlockType`. The function assumes the block's leading and trailing whitespace
    has already been stripped.

    Rules:
    - `HEADING`: Starts with 1-6 `#` characters, followed by a space (e.g., `# Heading`).
    - `CODE`: Starts and ends with triple backticks (` ``` `).
    - `QUOTE`: Every line starts with `> `.
    - `UNORDERED_LIST`: Every line starts with `- `.
    - `ORDERED_LIST`: Every line starts with sequential numbers. (e.g., `1. `, `2. `)
    - `PARAGRAPH`: Default type for blocks not matching the above.

    Args:
        `markdown_block` (str): The markdown block to inspect.

    Returns:
        `BlockType`: The `BlockType` corresponding to the type of the Markdown block.
    """
    # Check for heading block. (starts with 1 to 6 '#' characters followed by a space)
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Check for code block. (starts and ends with triple backticks)
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE

    # Check for quote block. (every line starts with '>')
    if markdown_block.startswith(">"):
        block_split = markdown_block.split("\n")
        for line in block_split:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # Check for unordered list. (every line starts with '- ')
    if markdown_block.startswith("- "):
        block_split = markdown_block.split("\n")
        for line in block_split:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    # Check for ordered list. (every line starts with sequential numbers like '1. ', '2. ', etc.)
    if markdown_block.startswith("1. "):
        block_split = markdown_block.split("\n")
        count = 1
        for line in block_split:
            if not line.startswith(f"{count}. "):
                return BlockType.PARAGRAPH
            count += 1
        return BlockType.ORDERED_LIST

    # Default to paragraph if no other type matches.
    return BlockType.PARAGRAPH

def block_to_html_node(markdown_block):
    """
    Converts a single Markdown block into its corresponding `HTMLNode`.

    The function determines the block type and delegates the conversion
    to a specific function for that type.

    Args:
        `markdown_block` (str): A single block of Markdown.

    Returns:
        `ParentNode`: The HTML representation of the block.
    """
    # Determine the type of the block.
    block_type = block_to_block_type(markdown_block)

    # Convert based on block type.
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(markdown_block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(markdown_block)
    if block_type == BlockType.CODE:
        return code_to_html_node(markdown_block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(markdown_block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(markdown_block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(markdown_block)
    
    # If no type matches (though it should), raise an error.
    raise ValueError("invalid block type")

def text_to_children(text):
    """
    Converts plain text into a list of child `HTMLNode`s.

    This function first transforms the input text into intermediate
    `TextNode`s, which are then converted into corresponding `HTMLNode`s.

    Args:
        `text` (str): The plain text to parse into child nodes.

    Returns:
        `list` (`HTMLNode`): A list of child `HTMLNode` objects representing the text.
    """
    text_nodes = text_to_textnodes(text)
    children_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children_nodes.append(html_node)
    return children_nodes

def paragraph_to_html_node(markdown_block):
    """
    Converts a Markdown paragraph block into an `HTMLNode` with `<p>` tags.

    Splits the block into lines, joins them into a single paragraph, and
    delegates text parsing to `text_to_children`.

    Args:
        `markdown_block` (str): The paragraph block of Markdown.

    Returns:
        `ParentNode`: An `HTMLNode` wrapped in `<p>` tags and containing child nodes.
    """
    # Capture the paragraph text.
    paragraph_lines = markdown_block.split("\n")
    paragraph = " ".join(paragraph_lines)

    # Process the paragraph block node tree.
    children_nodes = text_to_children(paragraph)
    return ParentNode("p", children_nodes)

def heading_to_html_node(markdown_block):
    """
    Converts a Markdown heading block into an `HTMLNode` with `<h1>-<h6>` tags.

    Identifies the level of the heading based on the number of `#` symbols,
    validates it, and parses the text into child nodes.

    Args:
        `markdown_block` (str): The heading block of Markdown.

    Returns:
        `ParentNode`: An `HTMLNode` with the appropriate `<h1>-<h6>` tag.

    Raises:
        `ValueError`: If the heading block is malformed or invalid.
    """
    # Capture heading symbols and the text separately, then counts the symbols.
    symbols_and_heading = markdown_block.split(" ", 1)
    count = symbols_and_heading[0].count("#")

    # Validate is formatted correctly and isn't empty.
    if count + 1 >= len(markdown_block):
        raise ValueError(f"invalid heading: h{count}")
    
    # Process the heading block node tree.
    children_nodes = text_to_children(symbols_and_heading[1])
    return ParentNode(f"h{count}", children_nodes)

def code_to_html_node(markdown_block):
    """
    Converts a Markdown code block into a `<pre>` and `<code>` wrapped `HTMLNode`.

    Validates that the block starts and ends with triple backticks (` ``` `),
    extracts the code content, and constructs nested nodes without inline parsing.

    Args:
        `markdown_block` (str): The code block in Markdown.

    Returns:
        `ParentNode`: An `HTMLNode` with `<pre>` and `<code>` tags.

    Raises:
        `ValueError`: If the code block is malformed.
    """
    # Validate the block starts and ends with triple backticks (```)
    if not markdown_block.startswith("```") or not markdown_block.endswith("```"):
        raise ValueError("invalid code block")
    
    # Capture the text of the code block.
    text = markdown_block[4:-3]

    # Process the code block node tree.
    raw_text_node = TextNode(text, TextType.TEXT)
    child_node = text_node_to_html_node(raw_text_node)
    code_node = ParentNode("code", [child_node])
    return ParentNode("pre", [code_node])

def unordered_list_to_html_node(markdown_block):
    """
    Converts a Markdown unordered list into a `<ul>` wrapped `HTMLNode`.

    Splits the block into list items and converts each into `<li>` nodes.

    Args:
        `markdown_block` (str): The unordered list block from Markdown.

    Returns:
        `ParentNode`: An `HTMLNode` wrapped in `<ul>` tags with `<li>` child nodes.

    Raises:
        `ValueError`: If a line within the block isn't formatted as a valid list item.
    """
    list_lines = markdown_block.split("\n")
    child_nodes = []

    for list_line in list_lines:
        # Validate unordered list line formatting.
        if not list_line.startswith("-"):
            raise ValueError("invalid unordered list line")
        
        # Capture the text of the unordered list line.
        list_line_text = list_line[2:]

        # Process the unordered line list node tree.
        node_list = text_to_children(list_line_text)
        child_nodes.append(ParentNode("li", node_list))

    # Process the unordered list block node tree.
    return ParentNode("ul", child_nodes)

def ordered_list_to_html_node(markdown_block):
    """
    Converts a Markdown ordered list into an `<ol>` wrapped `HTMLNode`.

    Splits the block into list items, validates their numbering,
    and converts each into `<li>` nodes.

    Args:
        `markdown_block` (str): The ordered list block from Markdown.

    Returns:
        `ParentNode`: An `HTMLNode` wrapped in `<ol>` tags with `<li>` child nodes.

    Raises:
        `ValueError`: If a line within the block isn't formatted with the proper numbering.
    """
    list_lines = markdown_block.split("\n")
    child_nodes = []
    count = 1

    for list_line in list_lines:
        # Validate ordered list line formatting.
        if not list_line.startswith(f"{count}."):
            raise ValueError(f"invalid ordered list line: {count}.")
        count += 1

        # Capture the text of the ordered list line.
        list_line_text = list_line[3:]

        # Process the ordered line list node tree.
        node_list = text_to_children(list_line_text)
        child_nodes.append(ParentNode("li", node_list))

    # Process the ordered list block node tree.
    return ParentNode("ol", child_nodes)

def quote_to_html_node(markdown_block):
    """
    Converts a Markdown blockquote into a `<blockquote>` wrapped `HTMLNode`.

    Processes each line of the blockquote, removes the `>` markers, and
    joins the lines into a single string. Inline Markdown is parsed
    while keeping the blockquote structure intact.

    Args:
        `markdown_block` (str): The blockquote text block from Markdown.

    Returns:
        `ParentNode`: An `HTMLNode` wrapped in `<blockquote>` tags with parsed children.

    Raises:
        `ValueError`: If a line within the block doesn't start with a `>` marker.
    """
    quote_lines = markdown_block.split("\n")
    processed_lines = []

    for quote_line in quote_lines:
        # Validate the quote block formatting.
        if not quote_line.startswith(">"):
            raise ValueError("invalid quote block")
        
        # Capture the text of the quote lines, strips whitespace, and joins them together.
        processed_lines.append(quote_line.lstrip(">").strip())
    quote_text = " ".join(processed_lines)

    # Process the quote block node tree.
    child_nodes = text_to_children(quote_text)
    return ParentNode("blockquote", child_nodes)
