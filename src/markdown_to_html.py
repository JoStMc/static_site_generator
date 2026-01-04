from block_builder import markdown_to_blocks
from block_type import *
from htmlnode import *
from textnode import *
from inline_builder import *

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    container = ParentNode("div", [])

    for block in blocks:
        block_type = block_to_block_type(block)
        children = text_to_children(block, block_type)
        block_node = ParentNode(block_type_to_tag(block, block_type), children)
        container.children.append(block_node)
    return container


def block_type_to_tag(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return 'p'
        case BlockType.HEADING:
            header_number = len(block.split(' ', 1)[0])
            return 'h' + str(header_number)
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case _:
            raise ValueError("Undefined block type.")

def text_to_children(text, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            # Text to TextNodes -> HTMLNodes -> Listed
            children = text_to_html_nodes(text.replace("\n", ' '))
        case BlockType.HEADING:
            # Text after hashes -> TextNodes -> HTMLNodes -> listed
            children = text_to_html_nodes(text.split(' ', 1)[1])
        case BlockType.CODE:
            # Return just the text as its own HTMLNode
            grand_children = [text_node_to_html_node(TextNode(text.strip('`'), TextType.TEXT))]
            children = [ParentNode("code", grand_children)]
        case BlockType.QUOTE:
            # Remove the inital '>' and any trailing whitespace -> join each 
            # line with a space -> TextNodes -> HTMLNode
            lines = text.split("\n")
            stripped_lines = list(map(lambda line: line.strip("> "), lines))
            quote = ' '.join(stripped_lines)
            children = text_to_html_nodes(quote)
        case BlockType.UNORDERED_LIST:
            # Separate lines -> make each line a HTML node with children
            # text_to_html_nodes(line[2:])
            lines = text.split("\n")
            children = list(map(
                lambda line: ParentNode("li", text_to_html_nodes(line[2:])), lines))

        case BlockType.ORDERED_LIST:
            lines = text.split("\n")
            children = list(map(
                lambda line: ParentNode("li", text_to_html_nodes(line[3:])), lines))
        case _:
            raise ValueError("Undefined block type.")

    return children

def text_to_html_nodes(text):
    return list(map(text_node_to_html_node, text_to_textnodes(text)))
